from aws_cdk import aws_s3 as s3, Stack

from packages.builder import Builder


class S3Builder(Builder):

    def __init__(self, construct_id: str, stack: Stack):
        super().__init__(construct_id, stack)
        self.__bucket_name = None
        self.__index_document = None
        self.__error_document = None

    def bucket_name(self, bucket_name):
        self.__bucket_name = bucket_name

    def website_documents(self, index_document, error_document=None):
        """
        The name of the index and error documents (e.g. "index.html", "error.html") for the website.
        Enables static website hosting for this bucket. Default: - No index document.
        :param index_document:
        :param error_document:
        :return:
        """
        self.__index_document = index_document
        self.__error_document = error_document
        return self

    def build(self) -> s3.Bucket:
        s3_bucket = s3.Bucket(self.stack, self.construct_id,
                              bucket_name=self.__bucket_name,
                              website_index_document=self.__index_document,
                              website_error_document=self.__error_document)
        return s3_bucket
