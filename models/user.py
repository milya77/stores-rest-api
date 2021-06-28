import sqlite3
from db import db

#if we have print statement python will run this stament during import
#we could have statements that we may want to avoid to be run during import
#like app.run(port=5000, debug=True)
#to avoid this we need add iff __name__ == '__main__':
#print("Hello")
#this user class must not be the same as the resource that we are going to sign up.
class UserModel(db.Model):
    __tablename__='users'
    #the properties that should be saved into db should much the ones under init method
    #othervise it will give us an error
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80)) #80 limit the size of the user name
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        # id is a python keyword. that is why we have to use _id name
        # self.id = _id # id will be assigned automatically by sql engine
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM users WHERE username=?"
        # # remember the parameters have to be in the form of tuple. that is why comma at the end needed.
        # result = cursor.execute(query, (username,))
        # row = result.fetchone()
        # #if row is not None:
        # if row:
        #     #user = cls(row[0], row[1], row[2])
        #     user = cls(*row)
        # else:
        #     user = None
        #
        # connection.close()
        # return user

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
        # if I run from jsvltr_sect5 as follows: D:\python\jsvltr_sect5>python code/app.py
        # the python is going to look for the files in the dir from which the program had run.
        # if I go to the code folder: cd code/ and run: python app.py we are going to have problem because there is no
        # data.db file in the code folder
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM users WHERE id=?"
        # # remember the parameters have to be in the form of tuple. that is why comma at the end needed.
        # result = cursor.execute(query, (_id,))
        # row = result.fetchone()
        # #if row is not None:
        # if row:
        #     #user = cls(row[0], row[1], row[2])
        #     user = cls(*row)
        # else:
        #     user = None
        #
        # connection.close()
        # return user
