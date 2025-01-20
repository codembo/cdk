from aws_cdk import aws_apigateway as api_gateway, Stack, Duration

from packages.builder import Builder


class RestApiGatewayBuilder(Builder):

    def __init__(self, construct_id: str, stack: Stack):
        super().__init__(construct_id, stack)
        self.__rest_api_name = None
        self.__endpoint_types = [api_gateway.EndpointType.REGIONAL]
        self.__proxy_http_integration_url = None
        self.__integration_timeout = 180
        self.__stage_name = ""

    def rest_api_name(self, rest_api_name):
        self.__rest_api_name = rest_api_name
        return self

    def endpoint_types(self, endpoint_types: list[api_gateway.EndpointType]):
        self.__endpoint_types = endpoint_types
        return self

    def proxy_http_integration_url(self, proxy_http_integration_url):
        self.__proxy_http_integration_url = proxy_http_integration_url
        return self

    def integration_timeout(self, integration_timeout: int):
        self.__integration_timeout = integration_timeout
        return self

    def stage_name(self, stage_name):
        self.__stage_name = stage_name
        return self

    def build(self) -> api_gateway.RestApi:
        api = api_gateway.RestApi(self.stack, self.construct_id,
                                  default_integration=None,
                                  endpoint_types=self.__endpoint_types,
                                  rest_api_name=self.__rest_api_name,
                                  deploy_options=api_gateway.StageOptions(stage_name=self.__stage_name),
                                  deploy=True)

        integration_options = api_gateway.IntegrationOptions(
            timeout=Duration.seconds(self.__integration_timeout),
            request_parameters={
                "integration.request.path.proxy": "method.request.path.proxy"
            })

        proxy_integration = api_gateway.HttpIntegration(url=self.__proxy_http_integration_url,
                                                        http_method="ANY",
                                                        options=integration_options,
                                                        proxy=True)
        api.root.add_proxy(default_integration=proxy_integration,
                           default_method_options=api_gateway.MethodOptions(request_parameters={
                               "method.request.path.proxy": True
                           }),
                           any_method=True,
                           default_cors_preflight_options=api_gateway.CorsOptions(
                               allow_origins=api_gateway.Cors.ALL_ORIGINS,
                               allow_methods=api_gateway.Cors.ALL_METHODS,
                               allow_headers=api_gateway.Cors.DEFAULT_HEADERS,
                               allow_credentials=True
                           ))

        return api
