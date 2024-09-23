import logging
import os
import time

from selenium import webdriver
from src.database_connector.postgres_connector import PostgresConnector
from src.player_data.player_profile.player_profile_builder import PlayerProfileBuilder
from src.web.driver_manager.driver_manager import DriverManager
from src.web.pages.squad_season_page import SquadSeasonPage


class SquadSeasonScraper:

    @staticmethod
    def scrape_squad_players(squad_id: str="b8fd03ef", season: str="2023-2024", driver: webdriver=None):

        try:
            if (driver is None):
                driver_manager = DriverManager()
                driver = DriverManager.get_driver(driver_manager)

            squad_page = SquadSeasonPage(driver)
            squad_page.navigate_to_match_url(squad_id, season)
            SquadSeasonScraper.save_player_profiles(squad_page)
        except Exception as e:
            print(str(e))
            #logging.log(level=0,message=str(e))
        finally:
            driver.close()

    @staticmethod
    def save_player_profiles(squad_page, postgres_connector=None):
        #open connection + cursor before all inserts
        if(postgres_connector is None):
            postgres_connector = PostgresConnector()
            postgres_connector.open_connection_cursor("premier_league_stats")

        try:
            player_standard_stat_rows = squad_page.get_player_table_rows_for_standard_stats()
            players = []

            #loop through home/away team
            for row in player_standard_stat_rows:
                # build profiles
                player_profile = PlayerProfileBuilder.build_player_profile_from_table_row(row, squad_page)
                players.append(player_profile)


            #save profiles to db
            postgres_connector = PlayerProfileBuilder.save_player_profiles(players, postgres_connector)
        except Exception as e:
            print(str(e))
            #logging.log("Error saving player profiles on " + squad_page.url_for_page() + "\n" + str(e))
            return False
        finally:
            postgres_connector.close_connection()
        return True