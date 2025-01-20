import unittest

from aws_cdk import Stack

from packages.ecs.ecs_cluster_builder import EcsClusterBuilder
from packages.ecs.ecs_fargate_service_builder import EcsFargateServiceBuilder
from packages.network.vpc_builder import VpcBuilder


class EcsFargateTestCase(unittest.TestCase):

    def test_ecs_fargate_builder(self):
        stack = Stack()

        vpc_builder = VpcBuilder("VpcExample", stack)
        vpc_builder.ip_addresses("10.64.32.0/20")
        vpc_builder.availability_zones(["us-east-1a", "us-east-1b", "us-east-1c"])
        vpc = vpc_builder.build()

        ecs_cluster_builder = EcsClusterBuilder("EcsClusterExample", stack)
        ecs_cluster_builder.vpc(vpc)
        ecs_cluster = ecs_cluster_builder.build()

        ecs_fargate_service_builder = EcsFargateServiceBuilder("EcsFargateServiceExample", stack)
        ecs_fargate_service_builder.ecs_cluster(ecs_cluster)
        ecs_fargate_service_builder.container_image("amazon/amazon-ecs-sample")
        ecs_fargate_service_builder.container_name("api-server")
        ecs_fargate_service_builder.container_port(5000)
        ecs_fargate_service_builder.certificate_arn("arn::example::certificate")
        ecs_fargate_service = ecs_fargate_service_builder.build()

        self.assertIsNotNone(ecs_cluster)
        self.assertIsNotNone(ecs_fargate_service)


if __name__ == '__main__':
    unittest.main()
