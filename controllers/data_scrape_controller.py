import os

from flask import Flask, request, jsonify

from src.data_scraper.match_scraper import MatchScraper

app = Flask(__name__)

@app.route('/scrape_match', methods=['POST'])
def api_endpoint():
    data = request.json

    if data.get("match_id") is None:
        response = {
            'status': 'Failed',
            'message': "Match Id not provided: "
        }
        return jsonify(response), 500

    match_id = data.get("match_id")

    MatchScraper.scrape_match(match_id)

    # Process the data as needed
    response = {
        'status': 'success',
        'message': "Scraped match with id: " + match_id
    }
    return jsonify(response), 200

@app.route('/db_setup', methods=['POST'])
def db_setup_endpoint():
    data = request.json
    db_pass = data.get('db_pass')

    os.environ['DB_PASS'] = db_pass

    # Process the data as needed
    response = {
        'status': 'success',
        'data_received': os.environ['DB_PASS']
    }
    return jsonify(response), 200




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)