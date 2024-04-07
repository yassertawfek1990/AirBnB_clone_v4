#!/usr/bin/python3
"""
Flask App that integrates with AirBnB static HTML Template
"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, render_template, url_for
from flask_cors import CORS, cross_origin
from flasgger import Swagger
from models import storage
import os
from werkzeug.exceptions import HTTPException

# Glapp
app = Flask(__name__)
swagger = Swagger(app)

# glashes
app.url_map.strict_slashes = False

# ftup
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)

# Crg
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# appws
app.register_blueprint(app_views)


# bing
@app.teardown_appcontext
def teardown_db(exception):
    """d"""
    storage.close()


@app.errorhandler(404)
def handle_404(exception):
    """d"""
    code = exception.__str__().split()[0]
    description = exception.description
    message = {'error': description}
    return make_response(jsonify(message), code)


@app.errorhandler(400)
def handle_404(exception):
    """d"""
    code = exception.__str__().split()[0]
    description = exception.description
    message = {'error': description}
    return make_response(jsonify(message), code)


@app.errorhandler(Exception)
def global_error_handler(err):
    """d"""
    if isinstance(err, HTTPException):
        if type(err).__name__ == 'NotFound':
            err.description = "Not found"
        message = {'error': err.description}
        code = err.code
    else:
        message = {'error': err}
        code = 500
    return make_response(jsonify(message), code)


def setup_global_errors():
    """d"""
    for cls in HTTPException.__subclasses__():
        app.register_error_handler(cls, global_error_handler)


if __name__ == "__main__":
    """d"""
    # initializes global error handling
    setup_global_errors()
    # start Flask app
    app.run(host=host, port=port)
