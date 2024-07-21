from datetime import datetime, timezone

import boto3

class DynamoConnection:
    def __init__(self, table_name):
        dynamodb = boto3.resource('dynamodb')
        self.__table = dynamodb.Table(table_name)

    def item_exists(self, url) -> bool:
        try:
            response = self.__table.get_item(Key={'url': f'{ url }'})
            return 'Item' in response
        except Exception as e:
            print(f'Failed to fetch from dynamodb: {e}')
            raise

    def add_item(self, url):
        try:
            timestamp = datetime.now(timezone.utc).isoformat()
            item = {
                'url': url,
                'timestamp': timestamp
            }

            self.__table.put_item(Item=item)
        except Exception as e:
            print(f'Failed to put item to dynamodb: {e}')
            raise


