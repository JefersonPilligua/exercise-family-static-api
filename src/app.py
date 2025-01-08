"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

#print(jackson_family);
#print(jackson_family.serialize())

new_member = jackson_family.add_member({
    'name': 'Jhon',
    'age': 33,
    'lucky_numbers': [7,13,22]
})

new_member = jackson_family.add_member({
    'name': 'Jane',
    'age': 35,
    'lucky_numbers': [10,14,3]
})

new_member = jackson_family.add_member({
    'name': 'Jimmy',
    'age': 35,
    'lucky_numbers': [1]
})

#print(new_member)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "family": members
    }


    return jsonify(response_body), 200

@app.route('/members', methods=['POST'])
def handle_add_members():
    member = request.get_json()

    if member is None:
        return 'Error', 400
    if member ['name'] is None:
        return 'Error name not empty', 400
    if member is ['age'] is None:
        return 'Error age not empty', 400
    if member is ['lucky_numbers'] is None:
        return 'Error lucky numbers not empty', 400
    
    new_member = jackson_family.add_member(member)
    return jsonify(new_member), 200

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    deleted_member = jackson_family.delete_member(id)
    if deleted_member is None:
        return 'Error member not found', 400
    return jsonify(deleted_member), 200

@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    member = jackson_family.get_member(id)
    if member is None:
        return 'Error member not found', 400
    return jsonify(member), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
