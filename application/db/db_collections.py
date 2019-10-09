import datetime
from application.db.db_constants import DEFAULT_PREFERENCE_VALUE
from flask_mongoengine import MongoEngine

db = MongoEngine()


class User(db.Document):
    user_id = db.IntField(required = True)
    first_name = db.StringField(max_length = 30)
    last_name = db.StringField(max_length = 30)
    is_owner = db.BooleanField(default = False)
    credit = db.IntField(default = 0)
    email = db.StringField(required = True)
    preference = db.DictField(default = DEFAULT_PREFERENCE_VALUE)


class AttendanceHistory(db.Document):
    user_id = db.IntField(required = True)
    event_id = db.IntField(required = True)


class Event(db.Document):
    user_id = db.IntField(required = True)
    event_id = db.IntField(required = True)
    event_name = db.StringField(max_length = 100, required = True)
    host_name = db.StringField(max_length = 100, required = True)
    date = db.DateTimeField(default = datetime.datetime.utcnow)
    location = db.StringField(required = True)
    tags = db.ListField(db.StringField(max_length=30))
    food = db.DictField(default={"foodName": db.StringField(max_length=30),
                                 "foodType": db.ListField(db.StringField(max_length=30)),
                                 "foodImages": db.ListField(db.StringField())})
