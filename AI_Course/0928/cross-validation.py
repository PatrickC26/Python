# ====== Import data ========
import pandas as pd

df = pd.read_csv('/Users/slothsmba/Downloads/mnist_784.csv', header=0)  # header is the up row

y = df.iloc[:, -1].values
X = df.iloc[:, 0:-1].values

print(X.shape)
print(y.shape)

# Build a binary classifier of digit 5 or non-5
import numpy as np
y = y.astype(np.uint8)

# True for all 5s, False for all other digits
y_5 = (y == 5)

from sklearn.linear_model import SGDClassifier
sgd_clf = SGDClassifier(random_state=42)

from sklearn.model_selection import cross_val_score
print(cross_val_score(sgd_clf, X, y_5, cv=3, scoring="accuracy"))

from sklearn.model_selection import cross_val_predict
y_pred = cross_val_predict(sgd_clf, X, y_5, cv=3)
print(y_pred)

from sklearn.metrics import confusion_matrix
print(confusion_matrix(y_5, y_pred))

from sklearn.metrics import precision_score, recall_score
precision_score(y_5, y_pred)

recall_score(y_5, y_pred)

from sklearn.metrics import f1_score
f1_score(y_5, y_pred)


# Precision/recall trade-off

from sklearn.model_selection import cross_val_predict
y_scores = cross_val_predict(sgd_clf, X, y_5, cv=3, method="decision_function")

from sklearn.metrics import precision_recall_curve
precisions, recalls, thresholds = precision_recall_curve(y_5, y_scores)

import matplotlib.pyplot as plt
def plot_precision_recall_vs_threshold(precisions, recalls, thresholds):
  plt.plot(thresholds, precisions[:-1], "b--", label="Precision")
  plt.plot(thresholds, recalls[:-1], "g-", label="Recall")

plot_precision_recall_vs_threshold(precisions, recalls, thresholds)
plt.show()


# ROC curve

from sklearn.metrics import roc_curve
fpr, tpr, thresholds = roc_curve(y_5, y_scores)

def plot_roc_curve(fpr, tpr, label=None):
  plt.plot(fpr, tpr, linewidth=2, label=label)
  plt.plot([0, 1], [0, 1], 'k--') # Dashed diagon

import matplotlib.pyplot as plt
plot_roc_curve(fpr, tpr)
plt.show()

from sklearn.metrics import roc_auc_score
roc_auc_score(y_5, y_scores)