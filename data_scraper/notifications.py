from datetime import datetime

import requests

webhook = "https://hooks.slack.com/services/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"
payload = {
    "channel":
    "#algotrading",
    "username":
    "Talebot",
    "icon_emoji":
    ":taleb:",
    "attachments": [{
        "color": "#B22222",
        "title": "data_scraper error",
        "footer": "Talebot",
    }]
}


def slack_notification(text, scraper):
    """Post Slack notification"""
    payload["attachments"][0]["fallback"] = text
    payload["attachments"][0]["text"] = text
    payload["attachments"][0]["fields"] = [{"title": scraper}]
    payload["attachments"][0]["ts"] = datetime.today().timestamp()

    response = requests.post(webhook, json=payload)

    if response.status_code != 200:
        raise ValueError(
            "Request to slack returned an error {}, the response is:\n{}".
            format(response.status_code, response.text))
