# -*- coding: utf-8 -*-

from coordinates import Polygon


class Pier(object):

    """ Pier class """

    def __init__(self, name, area, mark):
        """
        Create new instance of piers
        :name - `string` name of pier
        :area - `polygon` of territory covered
        :mark - `coordinates` point use as orientir
        """
        self.name = name
        self.area = area
        self.mark = mark

    def __str__(self):
        return 'pier: {name}; orientir mark: {mark}'.format(name=self.name, mark=self.mark)


class Route(object):

    """ Route class """

    def __init__(self, name, bay=None, piers=None):
        """
        Create new instance of piers
        :name - `string` name of pier
        :bay - `polygon` of territory covered
        :piers - `list` piers on this route
        """
        self.name = name
        self.bay = bay
        self.piers = piers

    def __str__(self):
        return 'route: {name};'.format(name=self.name)

    def verification(self, ship):
        """ Checks Is the ship on the route """
        if not self.bay.is_inside(ship.coordinates):
            return None
        else:
            count = 1

        if (ship.speed < MN.STOP):
            for pier in self.piers:
                if pier.area.is_inside(ship.coordinates):
                    return MN.TRUEPOS

        for point in ship.lastpos:
            count += self.bay.is_inside(point)

        return count
