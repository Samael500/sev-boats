import urllib2
from bs4 import BeautifulSoup
import re

# from src.coordinates import Coordinates


class Scrapper(object):

    """ Parse data from marinetraffic to get ship info """

    ais_domain_url = r'http://www.marinetraffic.com/en/ais/'
    ships_list_url = r'%sindex/ships/range/port_id:883/ship_type:6/flag:UA/page:{page}' % ais_domain_url
    ship_info_url = r'%sindex/ships/range/shipname:{NAME}/mmsi:{MMSI}' % ais_domain_url
    ship_details_url = r'%sdetails/ships/{MMSI}/vessel:{NAME}' % ais_domain_url

    def __init__(self):
        # create urllib2 opener, with costom user agent
        self.opener = urllib2.build_opener()
        # ~WARNING~ Need add normal user agents
        self.opener.addheaders = [('User-Agent', r'sevboats')]

    def scrape_ship(self, ship_name, ship_mmsi):
        """
        Scrape one ship data from AIS.
        return ( speed, course, (latitude, longitude), delay ) if error occured return None
        """
        url = self.ship_info_url.format(NAME=ship_name, MMSI=ship_mmsi).replace(' ', '+')

        try:
            soup = BeautifulSoup(self.opener.open(url).read())
            data_row = soup.find('span', text=ship_mmsi).find_parent('tr').find_all('td')
        except (AttributeError, urllib2.URLError):
            data_row = None

        if data_row is not None:
            return self._get_data(data_row)

    # def scrape_all_ships(self, ship_names):
    #     # TODO: Optimize parsing to reduce the number of processed items
    #     '''
    #     Scrape ships from array ship_name.
    #     return hash { name1 : (speed, course, (latitude, longitude) ), ...}
    #     if error occured while procssing http connection or html parsing return empty hash.
    #     if error occured while processing ship, than ship is not included in the result.
    #     '''
    #     url = r"http://www.marinetraffic.com/ais/index/ships/range/port_id:883/ship_type:6/per_page:0"
    #     data = []
    #     res = {}

    #     #for name in ship_names:
    #     #    res[name] = None

    #     try:
    #         soup = BeautifulSoup(urllib2.urlopen(url).read())
    #         raw_data = soup.find_all("a")
    #         for row in raw_data:
    #             if row.text in ship_names:
    #                 data.append( (row.text.encode('utf-8',"ignore"), row.find_parent("tr").find_all("td") ) )
    #     except :#(AttributeError, urllib2.URLError):
    #         data = None
    #     if data != None:
    #         for row in data:
    #             #print row[1][3]
    #             coord = self._get_data(row[1])
    #             if coord != None:
    #                 res[row[0]] = coord
    #     return res

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
            delay = float(pattern.search(raw_delay).group(1))
            # return result
            return (speed, course, (latitude, longitude), delay)
        except (AttributeError):
            return None
