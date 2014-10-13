# # -*- coding: utf-8 -*-

# from src.twitter import Twitter

# t = Twitter()

# _m = '012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234[140]'

# r = t.post_tweet(_m)
# print r

# # # print r['id_str']

# # # sleep(40)

# # # print (t.delete_tweet(r['id_str']))

# # # r = t.post_tweet('#севастополь sevboats')

# import time

# # s = t.search(count=10)


# # lll = t.follow_list(t.search(count=10))

# time.sleep(30)

# # t.unfollow_list(lll)

# # # ss = s['statuses']

# # # for i in ss:
# # #     print i['text'], '\033[92m', i['user']['name'], '\033[91m', i['user']['id_str'], '\033[0m'

# # # t.delete_tweet(r['id_str'])


# # # print t.follow('2635565586')
# # # print t.unfollow('2635565586')



# import settings
# import os
# from src.scrapper import Scrapper

# scrap = Scrapper()
# scrap.timeout = 0
# # scrap.ships_list_url = 'file:///%s' % os.path.join(settings.BASE_DIR, 'sevboats/tests/test_data/list-page:{page}.html')
# # scrap.ship_info_url = 'file:///%s' % os.path.join(settings.BASE_DIR, 'sevboats/tests/test_data/list.html')

# # # print scrap.ships_list_url

# mmsi_s = ['272083800', '272083600', '272093900', '272124300', '272083500', '272083700', '272092200', '272105500', '272126200', '272124400', ]
# scrap.ships_list_url = 'file:///%s' % os.path.join(settings.BASE_DIR, 'sevboats/tests/test_data/list.html')

# # x = scrap.scrape_ships_list(mmsi_s)

# # for key, value in x.iteritems():
# #     print key, value
# # print '--------------------------------------------------'
# x = scrap.scrape_ships_list(mmsi_s)

# # for key, value in x.iteritems():
# #     print key, value


# # x = scrap.scrape_ship('OST', '272093900')
# # print x


# from src.ships import ShipsContainer

# sc = ShipsContainer()

# sc.get_ships()

# sc.update_ships(x)
# sc.print_ships


from src.twitter import Twitter

t = Twitter()

res = t.follow_followers()
import time
time.sleep(90)

t.unfollow_list(res)

print res

