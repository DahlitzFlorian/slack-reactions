import os

from slackeventsapi import SlackEventAdapter
from slackclient import SlackClient


slack_signing_secret = os.environ["SLACK_SIGNING_SECRET"]
slack_events_adapter = SlackEventAdapter(slack_signing_secret, "/slack/events")

slack_bot_token = os.environ["SLACK_BOT_TOKEN"]
slack_client = SlackClient(slack_bot_token)


_CHANNEL = "introductions"
_REACTION = "wave"


@slack_events_adapter.on("message")
def handle_message(event_data):
    message = event_data["event"]
    if message.get("subtype") is None and message["channel"] == _CHANNEL:
        slack_client.api_call("reactions.add", channel=channel, name=_REACTION, timestamp=message["ts"])


@slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))


slack_events_adapter.start(port=3000)
