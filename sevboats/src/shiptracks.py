# -*- coding: utf-8 -*-

from xml.dom.minidom import parse
from coordinates import Polygon, Coordinates
from ships import Ship
from settings import DATA_DIR


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

    def is_inside(self, ship):
        return self.area.is_inside(ship.coordinates)


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

    def is_inside(self, ship):
        return self.bay.is_inside(ship.coordinates)

    def verification(self, ship):
        """ Checks Is the ship on the route """
        if not self.bay.is_inside(ship.coordinates):
            return None
        else:
            count = 1

        if (ship.speed < Ship.STOP_SPEED):
            for pier in self.piers:
                if pier.area.is_inside(ship.coordinates):
                    return MN.TRUEPOS

        for point in ship.lastpos:
            count += self.bay.is_inside(point)

        return count


class RoutesContainer(object):

    """ The container for save routes """

    container = []
    deadend = None

    def __init__(self):
        """ Create new instance and parse all bay info """
        for name in (
            'Gorod - Severnaja', 'Artbuhta - Severnaja', 'Artbuhta - Radiogorka',
                'Gorod - Gollandija - Inkerman', 'Gorod - Avlita', ):
            container.append(Route(self.parse_area(name)))

        piers = (
            ('Grafskaja pristan', 'Severnaja kater'),
            ('Art buhta parom', 'Severnaja parom'),
            ('Art buhta kater', 'Radiogorka'),
            ('Pirs u porta', 'Apolonovka', 'Gollandija', 'Ugolnaja', 'Inkerman - 1', 'Inkerman - 2', ),
            ('Pirs u porta', 'Apolonovka', 'Avlita'), )
        # add piers to routes
        for i in xrange(len(piers)):
            for name in piers[i]:
                self.container[i].piers.append(Pier(self.parse_pier(name)))
        # get deadend
        self.deadend = self.parse_pier('Dead end')

    def get_route_path(self, filename):
        """ Return file path to self route file """
        return os.path.join(DATA_DIR, 'bay', filename + '.kml')

    def parse_area(self, filename):
        """
        Parse coordinate from klm file.
        return: str_name, [Coordinates(latitude, longitude)]
        """
        placemark = parse(self.get_route_path(filename)).getElementsByTagName("Placemark")[0]        
        coordinates = placemark.getElementsByTagName("coordinates")[0].childNodes[0].nodeValue
        #Warning ENCODE CP 866 
        name = placemark.getElementsByTagName("name")[0].childNodes[0].nodeValue#.encode("CP866")
        polygon = []
        for coord in coordinates.split():
            #print "#", coord, "#"
            longitude, latitude, altitude = (float(c) for c in coord.split(',') if c != '')
            polygon.append(Coordinates(latitude, longitude))
        return name, Area(polygon)

    def parse_pier(self, filename):
        '''
        Parse coordinate from klm file.
        return: (str_name, [Coordinates(latitude, longitude)], Coordinates(latitude, longitude) )
        '''
        LookAt = parse(self.get_route_path(filename)).getElementsByTagName("LookAt")[0]
        latitude = float(LookAt.getElementsByTagName("latitude")[0].childNodes[0].nodeValue)
        longitude = float(LookAt.getElementsByTagName("longitude")[0].childNodes[0].nodeValue)
        mark = Coordinates(latitude, longitude)

        area = self.parse_area(filename)
        res = area[0], area[1], mark
