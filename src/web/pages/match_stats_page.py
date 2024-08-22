import selenium
from selenium.webdriver.common.by import By
import re


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
        return all_player_stat_div.find_element(By.XPATH, f".//table[contains(@id, 'summary')]")

    def get_summary_stats_table_body(self, all_player_stat_div):
        return all_player_stat_div.find_element(By.XPATH, f".//table[contains(@id, 'summary')]").find_element(By.XPATH, f".//tbody")

    def get_player_rows_from_tbody(self, tbody):
        return tbody.find_elements(By.XPATH, f".//tr")

    def get_stats_from_player_rows(self, tr):
        return tr.find_elements(By.XPATH, f".//td")

    def get_player_row_data_stat_text(self, tr, stat_name):
        return tr.find_element(By.XPATH, f".//th[contains(@data-stat, '" + stat_name + "')]").text.lstrip()

    def get_summary_player_row_data_stat_id(self, tr):
        return tr.find_element(By.XPATH, f".//th").get_attribute("data-append-csv")

    def get_player_shot_row_data_stat_id(self, tr):
        return tr.find_element(By.XPATH, f".//td").get_attribute("data-append-csv")

    def get_player_row_data_name(self, tr):
        return tr.find_element(By.XPATH, f".//th").text.lstrip()

    def get_shot_player_row_data_name(self, tr):
        return tr.find_element(By.XPATH, f".//td").text.lstrip()

    def get_passing_stats_table(self, all_player_stat_div):
        return all_player_stat_div.find_element(By.XPATH, f".//table[contains(@id, 'passing')]")

    def get_pass_types_stats_table(self, all_player_stat_div):
        return all_player_stat_div.find_element(By.XPATH, f".//table[contains(@id, 'pass_types')]")

    def print_data_stats(self, div):
        data_cells = div.find_element(By.XPATH, f".//thead").find_elements(By.XPATH, f".//th")
        for cell in data_cells:
            if "header" not in cell.get_attribute("data-stat"):
                print(cell.get_attribute("data-stat"))

    def get_all_shots_div(self):
        return self.driver.find_element(By.ID, "shots_all")

    def get_player_shots_table_body(self, all_player_stat_div):
        return all_player_stat_div.find_element(By.XPATH, f".//tbody")

    def get_player_shots_rows(selfself, tbody):
        return tbody.find_elements(By.XPATH, f".//tr")
