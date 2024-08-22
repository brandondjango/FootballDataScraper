import random
import string
import uuid
from src.database_connector.postgres_connector import PostgresConnector


class PlayerMatchStatShotTableUtil:

    @staticmethod
    def get_player_shots_from_rows(row, match_page, match_id):
        row_cells = match_page.get_stats_from_player_rows(row)
        player_shots_stats = {}

        for stat in row_cells:
            player_shots_stats[stat.get_attribute("data-stat")] = stat.text

            #get shot minute
            minute = match_page.get_shot_minute(row)
            player_shots_stats["minute"] = minute

            #get player id
            player_id = match_page.get_player_shot_row_data_stat_id(row)
            player_shots_stats["player_id"] = player_id

            #get player name
            player = match_page.get_shot_player_row_data_name(row)
            player_shots_stats["player"] = player

            #set match_id
            player_shots_stats["match_id"] = match_id

        return player_shots_stats

    @staticmethod
    def save_player_match_shot(player_shot, postgres_connector):
        shot_id = PlayerMatchStatShotTableUtil.generate_unique_id(player_shot)

        try:
            query = "INSERT INTO public.match_shots_stats(shot_id) VALUES (\'" + shot_id + "\')"
            parameters = ()
            postgres_connector.execute_parameterized_insert_query(query, parameters)
        except Exception as e:
            print(str(e))

        try:
            for stat in player_shot.keys():
                query = "UPDATE public.match_shots_stats SET " + stat + " = (%s) WHERE shot_id = (%s);"
                parameters = (player_shot[stat], shot_id)
                postgres_connector.execute_parameterized_insert_query(query, parameters)
        except Exception as e:
            print("Error inserting player_match_shot: " + str(e))

    @staticmethod
    def generate_unique_id(player_shot):
        shot_id = player_shot["player_id"] + player_shot["minute"] + player_shot["match_id"] + player_shot["xg_shot"] + player_shot["sca_1_player"] + player_shot["sca_1_type"] + player_shot["sca_2_player"] + player_shot["sca_2_type"]
        shot_id = shot_id.replace(" ", "").replace("(", "").replace(")", "").replace(".", "")
        shot_id = shot_id[:128]
        return str(shot_id)
