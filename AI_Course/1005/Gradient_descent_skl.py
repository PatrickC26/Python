import numpy as np
X = 2 * np.random.rand(50, 1) # uniform dist
y = -0.5 + 2.5 * X + np.random.randn(50, 1) # normal dist

from sklearn.linear_model import SGDRegressor
sgd_reg = SGDRegressor(max_iter=1000, tol=1e-3, penalty=None, eta0=0.1)
sgd_reg.fit(X, y)

print(sgd_reg.intercept_)
print(sgd_reg.coef_)


# Will have Error due to the array has one row, but code see it as two row
# Has error but could run