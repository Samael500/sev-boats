import pyowm
from src.weather import Weather

weth = Weather()

# print dir(weth.owm)

# print dir(tomorrow)


day = '{date} %d:00:00+00'.format(date=pyowm.timeutils.tomorrow().date())



# wf = weth.forecast()

# for w in wf:
#     print w
#     print w.get_wind()


weth.get_text()

#get_weather_at(tomorrow).to_XML()
