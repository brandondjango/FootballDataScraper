import selenium

from src.data_scraper.match_scraper import MatchScraper
from src.web.driver_manager.driver_manager import DriverManager
from src.web.pages.season_scores_and_fixtures_page import SeasonScoresAndFixturesPage


class MatchFetcher:

    @staticmethod
    def fetch_matches_from_season_scores_and_fixtures_page(comp_id, season, driver=None):

        if (driver is None):
            driver_manager = DriverManager()
            driver = DriverManager.get_driver(driver_manager)

        season_scores_and_fixtures_page = SeasonScoresAndFixturesPage(driver)
        driver.get(season_scores_and_fixtures_page.url_for_page(comp_id, season))

        #season_scores_and_fixtures_page.wait_for_games_to_load()

        match_ids = season_scores_and_fixtures_page.fetch_season_game_ids()
        driver.close()

        return match_ids




