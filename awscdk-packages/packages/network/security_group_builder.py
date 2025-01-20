from dataclasses import dataclass

from aws_cdk import aws_ec2 as ec2, Stack

from packages.builder import Builder


@dataclass
class IngressRule:
    peer: ec2.Peer
    description: str
    connection: ec2.Port


class SecurityGroupBuilder(Builder):

    def __init__(self, construct_id: str, stack: Stack, vpc: ec2.Vpc):
        super().__init__(construct_id, stack)
        self.__vpc = vpc
        self.__description = None
        self.__security_group_name = None
        self.__allow_all_outbound = True
        self.__ingress_rules: list[IngressRule] = []

    def description(self, description: str):
        self.__description = description

    def security_group_name(self, security_group_name: str):
        self.__security_group_name = security_group_name

    def allow_all_outbound(self, allow_all_outbound: bool):
        self.__allow_all_outbound = allow_all_outbound

    def ingress_rules(self, ingress_rules: list[IngressRule]):
        self.__ingress_rules = ingress_rules

    def build(self) -> ec2.Vpc:
        security_group = ec2.SecurityGroup(self.stack, self.construct_id,
                                           vpc=self.__vpc,
                                           description=self.__description,
                                           security_group_name=self.__security_group_name,
                                           allow_all_outbound=self.__allow_all_outbound)
        for ingress_rule in self.__ingress_rules:
            security_group.add_ingress_rule(peer=ingress_rule.peer,
                                            description=ingress_rule.description,
                                            connection=ingress_rule.connection)
        return security_group
