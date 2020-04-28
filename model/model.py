import numpy as np
import tensorflow as tf
from tensorflow.keras.datasets import mnist

#MNIST dataset parameters
num_classes = 10    # (0-9 digits)
num_features = 784  # img shape: 28*28

(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Convert to float32
x_train, x_test = np.array(x_train, np.float32), np.array(x_test, np.float32)

# Flatten images to 1D vector of 784
x_train, x_test = x_train.reshape([-1, num_features]), x_test.reshape([-1, num_features])

# Normalize images valuing from [0, 255] to [0, 1]
x_train, x_test = x_train/255, x_test/255
