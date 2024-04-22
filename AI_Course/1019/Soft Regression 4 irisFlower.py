import pandas as pd
df = pd.read_csv('/Users/slothsmba/Downloads/iris.csv', header=0)

import numpy as np
# 0,1,2 for Setosa, Versicolor, and Virginica
y = df.iloc[:, 4].values
y1 = np.where(y == 'setosa', 0, 1)
y2 = np.where(y == 'virginica', 1, 0)
print(y2)
y = y1+y2

# Use petal length, petal width as feature
X = df.iloc[:, [2,3]].values
print(X)

from sklearn.linear_model import LogisticRegression
softmax_reg = LogisticRegression(multi_class="multinomial",solver="lbfgs", C=10)
softmax_reg.fit(X, y)

print(softmax_reg.predict([[5, 2]]))
print(softmax_reg.predict_proba([[5, 2]]))


# Plotting decision regions
import matplotlib.pyplot as plt
# plot_decision_regions(X, y, classifier=softmax_reg)
plt.xlabel('petal length [cm]')
plt.ylabel('petal width [cm]')
plt.legend(loc='upper left')
plt.show()
