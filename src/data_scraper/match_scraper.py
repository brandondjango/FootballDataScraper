#external
from selenium.webdriver.common.by import By

#internal
from src.web.driver_manager.driver_manager import DriverManager

from src.web.pages.match_stats_page import MatchStatsPage

from src.player_data.player_shots.player_shot_data_util import MatchShotsStatsUtil

from src.player_data.player_profile.player_profile_builder import PlayerProfileBuilder

class MatchScraper:




    def scrape_match(self, match_id):

        driver_manager = DriverManager()
        driver = DriverManager.get_driver(driver_manager)

        match_page = MatchStatsPage(driver)
        match_page.navigate_to_match_url(match_id)

        #scrape
        match_player_stats_divs = match_page.get_player_stats_for_match_divs()

        #1 table for home team, one for away
        for div in match_player_stats_divs:
            #Get summary stats of match table
            match_player_summary_table_body = match_page.get_summary_stats_table_body(div)

            #build players if they don't exist
            player_rows = match_page.get_player_rows_from_tbody(match_player_summary_table_body)

            for row in player_rows:
                player_profile = PlayerProfileBuilder()
                PlayerProfileBuilder.build_player_profile_from_table_row(player_profile, row, match_page)


        #shots data
        #shots_data_table = driver.find_element(By.XPATH, f"//*[contains(@id, 'shots_all')]")
        #MatchShotsStatsUtil.read_table(match_id, shots_data_table)



match = MatchScraper()
match.scrape_match("0b8f50a5")