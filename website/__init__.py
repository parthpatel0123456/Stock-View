import sys
import os
print(sys.executable)

from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'asdflkjal aflknase',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )

    CORS(app)


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')


    return app
    