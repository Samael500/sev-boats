# -*- coding: utf-8 -*-
# import settings
# import pyowm
from src.weather import Weather
# from src.twitter import Twitter

weth = Weather()
# t = Twitter()

# t.post_image_weather()

# # print dir(weth.owm)

# # print dir(tomorrow)


# day = '{date} %d:00:00+00'.format(date=pyowm.timeutils.tomorrow().date())



# # wf = weth.forecast()

# # for w in wf:
# #     print w
# #     print w.get_wind()




out, date_title = weth.draw_img()

# out.save('out.jpg', format='JPEG', quality=95, subsampling=0, optimize=True, progressive=True)
out.save('out.png', format='PNG')


# from src.engine import send_fleet_message

# print send_fleet_message()
