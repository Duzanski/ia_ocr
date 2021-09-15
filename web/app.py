"""
Developed by Reinaldo Duzanski Júnior
14/09/2021

-> Challeng where the user must send a dirty image in base64 format
and the system should return its cleaned version + the string content

RESOURCE            ADDRES                  PROTOCOL        PARAM            RESPONSE/STATUS CODE
GetImageCleaned     /getcleanedimage        POST            ImageName        200 OK
                                                            Base64 image     Base64 cleaned image
                                                                             String text

GetString           /getstring              POST            ImageName        200 OK
                                                                             String text
"""

import base64
import numpy as np
import tensorflow as tf
import os
import cv2
import matplotlib.pyplot as plt
import pytesseract
from pymongo import MongoClient

from flask import Flask, jsonify, request
from flask_restful import Api, Resource


app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://db:27017')
db = client.OCRChallenge  # Db name
imageDB = db['ImageInfos']  # table name

# Method responsible to encode the cleaned image


def encodeImage():
    with open('cleaned_image.png', 'rb') as img_file:
        cleaned_image = base64.b64encode(img_file.read())

    return cleaned_image


# Method responsible to get de string base64, decode in an image and save it


def decodeImage(encoded_image):
    with open('dirty_image.png', 'wb') as file_to_save:
        decoded_image = base64.decodebytes(encoded_image)
        file_to_save.write(decoded_image)

# Method responsible for loading the trained models and weights


def loadModels():
    with open(os.path.join('models/', 'cnn_model.json'), 'r') as f:
        model_json = f.read()

        model = tf.keras.models.model_from_json(model_json)
        model.load_weights(os.path.join('models/', 'cnn_model.h5'))

    return model

# Method responsible to read the dirty image and process it to be predicted


def processingImage():
    path = 'dirty_image.png'
    img = cv2.imread(path)
    img = np.asarray(img, dtype="float32")
    img = cv2.resize(img, (540, 420))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img = img/255.0
    img = np.reshape(img, (420, 540, 1))
    img = np.expand_dims(img, axis=0)

    return img

# Method responsible to recieve the preticted image and save it as cleaned_image


def savePredictedImg(predicted_image):
    plt.figure(figsize=(15, 25))
    plt.subplot(4, 2, +1)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(predicted_image[0][:, :, 0], cmap='gray')
    plt.savefig('cleaned_image.png')

# Method responsible to read the cleaned image and get its string


def readImage():

    config_tesseract = '--psm 6'
    imagem = cv2.imread('cleaned_image.png')
    text = pytesseract.image_to_string(
        imagem, lang='eng', config=config_tesseract)

    return text


class GetImageCleaned(Resource):
    def post(self):

        # Getting posted data by the user
        postedData = request.get_json()

        # Get the data
        image_name = postedData['name']
        encoded_dirty_image = postedData['image']
        encoded_dirty_image = encoded_dirty_image.encode('utf-8')

        # Decoding and saving the image
        decodeImage(encoded_dirty_image)

        # Loading model and weight
        model = loadModels()

        # First processing the image and then predicting it
        predicted_image = model.predict(processingImage())

        # Recieving a nparray and converting into a image
        savePredictedImg(predicted_image)

        # Getting the image string
        image_string = readImage()

        # Encoding the cleaned image
        encoded_cleaned_image = encodeImage()

        imageDB.insert_one({
            'name': image_name,
            'dirty': encoded_dirty_image,
            'cleaned': encoded_cleaned_image,
            'texto': image_string,
        })

        retJson = {
            'string': image_string,
            'base64': encoded_cleaned_image.decode('utf-8'),
            'status': 200,
        }

        return jsonify(retJson)


class GetString(Resource):
    def post(self):

        # Getting posted data by the user
        postedData = request.get_json()

        # Get the data
        image_name = postedData['name']

        # Searching the string by the image name
        sentence = imageDB.find({'name': image_name})[0]['texto']

        retJson = {
            'status': 200,
            'string': sentence

        }
        return jsonify(retJson)


api.add_resource(GetImageCleaned, '/getimagecleaned')
api.add_resource(GetString, '/getstring')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
