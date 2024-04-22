import numpy as np
import pandas as pd

# Reading-in the Iris data


df = pd.read_csv('/Users/slothsmba/Downloads/iris.csv', header=0)

# 0,1,2 for Setosa, Versicolor, and Virginica
y = df.iloc[:, 4].values
y1 = np.where(y == 'setosa', 0, 1)
y2 = np.where(y == 'virginica', 1, 0)
print(y2)
y = y1+y2
print(y)

X = df.iloc[:, [2,3]].values
print(X)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test  = train_test_split(X, y, test_size=0.3, train_size=0.7)

from sklearn.linear_model import SGDClassifier # 隨機 一次一個smaple一次調整
sgd_C = SGDClassifier(loss="log") #LogisticRegression base on DGD
sgd_C.fit(X_train, y_train)


print(X_test)

y_predict = sgd_C.predict(X_test)
# a = sgd_C.decision_function(X_test)
# print(a)
# y_predict = np.argmax(a, axis=1)
# print(y_predict)

from sklearn.metrics import confusion_matrix
confmat = confusion_matrix(y_test, y_predict)
print(confmat)


from sklearn.metrics import accuracy_score
ascore = accuracy_score(y_test, y_predict)
print(ascore)

print("=-==--==---==")
avg = 'micro'
from sklearn.metrics import precision_score, recall_score
ps = precision_score(y_test, y_predict, average=avg)
rs = recall_score(y_test, y_predict, average=avg)
print(ps)
print(rs)

from sklearn.metrics import f1_score
f1 = f1_score(y_test, y_predict,average=avg)
print(f1)

print("--------")
avg = 'macro'
ps = precision_score(y_test, y_predict, average=avg)
rs = recall_score(y_test, y_predict, average=avg)
print(ps)
print(rs)
f1 = f1_score(y_test, y_predict,average=avg)
print(f1)

print("=======")
avg = 'weighted'
ps = precision_score(y_test, y_predict, average=avg)
rs = recall_score(y_test, y_predict, average=avg)
print(ps)
print(rs)
f1 = f1_score(y_test, y_predict,average=avg)
print(f1)


from matplotlib import pyplot as plt
fig, ax = plt.subplots(figsize=(2.5, 2.5))
ax.matshow(confmat, cmap=plt.cm.Blues, alpha=0.3)
for i in range(confmat.shape[0]):
    for j in range(confmat.shape[1]):
        ax.text(x=j, y=i, s=confmat[i, j], va='center', ha='center')
plt.xlabel('predicted label')
plt.ylabel('true label')
plt.show()