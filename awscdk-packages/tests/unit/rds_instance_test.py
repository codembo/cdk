import unittest

from aws_cdk import aws_ec2 as ec2, aws_rds as rds, Stack

from packages.databases.rds.rds_instance_builder import RdsInstanceBuilder
from packages.network.security_group_builder import IngressRule, SecurityGroupBuilder
from packages.network.vpc_builder import VpcBuilder


class RdsInstanceTestCase(unittest.TestCase):

    def test_rds_instance_builder(self):
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

        rds_instance_builder = RdsInstanceBuilder("RDS_Instance", stack)
        rds_instance_builder.engine(rds.DatabaseInstanceEngine.mysql(version=rds.MysqlEngineVersion.VER_8_0_35))
        # rds_instance_builder.engine(rds.DatabaseInstanceEngine.postgres(version=rds.PostgresEngineVersion.VER_16_3))
        rds_instance_builder.vpc(vpc)
        rds_instance_builder.credentials("root")
        rds_instance_builder.instance_type(ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MICRO))
        rds_instance_builder.port(3306)
        rds_instance_builder.multi_az(False)
        rds_instance_builder.auto_minor_version_upgrade(True)
        rds_instance_builder.allocated_storage(20)
        rds_instance_builder.deletion_protection(False)
        rds_instance_builder.publicly_accessible(False)
        rds_instance_builder.security_groups(security_group)

        rds_instance = rds_instance_builder.build()

        self.assertIsNotNone(rds_instance)


if __name__ == '__main__':
    unittest.main()
