# -*- coding: utf-8 -*-

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

    @staticmethod
    def deadend():
        return SingletonLazy.get(RoutesContainer).deadend


SlL = SingletonLazy


from .ships import ShipsContainer, Ship
from .shiptracks import RoutesContainer
from .scrapper import Scrapper


def loadship():
    """ Load ship info from data/ships.yaml """
    SlL.fleet().get_ships()

def update_ais_data():
    """ Request ais to get ship data and update it """
    mmsis = SlL.fleet().mmsi_list
    data = SlL.ais_scrapper().scrape_ships_list(mmsis)
    SlL.fleet().update_ships(data)

def update_ais_lastpos():
    """ Request ais to get ship lastpos """
    mmsis = SlL.fleet().get_online_mmsis()
    data = SlL.ais_scrapper().scrape_ships_list_lastpos(mmsis)
    SlL.fleet().update_ships_lastpos(data)

def check_ships_on_routes():
    """ Check how many ship on routes are moved in last hours """
    moved_on_routes = 0
    for mmsi, ship in SlL.fleet().container.iteritems():
        # run odometr and get distance
        distance = ship.odometer()
        # creacte checkers
        verification_max = -1
        route_index = None
        for index, route in enumerate(SlL.routes().container):
            verification = route.verification(ship)
            if verification > verification_max:
                verification_max = verification
                route_index = index
        # if ship moving and it on same route
        if (route_index is not None) and (distance > Ship.MOVING_LENGTH):
            moved_on_routes += 1
    return moved_on_routes
