from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

def post_to_slack(channel: str, text: str, token: str):
    client = WebClient(token=token)
    try:
        response = client.chat_postMessage(channel=channel, text=text)
    except SlackApiError as e:
        assert e.response["error"]