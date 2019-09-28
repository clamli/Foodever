import mongoengine
from db.db_collections import User, Event, AttendanceHistory
from db.db_constants import DB_NAME, ALIAS, PORT, DEFAULT_PREFERENCE_VALUE, MOCK_HOST, MOCK_ENGINE
from datetime import datetime


class DatabaseAPI():

    def connect(self, dry_run: bool = False):
        """connect to the Foodever database
        This is the first method you should call in the application
        @:param dry_run: false to connect to the real database, true to use a fake one"""
        if not dry_run:
            mongoengine.connect(DB_NAME, host = ALIAS, port = PORT)
        else:
            mongoengine.connect(MOCK_ENGINE, host = MOCK_HOST)

    # -- user operations starts here --

    def create_user(self, first_name: str, last_name: str, is_owner: bool, credit: int,
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

    def search_user(self, user_id: int = -1, first_name: str = "", last_name: str = "", email: str = ""):
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

    def delete_user(self, user_id: int = -1, first_name: str = "", last_name: str = "", email: str = ""):
        """delete user by either 1) user id 2) first name, last name, and email """
        user_found = self.search_user(user_id, first_name, last_name, email)
        if user_found is None:
            print("User not found")
            return False
        user_found.delete()
        return True

    def edit_user(self, user_id: int = -1, **fields):
        """edit user info by user_id
            @:param fields: key-value pair indicates which field to change"""
        user_found = self.search_user(user_id)
        if user_found is None:
            print("User not found")
            return None

        # update fields
        for key, value in fields.items():
            user_found[key] = value
        user_found.save()

        return user_found

    # -- events operations starts here --

    def create_event(self, user_id: int = -1, event_name: str = "", host_name: str = "",
                     date_time: datetime = datetime.now(), location: str = ""):
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
                          host_name = host_name, date = date_time, location = location).save()
        return new_event

    def search_events(self, **fields):
        """search events that match the condition"""
        events = Event.objects(**fields).all()
        return events

    def edit_event(self, event_id: int = -1, **fields):
        """edit a single event based on event id"""
        event = self.search_events(event_id = event_id).first()
        if event is None:
            print("No event found")
            return None

        # update fields
        for key, value in fields.items():
            event[key] = value
        event.save()

        return event

    def delete_events(self, event_id: int = -1):
        """delete a single event based on event id"""
        event = self.search_events(event_id = event_id).first()
        if event is None:
            print("No event found")
            return False
        event.delete()
        return True

    # -- attendence operation starts here --
    def confirm_attendance(self, user_id: int = -1, event_id: int = -1):
        """register the user for a specific event"""
        if user_id == -1:
            print("User Id cannot be empty")
            return None
        elif event_id == -1:
            print("")
            return None
        attendance = AttendanceHistory(user_id = user_id, event_id = event_id).save()

        return attendance

    def cancel_attendance(self, user_id: int = -1, event_id: int = -1):
        """remove the user from a specific event"""
        attendance = AttendanceHistory.objects(user_id = user_id, event_id = event_id).first()
        if attendance is None:
            print("User did not attend the event")
            return False

        attendance.delete()
        return True

    def search_attendance(self, **fields):
        """search attendance history
        Pass only user id will find all events the user attends
        Pass only event id will find all users attending the event
        Pass both will check if a user is registered for the event"""
        attendance = AttendanceHistory.objects(**fields).all()

        return attendance
