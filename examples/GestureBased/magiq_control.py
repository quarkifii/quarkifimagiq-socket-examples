import requests
import hmac
import hashlib
import json
from datetime import datetime, timezone

api_key = 'b36d91f3-8945-497c-bedf-f847c0907247'
secret_key = '104bee46-52cd-40bd-983b-f2b1d294de50'


# Function to get device
def get_device(device_id):
    timestamp = datetime.now(timezone.utc).isoformat()
    content = api_key + timestamp
    signature = hmac.new(secret_key.encode(), content.encode(), hashlib.sha256).hexdigest()

    url = 'https://api.magiqworks.com/api-ext-magiq/device'
    headers = {
        'MQ-TIMESTAMP': timestamp,
        'MQ-API-KEY': api_key,
        'MQ-SIGNATURE': signature,
        'Content-Type': 'application/json'
    }
    body = {
        'deviceId': device_id,
        'action': 'GET'
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(body))
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        print('Error getting device:', error)
        return None


# Function to check device is on or off
def get_device_state(device_id):
    response = get_device(device_id)
    device_json_str = response["device"].replace("'", '"')

    device_data = json.loads(device_json_str)[0]
    device_state = device_data['deviceState']
    switch = device_state['switch_1']
    return switch


# Function to turn device on or off
def device_on_off(device_id, operation):
    try:
        timestamp = datetime.now(timezone.utc).isoformat()
        content = api_key + timestamp
        signature = hmac.new(secret_key.encode(), content.encode(), hashlib.sha256).hexdigest()
        url = 'https://api.magiqworks.com/api-ext-magiq/device'
        headers = {
            'MQ-TIMESTAMP': timestamp,
            'MQ-API-KEY': api_key,
            'MQ-SIGNATURE': signature,
            'Content-Type': 'application/json'
        }
        request_data = {
            'deviceId': device_id,
            'action': 'SET',
            'device': {
                'deviceId': device_id,
                'deviceChangeCounter': 10,
                'deviceState': {'switch_1': '1' if operation else '0'}
            }
        }
        post_response = requests.post(url, headers=headers, data=json.dumps(request_data))
        post_response.raise_for_status()
        return post_response.json()
    except requests.RequestException as error:
        print('Error in device_on_off:', error)
        raise error
    except json.JSONDecodeError as parse_error:
        print('Error parsing device response:', parse_error)
        raise parse_error
