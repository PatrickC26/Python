# Fashion MNIST classification using sequential API
print("OK")

## Using Keras to load the dataset

from tensorflow import keras
# TODO M1 tensorflow is needed

fashion_mnist = keras.datasets.fashion_mnist
(X_train_full, y_train_full), (X_test, y_test) = fashion_mnist.load_data()

print(X_train_full.shape)
print(X_train_full.dtype)

## Create a validation set & standarization

X_valid, X_train = X_train_full[:5000] / 255.0, X_train_full[5000:] / 255.0
y_valid, y_train = y_train_full[:5000], y_train_full[5000:]
X_test = X_test / 255.0

## Create a list of class names & plot image

import numpy as np

class_names = ["T-shirt/top", "Trouser", "Pullover", "Dress", "Coat", "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"]
print(np.array(class_names)[0:10])

## Plot image
import matplotlib.pyplot as plt

some_cloth = X_train[0]
some_cloth_image = some_cloth.reshape(28, 28)
plt.imshow(some_cloth_image, cmap="binary")
plt.axis("off")
plt.show()

# Creating the model using the Sequential AP

model = keras.models.Sequential([
  keras.layers.Flatten(input_shape=[28,28]),
  keras.layers.Dense(300, activation="relu"),
  keras.layers.Dense(100, activation="relu"),
  keras.layers.Dense(10, activation="softmax")
])


# Display model information

model.summary()

model.layers

hidden1 = model.layers[1]
weights, biases = hidden1.get_weights()
