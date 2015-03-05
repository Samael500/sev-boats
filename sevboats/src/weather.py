# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageFont
from settings import OWM_APIKEY, DATA_DIR

import pyowm
import os
import time

weather_dict = {
    '01d': 'wi-day-sunny',          '01n': 'wi-night-clear',                # clear sky
    '02d': 'wi-day-cloudy',         '02n': 'wi-night-alt-cloudy',           # few clouds
    '03d': 'wi-cloud',              '03n': 'wi-cloud',                      # scattered clouds
    '04d': 'wi-cloudy',             '04n': 'wi-cloudy',                     # broken clouds

    '09d': 'wi-showers',            '09n': 'wi-showers',                    # shower rain
    '10d': 'wi-day-rain',           '10n': 'wi-night-alt-rain',             # rain
    '11d': 'wi-day-thunderstorm',   '11n': 'wi-night-alt-thunderstorm',     # thunderstorm

    '13d': 'wi-day-snow',           '13n': 'wi-night-alt-snow',             # snow

    '50d': 'wi-day-fog',            '50n': 'wi-night-fog',                  # mist
}


weather_codes = {
    'wi-cloud':                     u'\uf041',
    'wi-cloudy':                    u'\uf013',
    'wi-day-cloudy':                u'\uf002',
    'wi-day-fog':                   u'\uf003',
    'wi-day-rain':                  u'\uf008',
    'wi-day-snow':                  u'\uf00a',
    'wi-day-sunny':                 u'\uf00d',
    'wi-day-thunderstorm':          u'\uf010',
    'wi-night-alt-cloudy':          u'\uf086',
    'wi-night-alt-rain':            u'\uf028',
    'wi-night-alt-snow':            u'\uf02a',
    'wi-night-alt-thunderstorm':    u'\uf02d',
    'wi-night-clear':               u'\uf02e',
    'wi-night-fog':                 u'\uf04a',
    'wi-showers':                   u'\uf01a',
}


def get_wether_icon(value):
    """ Return wether character """
    return weather_codes[weather_dict[value]]


class Weather(object):

    """ Class for twitter use """

    city_id = 694423
    temperature_format = u'celsius'

    hours = [0, 6, 12, 18]  # in UTC
    months = [
        u'января', u'февраля', u'марта', u'апреля', u'мая', u'июня',
        u'июля', u'августа', u'сентября', u'октября', u'ноября', u'декабря']
    day_times = [u'ночь', u'утро', u'день', u'вечер']

    copyright_row = u'@SevastopolBoats'

    sleep_time = 10

    def __init__(self, apikey=OWM_APIKEY):
        self.owm = pyowm.OWM(apikey)

    def forecast(self, tommorow=None):
        """ Get tommorow 3h forecast for given times """
        day_str = '{date} %s:00:00+00'.format(date=tommorow or pyowm.timeutils.tomorrow().date())
        # get forecast
        forecast = self.owm.three_hours_forecast_at_id(self.city_id)
        weather = [forecast.get_weather_at(day_str % hour) for hour in self.hours]
        return weather

    def get_data(self, forecast):
        """ Get temp and weather status from forecast """
        weather_data = []
        for index, weather in enumerate(forecast):
            weather_data.append(dict(
                day_time=self.day_times[index],
                temp=weather.get_temperature(self.temperature_format)['temp'],
                icon=weather.get_weather_icon_name(),
                # wind=weather.get_wind(),
        ))
        return weather_data

    def safe_forecast(self, tomorrow=None):
        attemps = 10
        while attemps:
            try:
                forecast = self.forecast(tomorrow)
                return forecast
            except Exception as e:
                print e
                attemps -= 1
                time.sleep(self.sleep_time)
                forecast = None
        assert forecast
        return forecast

    def get_text(self):
        """ Return weather in text human readeble """
        tomorrow = pyowm.timeutils.tomorrow().date()
        date_title = u'{day} {month}'.format(day=tomorrow.day, month=self.months[tomorrow.month - 1])
        weather_data = self.get_data(self.safe_forecast(tomorrow))
        return date_title, weather_data

    def get_font_path(self, font_name):
        """ Return file path to font file """
        return os.path.join(DATA_DIR, 'fonts', font_name)

    def draw_img_weather(self):
        """ Create image of weather """
        date_title, weather_data = self.get_text()
        # make a blank image for the text, initialized to transparent text color
        text_layer = Image.new('RGBA', (1600, 1000), (255, 255, 255, 0))
        # scalable coeff
        coef = 2
        # open fonts
        font = ImageFont.truetype(self.get_font_path('Roboto-Regular.ttf'), 70 * coef)
        weather_font = ImageFont.truetype(self.get_font_path('weathericons-regular-webfont.ttf'), 70 * coef)
        little_font = ImageFont.truetype(self.get_font_path('Roboto-Regular.ttf'), 30 * coef)
        # create a drawing
        drawing = ImageDraw.Draw(text_layer)
        # calculate sizes
        WIDTH, HEIGHT = text_layer.size
        LEFT, RIGHT = 235, WIDTH - 235
        LINE_HEIGHT, BLANK_LINE, SPACE = 85 * coef, 15 * coef, 35 * coef
        # define lambdas
        color = lambda alpha: (0, 191, 255, alpha)
        row = lambda number: LINE_HEIGHT * number + BLANK_LINE
        # title row
        width, height = drawing.textsize(date_title.upper(), font=font)
        drawing.text((WIDTH // 2 - width // 2, row(0)), date_title.upper(), font=font, fill=color(255))
        drawing.line(((LEFT, row(1)), (RIGHT, row(1))), width=11, fill=color(128))
        # calculate columns sizes
        col1 = col2 = col3 = 0
        for wether in weather_data:
            col1 = max(col1, drawing.textsize(wether['day_time'], font=font)[0])
            col2 = max(col2, drawing.textsize('{0:.0f}'.format(wether['temp']), font=font)[0])
            col3 = max(col3, drawing.textsize(get_wether_icon(wether['icon']), font=weather_font)[0])
        # draw wether row's
        for index, wether in enumerate(weather_data, start=1):
            drawing.text((LEFT + SPACE, row(index)), wether['day_time'], font=font, fill=color(255))
            drawing.text(
                ((LEFT + col1 + RIGHT - col3) // 2 - col2 // 2, row(index)),
                '{0:.0f}'.format(wether['temp']), font=font, fill=color(255))
            drawing.text(
                (RIGHT - SPACE - col3, row(index)),
                get_wether_icon(wether['icon']), font=weather_font, fill=color(255))
        # draw copyright row
        width, height = drawing.textsize(self.copyright_row, font=little_font)
        drawing.text(
            (WIDTH - width - SPACE, HEIGHT - height - BLANK_LINE),
            self.copyright_row, font=little_font, fill=color(128))
        return text_layer, date_title

    def draw_img(self):
        """ Merge background and text layer and save """
        # get an image
        # background = Image.open('800x500.png').convert('RGBA')
        background = Image.new('RGBA', (800, 500), (200, 200, 200, 255))
        # draw text layer
        text_layer, date_title = self.draw_img_weather()
        text_layer.thumbnail(background.size, Image.BICUBIC)
        result = Image.alpha_composite(background, text_layer)
        return result, date_title
        # result.save('out.png', format='PNG')
