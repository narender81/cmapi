from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint

from v1 import not_found
from v1.config.db_config import mongo

volunteerapi = Blueprint('volunteerapi', __name__)


@volunteerapi.route('/add', methods=['POST'])
def add_volunteer():
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _password = _json['pwd']
    _mobile = _json['mobile']
    # validate the received values
    if _name and _email and _password and request.method == 'POST':
        # do not save password as a plain text
        _hashed_password = generate_password_hash(_password)
        # save details
        id = mongo.db.volunteer.insert({'mobile': _mobile, 'name': _name, 'email': _email, 'pwd': _hashed_password})
        resp = jsonify('Volunteer added successfully!')
        resp.status_code = 200
        return resp
    else:
        return not_found()


@volunteerapi.route('/list')
def volunteers():
    donor_list = mongo.db.volunteer.find()
    resp = dumps(donor_list)
    return resp


@volunteerapi.route('/<mobile>')
def get_volunteer_info(mobile):
    vol = volunteer = mongo.db.volunteer.find_one({'mobile': int(mobile)})
    if vol:
        resp = dumps(volunteer)
        return resp
    return not_found


@volunteerapi.route('/update', methods=['PUT'])
def update_volunteer():
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _password = _json['pwd']
    _mobile = _json['mobile']
    # validate the received values
    if _name and _mobile and request.method == 'PUT':
        # do not save password as a plain text
        _hashed_password = generate_password_hash(_password)
        # save edits
        mongo.db.volunteer.update_one({'_mobile': _mobile},
                                 {'$set': {'name': _name, 'email': _email, 'pwd': _hashed_password}})
        resp = jsonify('volunteer updated successfully!')
        resp.status_code = 200
        return resp
    else:
        return not_found()


@volunteerapi.route('/delete/<mobile>', methods=['DELETE'])
def delete_volunteer(mobile):
    vol = mongo.db.volunteer.delete_one({'_mobile': mobile})
    if vol:
        resp = jsonify('volunteer deleted successfully!')
        resp.status_code = 200
        return resp
    else:
        return not_found()
