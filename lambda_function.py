import os
from datetime import datetime, timezone, timedelta

import notion
from  twitter import TwitterAPIClient


def lambda_handler(event, context):
    # env for Twitter
    twitter_user_id = os.environ['TWITTER_USER_ID']
    twitter_consumer_key=os.environ['TWITTER_API_KEY']
    twitter_consumer_secret=os.environ['TWITTER_API_KEY_SECRET']
    twitter_access_token=os.environ['TWITTER_ACCESS_TOKEN']
    twitter_access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET']

    # env for Notion
    NOTION_API_TOKEN = os.environ['NOTION_API_TOKEN']
    NOTION_PARENT_DATABASE_ID = os.environ['NOTION_PARENT_DATABASE_ID']
    NOTION_POINTER_PAGE_ID = os.environ['NOTION_POINTER_PAGE_ID']

    # date range
    NOW = datetime.now()
    # this setting exepects that this function invoked every hour
    START = (NOW - timedelta(hours=1)).replace(minute=0, second=0, microsecond=0).astimezone(timezone.utc)
    END   = START + timedelta(hours=1)

    # get pointer from Notion pointer page
    pointer_block = notion.get_blocks_by_page_id(NOTION_API_TOKEN, NOTION_POINTER_PAGE_ID)[0]
    pointer_block_id = pointer_block['id']
    pointer = int(pointer_block['paragraph']['rich_text'][0]['text']['content'])

    twitter_client = TwitterAPIClient(
        twitter_consumer_key,
        twitter_consumer_secret,
        twitter_access_token,
        twitter_access_token_secret)
    liked_tweets = twitter_client.get_liked_tweets(twitter_user_id)

    # record next pointer
    next_pointer = str(liked_tweets[0].id)

    for lt in liked_tweets:
        if lt.id == pointer:
            print(f'[*] Tweet ID {lt.id} is match pointer.')
            break
        else:
            print(f'[*] Tweet ID {lt.id}')
            page = notion.generate_tweet_page(NOTION_PARENT_DATABASE_ID,
                lt.id, lt.text)
            notion.create_page(NOTION_API_TOKEN, page)
            print(f'[*] Tweet ID {lt.id} was inserted Notion database.')

    # update pointer
    candidate_block = {
        "paragraph": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                    "content": next_pointer,
                    "link": None
                    },
                    "plain_text": next_pointer,
                    "href": None
                }
            ],
        }
    }
    notion.update_block(NOTION_API_TOKEN, pointer_block_id, candidate_block)

    return
