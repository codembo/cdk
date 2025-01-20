from aws_cdk import aws_ec2 as ec2, Stack

from packages.builder import Builder


class VpcBuilder(Builder):

    def __init__(self, construct_id: str, stack: Stack):
        super().__init__(construct_id, stack)
        self.__ip_addresses = None
        self.__availability_zones = None
        self.__subnet_configuration = None
        self.__restrict_default_security_group = True

    def ip_addresses(self, ip_addresses):
        self.__ip_addresses = ip_addresses

    def availability_zones(self, availability_zones):
        self.__availability_zones = availability_zones

    def subnet_configuration(self, subnet_configuration):
        self.__subnet_configuration = subnet_configuration

    def restrict_default_security_group(self, restrict_default_security_group):
        self.__restrict_default_security_group = restrict_default_security_group

    def build(self) -> ec2.Vpc:
        vpc = ec2.Vpc(self.stack, self.construct_id,
                      ip_addresses=ec2.IpAddresses.cidr(self.__ip_addresses),
                      availability_zones=self.__availability_zones,
                      subnet_configuration=self.__subnet_configuration,
                      restrict_default_security_group=self.__restrict_default_security_group,
                      gateway_endpoints={
                          "S3": ec2.GatewayVpcEndpointOptions(
                              service=ec2.GatewayVpcEndpointAwsService.S3),
                          "DynamoDB": ec2.GatewayVpcEndpointOptions(
                              service=ec2.GatewayVpcEndpointAwsService.DYNAMODB)
                      })
        return vpc
