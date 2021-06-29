from app import app
from db import db

db.init_app(app)

# SQLAlchemy will create tables unless they exist already
# Flask decorator. It is going to run this method before
# the first request to this app
# it does create tables that it sees. so it does go through the imports
@app.before_first_request
def create_tables():
    db.create_all()
