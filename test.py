""" test module for code """
from timber_connection import *
c = ScrewConnection(5, 10, 'C24')
print(c.screw_withdrawal(tpen=50, n=1))
print(c.screw_pullthrough(n=1))
print(c.screw_axial(tpen=50, n=1))
print(f'This is the value for the nail: {c.nail_withdrawal(tpen=50)}')
