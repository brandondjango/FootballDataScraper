import random
import string
import uuid
from src.database_connector.postgres_connector import PostgresConnector
from selenium.webdriver.common.by import By


class PlayerMatchStatShotTableUtil:

    @staticmethod
    def get_player_shots_from_rows(row, match_page, match_id):
        row_cells = match_page.get_stats_from_player_rows(row)
        player_shots_stats = {}

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

        for stat in row_cells:
            player_shots_stats[stat.get_attribute("data-stat")] = stat.text

        return player_shots_stats

    @staticmethod
    def save_player_match_shot(player_shot, postgres_connector):
        try:
            shot_id = PlayerMatchStatShotTableUtil.generate_unique_id(player_shot)

            try:
                query = "INSERT INTO public.match_shots_stats(shot_id) VALUES (\'" + shot_id + "\')"
                parameters = ()
                postgres_connector.execute_parameterized_insert_query(query, parameters)
            except Exception as e:
                print(str(e))

            partial_query = ""
            parameters = ()
            #build part of query
            for stat in player_shot.keys():
                partial_query = partial_query + stat + " = (%s),"
                parameters = parameters + (player_shot[stat],)

            #remove last comma
            partial_query = partial_query[:-1]
            query = "UPDATE public.match_shots_stats SET " + partial_query + " WHERE shot_id = (%s);"

            parameters = parameters + (shot_id,)

            try:
                postgres_connector.execute_parameterized_insert_query(query, parameters)
            except Exception as e:
                print("Error inserting player_match_shot: " + str(e))
        except Exception as e:
            print("Skipping shot because of: " + str(e))



    @staticmethod
    def get_sca_player_ids(row, player_shot, match_page):
        match_page.driver.implicitly_wait(2)
        try:
            player_link1 = row.find_element(By.XPATH, ".//*[@data-stat='sca_1_player']").find_element(By.XPATH, ".//a").get_attribute("href")
            print(player_link1)
            player_id1 = match_page.extract_player_id(player_link1)
            print(player_id1)
            player_shot["sca1_player_id"] = player_id1
        except Exception as e:
            print("Skip SCA1")
        try:
            player_link2 = row.find_element(By.XPATH, ".//*[@data-stat='sca_2_player']").find_element(By.XPATH, ".//a").get_attribute("href")
            print(player_link2)
            player_id2 = match_page.extract_player_id(player_link2)
            print(player_id2)
            player_shot["sca2_player_id"] = player_id2
        except Exception as e:
            print("Skip SCA2")
        match_page.driver.implicitly_wait(20)
        return player_shot

    @staticmethod
    def generate_unique_id(player_shot):
        shot_id = player_shot["player_id"] + player_shot["minute"] + player_shot["match_id"] + player_shot["xg_shot"] + player_shot["sca_1_player"] + player_shot["sca_1_type"] + player_shot["sca_2_player"] + player_shot["sca_2_type"]
        shot_id = shot_id.replace(" ", "").replace("(", "").replace(")", "").replace(".", "")
        shot_id = shot_id[:128]
        return str(shot_id)
