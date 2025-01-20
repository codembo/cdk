from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_iam as iam, Stack
from constructs import Construct
from packages.ecs.ecs_fargate_service_builder import EcsFargateServiceBuilder

from config import env_config


class EcsFargateServiceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, ecs_cluster: ecs.Cluster, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.__create_ecs_fargate_service(ecs_cluster)

    def __create_ecs_fargate_service(self, ecs_cluster):
        ecs_fargate_service_builder = EcsFargateServiceBuilder("EcsFargateService", self)
        ecs_fargate_service_builder.ecs_cluster(ecs_cluster)
        ecs_fargate_service_builder.certificate_arn(env_config.ECS_FARGATE_CERTIFICATE_ARN)
        ecs_fargate_service_builder.container_image(env_config.ECS_FARGATE_CONTAINER_IMAGE)
        ecs_fargate_service_builder.container_name("api-server")
        ecs_fargate_service_builder.container_port(5000)
        ecs_fargate_service_builder.assign_public_ip(False)
        ecs_fargate_service_builder.execution_role(self.__create_execution_role())
        ecs_fargate_service_builder.task_role(self.__create_task_role())
        ecs_fargate_service_builder.environment(self.__create_environment())
        return ecs_fargate_service_builder.build()

    def __create_execution_role(self):
        task_role = iam.Role(
            self, "EcsTaskExecutionRole",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com")
        )
        task_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEC2ContainerRegistryReadOnly")
        )
        task_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonECSTaskExecutionRolePolicy")
        )
        return task_role

    def __create_task_role(self):
        task_role = iam.Role(
            self, "EcsTaskRole",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com")
        )
        task_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
        )
        task_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("SecretsManagerReadWrite")
        )
        return task_role

    @staticmethod
    def __create_environment():
        return {

            # "PASSWORD": env_config.PASSWORD,
            # "NIDERA_AUTHENTICATION_FLAG": env_config.NIDERA_AUTHENTICATION_FLAG,
            # "FARMSHOTS_USER_ID": env_config.FARMSHOTS_USER_ID,
            # "CROPWISE_BASE_URL": env_config.CROPWISE_BASE_URL,
            # "NIDERA_AUTH_URL": env_config.NIDERA_AUTH_URL,
            # "BASE_AUTH_URL": env_config.BASE_AUTH_URL,
            # "AWS_SECRETS_NAME": env_config.AWS_SECRETS_NAME,
            "AWS_DEFAULT_REGION": env_config.AWS_DEFAULT_REGION,
            # "CROPWISE_RS2_URL": env_config.CROPWISE_RS2_URL,
            # "S3_BUCKET_NAME": env_config.S3_BUCKET_NAME,
            # "CROPWISE_NIDERA_PASSWORD": env_config.CROPWISE_NIDERA_PASSWORD,
            # "DD_LOGS_INJECTION": env_config.DD_LOGS_INJECTION,
            # "DD_TAGS": env_config.DD_TAGS,
            # "DD_TRACE_AGENT_URL": env_config.DD_TRACE_AGENT_URL
        }
