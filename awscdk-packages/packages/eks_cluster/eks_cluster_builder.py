import os
from dataclasses import dataclass
from enum import StrEnum
from typing import Optional, Sequence

from aws_cdk import aws_eks as eks, aws_ec2 as ec2, aws_iam as iam, cloudformation_include as cfn_inc, Stack

from packages.builder import Builder
from packages.parser.yaml_parser import load_yaml

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ADDONS_DIR = BASE_DIR + "/addons/"


@dataclass
class AccessPolicy:
    access_scope_type: eks.AccessScopeType
    policy_name: Optional[str] = None
    namespaces: Optional[Sequence[str]] = None


@dataclass
class AccessEntry:
    id: str
    access_policies: Optional[Sequence[AccessPolicy]]
    principal_arn: Optional[str] = None


class AccessPolicies(StrEnum):
    ADMIN_POLICY = 'AmazonEKSAdminPolicy'
    ADMIN_VIEW_POLICY = 'AmazonEKSAdminViewPolicy'
    CLUSTER_ADMIN_POLICY = 'AmazonEKSClusterAdminPolicy'
    EDIT_POLICY = 'AmazonEKSEditPolicy'
    VIEW_POLICY = 'AmazonEKSViewPolicy'


class EksClusterBuilder(Builder):

    def __init__(self, construct_id: str, stack: Stack, vpc: ec2.Vpc):
        super().__init__(construct_id, stack)
        self.__vpc = vpc
        self.__cluster_name = None
        self.__security_group = None
        self.__version = None
        self.__kubectl_layer = None
        self.__create_karpenter = True
        self.__create_argocd = True
        self.__authentication_mode = eks.AuthenticationMode.API_AND_CONFIG_MAP
        self.__endpoint_access = eks.EndpointAccess.PUBLIC_AND_PRIVATE
        self.__access_entries: Optional[Sequence[AccessEntry]] = None

    def cluster_name(self, cluster_name):
        self.__cluster_name = cluster_name
        return self

    def security_group(self, security_group):
        self.__security_group = security_group
        return self

    def version(self, version):
        self.__version = version
        return self

    def kubectl_layer(self, kubectl_layer):
        self.__kubectl_layer = kubectl_layer
        return self

    def create_karpenter(self, create_karpenter):
        self.__create_karpenter = create_karpenter
        return self

    def create_argocd(self, create_argocd):
        self.__create_argocd = create_argocd
        return self

    def authentication_mode(self, authentication_mode: eks.AuthenticationMode):
        self.__authentication_mode = authentication_mode
        return self

    def endpoint_access(self, endpoint_access: eks.EndpointAccess):
        self.__endpoint_access = endpoint_access
        return self

    def access_entries(self, access_entries: Sequence[AccessEntry]):
        self.__access_entries = access_entries
        return self

    def __iam_masters_role(self):
        return iam.Role(self.stack, "MastersRole",
                        role_name="mastersRole",
                        assumed_by=iam.AccountRootPrincipal())

    def __karpenter_addon(self, eks_cluster):
        cfn_inc.CfnInclude(self.stack, "KarpenterTemplate",
                           template_file=ADDONS_DIR + "karpenter/karpenter_template.yaml",
                           parameters={"ClusterName": self.__cluster_name,
                                       "OICPIssuer": eks_cluster.cluster_open_id_connect_issuer})
        eks_cluster.add_helm_chart("Karpenter",
                                   chart="karpenter",
                                   release="karpenter",
                                   repository="oci://public.ecr.aws/karpenter/karpenter",
                                   namespace="karpenter",
                                   version="0.37.0",
                                   create_namespace=True,
                                   values=load_yaml(ADDONS_DIR + "karpenter/karpenter_values.yaml", parse_env=True))

    def __create_access_entries(self, eks_cluster):
        for access_entry in self.__access_entries:
            access_policies = self.__create_access_policies(access_entry)
            eks_cluster.grant_access(access_entry.id,
                                     principal=access_entry.principal_arn,
                                     access_policies=access_policies)

    @staticmethod
    def __create_access_policies(access_entry):
        return [eks.AccessPolicy.from_access_policy_name(policy_name=access_policy.policy_name,
                                                         access_scope_type=access_policy.access_scope_type,
                                                         namespaces=access_policy.namespaces) for access_policy in
                access_entry.access_policies]

    @staticmethod
    def __argocd_addon(eks_cluster):
        eks_cluster.add_helm_chart("ArgoCDAddOn",
                                   chart="argo-cd",
                                   release="argocd",
                                   repository="https://argoproj.github.io/argo-helm",
                                   namespace="argocd",
                                   version="6.7.8",
                                   create_namespace=True,
                                   values=load_yaml(ADDONS_DIR + "argocd/argocd_values.yaml", parse_env=True))

        argocd_devops_application = load_yaml(ADDONS_DIR + "argocd/argocd_devops_application.yaml")
        eks_cluster.add_manifest("ArgoCdDevOps", argocd_devops_application)

        argocd_github_secret = load_yaml(ADDONS_DIR + "argocd/argocd_github_secret.yaml", parse_env=True)
        eks_cluster.add_manifest("ArgoCdGithubSecret", argocd_github_secret)

    def build(self) -> eks.FargateCluster:
        eks_cluster = eks.FargateCluster(self.stack, self.construct_id,
                                         cluster_name=self.__cluster_name,
                                         vpc=self.__vpc,
                                         vpc_subnets=[
                                             ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS)],
                                         cluster_logging=[eks.ClusterLoggingTypes.API,
                                                          eks.ClusterLoggingTypes.AUTHENTICATOR,
                                                          eks.ClusterLoggingTypes.SCHEDULER],
                                         masters_role=self.__iam_masters_role(),
                                         kubectl_layer=self.__kubectl_layer,
                                         security_group=self.__security_group,
                                         core_dns_compute_type=eks.CoreDnsComputeType.EC2,
                                         authentication_mode=self.__authentication_mode,
                                         default_profile=eks.FargateProfileOptions(
                                             selectors=[eks.Selector(namespace="karpenter")]),
                                         version=self.__version,
                                         endpoint_access=self.__endpoint_access)

        if self.__create_karpenter:
            self.__karpenter_addon(eks_cluster)

        if self.__create_argocd:
            self.__argocd_addon(eks_cluster)

        if self.__access_entries:
            self.__create_access_entries(eks_cluster)

        return eks_cluster
