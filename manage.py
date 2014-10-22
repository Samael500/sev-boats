#!./venv/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import logging
from datetime import datetime
import sevboats

from apscheduler.schedulers.blocking import BlockingScheduler

# init variables
scheduler = BlockingScheduler()
twitter = sevboats.Twitter()
middaygun = sevboats.MiddayGun()
ship_messenger = sevboats.ShipMessenger()

date_format = '%Y-%m-%d %H:%M:%S :'

logging.basicConfig(level=logging.ERROR)

class bcolors:
    INFOBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

# def functions

def logger(function):

    def wrapper():
        try:
            print bcolors.INFOBLUE, datetime.now().strftime(date_format),
            result = function()
            print bcolors.OKGREEN, result['text'].replace('\n', ' - '),
        except Exception, e:
            print bcolors.FAIL, e.message,
        finally:
            print bcolors.ENDC
    return wrapper


@scheduler.scheduled_job('cron', hour='12', minute='0', second='5', id='middaygun')
@logger
def middaygun_msg():
    """ Post middaygun messages """
    message = middaygun.get_message()
    return twitter.post_tweet(message)


@scheduler.scheduled_job('cron', minute='*/30', id='ship_status')
@logger
def ship_status_msg():
    """ Post ship status messages """
    hour = datetime.now().hour
    if hour > 5 and hour < 23:
        status = sevboats.send_fleet_message()
        message = ship_messenger.get_message(status)
        message = message.format(datetime=datetime.now().strftime(date_format))
        return dict(text=message)
        return twitter.post_tweet(message)


if __name__ == '__main__':
    # print (sys.argv)
    print 'Press Ctrl+C to exit'
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
