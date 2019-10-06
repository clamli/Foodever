from application import get_db_api
from application.api import storage_api
from flask import Blueprint, render_template, request, current_app


crud = Blueprint('crud', __name__)


@crud.route("/")
def test():

    user = {"first_name": "Stan", "last_name": "Marsh",
            "is_owner": False, "credit": 100, "email": "stanmarsh@utexas.edu"}
    get_db_api().create_user(**user)

    return render_template("hello_world.html")


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