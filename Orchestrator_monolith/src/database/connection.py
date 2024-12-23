import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import os

class DynamoDBClient:
    def __init__(self, region: str = 'eu-north-1'):
        try:
            aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
            aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

            if aws_access_key_id and aws_secret_access_key:
                self.dynamodb = boto3.resource(
                    'dynamodb',
                    region_name=region,
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key
                )
            else:
                self.dynamodb = boto3.resource('dynamodb', region_name=region)


            self.dynamodb.tables.all()

        except (NoCredentialsError, PartialCredentialsError) as e:
            print("AWS credentials are missing or incomplete:", e)
            raise
        except Exception as e:
            print(f"Connection failed: {str(e)}")
            raise

    def get_client(self):
        return self.dynamodb
