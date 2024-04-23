import re
from flask import Blueprint, Flask, request, jsonify
import subprocess
import json

app = Flask(__name__)
api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/version', methods=['GET'])
def version():
    version = subprocess.check_output(['sui', '--version'])
    return jsonify({'version': version.strip()})

@api_blueprint.route('/envs', methods=['GET'])
def envs():
    response = json.loads(subprocess.check_output(['sui', 'client', 'envs', '--json']))
    # regex = r'\│\s*([^\s]+)\s*\│\s*(https?:\/\/[^\s\│]+)\s*\│'
    # envs = [{'name': m.group(1), 'url': m.group(2)} for m in re.finditer(regex, envs)]
    return jsonify({'active_env': response[1]})

@api_blueprint.route('/address', methods=['GET'])
def address():
    response = subprocess.check_output(['sui', 'client', 'addresses', '--json'])
    return json.loads(response)

app.register_blueprint(api_blueprint, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)

