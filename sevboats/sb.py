# -*- coding: utf-8 -*-

from src import messages

m = messages.Message()

mm = m.get_messages()

for _m in mm:
    print (_m)
