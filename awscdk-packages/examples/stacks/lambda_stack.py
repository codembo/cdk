from aws_cdk import aws_lambda as _lambda, Stack
from constructs import Construct

from packages.lambda_function.lambda_builder import LambdaBuilder


class LambdaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self._lambda = self.__create_lambda()

    def __create_lambda(self):
        lambda_builder = LambdaBuilder("LambdaExample", self)
        lambda_builder.function_name("lambda-example")
        lambda_builder.runtime(_lambda.Runtime.PYTHON_3_9)
        lambda_builder.handler("example.handler")
        lambda_builder.code_from_bucket(bucket_name="example-bucket", object_key="example")
        lambda_builder.rest_api_enabled(True)

        return lambda_builder.build()
