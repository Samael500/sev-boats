# -*- coding: utf-8 -*-

import unittest

from sevboats.src.coordinates import Coordinates
from random import uniform


class TestCoordinates(unittest.TestCase):

    """ Test coordinates class """

    def test_coord_init(self):
        """ Create coord instance and check it """
        coord = Coordinates(44.6215507, 33.530091)
        # check correct set latitude, longitude
        self.assertEquals(coord.latitude, 44.6215507)
        self.assertEquals(coord.longitude, 33.530091)
        # check property lat, long
        self.assertEquals(coord.lat, 44.6215507)
        self.assertEquals(coord.long, 33.530091)
        self.assertEquals(coord.latitude, coord.lat)
        self.assertEquals(coord.longitude, coord.long)

    def test_coord_square_and_det(self):
        """ Check triangle square and correct det """
        A = Coordinates(0, 0)
        B = Coordinates(0, 3)
        C = Coordinates(4, 0)
        squares = [
            Coordinates.square(A, B, C), Coordinates.square(A, C, B), Coordinates.square(B, A, C),
            Coordinates.square(B, C, A), Coordinates.square(C, A, B), Coordinates.square(C, B, A), ]
        dets = [
            Coordinates.det(A, B, C), Coordinates.det(B, C, A), Coordinates.det(C, A, B),
            Coordinates.det(A, C, B), Coordinates.det(C, B, A), Coordinates.det(B, A, C), ]
        for square in squares:
            self.assertEquals(square, 6)
        for det in dets[:3]:
            self.assertEquals(det, -12)
        for det in dets[3:]:
            self.assertEquals(det, 12)

    def test_coord_square(self):
        """ Check triangle squares """
        A = Coordinates(2, -4)
        B = Coordinates(-5, -6)
        C = Coordinates(1, 3)
        square = Coordinates.square(A, B, C)
        self.assertEquals(square, 25.5)
        A = Coordinates(-124.523, 3445.453)
        B = Coordinates(9235.253, -234.234)
        C = Coordinates(235.2352, -21.2131)
        square = Coordinates.square(A, B, C)
        self.assertEquals(square, 15561710.295555102)

    def test_coord_eq(self):
        """ Check coord equal and don't equal """
        A = Coordinates(7, 4)
        B = Coordinates(7, 4)
        C = Coordinates(4, 7)
        D = Coordinates(7, 7)
        E = Coordinates(4, 4)
        # check Equals
        self.assertEquals(A, B)
        self.assertNotEquals(A, C)
        self.assertNotEquals(A, D)
        self.assertNotEquals(A, E)
        # check operator ==
        self.assertTrue(A == B)
        self.assertFalse(A == C)
        self.assertFalse(A == D)
        self.assertFalse(A == E)
        # check operator !=
        self.assertFalse(A != B)
        self.assertTrue(A != C)
        self.assertTrue(A != D)
        self.assertTrue(A != E)

    def test_coord_neg(self):
        """ Check operator - unar """
        A = Coordinates(19, -84)
        B = Coordinates(-19, 84)
        self.assertEquals(A, -B)
        self.assertEquals(-A, B)

    def test_coord_lt(self):
        """ Check operator A < B """
        A = Coordinates(7, 4)
        B = Coordinates(7, 4)
        C = Coordinates(4, 7)
        D = Coordinates(7, 7)
        E = Coordinates(4, 4)
        # check A < *
        self.assertFalse(A < B)
        self.assertFalse(A < C)
        self.assertTrue(A < D)
        self.assertFalse(A < E)
        # check * < A
        self.assertFalse(B < A)
        self.assertTrue(C < A)
        self.assertFalse(D < A)
        self.assertTrue(E < A)

    def test_coord_sub(self):
        """ Check operator A - B coord """
        A = Coordinates(7, 15)
        B = Coordinates(9, 3)
        C = Coordinates(-2, 12)
        D = A - B
        E = B - A
        self.assertEquals(C, D)
        self.assertEquals(C, - E)
        A = Coordinates(4, 0)
        B = Coordinates(0, 3)
        C = Coordinates(4, -3)
        self.assertEquals(C, A - B)
        self.assertEquals(-C, B - A)

    def test_coord_add(self):
        """ Check operator A + B coord """
        A = Coordinates(7, 15)
        B = Coordinates(9, 3)
        C = Coordinates(16, 18)
        D = A + B
        E = B + A
        self.assertEquals(C, D)
        self.assertEquals(C, E)
        A = Coordinates(4, 0)
        B = Coordinates(0, 3)
        C = Coordinates(4, 3)
        self.assertEquals(C, A + B)
        self.assertEquals(C, B + A)

    def test_coord_mul(self):
        """ Check operator A * B coord """
        A = Coordinates(7, 15)
        B = Coordinates(9, 3)
        C = 7 * 9 + 15 * 3
        self.assertEquals(C, A * B)

    def test_coord_str(self):
        """ Check str coord """
        msg = 'latitude: {0}, longitude: {1}'
        for i in xrange(10):
            _lat = uniform(-100, 100)
            _long = uniform(-100, 100)
            A = Coordinates(_lat, _long)
            self.assertEquals(msg.format(_lat, _long), str(A))

    def test_coord_length(self):
        """ Check coord length """
        A = Coordinates(0, 3)
        B = Coordinates(4, 0)
        C = Coordinates(4, 3)
        self.assertEquals(A.length, 3)
        self.assertEquals(B.length, 4)
        self.assertEquals(C.length, 5)

    def test_coord_scalar(self):
        """ Check coord scalar """
        angle = 30
        A = Coordinates(0, 0)
        B = Coordinates(0, 1)
        scalar = Coordinates.scalar(A, B, angle)
        self.assertEquals(round(scalar, 2), 0.5)
        angle = 90
        scalar = Coordinates.scalar(A, B, angle)
        self.assertEquals(round(scalar, 2), 1)
        angle = 180
        scalar = Coordinates.scalar(A, B, angle)
        self.assertEquals(round(scalar, 2), 0)
        angle = 270
        scalar = Coordinates.scalar(A, B, angle)
        self.assertEquals(round(scalar, 2), -1)
        angle = 330
        scalar = Coordinates.scalar(A, B, angle)
        self.assertEquals(round(scalar, 2), -0.5)

    def test_coord_angle(self):
        """ Check angle betwen point with course """
        A = Coordinates(0, 0)
        B = Coordinates(1, 0)
        # check A - B angle
        for course in xrange(181):
            self.assertEquals(round(A.angle(course, B), 2), course)
            self.assertEquals(round(B.angle(course, A), 2), 180 - course)
        for course in xrange(181, 361):
            self.assertEquals(round(A.angle(course, B), 2), 360 - course)
            self.assertEquals(round(B.angle(course, A), 2), course - 180)
        for course in xrange(361, 450):
            self.assertEquals(round(A.angle(course, B), 2), course - 360)
            self.assertEquals(round(B.angle(course, A), 2), 540 - course)

    def test_coord_collinear(self):
        """ Check vector 'collinear' """
        A = Coordinates(0, 0)
        B = Coordinates(1, 0)
        # check A - B angle
        for course in xrange(90):
            self.assertFalse(A.collinear(course, B))
            self.assertTrue(B.collinear(course,  A))
        for course in xrange(91, 270):
            self.assertTrue(A.collinear(course,  B))
            self.assertFalse(B.collinear(course, A))
        for course in xrange(271, 360):
            self.assertFalse(A.collinear(course, B))
            self.assertTrue(B.collinear(course,  A))
        for course in (0, 270, 360):
            self.assertFalse(A.collinear(course, B))
            self.assertTrue(B.collinear(course,  A))
        # 90 - allways False - scalar is 0
        self.assertFalse(A.collinear(90, B))
        self.assertFalse(B.collinear(90, A))
