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
