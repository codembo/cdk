#!/usr/bin/env python3

import aws_cdk as cdk

from config import env_config
from stacks.cloud_front.cloud_front_stack import CloudFrontStack
from stacks.ecr.ecr_stack import EcrStack
from stacks.ecs_fargate.ecs_cluster_stack import EcsClusterStack
from stacks.ecs_fargate.ecs_fargate_service_stack import EcsFargateServiceStack
from stacks.s3.s3_stack import S3Stack

DEVOPS_AWS_CDK = "DevOps - AWS CDK"
PROD = "prod"


def create_app():
    cdk_app = cdk.App()
    env = cdk.Environment(region=env_config.AWS_DEFAULT_REGION, account=env_config.AWS_DEFAULT_ACCOUNT)

    if env_config.ENVIRONMENT == PROD:
        create_ecr_stack(cdk_app, env)

    ecs_cluster_stack = create_ecs_cluster_stack(cdk_app, env)
    create_ecs_fargate_service_stack(cdk_app, env, ecs_cluster_stack)
    create_cloud_front_stack(cdk_app, env)
    create_s3_stack(cdk_app, env)

    return cdk_app


def create_ecr_stack(cdk_app, env):
    ecr_stack = EcrStack(cdk_app, "EcrStack", env=env)
    cdk.Tags.of(ecr_stack).add("CreatedBy", DEVOPS_AWS_CDK)
    return ecr_stack


def create_ecs_cluster_stack(cdk_app, env):
    ecs_cluster_stack = EcsClusterStack(cdk_app, "EcsFargateStack", env=env)
    cdk.Tags.of(ecs_cluster_stack).add("CreatedBy", DEVOPS_AWS_CDK)
    return ecs_cluster_stack


def create_ecs_fargate_service_stack(cdk_app, env, ecs_cluster_stack):
    ecs_fargate_service_stack = EcsFargateServiceStack(cdk_app, "EcsFargateServiceStack",
                                                       ecs_cluster=ecs_cluster_stack.ecs_cluster,
                                                       env=env)
    cdk.Tags.of(ecs_fargate_service_stack).add("CreatedBy", DEVOPS_AWS_CDK)
    ecs_fargate_service_stack.add_dependency(ecs_cluster_stack)
    return ecs_fargate_service_stack


def create_cloud_front_stack(cdk_app, env):
    cloud_front_stack = CloudFrontStack(cdk_app, "CloudFrontStack", env=env)
    cdk.Tags.of(cloud_front_stack).add("CreatedBy", DEVOPS_AWS_CDK)
    return cloud_front_stack


def create_s3_stack(cdk_app, env):
    s3_stack = S3Stack(cdk_app, "S3Stack", env=env)
    cdk.Tags.of(s3_stack).add("CreatedBy", DEVOPS_AWS_CDK)
    return s3_stack


def synth(cdk_app):
    cdk_app.synth()


app = create_app()
synth(app)

if __name__ == '__main__':
    synth(app)
