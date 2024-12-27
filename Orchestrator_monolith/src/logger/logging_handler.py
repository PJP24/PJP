import logging
import boto3
from datetime import datetime
from uuid import uuid4
import pytz
from botocore.exceptions import ClientError


class DynamoDBLogHandler(logging.Handler):
    def __init__(self, table_name='logs'):
        super().__init__()
        self.dynamodb = boto3.resource('dynamodb', region_name='eu-north-1')
        self.table = self.dynamodb.Table(table_name)

    def emit(self, record):
        log_entry = self.format(record)
        log_id = str(uuid4())

        utc_time = datetime.utcnow().replace(tzinfo=pytz.utc)
        gmt_plus_2_time = utc_time.astimezone(pytz.timezone('Europe/Stockholm'))
        timestamp = gmt_plus_2_time.strftime('%Y-%m-%d %H:%M:%S')

        try:
            self.table.put_item(
                Item={
                    'id': log_id,
                    'timestamp': timestamp,
                    'log_level': record.levelname,
                    'message': log_entry,
                }
            )
        except ClientError as e:
            print(f"Failed to log to DynamoDB: {e}")
