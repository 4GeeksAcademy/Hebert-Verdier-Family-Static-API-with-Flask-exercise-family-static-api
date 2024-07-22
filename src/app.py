"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for #type: ignore
from flask_cors import CORS #type: ignore
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

jackson_family.add_member({
    "first_name": "John",
    "age": 33,
    "lucky_numbers": [7, 13, 22]
})
jackson_family.add_member({
    "first_name": "Jane",
    "age": 35,
    "lucky_numbers": [10, 14, 3]
})
jackson_family.add_member({
    "first_name": "Jimmy",
    "age": 5,
    "lucky_numbers": [1]
})

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# ENDPOINTS
# GET MEMBERS
@app.route('/members', methods=['GET'])
def handle_hello():
    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()

    return jsonify(members), 200
    
# GET ONE MEMBER
@app.route('/member/<int:id>', methods=['GET'])
def get_one_member(id):
    member = jackson_family.get_member(id)
    if member:
            return jsonify(member), 200
    else:
        return jsonify({'error':'member not found'}), 404
    
# POST MEMBER
@app.route('/member', methods=['POST'])
def add_member():
    member_data = request.get_json()
    
    if not isinstance(member_data['age'], int):
         return({'error':'"age" must be a integer value'}), 400
    if not isinstance(member_data['first_name'], str):
         return({'error':'"first_name" must be a string'}), 400
    if not isinstance(member_data['lucky_numbers'], list):
         return({'error':'"lucky_numbers" must be a list'}), 400
    if not all (isinstance(num, int) for num in member_data['lucky_numbers']):
        return({'error':'all "lucky_numbers" must be integers values'}), 400

    new_member = jackson_family.add_member(member_data)
    return jsonify(new_member), 200

# PUT MEMBER
@app.route('/member/<int:id>', methods=['PUT'])
def update_member(id):
    member = jackson_family.get_member(id)
    if not member:
         return jsonify({'error':'member not found'}), 404
    
    member_data = request.get_json()   
    if not isinstance(member_data['age'], int):
         return({'error':'"age" must be a integer value'}), 400
    if not isinstance(member_data['first_name'], str):
         return({'error':'"first_name" must be a string'}), 400
    if not isinstance(member['lucky_numbers'], list):
         return({'error':'"lucky_numbers" must be a list'})
    if not all (isinstance(num, int) for num in member_data['lucky_numbers']):
        return({'error':'all "lucky_numbers" must be integers values'}), 400

    jackson_family.update_member(id, member_data)
    return jsonify('member updated'), 200

# DELETE MEMBER
@app.route('/member/<int:id>', methods=['DELETE'])
def delte_one_member(id):
    member = jackson_family.get_member(id)
    if not member:
         return jsonify({'error':'member not found'}), 404
    
    deleted_member = jackson_family.delete_member(id)
    return jsonify(deleted_member), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)