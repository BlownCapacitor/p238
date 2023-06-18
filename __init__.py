import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
load_dotenv()


# instantiate the extensions
#defines "SQLAlchemy" as the database type
db = SQLAlchemy()

migrate = Migrate()

def create_app(script_info=None):

    # initialise the app and import settings
    app = Flask(__name__)
    cors = CORS(app)
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)
    app.config['CORS_HEADERS'] = 'Content-Type'
    db.init_app(app)
    migrate.init_app(app, db)

    #register blueprints
    from .views.views import views
    from .api.api import api

    app.register_blueprint(views)
    app.register_blueprint(api)


    #handles the many possible errors
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({
            "status":"error",
            "error":e.description
        }), 400

    @app.errorhandler(404)
    def not_found_error(e):
        return jsonify({
            "status":"error",
            "error":e.description
        }), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({
            "status":"error",
            "error":"this wasn't suppose to happen"
        })


#allows database and flask to be used the in the shell
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}
    return app
