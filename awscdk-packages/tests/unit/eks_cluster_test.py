import os
import unittest

from aws_cdk import Stack, aws_ec2 as ec2, aws_eks as eks, Tags
from aws_cdk.lambda_layer_kubectl_v30 import KubectlV30Layer

from packages.eks_cluster.eks_cluster_builder import EksClusterBuilder, AccessEntry, AccessPolicy, AccessPolicies
from packages.network.security_group_builder import SecurityGroupBuilder, IngressRule
from packages.network.vpc_builder import VpcBuilder


class EksClusterTestCase(unittest.TestCase):

    def test_eks_cluster_builder(self):
        stack = Stack()
        vpc_builder = VpcBuilder("VPC_NAME", stack)
        vpc_builder.ip_addresses("10.64.32.0/20")
        vpc_builder.availability_zones(["us-east-1a", "us-east-1b", "us-east-1c"])
        vpc = vpc_builder.build()

        os.environ["EKS_CLUSTER_NAME"] = "EKS_CLUSTER_NAME"
        os.environ["KARPENTER_ROLE_ARN"] = "KARPENTER_ROLE_ARN"
        os.environ["ARGOCD_DOMAIN"] = "ARGOCD_DOMAIN"
        os.environ["ENVIRONMENT"] = "prod"
        os.environ["GITHUB_TOKEN"] = "GITHUB_TOKEN"
        os.environ["GITHUB_EMAIL"] = "GITHUB_EMAIL"

        security_group_builder = SecurityGroupBuilder("ClusterSecurityGroup", stack, vpc)
        security_group_builder.security_group_name("EKS Cluster Security Group")
        security_group_builder.description("EKS Control Plane Security Group tagged by Karpenter")
        security_group_builder.ingress_rules([
            IngressRule(peer=ec2.Peer.ipv4("10.64.32.0/20"),
                        description="Allow all traffic from VPC CIDR",
                        connection=ec2.Port.all_traffic())
        ])
        security_group = security_group_builder.build()
        Tags.of(security_group).add('karpenter.sh/discovery', "EKS_CLUSTER_NAME")

        eks_cluster_builder = EksClusterBuilder("EKS_CLUSTER_ID", stack, vpc)
        eks_cluster_builder.cluster_name("EKS_CLUSTER_NAME")
        eks_cluster_builder.security_group(security_group)
        eks_cluster_builder.kubectl_layer(KubectlV30Layer(stack, "KubectlV30Layer"))
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

        eks_cluster = eks_cluster_builder.build()

        self.assertIsNotNone(vpc)
        self.assertIsNotNone(eks_cluster)


if __name__ == '__main__':
    unittest.main()
