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

jackson_family.add_member({
    "first_name": "John",
    "last_name": "Jackson",
    "age": 31,
    "lucky_numbers": [7, 13, 22]
}),
jackson_family.add_member({
    "first_name": "Jane",
    "last_name": "Jackson",
    "age": 35,
    "lucky_numbers": [10, 14, 3]
}),
jackson_family.add_member({
    "first_name": "Jimmy",
    "last_name": "Jackson",
    "age": 5,
    "lucky_numbers": [1]
})

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_family_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200


@app.route('/member/<int:member_id>', methods=['GET'])
def get_single_family_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"message": "Member not found"}), 404


@app.route('/member', methods = ['POST'])
def create_new_member():
    member =request.json
    jackson_family.add_member(member)
    return f"You successfully added {member['first_name']} {member['last_name']} to the list" , 200

@app.route("/member/<int:member_id>", methods=["DELETE"])
def delete_member(member_id):
    if jackson_family.delete_member(member_id):
        return f"You successfully deleted member with ID {member_id} from the list", 200
    else:
        return f"Member with ID {member_id} not found in the list", 404

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
