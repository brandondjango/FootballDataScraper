

class PlayerMatchStatShotTableUtil:

    @staticmethod
    def get_player_shots_from_rows(row, match_page, match_id):
        row_cells = match_page.get_stats_from_player_rows(row)
        player_shots_stats = {}

        for stat in row_cells:
            player_shots_stats[stat.get_attribute("data-stat")] = stat.text

            #get player id
            player_id = match_page.get_player_shot_row_data_stat_id(row)
            player_shots_stats["player_id"] = player_id

            #get player name
            player = match_page.get_shot_player_row_data_name(row)
            player_shots_stats["player"] = player

            #set match_id
            player_shots_stats["match_id"] = match_id

        return player_shots_stats

