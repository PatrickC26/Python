import numpy as np
import pandas as pd

# Reading-in the Iris data
df = pd.read_csv('/Users/slothsmba/Downloads/iris.csv', header=0)

# df = df[50:, :]

y = df.iloc[50:, 4].values
y = np.where(y == 'virginica', 1, 0) # 1 if Iris virginica, versicolor 0


# Use petal width as feature
X = df.iloc[50:, 0:4].values
print(X)
print("\n---\n")



from sklearn.linear_model import LogisticRegression # 所有sample 的誤差一起下去sum/ BATCH METHOD
log_reg = LogisticRegression(penalty="l1", C=20.0, solver='saga')
log_reg.fit(X, y) # Train logistic regression model

y_hat = log_reg.predict(X)

from  sklearn.metrics import accuracy_score
print(accuracy_score(y, y_hat))




from sklearn.linear_model import SGDClassifier # 隨機 一次一個smaple一次調整
sgd_reg = SGDClassifier(penalty="l1", loss="log", alpha=0.05) #LogisticRegression base on DGD
sgd_reg.fit(X, y)

y_hat = sgd_reg.predict(X)

from  sklearn.metrics import accuracy_score
print(accuracy_score(y, y_hat))



