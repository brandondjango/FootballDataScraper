from selenium.webdriver.common.by import By

from src.web.driver_manager.driver_manager import DriverManager
from src.web.pages.match_stats_page import MatchStatsPage
from src.player_data.player_shot_data_util import MatchShotsStatsUtil


class MatchScraper:




    def scrape_match(self, match_id):

        driver = DriverManager.get_driver()

        match_page = MatchStatsPage(driver)
        match_page.naviagte_to_match_url(match_id)

        #scrape
        match_player_stats_tables = match_page.get_player_stats_for_match_divs()
        for stat_table in match_player_stats_tables:
            stat_table.find_element(By.XPATH, f".//table[contains(@id, 'summary')]").find_element(By.XPATH, ".//tbody")




        #shots data
        shots_data_table = driver.find_element(By.XPATH, f"//*[contains(@id, 'shots_all')]")
        MatchShotsStatsUtil.read_table(match_id, shots_data_table)



match = MatchScraper()
match.scrape_match("0b8f50a5")