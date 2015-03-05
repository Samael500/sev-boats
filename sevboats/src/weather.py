# -*- coding: utf-8 -*-

from settings import OWM_APIKEY
import pyowm


class Weather(object):

    """ Class for twitter use """

    city_id = 694423
    temperature_format = u'celsius'

    hours = [3, 9, 15, 21]
    months = [
        u'января', u'февраля', u'марта', u'апреля', u'мая', u'июня',
        u'июля', u'августа', u'сентября', u'октября', u'ноября', u'декабря']
    day_times = [u'ночь', u'утро', u'день', u'вечер']

    def __init__(self, apikey=OWM_APIKEY):
        self.owm = pyowm.OWM(apikey, language='ru')

    def forecast(self, tommorow=None):
        """ Get tommorow 3h forecast for given times """
        day_str = '{date} %s:00:00+00'.format(date=tommorow or pyowm.timeutils.tomorrow().date())
        forecast = self.owm.three_hours_forecast_at_id(self.city_id)
        weather = [forecast.get_weather_at(day_str % hour) for hour in self.hours]
        return weather

    def get_data(self, forecast):
        """ Get temp and wether status from forecast """
        weather_data = []
        for index, weather in enumerate(forecast):
            weather_data.append(dict(
                day_time=self.day_times[index],
                temp=weather.get_temperature(self.temperature_format)['temp'],
                icon=weather.get_weather_icon_name(),
                wind=weather.get_wind(), ))
        return weather_data

    def get_text(self):
        """ Return weather in text human readeble """
        tomorrow = pyowm.timeutils.tomorrow().date()
        date_title = u'{day} {month}'.format(day=tomorrow.day, month=self.months[tomorrow.month - 1])
        weather_data = self.get_data(self.forecast(tomorrow))
        return date_title, weather_data
