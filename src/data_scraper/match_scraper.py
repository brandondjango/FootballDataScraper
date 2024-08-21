from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import selenium
from selenium.webdriver.common.by import By

from src.player_data.player_match_stat_util import PlayerMatchStatUtil
from src.player_data.player_shot_data_util import MatchShotsStatsUtil


class MatchScraper:

    def url(self, id):
        return 'https://fbref.com/en/matches/' + id

    def scrape_match(self, match_id):
        #open chrome
        chrome_options = Options()
        chrome_options.add_argument("--incognito")  # Use incognito mode

        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities['browserName'] = 'chrome'

        options = webdriver.ChromeOptions()
        options.binary_location = "./chromedriver"


        driver = webdriver.Chrome(options)
        driver.get(self.url(match_id))

        #scrape
        match_stats_tables = driver.find_elements(By.XPATH, f"//*[contains(@id, 'all_player_stats')]")
        for stat_table in match_stats_tables:
            PlayerMatchStatUtil.read_table(match_id, stat_table)

        #shots data
        shots_data_tables = driver.find_elements(By.XPATH, f"//*[contains(@id, 'shots_all')]")
        MatchShotsStatsUtil.read_table(match_id, stat_table)



match = MatchScraper()
match.scrape_match("0b8f50a5")