# Partial code for Linear regression by Stochastci Gradeint Descent

import numpy as np

X = -0.5 + 2 * np.random.rand(50, 1)
y = -1 + 5 * X + np.random.randn(50, 1) * 2

print(X)
X_b = np.c_[np.ones((50, 1)), X]
print(X_b)

n_epochs = 50
t0 = 5
t1 = 50
# learning schedule hyperparameters
m = 50

theta = np.random.randn(2, 1)  # random initialization

for epoch in range(n_epochs):
    for i in range(m):
        ri = np.random.randint(m, size=10) # random_index
        xi = X_b[ri]
        yi = y[ri]
        gradients = 2 / 9 * xi.T.dot(xi.dot(theta) - yi)
        eta = t0 / (epoch * m + i + t1)
        theta = theta - eta * gradients

X_new = np.array([[-1], [2]])
X_new_b = np.c_[np.ones((2, 1)), X_new]
y_predict = X_new_b.dot(theta)

import matplotlib.pyplot as plt

plt.plot(X_new, y_predict, 'g-')
plt.plot(X, y, 'b.')
plt.axis([-1, 2, -10, 15])
plt.xlabel('x')
plt.ylabel('y')
plt.legend(['Predictions', 'x1'])
plt.show()
