import selenium

from src.database_connector.postgres_connector import PostgresConnector
from src.web.pages.match_stats_page import MatchStatsPage


class PlayerProfileBuilder:

    @staticmethod
    def build_player_profile_from_table_row(tr, match_page):
        player_stat_names = ["player"]
        for stat in player_stat_names:
            #new player profile
            player_profile = {}

            #pull stat from row
            stat_value = match_page.get_player_row_data_stat_text(tr, stat)

            # add to profile, remove leading white space
            player_profile[stat] = stat_value.lstrip()

            #pull id from player
            if stat == "player":
                player_id = match_page.get_summary_player_row_data_stat_id(tr)
                player_profile["id"] = player_id

            return player_profile

    @staticmethod
    def save_player_profile(player_profile):
        postgres_connector = PostgresConnector()

        query = "INSERT INTO players(player_id, player_name) VALUES (%s, %s)"
        parameters = (player_profile["id"], player_profile["player"])
        postgres_connector.execute_parameterized_insert_query("premier_league_stats", query, parameters)

    @staticmethod
    def update_player_profile(player_profile):
        postgres_connector = PostgresConnector()

        query = "UPDATE players SET player_name = %s where player_id = %s"
        parameters = (player_profile["player"], player_profile["id"])
        print(parameters)
        postgres_connector.execute_parameterized_insert_query("premier_league_stats", query, parameters)


