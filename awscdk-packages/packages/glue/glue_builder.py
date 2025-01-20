from aws_cdk import aws_glue as glue, Stack

from packages.builder import Builder


class GlueBuilder(Builder):

    def __init__(self, construct_id: str, stack: Stack):
        super().__init__(construct_id, stack)
        # https://github.com/aws-samples/aws-cdk-examples/blob/main/python/athena-s3-glue/athena_s3_glue/athena_s3_glue_stack.py
    #     self.__queue_name = None
    #
    #
    # def queue_name(self, queue_name):
    #     self.__queue_name = queue_name
    #     return self
    #
    # def build(self) -> glue.CfnConnection:
    #     return sqs.Queue(self.stack, self.construct_id,
    #                      queue_name=self.__queue_name,
    #                      fifo=self.__fifo,
    #                      retention_period=self.__retention_period,
    #                      dead_letter_queue=self.__dead_letter_queue)
