import mongoengine
from db.db_collections import User, Event
from db.db_constants import DB_NAME, ALIAS, PORT, DEFAULT_PREFERENCE_VALUE
from datetime import datetime


def connect():
    """connect to the Foodever database
    This is the first method you should call in the application"""
    mongoengine.connect(DB_NAME, host = ALIAS, port = PORT)


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
    """search user by either 1) user id 2) first name, last name, and email """
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
        return False

    # update fields
    for key, value in fields.items():
        user_found[key] = value
    user_found.save()

    return user_found


# -- events operations starts here --


def create_event(user_id: int = -1, event_name: str = "", host_name: str = "",
                 date_time: datetime = datetime.now(), location: str = ""):
    """create an event in the database
        @:param user_id: user creating the event (owner or first responder)
        @:param event_name
        @:param host_name
        @:param date_time: the time of the event
        @:param location: the location of the event"""
    if user_id == -1:
        print("There must be a user creating the event")
        return False
    elif event_name == "":
        print("Event name can't be empty")
        return False
    elif location == "":
        print("Location can't be empty")
        return False
    new_event = Event(user_id = user_id, event_id = Event.objects().count() + 1, event_name = event_name,
                      host_name = host_name, date = date_time, location = location).save()
    return new_event


def search_events(**fields):
    """search events that match the condition"""
    events = Event.objects(**fields).all()
    return events


def edit_event(event_id: int = -1, **fields):
    """edit a single event based on event id"""
    event = search_events(event_id = event_id).first()
    if event is None:
        print("No event found")
        return False

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


def test_api():
    """test api usage"""
    connect()

    print("Create a clone of me :p")
    new_user = create_user("Zinan", "Zhuang", False, 100, "zinan@utexas.edu")
    print(new_user.to_json())

    print("Search me in the database")
    result = search_user(first_name = "Zinan", last_name = "Zhuang", email = "zinan@utexas.edu")
    if result is not None:
        print(result.to_json())

    print("Edit my info")
    changes = {"first_name" : "Lin", "last_name": "Jun", "email": "jlin21@lsu.edu"}
    new_me = edit_user(result.user_id, **changes)
    print(new_me.to_json())

    print("Let meeee create an event")
    new_event = create_event(1, "Group Meeting", "Zinan", datetime(2019, 9, 27, 14, 00), "PCL")
    print(new_event.to_json())

    print("Search events")
    condition = {"event_name": "Group Meeting", "location" : "PCL"}
    events = search_events(**condition)
    for e in events:
        print(e.to_json())

    print("Oh, missing something in the event")
    updates = {'location': 'PCL Group Study Room', 'host_name': 'Team X'}
    event = edit_event(1, **updates)
    print(event.to_json())

    print("Data clean up")
    result = delete_user(user_id = 1)
    print("User Deleted? %s" % result)
    result = delete_events(event_id = 1)
    print("Event Deleted? %s" % result)


if __name__ == "__main__":
    test_api()
