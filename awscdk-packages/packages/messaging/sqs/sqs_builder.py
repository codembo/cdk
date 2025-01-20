from aws_cdk import aws_sqs as sqs, Stack, Duration

from packages.builder import Builder


class SqsBuilder(Builder):

    def __init__(self, construct_id: str, stack: Stack):
        super().__init__(construct_id, stack)
        self.__queue_name = None
        self.__fifo = None
        self.__retention_period = None
        self.__dead_letter_queue = None

    def queue_name(self, queue_name):
        self.__queue_name = queue_name
        return self

    def fifo(self, fifo: bool):
        self.__fifo = fifo
        return self

    def retention_period(self, retention_period: Duration):
        self.__retention_period = retention_period
        return self

    def add_dead_letter_queue(self, max_receive_count: int):
        dlq = sqs.Queue(self.stack, self.construct_id + "-dlq",
                        queue_name=self.__queue_name + "-dlq")
        self.__dead_letter_queue = sqs.DeadLetterQueue(max_receive_count=max_receive_count, queue=dlq)

    def build(self) -> sqs.Queue:
        return sqs.Queue(self.stack, self.construct_id,
                         queue_name=self.__queue_name,
                         fifo=self.__fifo,
                         retention_period=self.__retention_period,
                         dead_letter_queue=self.__dead_letter_queue)
