from timber_connection import *
import matplotlib.pyplot as plt
s = ScrewConnection(diam=2.8, diamh=5.6, grade='C24', load_duration='permanent',
                   service_class=2)
s.screw_withdrawal(tpen=100, t=75, number=1)
e1 = s.faxk() * s.diam * 75
x = range(1,100,1)
y = []
for i in range(len(x)):
    e2 = s.screw_withdrawal(75, i, 1)
    y.append(e2)

plt.plot(x,y)
plt.axhline(e1)
plt.grid()
plt.show()
