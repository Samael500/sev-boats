#!./venv/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import logging
from colorama import Fore
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

# def functions


def logger(function):

    def wrapper():
        try:
            print Fore.BLUE, datetime.now().strftime(date_format),
            result = function()
            print Fore.GREEN, result['text'].replace('\n', ' - '),
        except Exception, e:
            print Fore.RED, e.message,
        finally:
            print Fore.RESET
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
        status, change = sevboats.send_fleet_message()
        message = ship_messenger.get_message(status)
        if change or not(hour % settings.MESSAGE_PERIOD):
            return twitter.post_tweet(message)
        else:
            return dict(text=Fore.YELLOW + message)


if __name__ == '__main__':
    # print (sys.argv)
    print 'Press Ctrl+C to exit'
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
