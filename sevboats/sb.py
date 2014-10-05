# -*- coding: utf-8 -*-

from src import messages
from src.twitter import Twitter

m = messages.Messenger()

mm = m.get_messages()

t = Twitter()

_m = m.get_message()

t.post(_m)
r = t.post_tweet(_m)

# print r['id_str']

from time import sleep 

# sleep(40)

print (t.delete_tweet(r['id_str']))

