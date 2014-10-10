import urllib2
from bs4 import BeautifulSoup
import re
import time


class Scrapper(object):

    """ Parse data from marinetraffic to get ship info """

    ais_domain_url = r'http://www.marinetraffic.com/en/ais/'
    index_prefix = r'%sindex/ships/range/' % ais_domain_url
    details_prefix = r'%sdetails/ships/' % ais_domain_url

    ships_list_url = r'%sport_id:883/ship_type:6/flag:UA/per_page:50/page:{page}' % index_prefix
    ship_info_url = r'%sshipname:{NAME}/mmsi:{MMSI}' % index_prefix
    ship_details_url = r'%s{MMSI}/vessel:{NAME}' % details_prefix

    # timeout with page request in seconds
    timeout = 10

    def __init__(self):
        # create urllib2 opener, with costom user agent
        self.opener = urllib2.build_opener()
        # ~WARNING~ Need add normal user agents
        self.opener.addheaders = [('User-Agent', '')]

    def scrape_ship(self, ship_name, ship_mmsi):
        """
        Scrape one ship data from AIS.
        return (speed, course, (latitude, longitude), delay) if error occured return None
        """
        url = self.ship_info_url.format(NAME=ship_name, MMSI=ship_mmsi).replace(' ', '+')

        try:
            soup = BeautifulSoup(self.opener.open(url).read())
            data_row = soup.find('span', text=ship_mmsi).find_parent('tr').find_all('td')
        except (AttributeError, urllib2.URLError):
            data_row = None

        if data_row is not None:
            return self._get_data(data_row)

    def scrape_ships_list(self, ships_mmsi):
        """
        Scrape ships from array ships_mmsi.
        return hash { mmsi : (speed, course, (latitude, longitude), delay ), ...}
        if error occured while procssing http connection or html parsing return empty hash.
        if error occured while processing ship, than ship is not included in the result.
        """

        data = []
        result = {}

        try:
            # get first page url
            url = self.ships_list_url.format(page=1)
            soup = BeautifulSoup(self.opener.open(url).read())
            # get page all count
            page_all = soup.find('div', {'class': 'col-xs-6 page-nav'}).encode('utf-8')
            pattern = re.compile(r'</form>.+of.+(\d+)<span')
            search = pattern.search(page_all)
            count = int(search.group(1)) if search else 1
            # get raw_data of first page
            raw_data = soup.find_all('td', {'data-column': '20'})
            # get raw_data from other pages
            for i in range(2, count + 1):
                time.sleep(self.timeout)
                url = self.ships_list_url.format(page=i)
                soup = BeautifulSoup(self.opener.open(url).read())
                raw_data += soup.find_all('td', {'data-column': '20'})
            # filter raw data - only neaded ships
            for row in raw_data:
                if row.text in ships_mmsi:
                    data.append((row.text.encode('utf-8'), row.find_parent('tr').find_all('td')))
        except (AttributeError, urllib2.URLError):
            data = None

        if data is not None:
            for row in data:
                coord_info = self._get_data(row[1])
                if coord_info is not None:
                    result[row[0]] = coord_info
        return result

    def _get_data(self, row):
        """
        Get data from raw data row. row is <tr> element from website wraped with bs4.
        return ( speed, course, (latitude, longitude), delay ) if error occured return none
        """
        # define magic numbers - is data row index
        VESSEL_NAME = 3  # get course as rotate icon
        SPEED = 7        # get speed
        RECEIVED = 9     # get time delay and coord pos

        try:
            # get speed info
            raw_speed = row[SPEED].find('span').encode('utf-8')
            pattern = re.compile(r'\d+\.?\d*')
            speed = float(pattern.search(raw_speed).group(0))
            # get course info
            raw_course = row[VESSEL_NAME].find('div').encode('utf-8')
            pattern = re.compile(r'rotate\((\d+)deg\)')
            course = float(pattern.search(raw_course).group(1))
            # get coordinat info
            raw_position = row[RECEIVED].find('a')['href'].encode('utf-8')
            pattern = re.compile(r'centerx:(-?\d+\.?\d*)/centery:(-?\d+\.?\d*)')
            m = pattern.search(raw_position)
            longitude = float(m.group(1))
            latitude = float(m.group(2))
            # get time delay info
            raw_delay = row[RECEIVED].find('span')['title'].encode('utf-8')
            pattern = re.compile(r'(\d+)s')
            delay = int(pattern.search(raw_delay).group(1))
            # return result
            return (speed, course, (latitude, longitude), delay)
        except (AttributeError):
            return None
