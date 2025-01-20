import unittest

from aws_cdk import aws_lambda as _lambda, Stack

from packages.lambda_function.lambda_builder import LambdaBuilder


class LambdaTestCase(unittest.TestCase):

    def test_lambda_builder(self):
        stack = Stack()
        lambda_builder = LambdaBuilder("LambdaExample", stack)
        lambda_builder.function_name("lambda-example")
        lambda_builder.runtime(_lambda.Runtime.PYTHON_3_9)
        lambda_builder.handler("example.handler")
        lambda_builder.code_from_bucket(object_key="example")

        lambda_function = lambda_builder.build()

        self.assertIsNotNone(lambda_function)


if __name__ == '__main__':
    unittest.main()
