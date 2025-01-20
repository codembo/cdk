from aws_cdk import aws_ecr as ecr, Stack
from constructs import Construct
from packages.ecr.ecr_builder import EcrBuilder

from config import env_config


class EcrStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.__create_ecr()

    def __create_ecr(self):
        ecr_builder = EcrBuilder("Ip360Repository", self)
        ecr_builder.repository_name(f"api-node-ip360-integration")
        #ecr_builder.grant_cross_account_access(env_config.CROSS_ACCOUNT_ACCESS_ACCOUNT_IDS.split(","))
        ecr_builder.encryption(ecr.RepositoryEncryption.AES_256)

        return ecr_builder.build()
