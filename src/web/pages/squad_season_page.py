import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
import re

from selenium.webdriver.support.wait import WebDriverWait


class SquadSeasonPage:

    def __init__(self, webdriver):
        self.driver = webdriver

    def url_for_page(self):
        return self.driver.current_url
    @staticmethod
    def url_for_match(team_id, season):
        #season follows format XXXX-XXXX(example: 2023-2024)
        return 'https://fbref.com/en/squads/' + team_id + "/" + season

    def navigate_to_match_url(self, team_id, season):
        self.driver.get(self.url_for_match(team_id, season))

    def standard_stats_table(self):
        return self.driver.find_element(By.ID, "all_stats_standard")

    def table_body_for_standard_stats(self):
        return self.standard_stats_table().find_element(By.XPATH, ".//tbody")

    def get_player_table_rows_for_standard_stats(self):
        cells = self.table_body_for_standard_stats().find_elements(By.XPATH, f".//th[@data-stat='player']")
        rows = []
        for cell in cells:
            rows.append(cell.find_element(By.XPATH, ".."))
        return rows

    def get_player_row_data_stat_text(self, tr, stat_name):
        return tr.find_element(By.XPATH, f".//th[@data-stat='" + stat_name + "']").text.lstrip()

    def get_summary_player_row_data_stat_id(self, tr):
        return tr.find_element(By.XPATH, f".//th").get_attribute("data-append-csv")

