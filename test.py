""" test module for code """
from timber_connection import *
c = ScrewConnection(3, 6, 'C24')
print(c.screw_withdrawal(tpen=50, n=1))
print(c.faxk_screw(tpen=50))
print(c.nef_axial(n=1))
print(c.nail_withdrawal(tpen=50, t=50, number=1))
