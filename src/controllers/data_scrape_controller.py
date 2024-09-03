import os

import yaml
from flask import Flask, request, jsonify

from src.config_util.config_util import ConfigUtil

app = Flask(__name__)

@app.route('/data_scrape', methods=['POST'])
def api_endpoint():
    data = request.json
    # Process the data as needed
    response = {
        'status': 'success',
        'data_received': data
    }
    return jsonify(response), 200

@app.route('/db_setup', methods=['POST'])
def db_endpoint():
    data = request.json
    db_pass = data.get('db_pass')

    ConfigUtil.add_config_value("db_pass", db_pass, "database")

    # Process the data as needed
    response = {
        'status': 'success',
        'data_received': ConfigUtil.get_current_configs("database")
    }
    return jsonify(response), 200




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)