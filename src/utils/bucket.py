import boto3
from botocore.exceptions import ClientError

from config import settings

class Bucket:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.client = boto3.client(
            "s3",
            aws_access_key_id=settings.MINIO_ACCESS_KEY,
            aws_secret_access_key=settings.MINIO_SECRET_KEY,
            endpoint_url=settings.MINIO_ENDPOINT,
        )
        self._create_bucket_if_not_exists()

    def _create_bucket_if_not_exists(self):
        try:
            self.client.head_bucket(Bucket=self.bucket_name)
        except ClientError:
            self.client.create_bucket(Bucket=self.bucket_name)

    def upload_data(self, name, data):
        self.client.put_object(Bucket=self.bucket_name, Key=name, Body=data)

    def upload_file(self, file, file_name):
        self.client.put_object(Bucket=self.bucket_name, Key=file_name, Body=file)

    def download_file(self, file_name):
        self.client.download_file(self.bucket_name, file_name, file_name)

    def delete_file(self, file_name):
        self.client.delete_object(Bucket=self.bucket_name, Key=file_name)

    def get_file_url(self, file_name):
        return self.client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket_name, "Key": file_name},
            ExpiresIn=3600,
        )


bucket_images = Bucket("images")
bucket_videos = Bucket("videos")


