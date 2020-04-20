from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash

from v1 import not_found
from v1.config.db_config import mongo

itemapi = Blueprint('itemapi', __name__)


@itemapi.route('/add', methods=['POST'])
def add_volunteer():
    _json = request.json
    _name = _json['name']
    _desc = _json['desc']
    # validate the received values
    if _name and request.method == 'POST':
        # save details
        id = mongo.db.items.insert({'name': _name, 'desc': _desc})
        resp = jsonify('Item added successfully!')
        resp.status_code = 200
        return resp
    else:
        return not_found()


@itemapi.route('/list')
def items():
    items_list = mongo.db.items.find()
    resp = dumps(items_list)
    return resp


@itemapi.route('/<id>')
def get_item_info(id):
    item = mongo.db.items.find_one({'_id': ObjectId(id)})
    resp = dumps(item)
    return resp


@itemapi.route('/update', methods=['PUT'])
def update_item():
    _json = request.json
    _name = _json['name']
    _id = _json['_id']
    _desc = _json['desc']

    # validate the received values
    if _name and request.method == 'PUT':
        # save edits
        mongo.db.items.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
                                      {'$set': {'name': _name}})
        resp = jsonify('Item updated successfully!')
        resp.status_code = 200
        return resp
    else:
        return not_found()


@itemapi.route('/delete/<id>', methods=['DELETE'])
def delete_item(id):
    item = mongo.db.items.delete_one({'_id': ObjectId(id)})
    if item.deleted_count:
        resp = jsonify('Item deleted successfully!')
        resp.status_code = 200
        return resp
    else:
        return not_found()
