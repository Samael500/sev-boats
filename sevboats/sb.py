from src.engine import *
from src.coordinates import Coordinates

loadship()
update_ais_data()
update_ais_lastpos()

SlL.fleet().print_ships(True)
print 'on routes: ', check_ships_on_routes()

# for mmsi, ship in SlL.fleet().container.iteritems():
#     print 


    # print len(ship.lastpos)


# from src.scrapper import Scrapper

# sr = Scrapper()

# lastpos = sr.scrape_lastpos('272083800')
# print lastpos
