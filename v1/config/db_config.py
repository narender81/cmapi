# from app import app
# from flaskext.mysql import MySQL
#
# mysql = MySQL()
#
# # MySQL configurations
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = ''
# app.config['MYSQL_DATABASE_DB'] = 'roytuts'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# mysql.init_app(app)

from flask_pymongo import PyMongo
from v1 import app
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from pymongo import MongoClient, ASCENDING, DESCENDING


try:
    app.secret_key = "secret key"
    app.config["MONGO_DBNAME"] = "test"
    app.config["MONGO_URI"] = "mongodb://192.168.0.11:27017/test"
    mongo = PyMongo(app)
except ConnectionFailure as connectError:
    print("Connection Failure to MongoDB: {0}".format(connectError))
except ServerSelectionTimeoutError as timeoutErr:
    print("Unable to connect Timeout: {0}".format(timeoutErr))
except Exception as err:
    print ("Error: {0}".format(err.args))


def create_or_update_db():
    resp=mongo.db.donor.ensure_index([("mobile", ASCENDING), ("email", DESCENDING)], unique=True)
    print('donor index {}'.format(resp))
    resp=mongo.db.volunteer.create_index([("mobile", ASCENDING), ("email", DESCENDING)], unique=True)
    print('Volunteer index {}'.format(resp))
    resp=mongo.db.items.create_index([("name", ASCENDING)], unique=True)
    print('Items index {}'.format(resp))