import io
import boto3
from botocore.exceptions import ClientError
from app.conf.settings import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY


class MediaService:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.s3 = boto3.client(
        "s3",
        endpoint_url = f"http://{MINIO_ENDPOINT}",
        aws_access_key_id = MINIO_ACCESS_KEY,
        aws_secret_access_key = MINIO_SECRET_KEY,
        region_name = "us-east-1"
    )
        self.create_bucket()

    def create_bucket(self):
        try:
            self.s3.head_bucket(Bucket=self.bucket_name)
        except ClientError as e:
            error_code = int(e.response.get('Error', {}).get('Code', 0))
            if error_code in [404, 400]:
                try:
                    self.s3.create_bucket(Bucket=self.bucket_name)
                except ClientError as ce:
                    print(f"Failed to create bucket: {ce}")
            else:
                print(f"Unexpected error when checking bucket: {e}")

    def upload_media(self, file):
        try:
            try:
                file.file.seek(0)
            except Exception:
                pass
            self.s3.upload_fileobj(file.file, self.bucket_name, file.filename)
            print(f"Successfully uploaded {file.filename} to bucket {self.bucket_name}")
            return True
        except ClientError as e:
            print(f"Failed to upload {file.filename}: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error uploading {file.filename}: {e}")
            return False

    def download_media(self, filename):
        try:
            fileobj = io.BytesIO()
            self.s3.download_fileobj(self.bucket_name, filename, fileobj)
            fileobj.seek(0)
            print(f"Successfully downloaded {filename} from bucket {self.bucket_name}")
            return fileobj
        except ClientError as e:
            print(f"Failed to download {filename}: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error downloading {filename}: {e}")
            return None
