"""This module contains the required code in order to create a
slack client instance so this app cand post messages. In
order to be loaded correctly remember to set the SLACK_BOT_TOKEN
environment variable."""

import os

from .envtools import getenv

from slack_sdk import WebClient

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend_test.settings")

slack_client = WebClient(token=getenv("SLACK_BOT_TOKEN"))
