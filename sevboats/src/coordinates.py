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
        """ Calculate the Polygon of a triangle for given points - matrix solution calc det with div 2 """
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


class Polygon:

    """ Polygon class """

    # polygon positions
    POLYGON_INSIDE = 'INSIDE'          # Внутри
    POLYGON_OUTSIDE = 'OUTSIDE'        # Снаружи
    POLYGON_BOUNDARY = 'BOUNDARY'      # На границе

    # edge positions
    EDGE_TOUCHING = 'TOUCHING'         # Касается
    EDGE_CROSSING = 'CROSSING'         # Пересекает
    EDGE_INESSENTIAL = 'INESSENTIAL'   # Не имеет значения

    # point positions
    POINT_LEFT = 'LEFT'                # Слева
    POINT_RIGHT = 'RIGHT'              # Справа
    POINT_BEYOND = 'BEYOND'            # Впереди
    POINT_BEHIND = 'BEHIND'            # Сзади
    POINT_BETWEEN = 'BETWEEN'          # Между
    POINT_ORIGIN = 'ORIGIN'            # В начале
    POINT_DESTINATION = 'DESTINATION'  # В конце

    def __init__(self, points):
        self.points = points
        self.length = len(points)
        self.start_point()

    @property
    def start_point(self):
        """ Regroups the point of the polygon for the clockwise bottom left """
        zero_id = 0   # start poin pointer
        for i in xrange(self.length):
            if (self.points[i] < self.points[zero_id]):
                zero_id = i
        # regroup polygon points
        self.points = self.points[zero_id:] + self.points[:zero_id]

    def is_inside(self, point):
        """ If point in polygon return True """
        return Polygon.POLYGON_INSIDE == self._point_in_polygon(point)

    def _point_in_polygon(self, point):
        """ Check the point of the polygon relation """
        is_in = False
        for i in xrange(self.length):
            if (i == self.length - 1):
                # get closed edge from last - to first point
                edge = self.points[i], self.points[0]
            else:
                # get normal edge from current - to next
                edge = self.points[i], self.points[i+1]
            # classify edge typy for point
            edge_type = self._edge_type(point, edge)
            if (edge_type == Polygon.EDGE_TOUCHING):
                return Polygon.POLYGON_BOUNDARY
            elif (edge_type == Polygon.EDGE_CROSSING):
                is_in = not is_in
        return (Polygon.POLYGON_OUTSIDE, Polygon.POLYGON_INSIDE)[is_in]

    def _edge_type(self, point, edge):
        """ Determines how towards the point is an edge """
        start, end = edge
        pos = Polygon._classify(point, start, end)
        if (pos == Polygon.POINT_LEFT):
            return (Polygon.EDGE_INESSENTIAL, Polygon.EDGE_CROSSING)[
                (start.longitude < point.longitude) and (point.longitude <= end.longitude)]
        if (pos == Polygon.POINT_RIGHT):
            return (Polygon.EDGE_INESSENTIAL, Polygon.EDGE_CROSSING)[
                (end.longitude < point.longitude) and (point.longitude <= start.longitude)]
        if (pos == Polygon.POINT_BETWEEN) or (pos == Polygon.POINT_ORIGIN) or (pos == Polygon.POINT_DESTINATION):
            return Polygon.EDGE_TOUCHING
        # total elif - edge is inessential
        return Polygon.EDGE_INESSENTIAL

    def _classify(point, start, end):
        a = end - start
        b = point - start
        sa = a.latitude * b.longitude - b.latitude * a.longitude

        if (sa > 0.0) :
            return Polygon.POINT_LEFT
        elif (sa < 0.0) :
            return Polygon.POINT_RIGHT

        if (a.latitude * b.latitude < 0.0) or (a.longitude * b.longitude < 0.0) :
            return Polygon.POINT_BEHIND
        if (a.length() < b.length()):
            return Polygon.POINT_BEYOND
        if (start == point):
            return Polygon.POINT_ORIGIN
        if (end == point):
            return Polygon.POINT_DESTINATION
        return Polygon.POINT_BETWEEN
