import mongoengine


class DBHelper:

    # Database config constants
    ALIAS = "localhost"
    PORT = 27017
    DB_NAME = "foodeverdb"

    # Collection names
    USER = "user"
    ATTENDANCE_HISTORY = "attendanceHistory"
    EVENT = "event"

    def __init__(self):
        mongoengine.connect(DBHelper.DB_NAME, DBHelper.ALIAS, DBHelper.PORT)
