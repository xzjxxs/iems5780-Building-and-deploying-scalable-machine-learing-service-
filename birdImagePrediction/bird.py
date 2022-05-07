# 1155161089 XUZijun
# bird.py
# Training a Convolutional Neural Network

import glob
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import datasets, layers, models
from PIL import Image
from sklearn.metrics import classification_report


def read_image(path):
    # get each folder path of each bird
    # 0: Asian Brown Flycatcher
    # 1: Blue Rock Thrush
    # 2: Brown Shrike
    # 3: Grey-faced Buzzard
    cate = [path + x for x in os.listdir(path) if os.path.isdir(path + x)]
    imgs = []
    labels = []
    report_Asian = []
    report_Blue = []
    report_Brown = []
    report_Grey = []
    for idx, folder in enumerate(cate):
        for im in glob.glob(folder + '/*.jpg'):
            # print('reading the images:%s' % (im))
            # report the IDs of the select images
            if "Asian Brown Flycatcher" in folder:
                report_Asian.append(os.path.basename(im).split('_')[0])
            if "Blue Rock Thrush" in folder:
                report_Blue.append(os.path.basename(im).split('_')[0])
            if "Brown Shrike" in folder:
                report_Brown.append(os.path.basename(im).split('_')[0])
            if "Grey-faced Buzzard" in folder:
                report_Grey.append(os.path.basename(im).split('_')[0])
            img = Image.open(im)
            img = img.convert("L")  # convert them to gray scale
            resize_img = np.array(img.resize((256, 256)))
            imgs.append(resize_img)
            labels.append(idx)
    return imgs, labels, report_Asian, report_Blue, report_Brown, report_Grey


def standardized(x, y):
    if(len(x) == 160):
        x_train = np.array(x)
        # In order to rank 1 array
        y_train = np.array(y).reshape(160, 1)
        x_train = x_train / 255.0
        x_train = x_train.reshape((160, 256, 256, 1))
        return x_train, y_train
    else:
        x = np.array(x)
        # In order to rank 1 array
        y = np.array(y).reshape(40, 1)
        x = x / 255.0
        x = x.reshape((40, 256, 256, 1))
        return x, y


def cnn():
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(256, 256, 1)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dropout(0.4),
        layers.Dense(64, activation='relu'),
        layers.Dense(4)
    ])
    model.compile(optimizer='Adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    return model


def save(model):
    model.save('bird_model.h5')


if __name__ == '__main__':
    # load the training set
    x_train, y_train, report_Asian, report_Blue, report_Brown, report_Grey = read_image('train/')
    print("Images of Asian Brown Flycatcher used in the training set are " + str(report_Asian))
    print("Images of Blue Rock Thrush used in the training set are " + str(report_Blue))
    print("Images of Brown Shrike used in the training set are " + str(report_Brown))
    print("Images of Grey-faced Buzzard used in the training set are " + str(report_Grey))
    x_train, y_train = standardized(x_train, y_train)
    # load the testing set
    x_test, y_test, report_Asian, report_Blue, report_Brown, report_Grey = read_image('test/')
    print("Images of Asian Brown Flycatcher used in the testing set are " + str(report_Asian))
    print("Images of Blue Rock Thrush used in the testing set are " + str(report_Blue))
    print("Images of Brown Shrike used in the testing set are " + str(report_Brown))
    print("Images of Grey-faced Buzzard used in the testing set are " + str(report_Grey))
    x_test, y_test = standardized(x_test, y_test)
    # load the validation set
    x_val, y_val, report_Asian, report_Blue, report_Brown, report_Grey = read_image('val/')
    x_val, y_val = standardized(x_val, y_val)

    # train model
    model = cnn()
    # save the model
    save(model)
    history = model.fit(x_train, y_train, epochs=10, validation_data=(x_val, y_val))
    prediction = model.predict(x_test)

    # prediction
    yhat = []
    for i in range(len(prediction)):
        yhat.append(np.argmax(prediction[i]))
    yhat = np.array(yhat).reshape(40, 1)

    # get the classification_report
    print(classification_report(yhat, y_test))

