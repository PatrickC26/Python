import numpy as np
X = 2 * np.random.rand(50, 1) # uniform dist
y = -0.5 + 2.5 * X + np.random.randn(50, 1)*0.8 # normal dist


from sklearn.linear_model import LinearRegression
lin_reg = LinearRegression()
lin_reg.fit(X, y) # Train model

X_new = np.array([[0], [2]]) # give a double array as [ [0] [2] ], which x is at 0 & 2
y_predict = lin_reg.predict(X_new) # export y points from according X array point

print(X_new)  #[[0] [2]]
print(y_predict)  #[[0.12] [4.12]]

print(lin_reg.intercept_) # b
print(lin_reg.coef_) # a
    # y = ax + b

import matplotlib.pyplot as plt
plt.plot(X_new, y_predict, 'r-')
plt.plot(X, y, 'b.')
plt.axis([-0, 2, -1, 15])
plt.xlabel('x1')
plt.ylabel('y')
plt.legend(['Predictions','x1'])
plt.show()