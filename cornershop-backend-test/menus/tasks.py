import json

from backend_test.celery import app
from backend_test.slack_bot import slack_client

from slack_sdk.errors import SlackApiError

from menus.models.menu import Menu

FOOD_CHANNEL = 'C023WJKGU4Q'

@app.task
def publish_menu(menu_id):
    try:
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
                    "text": "Customize your menu",
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
    except SlackApiError as e:
        print(e)
    return True
