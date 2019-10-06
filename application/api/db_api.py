from flask_mongoengine import MongoEngine
from application.db.db_collections import User, Event, AttendanceHistory
from application.db.db_constants import DEFAULT_PREFERENCE_VALUE
from datetime import datetime

mongo_engine = None


def init_app(app):
    global mongo_engine
    mongo_engine = MongoEngine()
    mongo_engine.init_app(app)

# -- user operations starts here --


def create_user(first_name: str, last_name: str, is_owner: bool, credit: int,
                email: str, preference: dict = DEFAULT_PREFERENCE_VALUE):
    """add a user to the database
      @:param first_name
      @:param last_name
      @:param is_owner: is this user a owner of restaurant or food truck
      @:param credit: user's credit score, initially should be zero
      @:param email
      @:param preference: user's preference over certain types of food, 1 means interested, 0 means not. Default to nothing"""
    new_user = User(user_id = User.objects().count() + 1, first_name = first_name,
                    last_name = last_name, is_owner = is_owner, credit = credit,
                    email = email, preference = preference).save()
    return new_user


def search_user(user_id: int = -1, first_name: str = "", last_name: str = "", email: str = ""):
    """search user by either 1) user id 2) first name, last name, and email, return a single user """
    if user_id == -1 and (first_name == "" or last_name == "" or email == ""):
        print("Search Criteria not met. You can search by either 1) user id "
              "2) first name + last name + email")
        return None
    if user_id != -1:
        user = User.objects(user_id = user_id).first()
    else:
        user = User.objects(first_name = first_name, last_name = last_name, email = email).first()
    return user


def delete_user(user_id: int = -1, first_name: str = "", last_name: str = "", email: str = ""):
    """delete user by either 1) user id 2) first name, last name, and email """
    user_found = search_user(user_id, first_name, last_name, email)
    if user_found is None:
        print("User not found")
        return False
    user_found.delete()
    return True


def edit_user(user_id: int = -1, **fields):
    """edit user info by user_id
        @:param fields: key-value pair indicates which field to change"""
    user_found = search_user(user_id)
    if user_found is None:
        print("User not found")
        return None

    # update fields
    for key, value in fields.items():
        user_found[key] = value
    user_found.save()

    return user_found

# -- events operations starts here --


def create_event(user_id: int = -1, event_name: str = "", host_name: str = "",
                 date_time: datetime = datetime.now(), location: str = "", food: dict = {}):
    """create an event in the database
        @:param user_id: user creating the event (owner or first responder)
        @:param event_name
        @:param host_name
        @:param date_time: the time of the event
        @:param location: the location of the event"""
    if user_id == -1:
        print("There must be a user creating the event")
        return None
    elif event_name == "":
        print("Event name can't be empty")
        return None
    elif location == "":
        print("Location can't be empty")
        return None
    new_event = Event(user_id = user_id, event_id = Event.objects().count() + 1, event_name = event_name,
                      host_name = host_name, date = date_time, location = location, food = food).save()
    return new_event


def search_events(**fields):
    """search events that match the condition, return a list of events
    @:returns list: a list of events ranging from 0 to all events in the database"""
    events = Event.objects(**fields).all()
    return events


def edit_event(event_id: int = -1, **fields):
    """edit a single event based on event id"""
    event = search_events(event_id = event_id).first()
    if event is None:
        print("No event found")
        return None

    # update fields
    for key, value in fields.items():
        event[key] = value
    event.save()

    return event


def delete_events(event_id: int = -1):
    """delete a single event based on event id"""
    event = search_events(event_id = event_id).first()
    if event is None:
        print("No event found")
        return False
    event.delete()
    return True


# -- attendence operation starts here --
def confirm_attendance(user_id: int = -1, event_id: int = -1):
    """register the user for a specific event"""
    if user_id == -1:
        print("User Id cannot be empty")
        return None
    elif event_id == -1:
        print("")
        return None
    attendance = AttendanceHistory(user_id = user_id, event_id = event_id).save()

    return attendance


def cancel_attendance(user_id: int = -1, event_id: int = -1):
    """remove the user from a specific event"""
    attendance = AttendanceHistory.objects(user_id = user_id, event_id = event_id).first()
    if attendance is None:
        print("User did not attend the event")
        return False

    attendance.delete()
    return True


def search_attendance(**fields):
    """search attendance history, return a list of attendance
    Pass only user id will find all events the user attends
    Pass only event id will find all users attending the event
    Pass both will check if a user is registered for the event
    @:returns list: a list of attendance ranging from 0 to all attendance in the database"""
    attendance = AttendanceHistory.objects(**fields).all()

    return attendance