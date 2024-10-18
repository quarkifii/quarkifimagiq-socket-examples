from flask import request
from twilio.twiml.messaging_response import MessagingResponse

from app.magiq import device_on_off
from . import app

# Device IDs
devices = {
    'ac': '16612385',
    'light': '11715506'
}

device_list = list(devices.keys())

# Creating the message
message = "You have these registered devices:\n" + "\n".join(device_list)


@app.route("/whatsapp", methods=['POST'])
def whatsapp():
    message_body = request.form.get('Body', '').lower()
    print('Message received:', message_body)
    response = MessagingResponse()

    command = "turn on" if "on" in message_body \
        else "turn off" if "off" in message_body \
        else "list" if "list" in message_body \
        else None
    device = "ac" if "ac" in message_body else "light" if "light" in message_body else None

    if command and device:
        operation = command == "turn on"
        device_on_off(devices[device], operation)
        response.message(f"The {device} has been turned {'ON' if operation else 'OFF'}.")
    elif command == "list":
        response.message(message)
    else:
        response.message("Hello, How may I help you. \n\n use 'List' for all your MagIQ Socket\n\n use "
                         "'on/off <device name>' to operate")

    return str(response)
