# -*- coding: utf-8 -*-

import unittest

from sevboats.src.ships import Ship
from sevboats.src.engine import SlL


class TestShip(unittest.TestCase):

    """ Test ship class """

    def setUp(self):
        SlL.fleet().get_ships()
        self.ship = SlL.fleet().container.itervalues().next()

    def test_ship_constants(self):
        """ Check constants of Ship class """
        # Vessel kind constants
        self.assertEquals(Ship.KIND_BOAT, 'BOAT')
        self.assertEquals(Ship.KIND_FERRY, 'FERRY')
        # Vessel status constants
        self.assertEquals(Ship.STATUS_ONLINE, 'ONLINE')
        self.assertEquals(Ship.STATUS_OFFLINE, 'OFFLINE')
        self.assertEquals(Ship.STATUS_INDEADEND, 'INDEADEND')
        self.assertEquals(Ship.STATUS_DEAD_PING, 'DEAD_PING')
        self.assertEquals(Ship._STATUS_DEFAULT, Ship.STATUS_OFFLINE)
        # Constants used ship
        self.assertEquals(Ship.DEAD_PING_TIMELIMIT, 90 * 60)
        self.assertEquals(Ship.STOP_SPEED, 0.55)
        self.assertEquals(Ship.VIEWANGLE, 80)
        self.assertEquals(Ship.DELTA, 0.0025)
        self.assertEquals(Ship.DEADEND_DISTANCE, 0.0090)
        self.assertEquals(Ship.MOVING_LENGTH, 0.005)
        self.assertEquals(Ship.CRITICAL_MINIMUM, 1)
        self.assertEquals(Ship.MAX_LASTPOS_LEN, 50)

    def test_ship_propertyes(self):
        """ Check ship.is_? property """
        # must be false default
        self.assertFalse(self.ship.is_online)
        self.assertFalse(self.ship.is_indeadend)
        self.assertFalse(self.ship.is_dead_ping)
        self.assertFalse(self.ship.is_ferry)
        # must be true
        self.assertTrue(self.ship.is_offline)
        self.assertTrue(self.ship.is_boat)

    def test_ship_str(self):
        """ Check str and unicode """
        self.assertEquals('URAN: OFFLINE', str(self.ship))
        self.assertEquals(u'Уран: 272105400 - OFFLINE', unicode(self.ship))
