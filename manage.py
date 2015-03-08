#!venv/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import traceback
import logging
from colorama import Fore
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from daemon import Daemon

import sevboats


# init variables
scheduler = BlockingScheduler()
twitter = sevboats.Twitter()
middaygun = sevboats.MiddayGun()
ship_messenger = sevboats.ShipMessenger()

date_format = '%Y-%m-%d %H:%M :'

logging.basicConfig(level=logging.INFO)

# def functions

def logger(function):

    def wrapper():
        try:
            result = function()
            print Fore.BLUE, datetime.now().strftime(date_format),
            print Fore.GREEN, result['text'].replace('\n', ' - '),
        except Exception, e:
            print Fore.BLUE, datetime.now().strftime(date_format),
            print Fore.RED, e.message
            traceback.print_exc(file=sys.stdout)
        finally:
            print Fore.RESET
    return wrapper


@scheduler.scheduled_job('cron', hour='12', minute='0', second='5', id='middaygun')
@logger
def middaygun_msg():
    """ Post middaygun messages """
    message = middaygun.get_message()
    print 'middaygun:', message
    return twitter.post_tweet(message)


@scheduler.scheduled_job('cron', hour='19', minute='0', second='5', id='weather')
@logger
def weather_msg():
    """ Post weather messages """
    print 'weather: message'
    return twitter.post_image_weather()


# @scheduler.scheduled_job('cron', hour='6-22', minute='15,45', id='ship_status')
# @logger
# def ship_status_msg():
#     """ Post ship status messages """
#     now = datetime.now()
#     minute = now.minute
#     hour = now.hour
#     status, change = sevboats.send_fleet_message()
#     message = ship_messenger.get_message(status)
#     if change or (not(hour % sevboats.settings.MESSAGE_PERIOD) and minute < 30):
#         print 'ship status:', message
#         return twitter.post_tweet(message)
#     else:
#         return dict(text=Fore.YELLOW + message)


class SevboatsDaemon(Daemon):

    pidfile_path = 'sevboats.pid'
    # logfile_path = 'sevboats.log'

    def __init__(self):
        super(SevboatsDaemon, self).__init__(pidfile=self.pidfile_path)

    def run(self):
        print 'daemon run at:', datetime.now().strftime(date_format)
        # ship_status_msg()
        scheduler.start()


if __name__ == '__main__':
    # init daemon
    sev_daemon = SevboatsDaemon()

    # run comand
    if 'start' in sys.argv:
        print 'start daemon: %s' % sev_daemon.pidfile_path
        sev_daemon.start()
    elif 'stop' in sys.argv:
        print 'stop daemon: %s' % sev_daemon.pidfile_path
        sev_daemon.stop()
    elif 'restart' in sys.argv:
        print 'restart daemon: %s' % sev_daemon.pidfile_path
        sev_daemon.restart()
    elif 'nodaemon' in sys.argv:
        print 'Press Ctrl+C to exit'
        # ship_status_msg()
        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            pass
    else:
        print 'wrong choice - must be: *start*, *stop* or *restart*'
