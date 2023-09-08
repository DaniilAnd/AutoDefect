import boto3
from abc import ABC, abstractmethod


class Connect(ABC):
    @abstractmethod
    def __init__(self, config_file):
        self.config_file = config_file


class ConnectS3(Connect):
    def __init__(self, config_file):
        super().__init__(config_file)
        self.self.s3 = boto3.client('s3', aws_access_key_id=config_file['your_access_key'],
                                    aws_secret_access_key=config_file['your_secret_key'],
                                    region_name=config_file['your_region'])
        self.bucket_name = config_file['bucket_name']

    def upload_file(self, local_file_path, remote_file_path):
        if not self.s3:
            raise Exception("S3 connection is not initialized. Call connect() method first.")

        try:
            self.s3.upload_file(local_file_path, self.bucket_name, remote_file_path)
            print(f"Uploaded {local_file_path} to S3 bucket {self.bucket_name} as {remote_file_path}")
        except Exception as e:
            print(f"Failed to upload {local_file_path} to S3: {str(e)}")


if __name__ == "__main__":
    config_file = 'test.yaml'
    s3_connection = ConnectS3(config_file)
    local_file_path = 'test.txt'
    remote_file_path = local_file_path

    s3_connection.upload_file(local_file_path, remote_file_path)
