import re
from flask import Blueprint, Flask, request, jsonify
import subprocess
import json

from utils import sui_command

app = Flask(__name__)
api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/version', methods=['GET'])
def version():
    version = sui_command([ '--version'],False,"version")
    return version

@api_blueprint.route('/envs', methods=['GET'])
def envs():
    response = sui_command(['client', 'envs'])
    return {'active_env': response[1], 'all_envs': response[0]}

@api_blueprint.route('/address', methods=['GET'])
def address():
    response = sui_command(['client', 'address'])
    return response

app.register_blueprint(api_blueprint, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)

