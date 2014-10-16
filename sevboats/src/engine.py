# -*- coding: utf-8 -*-

from sevboats.src.ships import ShipsContainer, Ship
from sevboats.src.scrapper import Scrapper
from sevboats.src.kmlparser import KmlParser


class StandaloneLazy(object):

    _fleet = None
    _ais_scrapper = None

    # ... ... ...

    @property
    @staticmethod
    def fleet():
        if StandaloneLazy._fleet is None:
            StandaloneLazy._fleet = ShipsContainer()
        return StandaloneLazy._fleet

    @property
    @staticmethod
    def ais_scrapper():
        if StandaloneLazy._ais_scrapper is None:
            StandaloneLazy._ais_scrapper = Scrapper()
        return StandaloneLazy._ais_scrapper

SlL = StandaloneLazy


def loadship():
    """ Load ship info from data/ships.yaml """
    SlL.fleet.get_ships()

def update_ais_data():
    """ Request ais to get ship data and update it """
    mmsis = SlL.fleet.mmsi_list
    data = SlL.ais_scrapper.scrape_ships_list(mmsis)
    SlL.fleet.update_ships(data)
