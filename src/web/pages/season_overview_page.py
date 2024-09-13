import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
import re

from selenium.webdriver.support.wait import WebDriverWait


class SeasonOverviewPage:

    def __init__(self, webdriver):
        self.driver = webdriver

    def url_for_page(self):
        return self.driver.current_url
    @staticmethod
    def url_for_season(competition_id, season):
        #season follows format XXXX-XXXX(example: 2023-2024)
        return 'https://fbref.com/en/comps/' + competition_id + "/" + season

    def navigate_to_match_url(self, competition_id, season):
        self.driver.get(self.url_for_season(competition_id, season))

    def extract_squad_id(self, team_link):
        # Use regex to find the text between "/squads/" and the next "/"
        match = re.search(r'/squads/([^/]+)/', team_link)

        if match:
            return match.group(1)  # Return the matched group (the squad ID)
        return None
    def get_team_ids_and_names_tuples(self):
        team_profiles = []
        team_table_cells = self.driver.find_elements(By.XPATH, "//td[@data-stat='team']")
        for cell in team_table_cells:
            print(cell.text)
            team_link = cell.find_element(By.XPATH, ".//a").get_attribute("href")
            team_id = self.extract_squad_id(team_link)
            team_name = cell.text.lstrip()
            team = (team_id, team_name)
            team_profiles.append(team)
        return team_profiles
