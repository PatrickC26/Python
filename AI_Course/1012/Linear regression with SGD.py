import numpy as np
X = 2 * np.random.rand(100, 1)
y = 4 + 3 * X + np.random.randn(100, 1)

from sklearn.linear_model import SGDRegressor
sgd_reg = SGDRegressor(max_iter=1000, tol=1e-3, penalty=None, eta0=0.1, loss="log")
sgd_reg.fit(X, y)

# y=ax+b
print(sgd_reg.intercept_) # b
print(sgd_reg.coef_) # a

# for drawing the line
X_new = np.array([[0], [2]])
y_predict = sgd_reg.coef_*X_new+sgd_reg.intercept_

import matplotlib.pyplot as plt
plt.plot(X_new, y_predict, 'r-')
plt.plot(X, y, 'b.')
plt.axis([-0, 2, -1, 15])
plt.xlabel('x1')
plt.ylabel('y')
plt.legend(['Predictions','x1'])
plt.show()