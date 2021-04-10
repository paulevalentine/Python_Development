import matplotlib.pyplot as plt

x = range(1, 100, 1)
y = [a**2 for a in x]
plt.plot(x,y)
plt.grid()
plt.xlabel('This is something')
plt.show()
