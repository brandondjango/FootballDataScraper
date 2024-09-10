from src.web.pages.match_stats_page import MatchStatsPage
from src.database_connector.postgres_connector import PostgresConnector
import logging


class PlayerMatchStatTableUtil:

    @staticmethod
    def get_summary_match_stats_for_player(row, match_page, match_id):
        row_cells = match_page.get_stats_from_player_rows(row)
        player_summary_stats = {}

        for stat in row_cells:
            player_summary_stats[stat.get_attribute("data-stat")] = stat.text

        #get player id
        player_id = match_page.get_summary_player_row_data_stat_id(row)
        player_summary_stats["player_id"] = player_id

        #get player name
        player = match_page.get_player_row_data_name(row)
        player_summary_stats["player"] = player

        #set match_id
        player_summary_stats["match_id"] = match_id

        return player_summary_stats

    @staticmethod
    def save_match_summary_stats(player_summary_stats, postgres_connector):
        try:
            query = "INSERT INTO public.match_summary_stats(player_id, match_id) VALUES (%s, %s)"
            parameters = (player_summary_stats["player_id"], player_summary_stats["match_id"])
            postgres_connector.execute_parameterized_insert_query(query, parameters)
        except Exception as e:
            print("Could not insert because of: " + str(e))
            print("Warning: Table has constraint on player_id and match_id combination being unique.")

        partial_query = ""
        parameters = ()
        #build part of query
        for stat in player_summary_stats.keys():
            if (stat != "player_id" and stat != "match_id"):
                partial_query = partial_query + stat + " = (%s),"
                parameters = parameters + (player_summary_stats[stat],)

        #remove last comma
        partial_query = partial_query[:-1]
        #query and params
        query = "UPDATE public.match_summary_stats SET " + partial_query + " WHERE match_id = (%s) and player_id = (%s);"
        parameters = parameters + (player_summary_stats['match_id'], player_summary_stats['player_id'])

        try:
            postgres_connector.execute_parameterized_insert_query(query, parameters)
        except Exception as e:
            print("Could not insert because: " + str(e))

    @staticmethod
    def save_substitute_info_to_match_summary(match_id, substitute_array, postgres_connector):
        try:
            for sub_tuple in substitute_array:
                print(sub_tuple)
                sub_minute = sub_tuple[0]
                subbed_on_player = sub_tuple[1]
                subbed_off_player = sub_tuple[2]


                subbed_on_query = "UPDATE public.match_summary_stats SET subbed_on = (%s) WHERE match_id = (%s) and player_id = (%s);"
                subbed_on_parameters = (sub_minute, match_id, subbed_on_player)

                subbed_off_query = "UPDATE public.match_summary_stats SET subbed_off = (%s) WHERE match_id = (%s) and player_id = (%s);"
                subbed_off_parameters = (sub_minute, match_id, subbed_off_player)

                try:
                    postgres_connector.execute_parameterized_insert_query(subbed_on_query, subbed_on_parameters)
                    postgres_connector.execute_parameterized_insert_query(subbed_off_query, subbed_off_parameters)
                except Exception as e:
                    logging("Could not insert substitution tuple: " + str(e))
        except Exception as e:
            logging("Could not insert substitution information: " + str(e))





