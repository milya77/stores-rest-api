#for some people that using python 2.7 it is usually a good idea
#to not compare strings directly with ==. because in different systems
#in different python versions things may come more complicated
#espessially when you are bringing a subject called "string encoding"
# fortunately flask comes with a nice library called workzeug.
# and it has very nice safe_str_cmp function to safely compare strings.
from werkzeug.security import safe_str_cmp
from models.user import UserModel

def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
