import selenium
from selenium.webdriver.common.by import By


class MatchStatsPage:

    def __init__(self, webdriver):
        self.driver = webdriver

    @staticmethod
    def url_for_match(match_id):
        return 'https://fbref.com/en/matches/' + match_id

    def navigate_to_match_url(self, match_id):
        self.driver.get(self.url_for_match(match_id))

    def get_player_stats_for_match_divs(self):
        return self.driver.find_elements(By.XPATH, f"//div[contains(@id, 'all_player_stats')]")

    def get_summary_stats_table(self, all_player_stat_div):
        all_player_stat_div.find_element(By.XPATH, f".//table[contains(@id, 'summary')]")

    def get_passing_stats_table(self, all_player_stat_div):
        all_player_stat_div.find_element(By.XPATH, f".//table[contains(@id, 'passing')]")

    def get_pass_types_stats_table(self, all_player_stat_div):
        all_player_stat_div.find_element(By.XPATH, f".//table[contains(@id, 'pass_types')]")
