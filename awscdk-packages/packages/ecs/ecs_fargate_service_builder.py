from aws_cdk import aws_ecs as ecs, aws_elasticloadbalancingv2 as elbv2, aws_ecs_patterns as ecs_patterns, \
    aws_certificatemanager as acm, Stack

from packages.builder import Builder


class EcsFargateServiceBuilder(Builder):

    def __init__(self, construct_id: str, stack: Stack):
        super().__init__(construct_id, stack)
        self.__ecs_cluster = None
        self.__load_balancer = None
        self.__cpu = 256
        self.__memory_limit_mib = 512
        self.__desired_count = 1
        self.__container_image = None
        self.__container_name = None
        self.__container_port = None
        self.__public_load_balancer = True
        self.__certificate_arn = None
        self.__task_role = None
        self.__execution_role = None
        self.__secrets = None
        self.__environment = None
        self.__assign_public_ip = None

    def ecs_cluster(self, ecs_cluster):
        self.__ecs_cluster = ecs_cluster

    def load_balancer(self, load_balancer: elbv2.IApplicationLoadBalancer):
        self.__load_balancer = load_balancer

    def cpu(self, cpu):
        self.__cpu = cpu

    def memory_limit_mib(self, memory_limit_mib):
        self.__memory_limit_mib = memory_limit_mib

    def desired_count(self, desired_count):
        self.__desired_count = desired_count

    def container_image(self, container_image):
        self.__container_image = container_image

    def container_name(self, container_name):
        self.__container_name = container_name

    def container_port(self, container_port: int):
        self.__container_port = container_port

    def public_load_balancer(self, public_load_balancer):
        self.__public_load_balancer = public_load_balancer

    def certificate_arn(self, certificate_arn):
        self.__certificate_arn = certificate_arn

    def task_role(self, task_role):
        self.__task_role = task_role

    def execution_role(self, execution_role):
        self.__execution_role = execution_role

    def secrets(self, secrets):
        self.__secrets = secrets

    def environment(self, environment):
        self.__environment = environment

    def assign_public_ip(self, assign_public_ip):
        self.__assign_public_ip = assign_public_ip

    def build(self) -> ecs_patterns.ApplicationLoadBalancedFargateService:
        task_image_options = ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
            image=ecs.ContainerImage.from_registry(self.__container_image),
            container_name=self.__container_name,
            container_port=self.__container_port,
            task_role=self.__task_role,
            execution_role=self.__execution_role,
            secrets=self.__secrets,
            environment=self.__environment
        )

        certificate = (
            acm.Certificate.from_certificate_arn(self.stack, f"{self.construct_id}Certificate",
                                                 certificate_arn=self.__certificate_arn)
            if self.__certificate_arn else None
        )

        service = ecs_patterns.ApplicationLoadBalancedFargateService(self.stack,
                                                                     f"{self.construct_id}ALB",
                                                                     cluster=self.__ecs_cluster,
                                                                     cpu=self.__cpu,
                                                                     load_balancer=self.__load_balancer,
                                                                     desired_count=self.__desired_count,
                                                                     task_image_options=task_image_options,
                                                                     memory_limit_mib=self.__memory_limit_mib,
                                                                     public_load_balancer=self.__public_load_balancer,
                                                                     certificate=certificate,
                                                                     assign_public_ip=self.__assign_public_ip)
        return service
