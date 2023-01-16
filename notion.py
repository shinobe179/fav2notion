import os

import requests


def generate_tweet_page(database_id, tweet_id, tweet_text, author_id):
    """
    Generate page block object for tweet.

    Parameters
    ----------
    database_id: int
        Notion database ID.
    
    tweet_id: int
        Tweet ID.
    
    tweet_text: str
        Tweet text.
    
    Returns
    -------
    page: dict
        Notion page data.
    """
    page = {
        'parent': {'database_id': database_id},
        'properties': {
            'Title': {
                'title': [{'text': {'content': tweet_text}}],
            },
            'URL': {
                'url': f'https://twitter.com/TwitterJP/status/{tweet_id}',
            }
        },
        'children': [
            {
                'object': 'block',
                'type': 'paragraph',
                'paragraph': {
                    'rich_text': [
                        {
                            'type': 'text',
                            'text': {
                                'content': tweet_text,
                                'link': {'url': f'https://twitter.com/TwitterJP/status/{tweet_id}'},
                            },
                        },
                    ],
                },
            },
            {
                'object': 'block',
                'type': 'paragraph',
                'paragraph': {
                    'rich_text': [
                        {
                            'type': 'text',
                            'text': {
                                'content': f'(author_id: {author_id})',
                                'link': {'url': f'https://twitter.com/i/user/{author_id}'},
                            },
                        },
                    ],
                },
            },
        ],
    }

    return page


def create_page(token, body):
    """
    Create page in Notion.

    Parameters
    ----------
    token: str
        Notion API token.
    
    body: dict
        Notion page data.
    
    Returns
    -------
    resopnse: requests.Response
        HTTP response data from Notion API.
    """
    headers = { 
        'Authorization': f'Bearer {token}',
	    'Notion-Version': '2022-06-28',
    }
    response = requests.post('https://api.notion.com/v1/pages', headers=headers, json=body)
    print(f'[*] Notion API response: {response.text}')

    return response


def get_blocks_by_page_id(token, page_id):
    headers = { 
        'Authorization': f'Bearer {token}',
	    'Notion-Version': '2022-06-28',
    }
    response = requests.get(f'https://api.notion.com/v1/blocks/{page_id}/children', headers=headers)
    print(f'[*] Notion API response: {response.text}')

    blocks = response.json()['results']

    return blocks


def update_block(token, block_id, block):
    headers = { 
        'Authorization': f'Bearer {token}',
	    'Notion-Version': '2022-06-28',
    }
    response = requests.patch(f'https://api.notion.com/v1/blocks/{block_id}', headers=headers, json=block)
    print(f'[*] Notion API response: {response.text}')

    return
