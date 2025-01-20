from aws_cdk import aws_ec2 as ec2, Stack
from constructs import Construct
from packages.ecs.ecs_cluster_builder import EcsClusterBuilder

from config import env_config


class EcsClusterStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.ecs_cluster = self.__create_ecs_cluster(vpc)

    def __create_ecs_cluster(self, vpc):
        ecs_cluster_builder = EcsClusterBuilder("EcsCluster", self)
        ecs_cluster_builder.vpc(vpc)
        return ecs_cluster_builder.build()
