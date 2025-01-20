import os

from aws_cdk import Stack, aws_eks as eks, aws_ec2 as ec2, Tags
from aws_cdk.lambda_layer_kubectl_v30 import KubectlV30Layer
from constructs import Construct

from packages.eks_cluster.eks_cluster_builder import AccessEntry, AccessPolicy, AccessPolicies, EksClusterBuilder
from packages.network.security_group_builder import SecurityGroupBuilder, IngressRule


class EksClusterStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        os.environ["EKS_CLUSTER_NAME"] = "EKS_CLUSTER_NAME"
        os.environ["KARPENTER_ROLE_ARN"] = "KARPENTER_ROLE_ARN"
        os.environ["ARGOCD_DOMAIN"] = "ARGOCD_DOMAIN"
        os.environ["ENVIRONMENT"] = "prod"
        os.environ["GITHUB_TOKEN"] = "GITHUB_TOKEN"
        os.environ["GITHUB_EMAIL"] = "GITHUB_EMAIL"

        security_group = self.__create_security_group(vpc)
        self.__create_cluster(vpc, security_group)

    def __create_security_group(self, vpc):
        security_group_builder = SecurityGroupBuilder("ClusterSecurityGroup", self, vpc)
        security_group_builder.security_group_name("EKS Cluster Security Group")
        security_group_builder.description("EKS Control Plane Security Group tagged by Karpenter")
        security_group_builder.ingress_rules([
            IngressRule(peer=ec2.Peer.ipv4("10.64.32.0/20"),
                        description="Allow all traffic from VPC CIDR",
                        connection=ec2.Port.all_traffic())])
        security_group = security_group_builder.build()
        Tags.of(security_group).add('karpenter.sh/discovery', "EKS Cluster")
        return security_group

    def __create_cluster(self, vpc, security_group) -> eks.FargateCluster:
        eks_cluster_builder = EksClusterBuilder("eks-cluster", self, vpc)
        eks_cluster_builder.cluster_name("EKS Cluster")
        eks_cluster_builder.security_group(security_group)
        eks_cluster_builder.kubectl_layer(KubectlV30Layer(self, "KubectlV30Layer"))
        eks_cluster_builder.version(eks.KubernetesVersion.V1_30)
        access_entries = [AccessEntry(id="ClusterAdminPolicy",
                                      principal_arn="",
                                      access_policies=[AccessPolicy(policy_name=AccessPolicies.CLUSTER_ADMIN_POLICY,
                                                                    access_scope_type=eks.AccessScopeType.CLUSTER)]),
                          AccessEntry(id="ClusterViewPolicy",
                                      principal_arn="role::arn",
                                      access_policies=[AccessPolicy(policy_name=AccessPolicies.VIEW_POLICY,
                                                                    access_scope_type=eks.AccessScopeType.NAMESPACE,
                                                                    namespaces=["staging"])])
                          ]
        eks_cluster_builder.access_entries(access_entries)

        return eks_cluster_builder.build()
