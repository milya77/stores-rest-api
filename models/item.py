#import sqlite3
from db import db

class ItemModel(db.Model):
    __tablename__="items"
    # id param will also be passed in because no is parameter used under __init__ method
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    #creates foreigh key
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    # it will create join internally
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        # the second name is an argument from method find_by_name
        # because of this is class method we don't have to use ItemModel we can use cls
        #return ItemModel.query.filter_by(name=name) # SELECT * FROM items WHERE name=name
        return cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name=name LIMIT 1
        #return ItemModel.query.filter_by(name=name).filter_by(id=1)
        #return ItemModel.query.filter_by(name=name, id=1) # if we want to filter multiple things it is always better to do this.
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * from items WHERE name=?"
        # result = cursor.execute(query, (name,))
        # # we have to retrieve only single row or no rows
        # row = result.fetchone()
        # connection.close()
        #
        # if row:
        #     #return cls(row[0], row[1])
        #     #exactly the same as a row above
        #     # use argument unpacking
        #     return cls(*row)

    # upserting
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "INSERT INTO items VALUES (?, ?)"
        # cursor.execute(query, (self.name, self.price))
        #
        # connection.commit()
        # connection.close()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "UPDATE items SET price=? WHERE name=?"
        # cursor.execute(query, (self.price, self.name))
        #
        # connection.commit()
        # connection.close()
