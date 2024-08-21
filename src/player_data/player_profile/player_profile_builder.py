import selenium

from src.web.pages.match_stats_page import MatchStatsPage


class PlayerProfileBuilder:

    def build_player_profile_from_table_row(self, tr, match_page):
        player_stat_names = ["player"]
        for stat in player_stat_names:
            #new player profile
            player_profile = {}

            #pull stat from row
            stat_value = match_page.get_player_row_data_stat_text(tr, stat)

            # add to profile
            player_profile[stat] = stat_value

            #pull id from player
            if stat == "player":
                player_id = match_page.get_player_row_data_stat_id(tr)
                player_profile["id"] = player_id

            print(player_profile)

