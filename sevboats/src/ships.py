# -*- coding: utf-8 -*-

from settings import DATA_DIR, PERIOD, UTC_OFFSET
from datetime import datetime, timedelta
from colorama import Fore

import os
import yaml

from .coordinates import Coordinates
from .engine import SingletonLazy
deadzone = SingletonLazy.deadend


class Ship(object):

    """ Ship class """

    # Vessel kind constants
    KIND_BOAT = 'BOAT'
    KIND_FERRY = 'FERRY'
    # Vessel status constants
    STATUS_ONLINE = 'ONLINE'
    STATUS_OFFLINE = 'OFFLINE'
    STATUS_INDEADEND = 'INDEADEND'
    STATUS_DEAD_PING = 'DEAD_PING'
    _STATUS_DEFAULT = STATUS_OFFLINE
    # Constants used ship
    DEAD_PING_TIMELIMIT = 35 * 60   # Timelimit for dead ping in seconds - 35 minutes
    STOP_SPEED = 0.55               # minimal cignificant speed khot
    VIEWANGLE = 80                  # angle at which it is considered that the boat went to target
    DELTA = 0.0025                  # distance to determinate next pier ~ 25 m
    DEADEND_DISTANCE = 0.0090       # distancedistance to deadend place ~ 900 m
    MOVING_LENGTH = 0.005 * PERIOD  # minimal cignificant length of ship track on last hour ~ 500 m / per hours
    CRITICAL_MINIMUM = 1            # is minimal online ship on routes for it be OK
    MAX_LASTPOS_LEN = 50            # max length of lastpos - use for true ship on routes

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
        self.lastpos = []
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
        return u'{ru_name}: {mmsi} - {status}'.format(ru_name=self.ru_name, mmsi=self.mmsi, status=self.status)

    def __str__(self):
        return '{name}: {status}'.format(name=self.name, status=self.status)

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
            self._reset()
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
        self.coordinates = Coordinates(*data[COORDINATES])
        self.delay = data[DELAY]
        # update status
        self.update_status()

    def update_status(self):
        """ Change ship status """
        status_old = self.status  # noqa
        status_new = None
        # check different situation
        if self.coordinates is None:
            status_new = Ship.STATUS_OFFLINE
        elif self.delay > Ship.DEAD_PING_TIMELIMIT:
            status_new = Ship.STATUS_DEAD_PING
        elif self.check_deadend():
            status_new = Ship.STATUS_INDEADEND
        else:
            status_new = Ship.STATUS_ONLINE
        self.status = status_new

    def distance(self, point):
        """ Get distance between two points (self.coordinates, point-destination) """
        return (point - self.coordinates).length

    def angle(self, point):
        """ Easy use for Coordinates.angle() """
        return self.coordinates.angle(self.course, point)

    def viewangle(self, point):
        return self.angle(point) < Ship.VIEWANGLE

    def check_deadend(self):
        """ Check are ship in dead end """
        if (deadzone().is_inside(self)):
            return ((self.speed < Ship.STOP_SPEED) or
                    (self.distance(deadzone().mark) < Ship.DEADEND_DISTANCE) or
                    (self.viewangle(deadzone().mark)))
        return False

    def _slice_lastpos(self):
        """Slice lastpos with timelimit"""
        # if already sliced lastpos - return
        if not len(self.lastpos) or isinstance(self.lastpos[0], Coordinates):
            return
        # get time now - and convert to utc - period
        starttime = datetime.now() - timedelta(hours=PERIOD + UTC_OFFSET)
        # define magic numbers
        TIMESTAMP = 0
        COORDINATES = 1
        for i in xrange(len(self.lastpos)):
            if self.lastpos[i][TIMESTAMP] < starttime:
                # remove point with timelimit
                self.lastpos = self.lastpos[:i]
                break
            # create coordinate - remove timesta
            self.lastpos[i] = Coordinates(*self.lastpos[i][COORDINATES])

    def odometer(self):
        """ Calculate the length of the path traveled in the last PERIOD """
        if not self.lastpos:
            return 0.
        self._slice_lastpos()
        # calculate distance
        distance = 0.
        for i in xrange(1, len(self.lastpos)):
            distance += (self.lastpos[i] - self.lastpos[i - 1]).length
        return distance


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
                self.container[ship.mmsi] = ship
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
        for mmsi, ship in self.container.iteritems():
            ship.update(ais_data_list.get(mmsi))

    def update_ships_lastpos(self, ais_data_latpos):
        """
        Update ships in container, set lastpos
        data format is { mmsi : [timelimit, (latitude, longitude)], ...}
        if not ship in ais data - remove attribute lastpos
        """
        # for all ship in container
        for mmsi, ship in self.container.iteritems():
            ship.lastpos = ais_data_latpos.get(mmsi, [])

    def print_ships(self, color=None):
        colors = {
            Ship.STATUS_ONLINE: Fore.GREEN, Ship.STATUS_OFFLINE: Fore.YELLOW,
            Ship.STATUS_INDEADEND: Fore.BLUE, Ship.STATUS_DEAD_PING: Fore.RED,
            'endline': Fore.RESET, }

        for mmsi, ship in self.container.iteritems():
            if color:
                print colors[ship.status], unicode(ship), ship.odometer(), colors['endline']
            else:
                print ship

    def get_online_mmsis(self):
        """ Return mmsis of ship with status online """
        mmsis = []
        for mmsi, ship in self.container.iteritems():
            if ship.is_online:
                mmsis.append(mmsi)
        return mmsis
