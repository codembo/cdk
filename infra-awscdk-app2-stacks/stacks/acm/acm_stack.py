from aws_cdk import aws_certificatemanager as acm, Environment, Stack
from constructs import Construct


class CertificateStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, *, env: Environment, domain_name: str, **kwargs) -> None:
        super().__init__(scope, construct_id, env=env, **kwargs)

        # Criação do certificado
        self.certificate = acm.Certificate(
            self,
            "Certificate",
            domain_name=domain_name,
            validation=acm.CertificateValidation.from_dns()
        )
