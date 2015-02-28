# -*- coding: utf-8 -*-

import unittest

from sevboats.src.coordinates import Coordinates, Polygon


class TestPolygon(unittest.TestCase):

    """ Test polygon class """

    def test_polygon_constants(self):
        """ Check correct constants """
        # polygon positions
        self.assertEquals(Polygon.POLYGON_INSIDE, 'INSIDE')
        self.assertEquals(Polygon.POLYGON_OUTSIDE, 'OUTSIDE')
        self.assertEquals(Polygon.POLYGON_BOUNDARY, 'BOUNDARY')
        # edge positions
        self.assertEquals(Polygon.EDGE_TOUCHING, 'TOUCHING')
        self.assertEquals(Polygon.EDGE_CROSSING, 'CROSSING')
        self.assertEquals(Polygon.EDGE_INESSENTIAL, 'INESSENTIAL')
        # point positions
        self.assertEquals(Polygon.POINT_LEFT, 'LEFT')
        self.assertEquals(Polygon.POINT_RIGHT, 'RIGHT')
        self.assertEquals(Polygon.POINT_BEYOND, 'BEYOND')
        self.assertEquals(Polygon.POINT_BEHIND, 'BEHIND')
        self.assertEquals(Polygon.POINT_BETWEEN, 'BETWEEN')
        self.assertEquals(Polygon.POINT_ORIGIN, 'ORIGIN')
        self.assertEquals(Polygon.POINT_DESTINATION, 'DESTINATION')

    def test_polygon_edge_classify(self):
        """ Check point posytion on edge """
        A = Coordinates(3, 3)
        B = Coordinates(9, 13)
        # point in left half-plane
        p = Coordinates(3, 10)
        self.assertEquals(Polygon._classify(p, A, B), Polygon.POINT_LEFT)
        p = Coordinates(6, 8.00000000000001)
        self.assertEquals(Polygon._classify(p, A, B), Polygon.POINT_LEFT)
        # point in right half-plane
        p = Coordinates(10, 3)
        self.assertEquals(Polygon._classify(p, A, B), Polygon.POINT_RIGHT)
        p = Coordinates(6, 7.99999999999999)
        self.assertEquals(Polygon._classify(p, A, B), Polygon.POINT_RIGHT)
        # point on edge behind it
        p = Coordinates(0, -2)
        self.assertEquals(Polygon._classify(p, A, B), Polygon.POINT_BEHIND)
        p = Coordinates(2.94, 2.9)
        self.assertEquals(Polygon._classify(p, A, B), Polygon.POINT_BEHIND)
        # point on edge beyond it
        p = Coordinates(15, 23)
        self.assertEquals(Polygon._classify(p, A, B), Polygon.POINT_BEYOND)
        p = Coordinates(9.006, 13.01)
        self.assertEquals(Polygon._classify(p, A, B), Polygon.POINT_BEYOND)
        # point on edge origin
        p = Coordinates(3, 3)
        self.assertEquals(Polygon._classify(p, A, B), Polygon.POINT_ORIGIN)
        # point on edge destination
        p = Coordinates(9, 13)
        self.assertEquals(Polygon._classify(p, A, B), Polygon.POINT_DESTINATION)
        # point on edge between
        p = Coordinates(6, 8)
        self.assertEquals(Polygon._classify(p, A, B), Polygon.POINT_BETWEEN)
        p = Coordinates(7.8, 11)
        self.assertEquals(Polygon._classify(p, A, B), Polygon.POINT_BETWEEN)
        p = Coordinates(4.5, 5.5)
        self.assertEquals(Polygon._classify(p, A, B), Polygon.POINT_BETWEEN)

    def test_polygon_edge_type(self):
        """ Check edge type for point """
        A = Coordinates(3, 3)
        B = Coordinates(9, 13)
        # point in left half-plane
        p = Coordinates(3, 10)  # crossing
        self.assertEquals(Polygon._classify(p, A, B), Polygon.POINT_LEFT)
        self.assertEquals(Polygon._edge_type(p, (A, B)), Polygon.EDGE_CROSSING)
        p = Coordinates(3, 100)  # inessential
        self.assertEquals(Polygon._classify(p, A, B), Polygon.POINT_LEFT)
        self.assertEquals(Polygon._edge_type(p, (A, B)), Polygon.EDGE_INESSENTIAL)
        # point in right half-plane
        p = Coordinates(3, 10)  # crossing
        self.assertEquals(Polygon._classify(p, B, A), Polygon.POINT_RIGHT)
        self.assertEquals(Polygon._edge_type(p, (B, A)), Polygon.EDGE_CROSSING)
        p = Coordinates(3, 100)  # inessential
        self.assertEquals(Polygon._classify(p, B, A), Polygon.POINT_RIGHT)
        self.assertEquals(Polygon._edge_type(p, (B, A)), Polygon.EDGE_INESSENTIAL)
        # point toch the edge
        p = Coordinates(6, 8)
        self.assertEquals(Polygon._classify(p, A, B), Polygon.POINT_BETWEEN)
        self.assertEquals(Polygon._edge_type(p, (A, B)), Polygon.EDGE_TOUCHING)
        p = Coordinates(3, 3)
        self.assertEquals(Polygon._classify(p, A, B), Polygon.POINT_ORIGIN)
        self.assertEquals(Polygon._edge_type(p, (A, B)), Polygon.EDGE_TOUCHING)
        p = Coordinates(9, 13)
        self.assertEquals(Polygon._classify(p, A, B), Polygon.POINT_DESTINATION)
        self.assertEquals(Polygon._edge_type(p, (A, B)), Polygon.EDGE_TOUCHING)
        # inessential edge
        # point on edge behind it
        p = Coordinates(0, -2)
        self.assertEquals(Polygon._classify(p, A, B), Polygon.POINT_BEHIND)
        self.assertEquals(Polygon._edge_type(p, (A, B)), Polygon.EDGE_INESSENTIAL)
        p = Coordinates(2.94, 2.9)
        self.assertEquals(Polygon._classify(p, A, B), Polygon.POINT_BEHIND)
        self.assertEquals(Polygon._edge_type(p, (A, B)), Polygon.EDGE_INESSENTIAL)
        # point on edge beyond it
        p = Coordinates(15, 23)
        self.assertEquals(Polygon._classify(p, A, B), Polygon.POINT_BEYOND)
        self.assertEquals(Polygon._edge_type(p, (A, B)), Polygon.EDGE_INESSENTIAL)
        p = Coordinates(9.006, 13.01)
        self.assertEquals(Polygon._classify(p, A, B), Polygon.POINT_BEYOND)
        self.assertEquals(Polygon._edge_type(p, (A, B)), Polygon.EDGE_INESSENTIAL)

    def get_polygon(self):
        points = []
        for point in (
                (1.40, 3.58), (5.96, 2.46), (4.64, 1.04), (5.00, -2.0),
                (1.10, -0.7), (2.70, 1.72), (4.00, 2.00), ):
            points.append(Coordinates(*point))
        return points

    def test_polygon_init(self):
        """ check correct create polygon """
        points = self.get_polygon()
        # create polygon
        polygon = Polygon(points)
        # check created instance
        for length in (len(polygon.points), len(points), 7):
            self.assertEquals(polygon.length, length)
        # check start point correct
        for i in xrange(7):
            self.assertEquals(polygon.points[i], points[(i + 4) % 7])

    def test_polygon_point_in(self):
        """ Check point detects """
        points = self.get_polygon()
        polygon = Polygon(points)
        # point on polygon boundary
        for point in points:
            self.assertEquals(polygon._point_in_polygon(point), Polygon.POLYGON_BOUNDARY)
            self.assertFalse(polygon.is_inside(point))
        # point inside
        for point in ((4.1, 0.1), (4, 1), (4.5, 2.3), (2, 3.3), (5.5, 2.1)):
            p = Coordinates(*point)
            self.assertEquals(polygon._point_in_polygon(p), Polygon.POLYGON_INSIDE)
            self.assertTrue(polygon.is_inside(p))
        # point outside
        for point in ((1, 0), (3.1, 2.4), (4.9, 3.1), (4.65, 1.04), (5.97, 2.46)):
            p = Coordinates(*point)
            self.assertEquals(polygon._point_in_polygon(p), Polygon.POLYGON_OUTSIDE)
            self.assertFalse(polygon.is_inside(p))
