import threading

from django.apps import AppConfig

from slack_bolt import App

from backend_test.envtools import getenv


class SlackdaemonConfig(AppConfig):
    name = 'slackdaemon'
