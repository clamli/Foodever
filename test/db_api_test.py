import os, sys
from datetime import datetime
from api.db_api import DatabaseAPI

sys.path.append(os.path.dirname(".."))

def test_api():
    """test api usage"""
    client = DatabaseAPI()
    client.connect()

    print("Create a clone of me :p")
    new_user = client.create_user("Zinan", "Zhuang", False, 100, "zinan@utexas.edu")
    print(new_user.to_json())

    print("Search me in the database")
    result = client.search_user(first_name = "Zinan", last_name = "Zhuang", email = "zinan@utexas.edu")
    if result is not None:
        print(result.to_json())

    print("Edit my info")
    changes = {"first_name" : "Lin", "last_name": "Jun", "email": "jlin21@lsu.edu"}
    new_me = client.edit_user(result.user_id, **changes)
    print(new_me.to_json())

    print("Let meeee create an event")
    new_event = client.create_event(1, "Group Meeting", "Zinan", datetime(2019, 9, 27, 14, 00), "PCL")
    print(new_event.to_json())

    print("Search events")
    condition = {"event_name": "Group Meeting", "location" : "PCL"}
    events = client.search_events(**condition)
    for e in events:
        print(e.to_json())

    print("Oh, missing something in the event")
    updates = {'location': 'PCL Group Study Room', 'host_name': 'Team X'}
    event = client.edit_event(1, **updates)
    print(event.to_json())

    print("Someone is joining our event!")
    attendence = client.confirm_attendence(1, 1)
    if attendence is not None:
        print(attendence.to_json())

    print("Double check that I am in")
    criteria = {"user_id": 1, "event_id": 1}
    attendence = client.search_attendence(**criteria)
    if attendence is not None:
        print(attendence.to_json())

    print("Data clean up")
    result = client.delete_user(user_id = 1)
    print("User Deleted? %s" % result)
    result = client.delete_events(event_id = 1)
    print("Event Deleted? %s" % result)
    cancelled = client.cancel_attendence(1, 1)
    print("Registration Deleted? %s" % cancelled)


if __name__ == "__main__":
    test_api()