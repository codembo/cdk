#!/usr/bin/env python3
import os

import aws_cdk as cdk

from stacks.ecr_stack import EcrStack
from stacks.ecs_fargate_service_stack import EcsFargateServiceStack
from stacks.ecs_cluster_stack import EcsClusterStack
from stacks.eks_cluster_stack import EksClusterStack
from stacks.lambda_stack import LambdaStack
from stacks.network_stack import NetworkStack
from stacks.rds_cluster_stack import RdsClusterStack
from stacks.rds_instance_stack import RdsInstanceStack

DEVOPS_AWS_CDK = "DevOps - AWS CDK"


def create_app():
    cdk_app = cdk.App()
    env = cdk.Environment(region=os.getenv('AWS_DEFAULT_REGION'), account=os.getenv('AWS_DEFAULT_ACCOUNT'))

    network_stack = create_network_stack(cdk_app, env)
    create_lambda_stack(cdk_app, env)
    create_rds_stack(cdk_app, env, network_stack)
    create_rds_cluster_stack(cdk_app, env, network_stack)
    create_eks_cluster_stack(cdk_app, env, network_stack)
    ecs_cluster_stack = create_ecs_cluster_stack(cdk_app, env, network_stack)
    create_ecs_fargate_service_stack(cdk_app, env, ecs_cluster_stack)
    create_ecr_stack(cdk_app, env)

    return cdk_app


def create_network_stack(cdk_app, env):
    network_stack = NetworkStack(cdk_app, "ResourcesNetworkStack", env=env)
    cdk.Tags.of(network_stack).add("CreatedBy", DEVOPS_AWS_CDK)
    return network_stack


def create_lambda_stack(cdk_app, env):
    lambda_stack = LambdaStack(cdk_app, "LambdaStack", env=env)
    cdk.Tags.of(lambda_stack).add("CreatedBy", DEVOPS_AWS_CDK)
    return lambda_stack


def create_rds_stack(cdk_app, env, network_stack):
    rds_stack = RdsInstanceStack(cdk_app, "RdsStack", vpc=network_stack.vpc, env=env)
    rds_stack.add_dependency(network_stack)
    cdk.Tags.of(rds_stack).add("CreatedBy", DEVOPS_AWS_CDK)
    return rds_stack


def create_rds_cluster_stack(cdk_app, env, network_stack):
    rds_cluster_stack = RdsClusterStack(cdk_app, "RdsClusterStack", vpc=network_stack.vpc, env=env)
    rds_cluster_stack.add_dependency(network_stack)
    cdk.Tags.of(rds_cluster_stack).add("CreatedBy", DEVOPS_AWS_CDK)
    return rds_cluster_stack


def create_eks_cluster_stack(cdk_app, env, network_stack):
    eks_cluster_stack = EksClusterStack(cdk_app, "EksClusterStack", vpc=network_stack.vpc, env=env)
    eks_cluster_stack.add_dependency(network_stack)
    cdk.Tags.of(eks_cluster_stack).add("CreatedBy", DEVOPS_AWS_CDK)
    return eks_cluster_stack


def create_ecs_cluster_stack(cdk_app, env, network_stack):
    ecs_cluster_stack = EcsClusterStack(cdk_app, "EcsClusterStack", vpc=network_stack.vpc, env=env)
    ecs_cluster_stack.add_dependency(network_stack)
    cdk.Tags.of(ecs_cluster_stack).add("CreatedBy", DEVOPS_AWS_CDK)
    return ecs_cluster_stack


def create_ecs_fargate_service_stack(cdk_app, env, ecs_cluster_stack):
    ecs_fargate_service_stack = EcsFargateServiceStack(cdk_app, "EcsFargateServiceStack",
                                                       ecs_cluster=ecs_cluster_stack.ecs_cluster,
                                                       env=env)
    ecs_fargate_service_stack.add_dependency(ecs_cluster_stack)
    cdk.Tags.of(ecs_fargate_service_stack).add("CreatedBy", DEVOPS_AWS_CDK)
    return ecs_fargate_service_stack


def create_ecr_stack(cdk_app, env):
    ecr_repository_stack = EcrStack(cdk_app, "EcrStack", env=env)
    cdk.Tags.of(ecr_repository_stack).add("CreatedBy", DEVOPS_AWS_CDK)
    return ecr_repository_stack


def synth(cdk_app):
    cdk_app.synth()


app = create_app()
synth(app)

if __name__ == '__main__':
    synth(app)
