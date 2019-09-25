import datetime
from mongoengine import Document, fields
from db.db_constants import DEFAULT_PREFERENCE_VALUE


class User(Document):
    user_id = fields.IntField(required = True)
    first_name = fields.StringField(max_length = 30)
    last_name = fields.StringField(max_length = 30)
    is_owner = fields.BooleanField(default = False)
    credit = fields.IntField(default = 0)
    email = fields.StringField(required = True)
    preference = fields.DictField(default = DEFAULT_PREFERENCE_VALUE)


class AttendanceHistory(Document):
    user_id = fields.IntField(required = True)
    event_id = fields.IntField(required = True)


class Event(Document):
    user_id = fields.IntField(required = True)
    event_id = fields.IntField(required = True)
    event_name = fields.StringField(max_length = 100, required = True)
    host_name = fields.StringField(max_length = 100, required = True)
    date = fields.DateTimeField(default = datetime.datetime.utcnow)
    location = fields.StringField(required = True)
    # food = fields.DictField(default={"foodName": fields.StringField(max_length=30),
    #                                  "foodTags": fields.ListField(fields.StringField(max_length=30)),
    #                                  "foodType": fields.ListField(fields.StringField(max_length=30)),
    #                                  "foodImages": fields.ListField(fields.ImageField())})
