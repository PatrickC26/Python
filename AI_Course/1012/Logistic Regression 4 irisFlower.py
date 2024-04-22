import numpy as np
import pandas as pd

# Reading-in the Iris data
df = pd.read_csv('/Users/slothsmba/Downloads/iris.csv', header=0)

y = df.iloc[:, 4].values
y = np.where(y == 'virginica', 1, 0) # 1 if Iris virginica, else 0

# Use petal width as feature
X = df.iloc[:, 3].values.reshape(-1,1) # Make array to double array

from sklearn.linear_model import LogisticRegression
log_reg = LogisticRegression()
log_reg.fit(X, y) # Train logistic regression model

y_hat = log_reg.predict(X) # Show the most likely class

print(y_hat)

# decision boundary
import matplotlib.pyplot as plt
X_new = np.linspace(0, 3, 1000).reshape(-1, 1)
y_proba = log_reg.predict_proba(X_new) # Show the possibility of all class
print(y_proba)
plt.plot(X_new, y_proba[:, 1], "g-", label="Iris virginica")
plt.plot(X_new, y_proba[:, 0], "b--", label="Not Iris virginica")
plt.show()


