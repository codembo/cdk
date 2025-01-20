from aws_cdk import Stack, aws_ec2 as ec2
from constructs import Construct

from packages.network.vpc_builder import VpcBuilder


class NetworkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = self.__create_vpc()

    def __create_vpc(self):
        vpc_builder = VpcBuilder("VPC_NAME", self)
        vpc_builder.ip_addresses("10.64.32.0/20")
        vpc_builder.availability_zones(["us-east-1a", "us-east-1b", "us-east-1c"])
        vpc_builder.subnet_configuration([
            ec2.SubnetConfiguration(name="Public", subnet_type=ec2.SubnetType.PUBLIC, cidr_mask=27),
            ec2.SubnetConfiguration(name="Database", subnet_type=ec2.SubnetType.PRIVATE_ISOLATED),
            ec2.SubnetConfiguration(name="Private", subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS)
        ])
        return vpc_builder.build()
