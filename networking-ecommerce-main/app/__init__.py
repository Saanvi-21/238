#Importing modules
import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# instantiate the extensions
# SQLAlchemy - write sql queries and execute sql queries through flask
# Migrate - used to migrate data into the database

db = SQLAlchemy()
migrate = Migrate()

#Function to create app
def create_app(script_info=None):
    # instantiate the app
    app = Flask(__name__)
    cors = CORS(app)

    # set configz
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)
    app.config['CORS_HEADERS'] = 'Content-Type'

    # set up extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    from .views.views import views
    from .api.api import api

    app.register_blueprint(views)
    app.register_blueprint(api)

    #Functions to handle errors
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

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}
    return app
