# Football Data Scraper API

Purpose of this personal project is to grab football(soccer) statistics and store them in a database for use as a data set for an AI to learn.

The project con be run locally or on a Docker container.

# Requirements

Python3
Postgres db setup

# Steps to run

Setup venv from project root(with python3):
```
python3 -m venv .
source bin/activate
```

Install project requirements:

```pip3 install -r requirements.txt```

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

## Driver support

This project uses a browser to scrape data from fbref.com/. In the container, currently it is neccessary specify the browser version.

Within Docker File, we download the latest stable chromedriver for linux.

Latest stable chrome versions can be found here: https://chromereleases.googleblog.com/search/label/Stable%20updates

Latest drivers can be found here: https://googlechromelabs.github.io/chrome-for-testing/


## Connect to Google postgres instance

If your postgres instance is hosted on Google Cloud, you'll need to add your IP address to Google Cloud SQL -> Connections -> Networking -> Authorized Networks