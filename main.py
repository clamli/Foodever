import application
import config
from flask import Flask, render_template, request
from google.auth.transport import requests
from google.cloud import datastore
import google.oauth2.id_token

# firebase_request_adapter = requests.Request()

app = application.create_app(config)

# @app.route('/login')
# def login():
#     # Verify Firebase auth.
#     id_token = request.cookies.get("token")
#     error_message = None
#     claims = None

#     if id_token:
#         try:
#             # Verify the token against the Firebase Auth API. This example
#             # verifies the token on each page load. For improved performance,
#             # some applications may wish to cache results in an encrypted
#             # session store (see for instance
#             # http://flask.pocoo.org/docs/1.0/quickstart/#sessions).
#             claims = google.oauth2.id_token.verify_firebase_token(
#                 id_token, firebase_request_adapter)
#         except ValueError as exc:
#             # This will be raised if the token is expired or any other
#             # verification checks fail.
#             error_message = str(exc)

#     return render_template(
#         'templates/login.html',
#         user_data=claims, error_message=error_message)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
