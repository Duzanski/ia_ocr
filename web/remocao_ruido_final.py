# -*- coding: utf-8 -*-
"""Remocao_ruido_final.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XCh0ZGK-hWU-keRU1WLs3e1mmCkIf9SQ
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import cv2

from sklearn.model_selection import train_test_split

from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, UpSampling2D, Dropout, Conv2DTranspose
from tensorflow.keras.callbacks import EarlyStopping

from google.colab import drive
drive.mount('/content/drive')

# Setting de main path
path = '/content/drive/MyDrive/data_cleaner/data/'

# Getting a list with the names of the entries in the directory
train_img = sorted(os.listdir(path + 'train_dirty/dirty/'))
train_cleaned_img = sorted(os.listdir(path + 'train_cleaned/cleaned/'))
test_img = sorted(os.listdir(path + 'test_dirty/test/'))

# Processing de images giving it a new dtype, shape and dimension
def process_image(path):
    img = cv2.imread(path)
    img = np.asarray(img, dtype="float32")
    img = cv2.resize(img, (540, 420)) #changing image dimensions
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img = img/255.0
    img = np.reshape(img, (420, 540, 1))

    return img

# Crating the lists
train = []
train_cleaned = []
test = []

# Processing the imagens 
for i in sorted(os.listdir(path + 'train_dirty/dirty/')):
    train.append(process_image(path + 'train_dirty/dirty/' + i))

for f in sorted(os.listdir(path + 'train_cleaned/cleaned/')):
    train_cleaned.append(process_image(path + 'train_cleaned/cleaned/' + f))

for f in sorted(os.listdir(path + 'test_dirty/test/')):
    test.append(process_image(path + 'test_dirty/test/' + f))

# Creating a numpy array
X_train = np.asarray(train)
Y_train = np.asarray(train_cleaned)
X_test = np.asarray(test)

# Using sklearn to create train and test validation
X_train, X_val, Y_train, Y_val = train_test_split(X_train, Y_train, test_size=0.2)

autoencoder = Sequential()

# -> Encoder

# Adding Conv layer and decrease dimension
autoencoder.add(Conv2D(16,(3,3), strides=1, padding='same', activation='relu', input_shape=(420,540,1)))
autoencoder.add(MaxPooling2D((2,2), padding='same'))

# Avoiding overfitting
autoencoder.add(Dropout(0.2))

autoencoder.add(Conv2D(8,(3,3), strides=1, padding='same', activation='relu'))
autoencoder.add(MaxPooling2D((2,2), padding='same'))

# -> Encoded image
autoencoder.add(Conv2D(8,(3,3), strides=1, padding='same', activation='relu'))

# -> Decode image and increase dimension
autoencoder.add(UpSampling2D((2,2)))
autoencoder.add(Conv2DTranspose(8, (3,3), strides=1, padding='same', activation='relu'))

autoencoder.add(UpSampling2D((2,2)))
autoencoder.add(Conv2DTranspose(1, (3,3), strides=1, padding='same', activation='sigmoid')) # Returning values between zero and one for the pixels

autoencoder.compile(
    optimizer='adam', loss='binary_crossentropy')

# Stop training when a monitored metric has stopped improving
callback = EarlyStopping(monitor='loss', patience=30)

# Start training 
history = autoencoder.fit(X_train, Y_train, validation_data = (X_val, Y_val), epochs=100, batch_size=30, verbose=1, callbacks=[callback])

# Showing loss on train x validation datasets over epochs
epoch_loss = history.history['loss']
epoch_val_loss = history.history['val_loss']

plt.figure(figsize=(20,6))
plt.subplot(1,2,1)
plt.plot(range(0,len(epoch_loss)), epoch_loss, 'b-', linewidth=2, label='Train Loss')
plt.plot(range(0,len(epoch_val_loss)), epoch_val_loss, 'r-', linewidth=2, label='Val Loss')
plt.title('Evolution of loss on train & validation datasets over epochs')
plt.legend(loc='best')

plt.show()

# Predict/cleaning test images
Y_test = autoencoder.predict(X_test, batch_size=16)

# Showing dirty x cleaned images
plt.figure(figsize=(15,25))
for i in range(0,8,2):
    plt.subplot(4,2,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(X_test[i][:,:,0], cmap='gray')
    plt.title('Noisy image: {}'.format(test_img[i]))
    
    plt.subplot(4,2,i+2)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(Y_test[i][:,:,0], cmap='gray')
    plt.title('Denoised by autoencoder: {}'.format(test_img[i]))

plt.show()

# Savind the models
autoencoder.save('cnn_model.h5')

# Saving the weights
model_json = autoencoder.to_json()
with open("cnn_model.json", "w") as json_file:
    json_file.write(model_json)