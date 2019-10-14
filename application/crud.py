from application import get_db_api
from application.api import storage_api, db_api
from flask import Blueprint, render_template, request, current_app, redirect, session as login_session
from flask import jsonify
from datetime import datetime
import json

crud = Blueprint('crud', __name__)


@crud.route("/")
def show_events():
    api = get_db_api()
    events = api.search_events()
    # create some fake event if none
    if len(events) == 0:
        api.create_user("Zinan", "Zhuang", False, 0, "zinan@utexas.edu")
        api.create_event(1, "Library Dine", "Zinan", location = "pcl", tags=["school", "UT"])
        api.create_event(1, "Library Dine 2", "Zinan", location = "pcl", tags=["school"])
        events = api.search_events()

    if 'username' not in login_session:
        return render_template("public_show_events.html", events = events)
    else:
        return render_template("show_events.html", events = events)

@crud.route("/login")
def show_login():
    login_session['username'] = 'Zinan'
    return redirect("/")

@crud.route("/logout")
def show_logout():
    login_session.pop("username", None)
    return redirect("/")

@crud.route("/search", methods = ["GET", "POST"])
def search():
    return render_template("search_results.html")

@crud.route("/create_event", methods = ["GET", "POST"])
def create_event():
    if request.method == 'GET':
        return render_template("create_event.html")

    data = request.get_json()
    print("INFO: Creating event..." + format(data[4]))
    if request.method == 'POST':
        if data[0].get('value') is not None and data[4].get('value') is not None:
            db_api.create_event(1, "Meditation Session", "Kyle", datetime(2019, 9, 26, 14, 00), "School")
            # db_api.create_event(1, event_name=data[0].get('value'), host_name=data[1].get('value'), 
            #                     date_time=datetime.strptime(data[2].get('value'), '%Y-%m-%dT%H:%M'),
            #                     location=data[3].get('value'), tags=data[4].get('value').split(',')
            #                     # , food=data[5].get('value').split(',')
            #                     )
            return jsonify({'ok': True, 'message': 'Event created successfully!'}), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

@crud.route("/my_activities")
def show_activities():
    return render_template("activities.html")

@crud.route("/event/<event_id>")
def view_event(event_id):
    return render_template("event_details.html", event_id = event_id)

def upload_image_file(file):
    """
    Upload the user-uploaded file to Google Cloud Storage and retrieve its
    publicly-accessible URL.
    """
    if not file:
        return None

    public_url = storage_api.upload_file(
        file.read(),
        file.filename,
        file.content_type
    )

    current_app.logger.info(
        "Uploaded file %s as %s.", file.filename, public_url)

    return public_url


@crud.route('/image', methods=['GET'])
def image_upload_file():
    return render_template('upload.html')


@crud.route('/image/upload', methods=['POST'])
def image_upload():
    if request.method == 'POST':
        for image in request.files.getlist("face_image"):
            image_url = upload_image_file(image)
            food = {"foodName": "noodle",
                    "foodTags": ["delicious", "healthy"],
                    "foodType": ["chinese", "noodle"],
                    "foodImages": [image_url]}
            get_db_api().create_event(**{"user_id": "001", "event_name": "Party", "host_name": "Zinan", "location": "school", "food": food})

        return 'Image Upload Successfully'