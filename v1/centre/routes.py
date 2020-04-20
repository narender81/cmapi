from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash

from v1 import not_found
from v1.config.db_config import mongo

centreapi = Blueprint('centreapi', __name__)


@centreapi.route('/add', methods=['POST'])
def add_centre():
    _json = request.json
    _address = _json['address']
    _latitude = _json['latitude']
    _longitude = _json['longitude']

    # validate the received values
    if _address and _latitude and _longitude and request.method == 'POST':
        # save details
        result = mongo.db.centre.insert_one(
                    {
                        'address': _address,
                        'latitude': _latitude,
                        'longitude': _longitude
                     }
        )
        resp = jsonify({'id': str(result.inserted_id)})
        resp.status_code = 200
        return resp
    else:
        return not_found()


@centreapi.route('/list')
def collection_centres_list():
    centres_list = mongo.db.centre.find()
    resp = dumps(centres_list)
    return resp


@centreapi.route('/<id>')
def get_collection_centre_info(id):
    centre = mongo.db.centre.find_one({'_id': ObjectId(id)})
    resp = dumps(centre)
    return resp


@centreapi.route('/update', methods=['PUT'])
def update_item():
    _json = request.json
    _address = _json['address']
    _id = _json['_id']
    _latitude = _json['latitude']
    _longitude = _json['longitude']

    # validate the received values
    if _address and request.method == 'PUT':
        # save edits
        mongo.db.items.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
                                      {'$set': {'address': _address,
                                                'latitude': _latitude,
                                                'longitude': _longitude
                                                }})
        resp = jsonify('Centre updated successfully!')
        resp.status_code = 200
        return resp
    else:
        return not_found()


@centreapi.route('/delete/<id>', methods=['DELETE'])
def delete_collection_centre(id):
    item = mongo.db.centre.delete_one({'_id': ObjectId(id)})
    if item.deleted_count:
        resp = jsonify('Centre deleted successfully!')
        resp.status_code = 200
        return resp
    else:
        return not_found()

