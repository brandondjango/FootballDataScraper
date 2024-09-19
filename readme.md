# Football Data Scraper API

Purpose of this personal project is to grab football(soccer) statistics and store them in a database for use as a data set for an AI to learn.

The project can be run locally or on a Docker container.

# Requirements

- Python3
- Postgres db setup(psql)

# Steps to run

## Database setup:

First, you'll need to set up your db with the schema located at [premier_league_stats_9-16-24_schema.sql](schemas%2Fpremier_league_stats_9-16-24_schema.sql)

You can do this by running a command like:

``` 
psql -d premier_league_stats -f schemas/premier_league_stats_9-16-24_schema.sql
```

If you want existing data that has already been scraped, use [Premier_leage_data2023-2024.sql](sample_data%2FPremier_leage_data2023-2024.sql)

## Python libraries

Setup venv from project root(with python3):
```
python3 -m venv .
source bin/activate
```

Install project requirements:

```pip3 install -r requirements.txt```

# Start Football Scraper API

Start the server:

```python main.py```

Set up you database(WIP):
``` 
curl --location --request GET 'https://0.0.0.0:8080/db_setup' \
--header 'Content-Type: application/json' \
--data '{"db_pass" : "Insert_database_password"}'
```

Scrape a match from fbref.com/

```
curl --location --request GET 'https://0.0.0.0:8080/scrape_match' \
--header 'Content-Type: application/json' \
--data '{"match_id" : "Insert match id"}'
```

Scrape a season where competition_id is the id of the competition(premier league, mls, etc.) and the season is the year of data you want to collect:
Premier league:
``` 
curl --location 'http://0.0.0.0:8080/scrape_season' \
--header 'Content-Type: application/json' \
--data '{
    "competition_id" : "9",
    "season": "2023-2024"
}'
```

## Driver support

This project uses a browser to scrape data from fbref.com/. In the container, currently it is neccessary specify the browser version.

Within Docker File, we download the latest stable chromedriver for linux.

Latest stable chrome versions can be found here: https://chromereleases.googleblog.com/search/label/Stable%20updates

Latest drivers can be found here: https://googlechromelabs.github.io/chrome-for-testing/


## Connecting to Google postgres instance

If your postgres instance is hosted on Google Cloud, you'll need to add your IP address to Google Cloud SQL -> Connections -> Networking -> Authorized Networks

## Sample Data:

Sample SQL dump located in sample_data directory.

![sample_screenshot.png](sample_data%2Fsample_screenshot.png))

## Table Descriptions

Derived data means data that was derived from other tables as opposed to scraped.

### match_imported_status

Contains derived data: No.

Describes if an import has been attempted at the [match_scraper.py](src%2Fdata_scraper%2Fmatch_scraper.py) level.

### match_info

Contains derived data: No.

Details of the match: date, score, venue, competition, etc.

### match_shots_stats

Contains derived data: Yes, sca1_player_id, sca2_player_id.

Details on the shots that occured in the match, including player shooting, outcome, other player involvements, etc.

### match_summary_stats

Contains derived data: No.

Summary of stats for a player in a match.

### players

Contains derived data: No.

Just a mapping of player_name to player_id