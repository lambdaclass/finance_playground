import logging
from datetime import datetime

import requests

logger = logging.getLogger(__name__)

webhook = "https://hooks.slack.com/services/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"
payload = {
    "channel": "#sandbox",
    "username": "Talebot",
    "icon_emoji": ":taleb:",
    "attachments": [{
        "footer": "Talebot"
    }]
}


def slack_notification(text, scraper):
    """Post Slack notification"""
    payload["attachments"][0]["fallback"] = text
    payload["attachments"][0]["text"] = text
    payload["attachments"][0]["color"] = "#B22222"
    payload["attachments"][0]["title"] = "data_scraper error"
    payload["attachments"][0]["fields"] = [{"title": scraper}]
    payload["attachments"][0]["ts"] = datetime.today().timestamp()

    response = requests.post(webhook, json=payload)

    if response.status_code != 200:
        msg = "Error connecting to Slack {}. Response is:\n{}".format(
            response.status_code, response.text)
        logger.error(msg)


def slack_report(text, module):
    """Send report of successful backup/scraping to Slack"""
    payload["attachments"][0]["fallback"] = text
    payload["attachments"][0]["text"] = text
    payload["attachments"][0]["color"] = "#49C39E"
    payload["attachments"][0]["title"] = "data_scraper status report"
    payload["attachments"][0]["fields"] = [{"title": module}]
    payload["attachments"][0]["ts"] = datetime.today().timestamp()

    response = requests.post(webhook, json=payload)

    if response.status_code != 200:
        msg = "Error connecting to Slack {}. Response is:\n{}".format(
            response.status_code, response.text)
        logger.error(msg)
