#import sqlite3
from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

#CRUD API - create read update delete
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
       type=float,
       required=True,
       help="This field cannot be left blank!")
    parser.add_argument('store_id',
       type=int,
       required=True,
       help="Every item needs a store id!")

    #we are going to authenticate before we are calling "get" method
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'item not found'}, 404

    #how to get json payload -> request.get_json
    #get_json(force=True) -> means you do not need the content-type error.
    #it will look at the content and it will format even if content-type is not set
    #get_json(selecbt=True) -> it does not give an error it's just returns none.
    def post(self, name):
        # we can use either self. or Item. It doesn't really matter
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 400 #bad request

        #data = request.get_json()
        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        # we gonna try to insert and if we fail for any reason
        # we're just going to return a message saying an error occured.
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500 #internal server error
        #it can not return objects. it can only return dictionaries
        return item.json(), 201 #created

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        #if item exists
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "DELETE FROM items WHERE name=?"
        # cursor.execute(query, (name,))
        #
        # connection.commit()
        # connection.close()
        #
        # return {'message': 'Item deleted'}

    def put(self, name):
        # access to a class local variable
        data = Item.parser.parse_args()#request.get_json()

        item = ItemModel.find_by_name(name)
        #updated_item = ItemModel(name, data['price'])

        if item is None:
            item = ItemModel(name, **data)
          # try:
          #     updated_item.insert()
          # except:
          #     return {"message": "An error occurred inserting the item."}, 500
        else:
            item.price = data['price']
          # try:
          #     updated_item.update()
          # except:
          #     return {"message": "An error occurred updating the item."}, 500
        item.save_to_db()

        return item.json();

# classes should be separated by two lines and methods by single line by convention
class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]} # list comprehension (more pythonic - recommended)
        # you should use map only if you work with people that programming in other languages
        #return {'item': list(map(lambda x: x.json(), ItemModel.query.all()))} # by using lambda (it will apply finction in each element of this list)
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM items"
        # result = cursor.execute(query)
        # items = []
        # for row in result:
        #     items.append({'name': row[0], 'price': row[1]})
        #
        # connection.close()
        #
        # return {'items': items}
