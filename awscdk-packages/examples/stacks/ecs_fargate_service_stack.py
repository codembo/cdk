from aws_cdk import Stack, aws_ecs as ecs
from constructs import Construct

from packages.ecs.ecs_fargate_service_builder import EcsFargateServiceBuilder


class EcsFargateServiceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, ecs_cluster: ecs.Cluster, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.ecs_fargate_service_1 = self.__ecs_fargate_service_1(ecs_cluster)
        self.ecs_fargate_service_2 = self.__ecs_fargate_service_2(ecs_cluster)

    def __ecs_fargate_service_1(self, ecs_cluster: ecs.Cluster):
        ecs_fargate_service_builder = EcsFargateServiceBuilder("EcsFargateService1", self)
        ecs_fargate_service_builder.ecs_cluster(ecs_cluster)
        ecs_fargate_service_builder.container_image("amazon/amazon-ecs-sample")
        ecs_fargate_service_builder.certificate_arn("arn.test")

        return ecs_fargate_service_builder.build()

    def __ecs_fargate_service_2(self, ecs_cluster: ecs.Cluster):
        ecs_fargate_service_builder = EcsFargateServiceBuilder("EcsFargateService2", self)
        ecs_fargate_service_builder.ecs_cluster(ecs_cluster)
        ecs_fargate_service_builder.container_image("amazon/amazon-ecs-sample")
        ecs_fargate_service_builder.certificate_arn("arn.test")

        return ecs_fargate_service_builder.build()
