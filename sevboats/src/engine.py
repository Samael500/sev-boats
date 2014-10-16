# -*- coding: utf-8 -*-

from .ships import ShipsContainer, Ship
from .shiptracks import RoutesContainer
from .scrapper import Scrapper


class SingletonLazy(object):

    @staticmethod
    def get(cls, *args, **kwargs):
        if not hasattr(SingletonLazy, cls.__name__):
            setattr(SingletonLazy, cls.__name__, cls(*args, **kwargs))
        return getattr(SingletonLazy, cls.__name__)

    @staticmethod
    def fleet():
        return SingletonLazy.get(ShipsContainer)

    @staticmethod
    def ais_scrapper():
        return SingletonLazy.get(Scrapper)

    @staticmethod
    def routes():
        return SingletonLazy.get(RoutesContainer)


SL = SingletonLazy


def loadship():
    """ Load ship info from data/ships.yaml """
    SlL.fleet.get_ships()

def update_ais_data():
    """ Request ais to get ship data and update it """
    mmsis = SlL.fleet.mmsi_list
    data = SlL.ais_scrapper.scrape_ships_list(mmsis)
    SlL.fleet.update_ships(data)
