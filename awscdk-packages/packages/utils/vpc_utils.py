from aws_cdk import aws_ec2 as ec2


class VpcUtils:

    @staticmethod
    def get_private_subnets(vpc: ec2.Vpc) -> []:
        return [subnet.subnet_id for subnet in vpc.private_subnets]

    @staticmethod
    def get_public_subnets(vpc: ec2.Vpc) -> []:
        return vpc.public_subnets

    def get_vpc_by_id(self, vpc_id: str):
        return ec2.Vpc.from_lookup(self, "VPC", vpc_id=vpc_id)
