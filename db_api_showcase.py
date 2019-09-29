import os, sys
from datetime import datetime
from api.db_api import DatabaseAPI

sys.path.append(os.path.dirname(".."))

def showcase_api():
    """showcase the api"""

    client = DatabaseAPI()
    client.connect(dry_run = True)

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
    attendance = client.confirm_attendance(1, 1)
    if attendance is not None:
        print(attendance.to_json())
    input("Press Enter to continue...")
    print("Kyle tries to attend second session")
    attendance = client.confirm_attendance(2, 2)
    if attendance is not None:
        print(attendance.to_json())
    input("Press Enter to continue...")

    print("Kyle checks whether he's really attending")
    criteria = {"user_id": 2, "event_id": 2}
    attendance = client.search_attendance(**criteria)   # TODO what if an event is already canceled?
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

    # Lei edits
    input("Press Enter to continue...")

    print("Jimmy posts a communication event")
    search_result = \
        client.search_user(**{"first_name": "Jimmy", "last_name": "Valmer", "email": "handicapable@utexas.edu"})
    client.create_event(search_result.user_id, "Communication Session", "Jimmy", datetime(2019, 9, 28, 10, 00), "EER")
    input("Press Enter to continue...")

    print("Kenny are looking for Communication session at EER")
    condition = {"event_name": "Communication Session", "location": "EER"}
    events = client.search_events(**condition)
    print(events.to_json())
    input("Press Enter to continue...")

    print("Kenny attends Communication session")
    attendance = client.confirm_attendance(4, 2)
    if attendance is not None:
        print(attendance.to_json())
    input("Press Enter to continue...")

    print("After Kenny decided to attend the Communication, Jimmy cancels his section ")
    client.delete_events(2) # To do What if an event got canceled after a user decided to attend this event.
    input("Press Enter to continue...")

    print("Kenny posts a Career Fair")
    search_result = \
        client.search_user(**{"first_name": "Kenny", "last_name": "McCormick", "email": "kenny@utexas.edu"})
    client.create_event(search_result.user_id, "Career Fair Session", "Kenny", datetime(2019, 9, 26, 14, 00), "SAC")
    input("Press Enter to continue...")

    print(" Jimmy is looking for career fair at SAC ")
    condition = {"event_name": "Career Fair Session", "location": "SAC"}
    events = client.search_events(**condition)
    print(events.to_json())
    input("Press Enter to continue...")

    print("Jimmy attends career fair session")
    attendance = client.confirm_attendance(5, 2)
    if attendance is not None:
        print(attendance.to_json())
    input("Press Enter to continue...")

    print(" Jimmy is also looking for meditation session at School")
    condition = {"event_name": "Meditation Session", "location": "School"}
    events = client.search_events(**condition)
    print(events.to_json())
    input("Press Enter to continue...")

    print("Jimmy attends meditation  session")
    attendance = client.confirm_attendance(5, 1)
    if attendance is not None:
        print(attendance.to_json())
    input("Press Enter to continue...") # To do how does users know the events they want to attend having the same time?

    print("Kenny posts a prom")
    search_result = \
        client.search_user(**{"first_name": "Kenny", "last_name": "McCormick", "email": "kenny@utexas.edu"})
    client.create_event(search_result.user_id, "Prom Session", "Kenny", datetime(2019, 9, 30, 17, 00), "SAC")
    input("Press Enter to continue...")

    print(" Jimmy is looking for prom at SAC ")
    condition = {"event_name": "Prom Session", "location": "SAC"}
    events = client.search_events(**condition)
    print(events.to_json())
    input("Press Enter to continue...")

    print("Jimmy attends prom session")
    attendance = client.confirm_attendance(5, 3)
    if attendance is not None:
        print(attendance.to_json())
    input("Press Enter to continue...")

    print("After Jimmy attends the prom, Jimmy decide to delete his account ")
    result = client.search_user(first_name="Jimmy", last_name="Valmer", email="handicapable@utexas.edu")
    if result is not None:
        print(result.to_json())
    client.delete_user(5)
    input("Press Enter to continue...")  # To do after deleting a user, will a new user continue using this user's id or create a new id?


    # The following exists some mistakes.
    print("Eric posts a show")
    search_result = \
        client.search_user(**{"first_name": "Eric", "last_name": "Cartman", "email": "fightanxiety@utexas.edu"})
    client.create_event(search_result.user_id, "Prom Session", "Eric", datetime(2019, 10, 1, 17, 00), "SAC")
    input("Press Enter to continue...")

    print("Kyle is looking for a prom at SAC ")
    condition = {"event_name": "Prom Session", "location": "SAC"}
    events = client.search_events(**condition)
    print(events.to_json())
    input("Press Enter to continue...")

    print("After Kyle decided to attend the prom, Eric changes the datetime of prom event ")
    result = client.search_events(event_name = "Prom Session", host_name = "Eric",
                                  date = datetime(2019, 10, 1, 17, 00),location = "SAC")
    if result is not None:
        print(result.to_json())
    changes = {'event_name': 'Prom Session', 'host_name': 'Eric',
    'date': datetime(2019, 10, 1, 19, 00), 'location':'SAC'}
    new_time = client.edit_event(4, **changes)
    print(new_time.to_json())  # To do, how does the user know the datetime of the event have changed


if __name__ == "__main__":
    showcase_api()
