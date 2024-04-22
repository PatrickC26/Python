# Import MNIST
import pandas as pd
df = pd.read_csv('/Users/slothsmba/Downloads/mnist_784.csv', header=0)
y = df.iloc[:, -1].values
X = df.iloc[:, 0:-1].values

import numpy as np
y = y.astype(np.uint8)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.35)

from sklearn.linear_model import SGDClassifier
sgd_clf = SGDClassifier(random_state=42,loss='log')
sgd_clf.fit(X_train, y_train)

# print(sgd_clf.predict(X_test[0:10, :]))
# print(y_test[0:10])
#
# digit_scores = sgd_clf.decision_function(X_test)
# print(digit_scores[0:10])
#
# y_test_pred=np.argmax(digit_scores,axis=1)
# print(y_test_pred[0:10])
#
# from sklearn.metrics import confusion_matrix
y_test_pred=sgd_clf.predict(X_test)
# confmat=confusion_matrix(y_test, y_test_pred)
# print(confmat)

from sklearn.metrics import accuracy_score
accuracy_score(y_test, y_test_pred)