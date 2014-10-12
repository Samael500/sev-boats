# -*- coding: utf-8 -*-

from math import pi, sin, cos, acos, sqrt


class Coordinates:

    """ Coordinates class. With math operators """

    def __init__(self, latitude, longitude):
        """
        Init coordinates instance
        :fst param latitude - integer or float
        :scd param longitude - integer or float
        """
        self.latitude = latitude
        self.longitude = longitude

    def det(a, b, c):
        """ Calculate determinant for given points """
        return a.latitude * (b.longitude - c.longitude) + b.latitude * (c.longitude - a.longitude) + \
            c.latitude * (a.longitude - b.longitude)

    def square(a, b, c):
        """ Calculate the area of a triangle for given points - matrix solution calc det with div 2 """
        return abs(Coordinates.det(a, b, c)) / 2.

    def __sub__(self, point):
        """ Return self A - coord B """
        return Coordinates(self.latitude - point.latitude, self.longitude - point.longitude)

    def __add__(self, point):
        """ Return self A + coord B """
        return Coordinates(self.latitude + point.latitude, self.longitude + point.longitude)

    def __mul__(self, point):
        """ Return self A * coord B """
        return self.latitude * point.latitude + self.longitude * point.longitude

    def __lt__(self, point):
        """ Return self A < coord B. Left Down - is less than Right Up """
        return (self.latitude < point.latitude) or \
            ((self.latitude == point.latitude) and (self.longitude < point.longitude))

    def __eq__(self, point):
        """ Return self A == coord B """
        return (self.latitude == point.latitude) and (self.longitude == point.longitude)

    def __ne__(self, point):
        """ Return self A != coord B """
        return not (self == point)

    def __neg__(self):
        """ Return -self coord """
        return Coordinates(- self.latitude, - self.longitude)

    @property
    def length(self):
        """ Get vector length - by self coordinates """
        return sqrt(self.latitude * self.latitude + self.longitude * self.longitude)

    def __str__(self):
        return "latitude: {0}, longitude: {1}".format(self.latitude, self.longitude)

    def scalar(start, dest, course):
        # phi = cours to radian Decart angle
        phi = (450 - course) % 360  # grad
        phi = pi * phi / 180        # rad
        # create vectors
        A = Coordinates(sin(phi), cos(phi))
        B = dest - start
        # calculate scalar
        return A * B / (A.length * B.length)

    def angle(self, course, dest):
        """
        Calculates the angle between the vectors
        from the point "self" to the point "dest"
        and from the point of "self" with angle "course"
        """
        scalar = Coordinates.scalar(self, dest, course)
        return acos(scalar) / pi * 180

    def collinear(self, course, start):
        """ Return bool is a vectors are collinear """
        scalar = Coordinates.scalar(start, self, course)
        return scalar > 0

    @property
    def lat(self):
        return self.latitude

    @property
    def long(self):
        return self.longitude
