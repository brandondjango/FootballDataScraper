import os
import concurrent.futures
import logging

from flask import Flask, request, jsonify, Response

from src.data_scraper.match_fetcher import MatchFetcher
from src.data_scraper.match_scraper import MatchScraper
from datetime import datetime

from src.data_scraper.squad_fetcher import SquadFetcher
from src.data_scraper.squad_season_scraper import SquadSeasonScraper
from src.database_connector.postgres_connector import PostgresConnector

app = Flask(__name__)

def scrape_individual_match(match_id, jobs, postgres_connector):
    #todo add retry loging for import retrying. Imports don't always outright fail, you need to spot check if data was actually imported
    try:
        print("start scraping")
        MatchScraper.scrape_match(match_id, jobs)
    except Exception as e:
        print("Unable to import match: " + match_id + " because of \n:" + str(e))
        return match_id
    #return None

def scrape_matches_in_threads(match_ids, jobs):
    postgres_connector = PostgresConnector()
    postgres_connector.open_connection_cursor("premier_league_stats")
    match_ids_error = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        # Submit tasks to scrape each URL and write to the database
        futures = [executor.submit(scrape_individual_match, match_id, jobs, postgres_connector) for match_id in match_ids]

    # Wait for all tasks to complete
    for future in concurrent.futures.as_completed(futures):
        try:
            future.result()
        except Exception as e:
            print("Error in parallel: " + str(e))
    print(match_ids_error)



@app.route('/fetch/scrape_season', methods=['POST'])
def scrape_season():
    data = request.json
    comp_id = data.get("competition_id")
    season = data.get("season")

    #ignore previously imported matches
    force_all = data.get("force_all")

    #jobs to run
    jobs = data.get("jobs")


    match_ids = MatchFetcher.fetch_matches_from_season_scores_and_fixtures_page(comp_id, season)
    print("Number of total matches found: " + str(match_ids))


    #todo get this check in a function
    #ignore previously imported matches
    if force_all == False:
        try:
            #remove matches already imported:
            postgres_connector = PostgresConnector()
            postgres_connector.open_connection_cursor("premier_league_stats")
            query = "select match_id from match_imported_status where match_imported = true"
            parameters = ()
            imported_matches = postgres_connector.execute_parameterized_select_query(query, parameters)
            for match in imported_matches:
               match_ids.remove(match[0])
        except Exception as e:
            logging("Error removing previously imported matches:" + str(e))
        finally:
            postgres_connector.close_connection()


    #get matches
    scrape_matches_in_threads(match_ids, jobs)

    response = {
        "Start": "ok"
    }
    return jsonify(response), 200


@app.route('/fetch/scrape_match', methods=['POST'])
def scrape_match():
    data = request.json
    #jobs to run
    jobs = data.get("jobs")

    if data.get("match_id") is None:
        response = {
            'status': 'Failed',
            'message': "Match Id not provided: "
        }
        return jsonify(response), 500

    match_id = data.get("match_id")

    MatchScraper.scrape_match(match_id, jobs)

    # Process the data as needed
    response = {
        'status': 'success',
        'message': "Scraped match with id: " + match_id
    }
    return jsonify(response), 200

@app.route('/fetch/scrape_season_squads', methods=['POST'])
def scrape_season_squads():
    data = request.json
    #jobs to run
    competition_id = data.get("competition_id")
    season = data.get("season")
    team_squad_tuples = SquadFetcher.fetch_season_squads(competition_id, season)

    for tuple in team_squad_tuples:
        try:
            squad_id = tuple[0]
            SquadSeasonScraper.scrape_squad_players(squad_id=squad_id , season=season)
        except Exception as e:
            print("Error saving squad " + squad_id + " from season " + season)
            print(str(e))
            #logging.log(level=1, message="Error saving squad " + squad_id + " from season " + season)

    response = {
        'status': 'success',
        'message': "Scraped squads with ids: " + str(team_squad_tuples)
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