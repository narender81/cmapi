from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash

from v1 import Status, not_found
from v1.config.db_config import mongo

donationapi = Blueprint('donationapi', __name__)


def donation_details(donation):
    donor = mongo.db.donor.find_one({'_id': ObjectId(donation['donorid'])})
    items_donated = []
    for item_id in donation['items']:
        item = mongo.db.items.find_one({'_id': ObjectId(item_id)})
        items_donated.append(item['name'])
    don_det = {
        '_id': donation['_id'],
        'donor_name': donor['name'],
        'items': items_donated,
        'status': donation['status']
    }
    return don_det


@donationapi.route('/add', methods=['POST'])
def add_donation():
    _json = request.json
    _donor = _json['donorid']
    _items = _json['items']

    # validate the received values
    if _donor and len(_items) and request.method == 'POST':
        # save details
        id = mongo.db.donations.insert({'donorid': _donor,
                                        'items': _items,
                                        'status': Status.READY})
        resp = jsonify('Donation added successfully!')
        resp.status_code = 200
        return resp
    else:
        return not_found()


@donationapi.route('/list')
def donations():
    donations_list = mongo.db.donations.find()
    donations = []
    for donation in donations_list:
        donations.append(donation_details(donation))
    resp = dumps(donations)
    return resp


@donationapi.route('/<id>')
def get_donation(id):
    donation = mongo.db.donations.find_one(({'_id': ObjectId(id)}))
    resp = dumps(donation)
    return resp

@donationapi.route('/details/<id>')
def get_donation_info(id):
    donation = mongo.db.donations.find_one(({'_id': ObjectId(id)}))
    resp = dumps(donation_details(donation))
    return resp


@donationapi.route('/update', methods=['PUT'])
def update_donation():
    _json = request.json
    _id = _json['donation_id']
    _donor = _json['donorid']
    _items = _json['items']
    _status = _json['status']

    # validate the received values
    if _id and _donor and len(_items) and request.method == 'PUT':
        # save edits
        mongo.db.donations.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
                                 {'$set': {'items': _items,
                                           'status': _status
                                           }
                                  }
        )
        resp = jsonify('Donation updated successfully!')
        resp.status_code = 200
        return resp
    else:
        return not_found()

@donationapi.route('/delete/<id>', methods=['DELETE'])
def delete_donation(id):
    mongo.db.donations.delete_one({'_id': ObjectId(id)})
    resp = jsonify('Donation deleted successfully!')
    resp.status_code = 200
    return resp

