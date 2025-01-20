from typing import Any, Mapping

from aws_cdk import aws_lambda as _lambda, aws_s3 as s3, aws_iam as iam, Stack, Duration

from packages.api_gateway.lambda_rest_api_builder import LambdaRestApiBuilder
from packages.builder import Builder


class LambdaBuilder(Builder):

    def __init__(self, construct_id: str, stack: Stack):
        super().__init__(construct_id, stack)
        self.__function_name = None
        self.__runtime = None
        self.__vpc = None
        self.__vpc_subnets = None
        self.__handler = None
        self.__timeout = Duration.seconds(60)
        self.__environment = None
        self.__bucket_name = None
        self.__bucket_object_key = None
        self.__bucket_object_version = None
        self.__rest_api_enabled = False

    def function_name(self, function_name: str):
        self.__function_name = function_name
        return self

    def runtime(self, runtime: _lambda.Runtime):
        self.__runtime = runtime
        return self

    def handler(self, handler: str):
        self.__handler = handler
        return self

    def timeout(self, timeout: Duration):
        self.__timeout = timeout
        return self

    def environment(self, environment: Mapping[str, str]):
        self.__environment = environment
        return self

    def vpc(self, vpc):
        self.__vpc = vpc
        return self

    def vpc_subnets(self, vpc_subnets: dict[str, Any]):
        self.__vpc_subnets = vpc_subnets
        return self

    def code_from_bucket(self, bucket_name: str, object_key: str, object_version: str | None = None):
        self.__bucket_name = bucket_name
        self.__bucket_object_key = object_key
        self.__bucket_object_version = object_version
        return self

    def rest_api_enabled(self, rest_api_enabled: bool):
        self.__rest_api_enabled = rest_api_enabled
        return self

    def build(self) -> _lambda.Function:
        s3_bucket = self.__get_s3_bucket()
        lambda_function = _lambda.Function(self.stack, self.construct_id,
                                           function_name=self.__function_name,
                                           runtime=self.__runtime,
                                           handler=self.__handler,
                                           timeout=self.__timeout,
                                           vpc=self.__vpc,
                                           vpc_subnets=self.__vpc_subnets,
                                           environment=self.__environment,
                                           code=_lambda.Code.from_bucket(bucket=s3_bucket,
                                                                         key=self.__bucket_object_key,
                                                                         object_version=self.__bucket_object_version))
        lambda_function.add_to_role_policy(iam.PolicyStatement(
            actions=["s3:GetObject"],
            resources=[f"{s3_bucket.bucket_arn}/*"]))

        if self.__rest_api_enabled:
            self.__create_rest_api(lambda_function)

        return lambda_function

    def __create_rest_api(self, lambda_function):
        rest_api_builder = LambdaRestApiBuilder(f"RestApi{self.construct_id}", self.stack)
        rest_api_builder.handler(lambda_function)
        return rest_api_builder.build()

    def __get_s3_bucket(self):
        return s3.Bucket.from_bucket_name(self.stack, f"CodeBucket{self.construct_id}",
                                          bucket_name=self.__bucket_name)
