# external
import logging
import os
import time

from src.database_connector.postgres_connector import PostgresConnector
from src.match_data.match_info.match_info_builder import MatchInfoTableUtil
from src.player_data.player_match_stats.player_match_stat_reader_util import PlayerMatchStatTableUtil
# internal
from src.web.driver_manager.driver_manager import DriverManager

from src.web.pages.match_stats_page import MatchStatsPage

from src.player_data.player_shots.player_shot_data_util import PlayerMatchStatShotTableUtil

from src.player_data.player_profile.player_profile_builder import PlayerProfileBuilder


class MatchScraper:

    @staticmethod
    def scrape_match(match_id, driver=None, postgres_connector=None):
        #store status of each saving of statistics
        save_success = {}
        try:
            if (driver is None):
                driver_manager = DriverManager()
                driver = DriverManager.get_driver(driver_manager)

            match_page = MatchStatsPage(driver)
            match_page.navigate_to_match_url(match_id)

            #scrape match deets
            save_success["match_details"] = MatchScraper.scrape_match_details(match_id, match_page, postgres_connector)

            # Scrape summary statistics on a match page
            save_success["match_summary"] = MatchScraper.scrape_match_summary(match_id, match_page, postgres_connector)

            # Scrape player shot statistics on a match page
            save_success["player_shots"] = MatchScraper.scrape_match_player_shots(match_id, match_page, postgres_connector)

            #todo add seperate status for save states
            save_success["import_status"] = MatchScraper.save_match_import_status(match_id, True, postgres_connector)
        except Exception as e:
            #set save status as not saved if it was never attempted
            for save_status in save_success.keys():
                if save_success[save_status] is None:
                    save_success[save_status] = False

            logging.exception(save_success)
        finally:
            driver.close()

        #return save_success statuses
        #return save_success

    @staticmethod
    def scrape_match_details(match_id, match_page, postgres_connector=None):
        try:
            match_details = {}
            match_details["match_id"] = match_id
            match_details["date"] = match_page.get_match_date()
            match_details["competition_id"] = match_page.get_match_competition_id()
            match_details["season"] = match_page.get_match_season()
            match_details["home_team"] = match_page.get_home_team()
            match_details["away_team"] = match_page.get_away_team()
            match_details["home_score"] = match_page.get_home_team_score()
            match_details["away_score"] = match_page.get_away_team_score()


            if(postgres_connector is None):
                postgres_connector = PostgresConnector()
                postgres_connector.open_connection_cursor("premier_league_stats")

            MatchInfoTableUtil.save_match_info(match_details, postgres_connector)
        except Exception as e:
            logging("Failed to save match details")
            return False
        finally:
            postgres_connector.close_connection()
        return True





    @staticmethod
    def scrape_match_summary(match_id, match_page, postgres_connector=None):
        MatchScraper.save_player_profiles(match_page, postgres_connector)
        MatchScraper.save_player_summary_stats(match_id, match_page, postgres_connector)


    @staticmethod
    def save_player_summary_stats(match_id, match_page, postgres_connector=None):
        was_postgres_connector_none = False
        if(postgres_connector is None):
            was_postgres_connector_none = True
            postgres_connector = PostgresConnector()
            postgres_connector.open_connection_cursor("premier_league_stats")

        try:
            # get summary stats divs
            match_player_stats_divs = match_page.get_player_stats_for_match_divs()

            # loop through summary rows for both teams
            for div in match_player_stats_divs:
                player_summary_stats = []

                # Get summary stats of match table
                match_player_summary_table_body = match_page.get_summary_stats_table_body(div)

                # build players if they don't exist
                player_summary_rows = match_page.get_player_rows_from_tbody(match_player_summary_table_body)

                #loop through home/away team
                for row in player_summary_rows:
                    # build profiles
                    player_summary = PlayerMatchStatTableUtil.get_summary_match_stats_for_player(row, match_page, match_id)
                    PlayerMatchStatTableUtil.save_match_summary_stats(player_summary, postgres_connector)

            #get substitute information
            subsitution_info_array = match_page.get_substitute_info()
            PlayerMatchStatTableUtil.save_substitute_info_to_match_summary(match_id, subsitution_info_array, postgres_connector)


        except Exception as e:
            logging("Error saving player summary stats for match id: " + match_id)
            return False
        finally:
            postgres_connector.close_connection()
        return True

    @staticmethod
    def save_player_profiles(match_page, postgres_connector=None):
        #open connection + cursor before all inserts
        if(postgres_connector is None):
            postgres_connector = PostgresConnector()
            postgres_connector.open_connection_cursor("premier_league_stats")

        try:
            # get summary stats divs
            match_player_stats_divs = match_page.get_player_stats_for_match_divs()

            # loop through summary rows for both teams
            for div in match_player_stats_divs:
                players = []

                # Get summary stats of match table
                match_player_summary_table_body = match_page.get_summary_stats_table_body(div)

                # build players if they don't exist
                player_summary_rows = match_page.get_player_rows_from_tbody(match_player_summary_table_body)

                #loop through home/away team
                for row in player_summary_rows:
                    # build profiles
                    player_profile = PlayerProfileBuilder.build_player_profile_from_table_row(row, match_page)
                    players.append(player_profile)


                #save profiles to db
                PlayerProfileBuilder.save_player_profiles(players, postgres_connector)
        except:
            logging("Error saving player profiles on " + match_page.url_for_page())
            return False
        finally:
            postgres_connector.close_connection()
        return True

    @staticmethod
    def scrape_match_player_shots(match_id, match_page, postgres_connector=None):
        # Get shots data/table
        all_shots_div = match_page.get_all_shots_div()
        match_player_shots_table_body = match_page.get_player_shots_table_body(all_shots_div)

        # get player shots data rows
        player_match_shots_rows = match_page.get_player_shots_rows(match_player_shots_table_body)

        #open postgres connector if none exists
        if(postgres_connector is None):
            was_postgres_connector_none = True
            postgres_connector = PostgresConnector()
            postgres_connector.open_connection_cursor("premier_league_stats")
        try:
            for row in player_match_shots_rows:
                # get player shot
                player_shot = PlayerMatchStatShotTableUtil.get_player_shots_from_rows(row, match_page, match_id)
                # save player shot
                PlayerMatchStatShotTableUtil.save_player_match_shot(player_shot, postgres_connector)
        except Exception as e:
            logging("Error scraping player shots for match id: " + match_id)
            return False
        finally:
            postgres_connector.close_connection()
        return True


    @staticmethod
    def save_match_import_status(match_id, save_status, postgres_connector=None):
        try:
            if(postgres_connector is None):
                postgres_connector = PostgresConnector()
                postgres_connector.open_connection_cursor("premier_league_stats")

            query = "INSERT INTO public.match_imported_status(match_id, match_imported) VALUES (\'" + match_id + "\'," + str(save_status) + " )"
            parameters = ()
            postgres_connector.execute_parameterized_insert_query(query, parameters)
        except Exception as e:
            logging(e)
            return False
        finally:
            postgres_connector.close_connection()
        return True

