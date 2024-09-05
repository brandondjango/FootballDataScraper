import re
import time

from selenium.webdriver.common.by import By


class SeasonScoresAndFixturesPage:

    def __init__(self, driver):
        self.driver = driver

    def url_for_page(self, competition_id = "9", season_year = "2023-2024"):
        return "https://fbref.com/en/comps/" + competition_id + "/" + season_year + "/schedule/"

    def wait_for_games_to_load(self):
        while(len(self.driver.find_elements(By.XPATH, f"//a[text()='Match Report']")) < 379):
            time.sleep(3)

    def fetch_season_game_ids(self):
        match_tds = self.driver.find_elements(By.XPATH, f"//a[text()='Match Report']")
        print(len(match_tds))

        matches = []

        for match_cell in match_tds:
            #match_link = match_cell.find_element(By.XPATH, f".//a").get_attribute("href")
            match_link = match_cell.get_attribute("href")
            match_id = re.search(r'/([a-zA-Z0-9]{8})/', match_link)

            matches.append(match_id.group(1))

        return matches

