import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 5, 1000)
y = 1 / (1 + x)

plt.plot(x, y)
plt.xlabel('x')
plt.ylabel('1/(1+x)')
plt.title('Plot of 1/(1+x)')

plt.show()