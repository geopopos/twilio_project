from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World"

@app.route("/sms", methods=['GET', 'POST'])
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

