# ====== Import data ========
import pandas as pd

df = pd.read_csv('/Users/slothsmba/Downloads/mnist_784.csv', header=0)  # header is the upper row

y = df.iloc[:, -1].values
# get all columns and -1(last) row
X = df.iloc[:, 0:-1].values
# get all columns and 0~-1(0~last) rows

print(X.shape)
print(y.shape)

# ===== Show image =======

import matplotlib.pyplot as plt

images_labels = list(zip(X, y))
for index, (image, label) in enumerate(images_labels[:10]):
    plt.axis('off')
    plt.imshow(image.reshape(28, 28), cmap='gray', interpolation='nearest')
    plt.title(label)
    plt.tight_layout()
    # plt.show()

# ======= binary classifier of 5 or non 5


import numpy as np
y = y.astype(np.uint8)


X_train, X_test, y_train, y_test = X[:60000], X[60000:], y[:60000], y[60000:]
# X_train : 0~60,000 (0-last row)
# X_test : 60,000 ~ 70,000
# y_train : 0~60,000 (last row)
# y_test  : 60,000 ~ 70,000

y_train_5 = (y_train == 5)
# find data for target (5) in y_train
y_test_5 = (y_test == 5)
# find data for target (5) in y_test




from sklearn.linear_model import SGDClassifier
sgd_clf = SGDClassifier(random_state=42)
# init
sgd_clf.fit(X_train, y_train_5)
# use y to train X


y_train_pred=sgd_clf.predict(X_train)


# Predict the data
from sklearn.metrics import accuracy_score
ascore = accuracy_score(y_train_5, y_train_pred)
# get accuracy
print(ascore)

y_test_pred=sgd_clf.predict(X_test)
ascore = accuracy_score(y_test_5, y_test_pred)
print(ascore)

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test_5, y_test_pred)
# get confusion matrix
print(cm)

from sklearn.metrics import precision_score, recall_score
ps = precision_score(y_test_5, y_test_pred)
# get precision score
print(ps)

rs = recall_score(y_test_5, y_test_pred)
# get recall score
print(rs)

from sklearn.metrics import f1_score
f = f1_score(y_test_5, y_test_pred)
# get f1 score
print(f)