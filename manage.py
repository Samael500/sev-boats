# -*- coding: utf-8 -*-

import os
import sys
import sevboats

from apscheduler.schedulers.blocking import BlockingScheduler

# init variables
scheduler = BlockingScheduler()
twitter = sevboats.Twitter()
middaygun = sevboats.MiddayGun()

# def functions
@scheduler.scheduled_job('cron', hour='12', second='5', id='middaygun')
def middaygun_msg():
    """ Post middaygun messages """
    return twitter.post_tweet(middaygun.get_message())


if __name__ == '__main__':
    # print (sys.argv)
    print 'Press Ctrl+C to exit'

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
