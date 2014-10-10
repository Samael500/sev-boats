# -*- coding: utf-8 -*-

from settings import DATA_DIR
import os
import yaml
import random


class Ship(object):

    """ Ship class """

    # Vessel kind constants
    KIND_BOAT = 'boat'
    KIND_FERRY = 'ferry'
    # Vessel status constants
    STATUS_ONLINE = 'online'
    STATUS_OFFLINE = 'offline'
    STATUS_INDEADEND = 'indeadend'
    STATUS_DEAD_PING = 'dead_ping'
    _STATUS_DEFAULT = STATUS_OFFLINE
    # Timelimit for dead ping in seconds
    DEAD_PING_TIMELIMIT = 35 * 60

    def __init__(self, mmsi, name, ru_name, kind, speed=None, course=None, coordinates=None, delay=None):
        """
        Create new instance with given param
        :mmsi - Maritime Mobile Service Identity
        :name - Latin vessel name
        :ru_name - Cyrillic vessel name
        :kind - Vessel kind (boat or ferry)
        ---
        :speed - Vessel speed in khot's
        :course - Vessel course in deg
        :coordinates - Vessel position (latitude, longitude)
        :delay - Last update time
        """
        # static info
        self.mmsi = mmsi
        self.name = name
        self.ru_name = ru_name
        self.kind = kind
        # dynamic info
        self.speed = speed
        self.course = course
        self.coordinates = coordinates
        self.delay = delay
        # status info
        self.status = Ship._STATUS_DEFAULT

    @property
    def is_online(self):
        return self.status == Ship.STATUS_ONLINE

    @property
    def is_offline(self):
        return self.status == Ship.STATUS_OFFLINE

    @property
    def is_indeadend(self):
        return self.status == Ship.STATUS_INDEADEND

    @property
    def is_dead_ping(self):
        return self.status == Ship.STATUS_DEAD_PING

    @property
    def is_boat(self):
        return self.kind == Ship.KIND_BOAT

    @property
    def is_ferry(self):
        return self.kind == Ship.KIND_FERRY

    def __unicode__(self):
        return u'{ru_name}: {mmsi}'.format(ru_name=self.ru_name, mmsi=self.mmsi)

    def __str__(self):
        return '{name}: status: {status}'.format(name=self.name, status=self.status)

    @property
    def _reset(self):
        """ Set all dynamic info as None """
        self.coordinates = None
        self.speed = None
        self.delay = None

    def update(self, data):
        """
        Update ship info from AIS data returned of scrapper
        the data format is (speed, course, (latitude, longitude), delay)
        if no data - set offline and return
        """
        if data is None:
            self._reset
            self.update_status()
            return
        # magic numders
        SPEED = 0
        COURSE = 1
        COORDINATES = 2
        DELAY = 3
        # update data
        self.speed = data[SPEED]
        self.course = data[COURSE]
        self.coordinates = data[COORDINATES]
        self.delay = data[DELAY]
        # update status
        self.update_status()

    def update_status(self):
        """ Change ship status """
        status_old = self.status
        status_new = None
        # check different situation
        if self.coordinates is None:
            status_new = Ship.STATUS_OFFLINE
        elif self.delay > Ship.DEAD_PING_TIMELIMIT:
            status_new = Ship.STATUS_DEAD_PING
        else:
            status_new = Ship.STATUS_ONLINE
        # NEED CHECK DEAD END
        # NEED ADD CHANGE STATUS from A - to B message
        self.status = status_new


class ShipsContainer(object):

    """ The container for save ship """

    filename = 'ships'
    filename_suffix = '.yaml'

    container = {}
    mmsi_list = []

    @property
    def get_ship_data_path(self):
        """ Return file path to self ship file """
        return os.path.join(DATA_DIR, self.filename + self.filename_suffix)

    def get_ships(self):
        """ Create ships array if available file path, else - None """
        try:
            # clear containers
            self.container = {}
            self.mmsi_list = []
            # read file and load yaml
            with open(self.get_ship_data_path, 'r') as ships_file:
                raw_ships = yaml.load(ships_file)
            # create ships and append it to container
            for raw_ship in raw_ships:
                ship = Ship(**raw_ship)
                # the mmsi must be unique
                assert ship.mmsi not in self.mmsi_list
                self.container[ship.name] = ship
                self.mmsi_list.append(ship.mmsi)
            return self.mmsi_list
        except IOError:
            return None

    def update_ships(self, ais_data_list):
        """
        Update ships in container, set new data from ais
        data format is { mmsi : (speed, course, (latitude, longitude), delay ), ...}
        if not ship in ais data - set None to it
        """
        # for all ship in container
        for name, ship in self.container.iteritems():
            ship.update(ais_data_list.get(ship.mmsi))

    @property
    def print_ships(self):
        for name, ship in self.container.iteritems():
            print ship
