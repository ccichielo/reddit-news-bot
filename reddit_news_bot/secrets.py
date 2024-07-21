import boto3
import json
from botocore.exceptions import ClientError


def get_secret():

    secret_name = "reddit-news-bot/secret"
    # region_name = "us-east-1"

    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager')

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secret = get_secret_value_response['SecretString']
    return json.loads(secret)
