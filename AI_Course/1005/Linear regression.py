import numpy as np
X = 2 * np.random.rand(50, 1) # uniform dist
y = -0.5 + 2.5 * X + np.random.randn(50, 1)*0.8 # normal dist


X_b = np.c_[np.ones((50, 1)), X]
theta_best = np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T).dot(y)

X_new = np.array([[0], [2]]) # give a double array as [ [0] [2] ], which x is at 0 & 2
X_new_b = np.c_[np.ones((2, 1)), X_new]
y_predict = X_new_b.dot(theta_best) # Calculate the value out

print(theta_best)


import matplotlib.pyplot as plt
plt.plot(X_new, y_predict, 'r-')
plt.plot(X, y, 'b.')
plt.axis([-0, 2, -1, 15])
plt.xlabel('x1')
plt.ylabel('y')
plt.legend(['Predictions','x1'])
plt.show()