from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint
from v1.config.db_config import mongo

donorapi = Blueprint('donorapi', __name__)


@donorapi.route('/add', methods=['POST'])
def add_donor():
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
        result = mongo.db.donor.insert_one(
            {
                'mobile': _mobile,
                'name': _name,
                'email': _email,
                'pwd': _hashed_password
            }
        )
        resp = jsonify({'id':str(result.inserted_id)})
        resp.status_code = 200
        return resp
    else:
        return not_found()


@donorapi.route('/list')
def donors():
    donor_list = mongo.db.donor.find()
    resp = dumps(donor_list)
    return resp


@donorapi.route('/', methods=['GET'])
def get_donor_with_mobile():
    mobile = request.args.get('mobile')
    donor = mongo.db.donor.find_one({'mobile': int(mobile)})
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
    _name = _json['name']
    _id = _json['_id']
    _email = _json['email']
    _password = _json['pwd']
    _mobile = _json['mobile']
    # validate the received values
    if _name and _mobile and request.method == 'PUT':
        # do not save password as a plain text
        _hashed_password = generate_password_hash(_password)
        # save edits
        mongo.db.donor.update_one(
            {
                '_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)
            },
            {
                '$set':
                    {
                        'name': _name,
                        'email': _email,
                        'pwd': _hashed_password
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
