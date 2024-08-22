from src.web.pages.match_stats_page import MatchStatsPage
from src.database_connector.postgres_connector import PostgresConnector


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
    def save_match_summary_stats(player_summary_stats):
        postgres_connector = PostgresConnector()

        try:
            query = "INSERT INTO public.match_summary_stats(player_id, match_id) VALUES (%s, %s)"
            parameters = (player_summary_stats["player_id"], player_summary_stats["match_id"])
            postgres_connector.execute_parameterized_insert_query("premier_league_stats", query, parameters)
        except Exception as e:
            print("Could not insert because of: " + str(e))
            print("Table has constraint on player_id and match_id combination being unique.")



        for stat in player_summary_stats.keys():
            if (stat != "player_id" and stat != "match_id"):
                query = "UPDATE public.match_summary_stats SET " + stat + " = (%s) WHERE match_id = (%s) and player_id = (%s);"
                parameters = (player_summary_stats[stat], player_summary_stats['match_id'], player_summary_stats['player_id'])
                postgres_connector.execute_parameterized_insert_query("premier_league_stats", query, parameters)



