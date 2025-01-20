from aws_cdk import aws_ec2 as ec2, aws_rds as rds, Stack
from constructs import Construct

from packages.databases.rds.rds_cluster_builder import RdsClusterBuilder
from packages.network.security_group_builder import SecurityGroupBuilder, IngressRule


class RdsClusterStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.__vpc = vpc
        security_group = self.__create_security_group()
        self.__create_rds_cluster(security_group)

    def __create_security_group(self):
        security_group_builder = SecurityGroupBuilder("RDSSecurityGroup", self, self.__vpc)
        security_group_builder.security_group_name("RDS Security Group")
        security_group_builder.description("RDS Security Group to control incoming and outgoing traffic")
        security_group_builder.allow_all_outbound(True)
        security_group_builder.ingress_rules([
            IngressRule(peer=ec2.Peer.ipv4("10.64.32.0/20"),
                        description="Allow all traffic from VPC CIDR",
                        connection=ec2.Port.all_traffic())
        ])
        security_group = security_group_builder.build()
        return security_group

    def __create_rds_cluster(self, security_group):
        rds_cluster_builder = RdsClusterBuilder("RDS_Instance", self)

        rds_cluster_builder.engine("sample-cluster-name")
        rds_cluster_builder.engine(rds.DatabaseClusterEngine.aurora_mysql(version=rds.AuroraMysqlEngineVersion.VER_3_01_0))
        rds_cluster_builder.readers(3)
        rds_cluster_builder.credentials("root")
        rds_cluster_builder.port(3306)
        rds_cluster_builder.deletion_protection(False)
        rds_cluster_builder.security_groups(security_group)
        rds_cluster_builder.serverless_v2_min_capacity(2)
        rds_cluster_builder.serverless_v2_max_capacity(10)

        rds_cluster_builder.vpc(self.__vpc)
        rds_cluster_builder.security_groups(security_group)

        return rds_cluster_builder.build()
