import numpy as np
X = 2 * np.random.rand(50, 1)-0.5
y = -1 + 5 * X + 2*np.random.randn(50, 1)


for i in range(len(y)):
    y[i] = int(y[i])

print(y)


# from sklearn.linear_model import SGDClassifier
# sgd_mini = SGDClassifier(loss="log")
# sgd_mini.partial_fit(X, y, np.unique(y))


#
# # lasso -> l1
# # Ridge -> l2
from sklearn.linear_model import SGDRegressor
sgd_reg = SGDRegressor(max_iter=1000, tol=1e-3, penalty="l1", eta0=0.1, alpha=0)
sgd_reg.fit(X, y)




X_new = np.array([[-1], [2]])
Y_reg = sgd_reg.predict(X_new)
# Y_mini = sgd_mini.predict(X_new)


import matplotlib.pyplot as plt
plt.plot(X_new, Y_reg, 'r-')
# plt.plot(X_new, Y_mini, 'g-')
plt.plot(X, y, 'b.')
plt.axis([-1, 2, -10, 15])
plt.xlabel('x')
plt.ylabel('y')
plt.legend(['Predictions','data'])
plt.show()