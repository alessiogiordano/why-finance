#
#  main.py
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Created by Alessio Giordano on 14/12/24.
#

from os import environ # Environment Variables
from utils.logger import logger
from utils.subscribe import subscribe
import httpx
import uuid

def send_apns_notification(device_token, payload, lang_code='en'):
    identifier = str(uuid.uuid4())
    # 'https://api.sandbox.push.apple.com:443/3/device/'
    # 'https://api.push.apple.com:443/3/device/'
    endpoint = environ.get('APNS_ENDPOINT', 'https://api.sandbox.push.apple.com:443/3/device/')
    headers = {
        'apns-push-type': 'alert',
        'apns-topic': 'uni.alessiogiordano.NSWhyFinance.App'
    }
    if payload['reason']['high'] and payload['reason']['low']:
        payload['aps'] = {
            'alert': {
                'title': f"{payload['ticker']} ha superato i limiti" if lang_code == 'it' else f"{payload['ticker']} has exceeded its bounds",
                'body': f"{payload['price']} al {payload['timestamp']}" if lang_code == 'it' else f"{payload['price']} as of {payload['timestamp']}"
            }
        }
    elif payload['reason']['high']:
        payload['aps'] = {
            'alert': {
                'title': f"{payload['ticker']} ha superato il limite superiore" if lang_code == 'it' else f"{payload['ticker']} has exceeded its upper bound",
                'body': f"{payload['price']} al {payload['timestamp']}" if lang_code == 'it' else f"{payload['price']} as of {payload['timestamp']}"
            }
        }
    elif payload['reason']['low']:
        payload['aps'] = {
            'alert': {
                'title': f"{payload['ticker']} ha superato il limite inferiore" if lang_code == 'it' else f"{payload['ticker']} has exceeded its lower bound",
                'body': f"{payload['price']} al {payload['timestamp']}" if lang_code == 'it' else f"{payload['price']} as of {payload['timestamp']}"
            }
        }
    elif payload['reason']['background']:
        payload['aps'] = {
            'content-available': 1
        }
    else:
        return # Not handled
    
    with httpx.Client(http2=True, cert='aps.pem') as client:
        logger.info(f"willSendPushNotification: '{identifier}'")
        #
        response = client.post(endpoint + device_token, headers=headers, json=payload)
        #
        logger.info(f"{identifier} {response.status_code}")
#-----------------------------------------------------------------------------------------

def send_notification(message):
    try:
        if 'receiver' not in message:
            return # Malformed
        
        if 'apns' in message['receiver']:
            device_token = message['receiver']['apns']
            del message['receiver']
            #
            send_apns_notification(device_token, message)
    except Exception as e:
        logger.error(f"{e}")
        pass
#-----------------------------------------------------------------------------------------

if __name__ == '__main__':
    subscribe(callback=send_notification, json=True, log=True)
#-----------------------------------------------------------------------------------------