from aws_cdk import aws_ecs as ecs, Stack

from packages.builder import Builder


class EcsClusterBuilder(Builder):

    def __init__(self, construct_id: str, stack: Stack):
        super().__init__(construct_id, stack)
        self.__vpc = None

    def vpc(self, vpc):
        self.__vpc = vpc

    def build(self) -> ecs.Cluster:
        ecs_cluster = ecs.Cluster(self.stack,
                                  self.construct_id,
                                  vpc=self.__vpc)
        return ecs_cluster
