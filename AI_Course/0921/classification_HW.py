# ====== Import data ========
import pandas as pd

df = pd.read_csv('/Users/slothsmba/Downloads/mnist_784.csv', header=0)  # header is the up row

y = df.iloc[:, -1].values
X = df.iloc[:, 0:-1].values

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

X_train, X_test, y_train, y_test = X[:56000], X[56000:], y[:56000], y[56000:]  #!
y_train_5 = (y_train < 5) #!
y_test_5 = (y_test < 5) #!


from sklearn.linear_model import SGDClassifier
sgd_clf = SGDClassifier(random_state=42)
sgd_clf.fit(X_train, y_train_5)

from sklearn.metrics import accuracy_score
y_train_pred=sgd_clf.predict(X_train)
ascore = accuracy_score(y_train_5, y_train_pred)
print("Accuracy train_set : " + str(ascore))

y_test_pred=sgd_clf.predict(X_test)
ascore = accuracy_score(y_test_5, y_test_pred)
print("Accuracy test_set : " + str(ascore))

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_train_5, y_train_pred)
print("confusion_matrix train_set : " + str(cm))

cm = confusion_matrix(y_test_5, y_test_pred)
print("confusion_matrix test_set : " + str(cm))

# from sklearn.metrics import precision_score, recall_score
# ps = precision_score(y_test_5, y_test_pred)
# print(ps)
#
# rs = recall_score(y_test_5, y_test_pred)
# print(rs)

from sklearn.metrics import f1_score
f = f1_score(y_train_5, y_train_pred)
print("f1 score train_set" + str(f))

f = f1_score(y_test_5, y_test_pred)
print("f1 score test_set" + str(f))