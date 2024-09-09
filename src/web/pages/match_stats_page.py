import selenium
from selenium.webdriver.common.by import By
import re


class MatchStatsPage:

    def __init__(self, webdriver):
        self.driver = webdriver

    def url_for_page(self):
        return self.driver.current_url
    @staticmethod
    def url_for_match(match_id):
        return 'https://fbref.com/en/matches/' + match_id

    def navigate_to_match_url(self, match_id):
        self.driver.get(self.url_for_match(match_id))

    def match_scorebox(self):
        return self.driver.find_element(By.CLASS_NAME, "scorebox")

    def get_match_date(self):
        try:
            match_date = self.match_scorebox().find_element(By.CLASS_NAME, "venuetime").get_attribute("data-venue-date")
            return match_date
        except Exception as e:
            return ""

    def get_match_competition_id(self):
        try:
            content_div =  self.driver.find_element(By.ID, "content")
            comp_link = content_div.find_element(By.XPATH, f"//a[contains(@href, '/comps/')]").get_attribute("href")
            match = re.search(r'/en/comps/(\d+)/', comp_link)
            if match:
                competition_id = match.group(1)
                return competition_id
            return ""
        except Exception as e:
            return ""

    def get_match_season(self):
        try:
            comp_link = (MatchStatsPage.match_scorebox(self).find_element(By.XPATH, f"//div[contains(text(), 'Matchweek')]")
                         .find_element(By.XPATH, f"./a").get_attribute("href"))

            match = re.search(r'/\d{4}-\d{4}/', comp_link)
            if match:
                match_season = match.group(0)
                match_season = match_season.replace("/", "")
                return match_season
            return ""
        except Exception as e:
            return ""

    def get_home_team(self):
        try:
            home_team = self.match_scorebox().find_elements(By.XPATH, f".//a[contains(@href, 'squads')]")[0].text
            return home_team
        except Exception as e:
            ""

    def get_away_team(self):
        try:
            away_team = self.match_scorebox().find_elements(By.XPATH, f".//a[contains(@href, 'squads')]")[1].text
            return away_team
        except Exception as e:
            return ""

    def get_home_team_score(self):
        try:
            home_team_score = self.match_scorebox().find_elements(By.CLASS_NAME, "score")[0].text
            return home_team_score
        except Exception as e:
            return ""

    def get_away_team_score(self):
        try:
            away_team_score = self.match_scorebox().find_elements(By.CLASS_NAME, "score")[1].text
            return away_team_score
        except Exception as e:
            return ""

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

    def get_shot_minute(self, tr):
        return tr.find_element(By.XPATH, f".//*[contains(@data-stat, 'minute')]").text

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
        return tbody.find_elements(By.XPATH, f".//tr[not(contains(@class, 'spacer'))]")
