import os, sys
from datetime import datetime
from api.db_api import DatabaseAPI

sys.path.append(os.path.dirname(".."))

def showcase_api():
    """showcase the api"""

    client = DatabaseAPI()
    client.connect()

    print("Five users are using the service")

    user_list = []
    user_list.append({"first_name": "Stan", "last_name": "Marsh",
                      "is_owner": False, "credit": 100, "email": "stanmarsh@utexas.edu"})
    user_list.append({"first_name": "Kyle", "last_name": "Broflovski",
                      "is_owner": False, "credit": 100, "email": "broflovski@utexas.edu"})
    user_list.append({"first_name": "Eric", "last_name": "Cartman",
                      "is_owner": False, "credit": 100, "email": "fightanxiety@utexas.edu"})
    user_list.append({"first_name": "Kenny", "last_name": "McCormick",
                      "is_owner": False, "credit": 100, "email": "kenny@utexas.edu"})
    user_list.append({"first_name": "Jimmy", "last_name": "Valmer",
                      "is_owner": False, "credit": 100, "email": "handicapable@utexas.edu"})

    for user in user_list:
        client.create_user(**user)

    input("Press Enter to continue...")

    print("Kyle posts a meditation event")
    search_result = \
        client.search_user(**{"first_name": "Kyle", "last_name": "Broflovski", "email": "broflovski@utexas.edu"})
    client.create_event(search_result.user_id, "Meditation Session", "Kyle", datetime(2019, 9, 26, 14, 00), "School")
    input("Press Enter to continue...")

    print("Eric also posts a meditation event in the same time")
    search_result = \
        client.search_user(**{"first_name": "Eric", "last_name": "Cartman", "email": "fightanxiety@utexas.edu"})
    client.create_event(search_result.user_id, "Meditation Session", "Eric", datetime(2019, 9, 26, 16, 00), "School")
    input("Press Enter to continue...")

    print("Stan and Kenny are looking for meditation session at School")
    condition = {"event_name": "Meditation Session", "location": "School"}
    events = client.search_events(**condition)
    print(events.to_json())
    input("Press Enter to continue...")

    print("While Stan and Kenny are still deciding, Eric cancels his event")
    client.delete_events(2)  # TODO when deleting event, how does a user know their event?
    input("Press Enter to continue...")

    print("Stan attends first session")
    attendance = client.confirm_attendence(1, 1)
    if attendance is not None:
        print(attendance.to_json())
    input("Press Enter to continue...")

    print("Kyle tries to attend second session")
    attendance = client.confirm_attendence(2, 2)
    if attendance is not None:
        print(attendance.to_json())
    input("Press Enter to continue...")

    print("Kyle checks whether he's really attending")
    criteria = {"user_id": 2, "event_id": 2}
    attendance = client.search_attendence(**criteria)   # TODO what if an event is already canceled?
    if attendance is not None:
        print(attendance.to_json())
    input("Press Enter to continue...")

    print("After Stan attended the meditation session, he decides to change his name to Terrance")
    result = client.search_user(first_name="Stan", last_name="Marsh", email="stanmarsh@utexas.edu")
    if result is not None:
        print(result.to_json())
    changes = {"first_name": "Terrance", "last_name": "Marsh", "email": "stanmarsh@utexas.edu"}
    new_me = client.edit_user(result.user_id, **changes)
    print(new_me.to_json())

if __name__ == "__main__":
    showcase_api()