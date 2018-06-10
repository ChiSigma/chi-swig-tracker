import requests
import json
from src.app import app


def new_user_alert(name, email):
    message = "Hey! A new user with email: {0} and name: {1} signed up!"
    send_alert(message.format(email, name))


def exception_alert(e):
    message = str(e)
    send_alert(message)


def send_alert(message):
    slack_alert_url = app.config['SLACK_ALERTS']
    if slack_alert_url is None: 
        print "No slack alert configured: {0}".format(message)
        return

    payload = {"text": message}
    try:
        response = requests.post(
            slack_alert_url, data=json.dumps(payload),
            headers={'Content-Type': 'application/json'}
        )
    except Exception:
        print "SLACK ALERT FAILED!!!: {0}".format(message)
