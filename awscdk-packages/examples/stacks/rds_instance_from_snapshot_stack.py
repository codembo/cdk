from aws_cdk import aws_ec2 as ec2, aws_rds as rds, Stack
from constructs import Construct

from packages.databases.rds.rds_instance_from_snapshot_builder import RdsInstanceFromSnapshotBuilder
from packages.network.security_group_builder import SecurityGroupBuilder, IngressRule


class RdsInstanceFromSnapshotStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.__vpc = vpc
        security_group = self.__create_security_group()
        self.__create_rds_instance(security_group)

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

    def __create_rds_instance(self, security_group):
        rds_instance_builder = RdsInstanceFromSnapshotBuilder("RDS_Instance", self)

        rds_instance_builder.engine(
            rds.DatabaseInstanceEngine.mysql(version=rds.MysqlEngineVersion.VER_8_0_35))
        rds_instance_builder.snapshot_identifier("sample-snapshot")
        rds_instance_builder.vpc(self.__vpc)
        rds_instance_builder.credentials("root")
        rds_instance_builder.instance_type(
            ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MICRO))
        rds_instance_builder.port(3306)
        rds_instance_builder.multi_az(False)
        rds_instance_builder.auto_minor_version_upgrade(True)
        rds_instance_builder.allocated_storage(20)
        rds_instance_builder.deletion_protection(False)
        rds_instance_builder.publicly_accessible(False)
        rds_instance_builder.security_groups(security_group)

        return rds_instance_builder.build()
