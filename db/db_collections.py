import datetime
from mongoengine import Document, fields


class User(Document):
    id = fields.StringField(required=True)
    first_name = fields.StringField(max_length=30)
    last_name = fields.StringField(max_length=30)
    is_owner = fields.BooleanField(default=False)
    credit = fields.IntField(default=0)
    email = fields.StringField(required=True)
    preference = fields.DictField(default={"piazza": 0, "breakfast": 0, "burger": 0, "chinese": 0, "mexican": 0,
                                           "korean": 0, "steakHouses": 0, "thai": 0, "seafood": 0, "japanese": 0,
                                           "italian": 0, "vietnamese": 0, "sandwiches": 0, "vegetarian": 0,
                                           "sushiBars": 0, "american": 0, "dessert": 0})


class AttendanceHistory(Document):
    user_id = fields.StringField(required=True)
    event_id = fields.StringField(required=True)


class Event(Document):
    user_id = fields.StringField(required=True)
    event_id = fields.StringField(required=True)
    name = fields.StringField(max_length=100, required=True)
    date = fields.DateTimeField(default=datetime.datetime.utcnow)
    location = fields.StringField(required=True)
    food = fields.DictField(default={"foodName": fields.StringField(max_length=30),
                                     "foodTags": fields.ListField(fields.StringField(max_length=30)),
                                     "foodType": fields.ListField(fields.StringField(max_length=30)),
                                     "foodImages": fields.ListField(fields.ImageField())})
    endorsement = fields.IntField(default=0)
