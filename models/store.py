#import sqlite3
from db import db

class StoreModel(db.Model):
    __tablename__="stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    #back reference: it allows the store to see
    #which items with a store id equals to it's own id
    #many-to-one relationship
    #if we have a lot of items it can be really expensive operation
    #that is why we need lazy='dynamic'
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        #return {'name': self.name, 'items': [item.json() for item in self.items]}
        # which means untill we call json we are not locking into the table
        # (works together with lazy='dynamic')
        # so we have to consider what is more important speed of creation of a store
        # and speed of calling the json method
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
