#external
from selenium.webdriver.common.by import By

from src.player_data.player_match_stats.player_match_stat_reader_util import PlayerMatchStatTableUtil
#internal
from src.web.driver_manager.driver_manager import DriverManager

from src.web.pages.match_stats_page import MatchStatsPage

from src.player_data.player_shots.player_shot_data_util import PlayerMatchStatShotTableUtil

from src.player_data.player_profile.player_profile_builder import PlayerProfileBuilder

class MatchScraper:




    def scrape_match(self, match_id):

        driver_manager = DriverManager()
        driver = DriverManager.get_driver(driver_manager)

        match_page = MatchStatsPage(driver)
        match_page.navigate_to_match_url(match_id)


        match_player_stats_divs = match_page.get_player_stats_for_match_divs()

        #1 div for home team, one for away
        #for div in match_player_stats_divs:
        #    #Get summary stats of match table
        #    match_player_summary_table_body = match_page.get_summary_stats_table_body(div)
#
        #    #build players if they don't exist
        #    player_summary_rows = match_page.get_player_rows_from_tbody(match_player_summary_table_body)
#
        #    #save information from summary table row by row
        #    for row in player_summary_rows:
        #        #build profile
        #        player_profile = PlayerProfileBuilder.build_player_profile_from_table_row(row, match_page)
        #        #save profile to db: player names and ids
        #        PlayerProfileBuilder.save_player_profile(player_profile)
#
        #        #read row of summary table
        #        player_summary = PlayerMatchStatTableUtil.get_summary_match_stats_for_player(row, match_page, match_id)
        #        #write to player_summary db
        #        PlayerMatchStatTableUtil.save_match_summary_stats(player_summary)

        #Get shots data/table
        all_shots_div = match_page.get_all_shots_div()
        match_player_shots_table_body = match_page.get_player_shots_table_body(all_shots_div)

        #get player shots data rows
        player_match_shots_rows = match_page.get_player_shots_rows(match_player_shots_table_body)
        for row in player_match_shots_rows:
            #get player shot
            player_shot = PlayerMatchStatShotTableUtil.get_player_shots_from_rows(row, match_page, match_id)
            #save player shot
            PlayerMatchStatShotTableUtil.save_player_match_shot(player_shot)




        driver.close()




        #shots data
        #shots_data_table = driver.find_element(By.XPATH, f"//*[contains(@id, 'shots_all')]")
        #MatchShotsStatsUtil.read_table(match_id, shots_data_table)



match = MatchScraper()
match.scrape_match("0b8f50a5")