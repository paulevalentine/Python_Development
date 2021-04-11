""" test module for code """
from timber_connection import *
c = ScrewConnection(4.17, 8, 'C24')
x = range(20, 100, 1)
y = [c.Fvrk(a) for a in x]
print(c.Fvrk(t1=33, t2=33))

import matplotlib.pyplot as plt
plt.plot(x, y)
plt.grid()
plt.show()
