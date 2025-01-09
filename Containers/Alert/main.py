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
from utils.broadcast import broadcast
from utils.subscribe import subscribe

from handlers.users import queries as QueryHandler
query_handler = QueryHandler()

def dispatch_notification_for_user(user, ticker, price, timestamp):
    try:
        if type(user['device_token']) is not str:
            return # No device to send to
        #
        past_high_threshold = False
        past_low_threshold = False
        if user['high_value'] is not None:
            if user['low_value'] is not None:
                if user['high_value'] <= user['low_value']:
                    return # Invalid
            if price > user['high_value']:
                past_high_threshold = True
        if user['low_value'] is not None:
            if price < user['low_value']:
                past_low_threshold = True
        #
        broadcast('notification_center', {
            'receiver': {
                'apns': user['device_token']
            },
            'ticker': ticker,
            'price': price,
            'timestamp': timestamp,
            'reason': {
                'high': past_high_threshold,
                'low': past_low_threshold,
                'background': not (past_high_threshold or past_low_threshold)
            }
        })
    except Exception as e:
        logger.error(f"{e}")
        pass
#-----------------------------------------------------------------------------------------

def dispatch_notifications_for_updated_stock(stock):
    try:
        query_handler.foreach_user_with_ticker(stock['ticker'],
            lambda user : dispatch_notification_for_user(user, stock['ticker'], stock['price'], stock['timestamp']))
    except Exception as e:
        logger.error(f"{e}")
        pass
#-----------------------------------------------------------------------------------------

if __name__ == '__main__':
    subscribe(callback=dispatch_notifications_for_updated_stock, json=True, log=True)
#-----------------------------------------------------------------------------------------