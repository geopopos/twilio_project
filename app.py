import os
import json

from flask import Flask, abort, current_app, request, redirect
from functools import wraps
from twilio.twiml.messaging_response import MessagingResponse
from twilio.request_validator import RequestValidator
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

def validate_twilio_request(f):
    """Validates that incoming requests genuinely originated from Twilio"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get TWILIO_AUTH_TOKEN
        if app.env == "development":
            TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
        elif app.env == "production":
            with open('/etc/config.json') as config_file:
                config = json.load(config_file)
                TWILIO_AUTH_TOKEN = config.get("TWILIO_AUTH_TOKEN")
        # Create an instance of the RequestValidator class
        validator = RequestValidator(TWILIO_AUTH_TOKEN)

        # Validate the request using its URL, POST data,
        # and X-TWILIO-SIGNATURE header
        request_valid = validator.validate(
            request.url,
            request.form,
            request.headers.get('X-TWILIO-SIGNATURE', ''))

        # Continue processing the request if it's valid (or if DEBUG is True)
        # and return a 403 error if it's not
        if request_valid or current_app.debug:
            return f(*args, **kwargs)
        else:
            return abort(403)
    return decorated_function


@app.route("/")
def hello():
    return "Hello Groot"

@app.route("/sms", methods=['GET', 'POST'])
@validate_twilio_request
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response
    if request.values.get('From') == "+14436438559":
        resp = MessagingResponse()

        # Add a message
        resp.message("The Robots are coming! Head for the hills!")

        return str(resp)
    else:
        resp = MessagingResponse()

        # Add a message
        resp.message("Piss off, you aren't George")

        return str(resp)


if __name__ == "__main__":
    app.run()

