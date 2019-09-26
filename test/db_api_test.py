from datetime import datetime
from db.db_constants import DEFAULT_PREFERENCE_VALUE


import unittest
from mongoengine import connect, disconnect
from api.db_api import DatabaseAPI


class DatabaseAPITest(unittest.TestCase):

    MONGO_ENGINE_TEST = "mongoenginetest"
    HOST = "mongomock://localhost"
    USER_ID_1 = 1
    USER_ID_2 = -1
    FIRST_NAME_1 = "Zinan"
    LAST_NAME_1 = "Zhuang"
    IS_OWNER_1 = False
    CREDIT_1 = 100
    EMAIL_1 = "zinan@utexas.edu"
    PREFERENCE_1 = DEFAULT_PREFERENCE_VALUE
    DATETIME = datetime(2019, 9, 27, 14, 00)
    EVENT_ID = 1
    EVENT_NAME_1 = "event name 1"
    EVENT_NAME_2 = ""
    LOCATION_1 = "LOCATION 1"
    LOCATION_2 = ""

    DB_API = DatabaseAPI()

    @classmethod
    def setUp(cls):
        connect(DatabaseAPITest.MONGO_ENGINE_TEST, host = DatabaseAPITest.HOST)

    @classmethod
    def tearDown(cls):
        disconnect()

    def create_user(self):
        return DatabaseAPITest.DB_API.create_user(DatabaseAPITest.FIRST_NAME_1,
                                                  DatabaseAPITest.LAST_NAME_1,
                                                  DatabaseAPITest.IS_OWNER_1,
                                                  DatabaseAPITest.CREDIT_1,
                                                  DatabaseAPITest.EMAIL_1,
                                                  DatabaseAPITest.PREFERENCE_1)

    def create_user_test(self):
        user = self.create_user()
        self.assertEqual(user.first_name, DatabaseAPITest.FIRST_NAME_1)
        self.assertEqual(user.last_name, DatabaseAPITest.LAST_NAME_1)
        self.assertEqual(user.is_owner, DatabaseAPITest.IS_OWNER_1)
        self.assertEqual(user.credit, DatabaseAPITest.CREDIT_1)
        self.assertEqual(user.email, DatabaseAPITest.EMAIL_1)
        self.assertEqual(user.preference, DatabaseAPITest.PREFERENCE_1)

    def search_user_test(self):
        self.create_user()
        user = DatabaseAPITest.DB_API.search_user(first_name=DatabaseAPITest.FIRST_NAME_1,
                                                  last_name=DatabaseAPITest.LAST_NAME_1,
                                                  email=DatabaseAPITest.EMAIL_1)
        self.assertEqual(user.first_name, DatabaseAPITest.FIRST_NAME_1)
        self.assertEqual(user.last_name, DatabaseAPITest.LAST_NAME_1)
        self.assertEqual(user.is_owner, DatabaseAPITest.IS_OWNER_1)
        self.assertEqual(user.credit, DatabaseAPITest.CREDIT_1)
        self.assertEqual(user.email, DatabaseAPITest.EMAIL_1)
        self.assertEqual(user.preference, DatabaseAPITest.PREFERENCE_1)

    def delete_user_when_user_is_none_test(self):
        self.assertFalse(DatabaseAPITest.DB_API.delete_user(user_id = DatabaseAPITest.USER_ID_1))

    def delete_user_when_user_is_not_none_test(self):
        self.create_user()
        self.assertTrue(DatabaseAPITest.DB_API.delete_user(user_id = DatabaseAPITest.USER_ID_1))

    def edit_user_when_user_is_none_test(self):
        self.assertIsNone(DatabaseAPITest.DB_API.edit_user(user_id = DatabaseAPITest.USER_ID_1))

    def edit_user_when_user_is_not_none_test(self):
        self.create_user()
        user = DatabaseAPITest.DB_API.edit_user(user_id = DatabaseAPITest.USER_ID_1)
        self.assertEqual(user.first_name, DatabaseAPITest.FIRST_NAME_1)
        self.assertEqual(user.last_name, DatabaseAPITest.LAST_NAME_1)
        self.assertEqual(user.is_owner, DatabaseAPITest.IS_OWNER_1)
        self.assertEqual(user.credit, DatabaseAPITest.CREDIT_1)
        self.assertEqual(user.email, DatabaseAPITest.EMAIL_1)
        self.assertEqual(user.preference, DatabaseAPITest.PREFERENCE_1)

    def create_event_when_user_id_is_invalid_test(self):
        res = DatabaseAPITest.DB_API.create_event(user_id = DatabaseAPITest.USER_ID_2,
                                                  event_name = DatabaseAPITest.EVENT_NAME_1,
                                                  host_name = DatabaseAPITest.FIRST_NAME_1,
                                                  date_time = DatabaseAPITest.DATETIME,
                                                  location = DatabaseAPITest.LOCATION_1)
        self.assertIsNone(res)

    def create_event_when_event_name_is_empty_test(self):
        res = DatabaseAPITest.DB_API.create_event(user_id = DatabaseAPITest.USER_ID_1,
                                                  event_name = DatabaseAPITest.EVENT_NAME_2,
                                                  host_name = DatabaseAPITest.FIRST_NAME_1,
                                                  date_time = DatabaseAPITest.DATETIME,
                                                  location = DatabaseAPITest.LOCATION_1)
        self.assertIsNone(res)

    def create_event_when_event_location_is_empty_test(self):
        res = DatabaseAPITest.DB_API.create_event(user_id = DatabaseAPITest.USER_ID_1,
                                                  event_name = DatabaseAPITest.EVENT_NAME_1,
                                                  host_name = DatabaseAPITest.FIRST_NAME_1,
                                                  date_time = DatabaseAPITest.DATETIME,
                                                  location = DatabaseAPITest.LOCATION_2)
        self.assertIsNone(res)

    def create_event_test(self):
        event = DatabaseAPITest.DB_API.create_event(user_id = DatabaseAPITest.USER_ID_1,
                                                    event_name = DatabaseAPITest.EVENT_NAME_1,
                                                    host_name = DatabaseAPITest.FIRST_NAME_1,
                                                    date_time = DatabaseAPITest.DATETIME,
                                                    location = DatabaseAPITest.LOCATION_1)
        self.assertEqual(event.event_id, DatabaseAPITest.EVENT_ID)
        self.assertEqual(event.event_name, DatabaseAPITest.EVENT_NAME_1)
        self.assertEqual(event.host_name, DatabaseAPITest.FIRST_NAME_1)
        self.assertEqual(event.date, DatabaseAPITest.DATETIME)
        self.assertEqual(event.location, DatabaseAPITest.LOCATION_1)

    def search_event_test(self):
        DatabaseAPITest.DB_API.create_event(user_id = DatabaseAPITest.USER_ID_1,
                                            event_name = DatabaseAPITest.EVENT_NAME_1,
                                            host_name = DatabaseAPITest.FIRST_NAME_1,
                                            date_time = DatabaseAPITest.DATETIME,
                                            location = DatabaseAPITest.LOCATION_1)
        condition = {"event_name": DatabaseAPITest.EVENT_NAME_1, "location": DatabaseAPITest.LOCATION_1}
        event = DatabaseAPITest.DB_API.search_events(**condition).first()
        self.assertEqual(event.event_id, DatabaseAPITest.EVENT_ID)
        self.assertEqual(event.event_name, DatabaseAPITest.EVENT_NAME_1)
        self.assertEqual(event.host_name, DatabaseAPITest.FIRST_NAME_1)
        self.assertEqual(event.date, DatabaseAPITest.DATETIME)
        self.assertEqual(event.location, DatabaseAPITest.LOCATION_1)

    def edit_event_when_event_is_none_test(self):
        self.assertIsNone(DatabaseAPITest.DB_API.edit_event(user_id = DatabaseAPITest.USER_ID_1))

    def edit_user_when_user_is_not_none_test(self):
        event = DatabaseAPITest.DB_API.create_event(user_id = DatabaseAPITest.USER_ID_1,
                                                    event_name = DatabaseAPITest.EVENT_NAME_1,
                                                    host_name = DatabaseAPITest.FIRST_NAME_1,
                                                    date_time = DatabaseAPITest.DATETIME,
                                                    location = DatabaseAPITest.LOCATION_1)
        self.assertEqual(event.event_id, DatabaseAPITest.EVENT_ID)
        self.assertEqual(event.event_name, DatabaseAPITest.EVENT_NAME_1)
        self.assertEqual(event.host_name, DatabaseAPITest.FIRST_NAME_1)
        self.assertEqual(event.date, DatabaseAPITest.DATETIME)
        self.assertEqual(event.location, DatabaseAPITest.LOCATION_1)

    def delete_event_when_event_is_none_test(self):
        self.assertFalse(DatabaseAPITest.DB_API.delete_events(event_id = DatabaseAPITest.EVENT_ID))

    def delete_event_when_event_is_not_none_test(self):
        DatabaseAPITest.DB_API.create_event(user_id = DatabaseAPITest.USER_ID_1,
                                            event_name = DatabaseAPITest.EVENT_NAME_1,
                                            host_name = DatabaseAPITest.FIRST_NAME_1,
                                            date_time = DatabaseAPITest.DATETIME,
                                            location = DatabaseAPITest.LOCATION_1)
        self.assertTrue(DatabaseAPITest.DB_API.delete_events(event_id = DatabaseAPITest.EVENT_ID))

    def confirm_attendance_when_user_is_none_test(self):
        self.assertIsNone(DatabaseAPITest.DB_API.confirm_attendance(-1, DatabaseAPITest.EVENT_ID))

    def confirm_attendance_when_event_is_none_test(self):
        self.assertIsNone(DatabaseAPITest.DB_API.confirm_attendance(DatabaseAPITest.USER_ID_1, -1))

    def confirm_attendance_test(self):
        attendance = DatabaseAPITest.DB_API.confirm_attendance(DatabaseAPITest.USER_ID_1, DatabaseAPITest.EVENT_ID)
        self.assertEqual(attendance.user_id, DatabaseAPITest.USER_ID_1)
        self.assertEqual(attendance.event_id, DatabaseAPITest.EVENT_ID)

    def cancel_attendance_when_attendance_is_none_test(self):
        self.assertFalse(DatabaseAPITest.DB_API.cancel_attendance(DatabaseAPITest.USER_ID_1, DatabaseAPITest.EVENT_ID))

    def cancel_attendance_test(self):
        DatabaseAPITest.DB_API.confirm_attendance(DatabaseAPITest.USER_ID_1, DatabaseAPITest.EVENT_ID)
        self.assertTrue(DatabaseAPITest.DB_API.cancel_attendance(DatabaseAPITest.USER_ID_1, DatabaseAPITest.EVENT_ID))

    def search_attendance_test(self):
        DatabaseAPITest.DB_API.confirm_attendance(DatabaseAPITest.USER_ID_1, DatabaseAPITest.EVENT_ID)
        condition = {"user_id": DatabaseAPITest.USER_ID_1, "event_id": DatabaseAPITest.EVENT_ID}
        attendance = DatabaseAPITest.DB_API.search_attendance(**condition).first()
        self.assertEqual(attendance.user_id, DatabaseAPITest.USER_ID_1)
        self.assertEqual(attendance.event_id, DatabaseAPITest.EVENT_ID)


if __name__ == '__main__':
    unittest.main()
