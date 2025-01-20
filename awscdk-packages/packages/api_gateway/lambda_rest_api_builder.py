from aws_cdk import aws_apigateway as api_gateway, aws_lambda as _lambda, Stack

from packages.builder import Builder


class LambdaRestApiBuilder(Builder):

    def __init__(self, construct_id: str, stack: Stack):
        super().__init__(construct_id, stack)
        self.__handler = None
        self.__proxy = True

    def handler(self, handler: _lambda.IFunction):
        self.__handler = handler
        return self

    def proxy(self, proxy: bool):
        self.__proxy = proxy
        return self

    def build(self) -> api_gateway.LambdaRestApi:
        api = api_gateway.LambdaRestApi(self.stack, self.construct_id,
                                        handler=self.__handler,
                                        proxy=self.__proxy)
        return api
