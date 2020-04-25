from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint
from v1.config.db_config import mongo
from pymongo.errors import DuplicateKeyError

donorapi = Blueprint('donorapi', __name__)


@donorapi.route('/add', methods=['POST'])
def add_donor():

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
        # _hashed_password = generate_password_hash(_password)
        # save details
        try:
            result = mongo.db.donor.insert_one(
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
            resp = jsonify({'id':str(result.inserted_id)})
            resp.status_code = 200
        except DuplicateKeyError:
            resp = jsonify(' Donor {} already exists'.format(_fname))
            resp.status_code = 409
        return resp

    else:
        return not_found()


@donorapi.route('/list')
def donors():
    donor_list = mongo.db.donor.find()
    resp = dumps(donor_list)
    return resp

@donorapi.route('/', methods=['GET'])
def get_donor_using_mobile_or_email():
    mobile = request.args.get('mobile', None)
    email = request.args.get('email', None)
    if mobile:
        donor = mongo.db.donor.find_one({'mobile': int(mobile)})
    elif email:
        donor = mongo.db.donor.find_one({'email': email})
    resp = dumps(donor)
    return resp

@donorapi.route('/<id>')
def get_donor_info(id):
    donor = mongo.db.donor.find_one({'_id': ObjectId(id)})
    resp = dumps(donor)
    return resp


@donorapi.route('/update', methods=['PUT'])
def update_donor():
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
    if _fname and _mobile and request.method == 'PUT':
        # do not save password as a plain text
        _hashed_password = generate_password_hash(_password)
        # save edits
        mongo.db.donor.update_one(
            {
                'mobile': _mobile
            },
            {
                '$set':
                    {
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
            }
        )
        resp = jsonify('Donor updated successfully!')
        resp.status_code = 200
        return resp
    else:
        return not_found()


@donorapi.route('/delete/<mobile>', methods=['DELETE'])
def delete_donor(mobile):
    mongo.db.donor.delete_one({'_mobile': mobile})
    resp = jsonify('Donor deleted successfully!')
    resp.status_code = 200
    return resp


@donorapi.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp
