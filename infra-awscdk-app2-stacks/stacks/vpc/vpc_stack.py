from aws_cdk import Stack, aws_ec2 as ec2
from constructs import Construct
from packages.network.vpc_builder import VpcBuilder
from config import env_config


class VpcStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = self.__create_vpc()

    def __create_vpc(self):
        vpc_builder = VpcBuilder(env_config.VPC_NAME, self)
        vpc_builder.ip_addresses(env_config.VPC_CIDR)
        vpc_builder.availability_zones(["us-east-2a", "us-east-2b", "us-east-2c"])
        vpc_builder.subnet_configuration([
            ec2.SubnetConfiguration(name="Public", subnet_type=ec2.SubnetType.PUBLIC, cidr_mask=24),
            ec2.SubnetConfiguration(name="Database", subnet_type=ec2.SubnetType.PRIVATE_ISOLATED),
            ec2.SubnetConfiguration(name="Private", subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS)
        ])
        return vpc_builder.build()
