from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint
from pymongo.errors import DuplicateKeyError

from v1 import not_found
from v1.config.db_config import mongo

volunteerapi = Blueprint('volunteerapi', __name__)


@volunteerapi.route('/add', methods=['POST'])
def add_volunteer():
    _json = request.json
    _fname = _json['fname']
    _lname = _json['lname']
    _email = _json['email']
    _address = _json['address']
    _latitude = _json['lat']
    _longitude = _json['lng']
    _mobile = _json['mobile']
    _paddr = _json['paddress']
    _plat = _json['plat']
    _plng = _json['plng']
    _prefmode = _json['prefmode']
    _ver = _json['verified']
    # validate the received values
    if _fname and _mobile and _email and request.method == 'POST':
        # do not save password as a plain text
        _hashed_password = generate_password_hash(_password)
        # save details
        try:
            result = mongo.db.volunteer.insert_one(
                {
                    'mobile': _mobile,
                    'first_name': _fname,
                    'last_name': _lname,
                    'address': _address,
                    'latitude': _latitude,
                    'longitude': _longitude,
                    'email': _email,
                    'pickup_address': _paddr,
                    'pickup_addr_latitude': _plat,
                    'pickup_addr_longitude': _plng,
                    'pref_mode_of_contact': _prefmode,
                    'verified': _ver,
                }
            )
            resp = jsonify({'id': str(result.inserted_id)})
            resp.status_code = 200
        except DuplicateKeyError:
            resp = jsonify(' Volunteer {} already exists'.format(_fname))
            resp.status_code = 409
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
    volunteer = mongo.db.volunteer.find_one({'mobile': int(mobile)})
    resp = dumps(volunteer)
    return resp



@volunteerapi.route('/update', methods=['PUT'])
def update_volunteer():
    _json = request.json
    _fname = _json['fname']
    _lname = _json['lname']
    _email = _json['email']
    _address = _json['address']
    _latitude = _json['lat']
    _longitude = _json['lng']
    _mobile = _json['mobile']
    _prefmode = _json['prefmode']
    _ver = _json['verified']
    # validate the received values
    if _mobile and request.method == 'PUT':
        # do not save password as a plain text
        _hashed_password = generate_password_hash(_password)
        # save edits
        mongo.db.volunteer.update_one(
            {
                '_mobile': _mobile
            },
            {
                '$set':
                    {
                        'mobile': _mobile,
                        'first_name': _fname,
                        'last_name': _lname,
                        'address': _address,
                        'latitude': _latitude,
                        'longitude': _longitude,
                        'email': _email,
                        'pref_mode_of_contact': _prefmode,
                        'verified': _ver,
                    }
            }
        )
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
