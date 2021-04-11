""" test module for code """
from timber_connection import *
c = ScrewConnection(4.17, 8, 'C24')
print(c.screw_lateral(t1=33, t2=33))
print(c.splitting())
