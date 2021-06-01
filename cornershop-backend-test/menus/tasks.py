"""This module contains the tasks that will be executed
by celery"""
import json

from backend_test.celery import app
from backend_test.slack_bot import slack_client

from slack_sdk.errors import SlackApiError

from menus.models.menu import Menu

FOOD_CHANNEL = 'C023WJKGU4Q'


@app.task(autoretry_for=(SlackApiError,), max_retries=3)
def publish_menu(menu_id):
    """This method publish a specific menu to Slack.

    First it obtains the menu and its options
    Then it obtains the ids of the members of the food channel
    in slack.
    Then it creates a generator and the message with the required
    format for slack interactive message.
    Then it will send to the members of the group a message.
    Finally it verifies that all the responses given from slack
    are True and sets the is_published field of the menu
    to true.
    """
    menu = Menu.objects.prefetch_related('menuoption_set').get(id=menu_id)
    options = menu.get_options_for_slack()
    users_slack_request = slack_client.conversations_members(
        channel=FOOD_CHANNEL
    )
    users_slack_ids = ( member for member in users_slack_request['members'])
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Selecciona tu menú de hoy"
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "radio_buttons",
                    "options": options,
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Crear Orden",
                    },
                    "action_id": "gomenu"
                }
            ]
        },
        {
            "type": "input",
            "element": {
                "type": "plain_text_input",
                "multiline": True,
            },
            "label": {
                "type": "plain_text",
                "text": "Personaliza tu menú",
                "emoji": True
            }
        }
    ]
    results = [
        slack_client.chat_postMessage(
            channel=member,
            text="data",
            blocks=blocks
        )['ok']
        for member in users_slack_ids
    ]
    if all(results):
        menu.is_published = True
        menu.save()
    return True
