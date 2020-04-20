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

