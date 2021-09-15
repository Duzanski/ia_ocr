

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
