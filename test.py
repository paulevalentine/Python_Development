""" Test Module to quickly test Class coding """
from timber import *

a = TimberBeam(50,150, 'C24',
              load_duration='permanent',
              service_class=1)

print(a.fmd)
