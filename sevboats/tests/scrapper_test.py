# -*- coding: utf-8 -*-

import unittest
import os

from sevboats.src.scrapper import Scrapper
from sevboats.settings import BASE_DIR


class TestAISScrapper(unittest.TestCase):

    """ Test ais scrapper class """

    def setUp(self):
        self.scrapper = Scrapper()
        # change timelimit and scrapp urls
        self.scrapper.timeout = 0
        file_url = r'file:///'
        self.scrapper.ships_list_url = file_url + os.path.join(
            BASE_DIR, 'sevboats', 'tests', 'test_data', 'list-page:{page}.html')
        self.scrapper.ship_info_url = file_url + os.path.join(BASE_DIR, 'sevboats', 'tests', 'test_data', 'list.html')
        self.scrapper.ship_lastpos_url = file_url + os.path.join(
            BASE_DIR, 'sevboats', 'tests', 'test_data', 'lastpos.html')
        self.scrapper.none_url = file_url + os.path.join(
            BASE_DIR, 'sevboats', 'tests', 'test_data', '{types}_none.html')
        self.mmsi_list = (
            '272083500', '272083600', '272083700', '272083800', '272092200', '272093800', '272093900',
            '272094100', '272094200', '272094300', '272094700', '272100500', '272105400', '272105500',
            '272124300', '272124400', '272126200', '273340450', )

    def test_scrapper_constants(self):
        """ Chec correct constants in scrapper """
        self.assertEquals(Scrapper.ais_domain_url, r'http://www.marinetraffic.com/en/ais/')
        self.assertEquals(Scrapper.index_prefix, r'http://www.marinetraffic.com/en/ais/index/ships/range/')
        self.assertEquals(Scrapper.details_prefix, r'http://www.marinetraffic.com/en/ais/details/ships/')
        self.assertEquals(Scrapper.lastpos_prefix, r'http://www.marinetraffic.com/en/ais/index/positions/all/')
        self.assertEquals(
            Scrapper.ships_list_url,
            r'http://www.marinetraffic.com/en/ais/index/ships/range/port_id:883/ship_type:6/per_page:50/page:{page}')
        self.assertEquals(
            Scrapper.ship_info_url,
            r'http://www.marinetraffic.com/en/ais/index/ships/range/shipname:{NAME}/mmsi:{MMSI}')
        self.assertEquals(
            Scrapper.ship_details_url, r'http://www.marinetraffic.com/en/ais/details/ships/{MMSI}/vessel:{NAME}')
        self.assertEquals(
            Scrapper.ship_lastpos_url,
            r'http://www.marinetraffic.com/en/ais/index/positions/all/mmsi:{MMSI}/per_page:50/page:1')
        # timeout with page request in seconds
        self.assertEquals(Scrapper.timeout, 30)

    def test_scrape_ships_list(self):
        """ Get all ship ais data use one page """
        data_many_page = self.scrapper.scrape_ships_list(self.mmsi_list)
        self.scrapper.ships_list_url = self.scrapper.ship_info_url
        data_one_page = self.scrapper.scrape_ships_list(self.mmsi_list)
        self.assertEquals(len(data_many_page), len(data_one_page))
        for mmsi in self.mmsi_list:
            d1 = data_many_page.get(mmsi, [])
            d2 = data_one_page.get(mmsi, [])
            self.assertEquals(d1, d2)

    def test_scrape_ship(self):
        """ Get one ship ais data """
        data = self.scrapper.scrape_ship('ADMIRAL LAZAREV', '272124400')
        self.scrapper.ships_list_url = self.scrapper.ship_info_url
        data_one_page = self.scrapper.scrape_ships_list(self.mmsi_list)
        self.assertEquals(data, data_one_page['272124400'])

    def test_scrape_ship_none(self):
        """ Get one ship ais data """
        data = self.scrapper.scrape_ship('ADMIRAL LAZAREV', '777777777')
        self.assertTrue(data is None)
        self.scrapper.ship_info_url = 'file:///path/to/None'
        data = self.scrapper.scrape_ship('ZUYD', '272083800')
        self.assertTrue(data is None)
        self.scrapper.ship_info_url = self.scrapper.none_url.format(types='info')
        data = self.scrapper.scrape_ship('ZUYD', '272083800')
        self.assertTrue(data is None)

    def test_scrape_ship_list_none(self):
        """ Get one ship ais data """
        data = self.scrapper.scrape_ships_list(('777777777'))
        self.assertTrue(data.get('777777777') is None)
        self.scrapper.ships_list_url = 'file:///path/to/None'
        data = self.scrapper.scrape_ships_list(self.mmsi_list)
        self.assertEquals(data, {})

    def test_scrape_ship_lastpos(self):
        """ Get ship lastpos """
        lastpos_1 = self.scrapper.scrape_lastpos('272083800')
        lastpos_2 = self.scrapper.scrape_ships_list_lastpos(('272083800', ))['272083800']
        self.assertEquals(lastpos_1, lastpos_2)
        self.assertEquals(len(lastpos_1), 50)

    def test_scrape_ship_lastpos_none(self):
        """ Get ship lastpos None """
        self.scrapper.ship_lastpos_url = 'file:///path/to/None'
        lastpos = self.scrapper.scrape_lastpos('272083800')
        self.assertTrue(lastpos is None)
        self.scrapper.ship_lastpos_url = self.scrapper.none_url.format(types='lastpos')
        lastpos = self.scrapper.scrape_lastpos('272083800')
        self.assertEquals(lastpos, [None, ])
