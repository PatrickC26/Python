import numpy as np
X = 2 * np.random.rand(50, 1) # uniform dist
y = -0.5 + 2.5 * X + np.random.randn(50, 1)*0.8 # normal dist

X_b = np.c_[np.ones((50, 1)), X]
eta = 0.1 # learning rate
n_iterations = 1000
m = 100

theta = np.random.randn(2,1) # random initialization

for iteration in range(n_iterations):
  gradients = 2/m * X_b.T.dot(X_b.dot(theta) - y)
  theta = theta - eta * gradients

print(theta)

X_new = np.array([[-1], [2]])
X_new_b = np.c_[np.ones((2, 1)), X_new]
y_predict = X_new_b.dot(theta)

import matplotlib.pyplot as plt
plt.plot(X_new, y_predict, 'g-')
plt.plot(X, y, 'b.')
plt.axis([-1, 2, -10, 15])
plt.xlabel('x')
plt.ylabel('y')
plt.legend(['Predictions','x1'])
plt.show()