import reddit_news_bot.lambda_handler as sut
import boto3
from moto import mock_aws
from unittest.mock import patch, MagicMock

table_name = 'test-table'

def __create_table(dynamodb):
    return dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'url',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'url',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

def __put_item(table, url):
    table.put_item(
            Item={
                'url': f'{url}'
            }
    )

def __item_exists(table, url) -> bool:
    response = table.get_item(Key={'url': f'{ url }'})
    return 'Item' in response


@patch('reddit_news_bot.lambda_handler.TABLE_NAME', table_name)
@patch('reddit_news_bot.lambda_handler.get_secret', MagicMock())
@patch('reddit_news_bot.lambda_handler.get_latest_post')
@patch('reddit_news_bot.lambda_handler.RedditPoster')
@mock_aws
def test_already_posted(mock_reddit_poster, mock_get_latest_post):
    # arrange
    url = "https://google.com"

    dynamodb = boto3.resource('dynamodb')
    table = __create_table(dynamodb)
    __put_item(table, url)

    expected_title = 'title'
    expected_content = MagicMock()
    expected_url = url
    mock_get_latest_post.return_value = (expected_title, expected_content, expected_url)

    # act 
    sut.handler(None, None)

    # assert
    assert mock_reddit_poster.submit.call_count == 0
    assert __item_exists(table, expected_url)


@patch('reddit_news_bot.lambda_handler.TABLE_NAME', table_name)
@patch('reddit_news_bot.lambda_handler.get_secret', MagicMock())
@patch('reddit_news_bot.lambda_handler.get_latest_post')
@patch('reddit_news_bot.lambda_handler.RedditPoster')
@mock_aws
def test_new_post(mock_reddit_poster, mock_content_scraper):
    # arrange
    url = "https://google.com"

    dynamodb = boto3.resource('dynamodb')
    table = __create_table(dynamodb)
    __put_item(table, url)

    expected_title = 'title'
    expected_content = MagicMock()
    first_url = "https://google2.com"
    second_url = "https://google3.com"

    mock_content_scraper.side_effect = [
        (expected_title, expected_content, first_url),
        (expected_title, expected_content, second_url)
    ]

    # act
    sut.handler(None, None)

    # assert
    instance = mock_reddit_poster.return_value
    assert instance.submit.call_count == 2
    assert __item_exists(table, first_url)
    assert __item_exists(table, second_url)
