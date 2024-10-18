import requests
import hmac
import hashlib
import json
from datetime import datetime, timezone

api_key = '__COLLECT_API_KEY_FROM_MAGIQ_STORE__'
secret_key = '__COLLECT_SECRET_KEY_FROM_MAGIQ_STORE__'

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
