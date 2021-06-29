import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
# python will look at resources packages to find the file
from resources.user import UserRegister
# "item" just a name of the file
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
# database is going to live in our root folder of our project
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL_NEW', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth

api.add_resource(Store, '/store/<string:name>')
#api.add_resource(Student, '/student/<string:name>') # http://127.0.0.1:5000/student/Rolf
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
#this means if do request to this url the flask is going to call class UserRegester
#and call overriden post method
api.add_resource(UserRegister, '/register')

#
#if we have print statement python will run this stament during import
#we could have statements that we may want to avoid to be run during import
#like app.run(port=5000, debug=True)
#to avoid this we need add iff __name__ == '__main__':
#print("Hello")
#when you run a python file (for example app.py) python will assign a special name to the file we run
#and the file name is always __main__
#so only the file you run is __main__. if it is not main then that means we have imported this file from elsewhere
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
