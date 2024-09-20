"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)
jackson_family = FamilyStructure("Jackson") # create the jackson family object


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/mebmers', methods=['GET'])
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET', 'POST'])
def handle_hello():
    response_body = {}
    if request.method == 'GET':
        members = jackson_family.get_all_members()
        response_body["mensage"] = "world"
        response_body["result"] = members
        return jsonify(response_body), 200
    if request.method == 'POST':
        data = request.json
        jackson_family.add_member(data)
        response_body["mensage"] = "quiero agregar un member",
        response_body["result"] = jackson_family.get_all_members() 
        return response_body, 200


@app.route('/members/<int:member_id>', method=['GET', 'PUT', 'DELETE'])
def member (member_id):
    response_body = {}
    if request.method == 'GET':
       jackson_family.get_member(member_id)
       response_body["mensage"] = f"mensaje desde el GET con int:member_id: {member_id}"
       response_body["result"] = member
       return response_body, 200
    if request.method == 'PUT':
       pass
       response_body["mensage"] = f"mensaje desde el PUT con int:member_id: {member_id}"
       response_body["result"] = {}
       return response_body, 200
    if request.method == 'DELETE':
       pass
       response_body["mensage"] = f"mensaje desde el DELETE con int:member_id: {member_id}"
       response_body["result"] = {}
       return response_body, 200


# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
