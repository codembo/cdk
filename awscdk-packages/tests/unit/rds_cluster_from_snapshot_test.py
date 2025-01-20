import unittest

from aws_cdk import aws_ec2 as ec2, aws_rds as rds, Stack

from packages.databases.rds.rds_cluster_from_snapshot_builder import  RdsClusterFromSnapshotBuilder
from packages.network.security_group_builder import IngressRule, SecurityGroupBuilder
from packages.network.vpc_builder import VpcBuilder


class RdsInstanceFromSnapshotTestCase(unittest.TestCase):

    def test_rds_cluster_from_snapshot_builder(self):
        stack = Stack()

        vpc_builder = VpcBuilder("VPC_NAME", stack)
        vpc_builder.ip_addresses("10.0.0.0/16")
        vpc_builder.availability_zones(["us-east-1a", "us-east-1b", "us-east-1c"])
        vpc_builder.subnet_configuration([
            ec2.SubnetConfiguration(name="Public", subnet_type=ec2.SubnetType.PUBLIC, cidr_mask=20),
            ec2.SubnetConfiguration(name="Database", subnet_type=ec2.SubnetType.PRIVATE_ISOLATED, cidr_mask=20),
            ec2.SubnetConfiguration(name="Private", subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS, cidr_mask=20)
        ])
        vpc = vpc_builder.build()
        security_group_builder = SecurityGroupBuilder("RDSSecurityGroup", stack, vpc)
        security_group_builder.security_group_name("RDS Security Group")
        security_group_builder.description("RDS Security Group to control incoming and outgoing traffic")
        security_group_builder.allow_all_outbound(True)
        security_group_builder.ingress_rules([
            IngressRule(peer=ec2.Peer.ipv4("10.0.0.0/20"),
                        description="Allow all traffic from VPC CIDR",
                        connection=ec2.Port.all_traffic())
        ])
        security_group = security_group_builder.build()
        rds_cluster_from_snapshot_builder = RdsClusterFromSnapshotBuilder("RDS_Cluster", stack)
        rds_cluster_from_snapshot_builder.snapshot_identifier("sample-snapshot")
        rds_cluster_from_snapshot_builder.cluster_identifier("sample-cluster-name")
        rds_cluster_from_snapshot_builder.engine(rds.DatabaseClusterEngine.aurora_mysql(version=rds.AuroraMysqlEngineVersion.VER_3_01_0))
        rds_cluster_from_snapshot_builder.readers(1)
        rds_cluster_from_snapshot_builder.vpc(vpc)
        rds_cluster_from_snapshot_builder.credentials("root")
        rds_cluster_from_snapshot_builder.port(3306)
        rds_cluster_from_snapshot_builder.deletion_protection(False)  #package will override this to True
        rds_cluster_from_snapshot_builder.security_groups(security_group)
        rds_cluster_from_snapshot_builder.serverless_v2_min_capacity(2)
        rds_cluster_from_snapshot_builder.serverless_v2_max_capacity(10)

        rds_cluster = rds_cluster_from_snapshot_builder.build()

        self.assertIsNotNone(rds_cluster)

    def test_rds_cluster_builder_without_reader(self):
        stack = Stack()

        vpc_builder = VpcBuilder("VPC_NAME", stack)
        vpc_builder.ip_addresses("10.0.0.0/16")
        vpc_builder.availability_zones(["us-east-1a", "us-east-1b", "us-east-1c"])
        vpc_builder.subnet_configuration([
            ec2.SubnetConfiguration(name="Public", subnet_type=ec2.SubnetType.PUBLIC, cidr_mask=20),
            ec2.SubnetConfiguration(name="Database", subnet_type=ec2.SubnetType.PRIVATE_ISOLATED, cidr_mask=20),
            ec2.SubnetConfiguration(name="Private", subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS, cidr_mask=20)
        ])
        vpc = vpc_builder.build()
        security_group_builder = SecurityGroupBuilder("RDSSecurityGroup", stack, vpc)
        security_group_builder.security_group_name("RDS Security Group")
        security_group_builder.description("RDS Security Group to control incoming and outgoing traffic")
        security_group_builder.allow_all_outbound(True)
        security_group_builder.ingress_rules([
            IngressRule(peer=ec2.Peer.ipv4("10.0.0.0/20"),
                        description="Allow all traffic from VPC CIDR",
                        connection=ec2.Port.all_traffic())
        ])
        security_group = security_group_builder.build()
        rds_cluster_from_snapshot_builder = RdsClusterFromSnapshotBuilder("RDS_Cluster", stack)
        rds_cluster_from_snapshot_builder.snapshot_identifier("sample-snapshot")
        rds_cluster_from_snapshot_builder.cluster_identifier("sample-cluster-name")
        rds_cluster_from_snapshot_builder.engine(rds.DatabaseClusterEngine.aurora_mysql(version=rds.AuroraMysqlEngineVersion.VER_3_01_0))
        rds_cluster_from_snapshot_builder.readers(0)
        rds_cluster_from_snapshot_builder.vpc(vpc)
        rds_cluster_from_snapshot_builder.credentials("root")
        rds_cluster_from_snapshot_builder.port(3306)
        rds_cluster_from_snapshot_builder.deletion_protection(False) #package will override this to True
        rds_cluster_from_snapshot_builder.security_groups(security_group)
        rds_cluster_from_snapshot_builder.serverless_v2_min_capacity(2)
        rds_cluster_from_snapshot_builder.serverless_v2_max_capacity(10)

        rds_cluster = rds_cluster_from_snapshot_builder.build()

        self.assertIsNotNone(rds_cluster)
if __name__ == '__main__':
    unittest.main()
