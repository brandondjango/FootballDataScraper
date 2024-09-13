import os

import selenium


from src.web.driver_manager.driver_manager import DriverManager
from src.web.pages.season_overview_page import SeasonOverviewPage


class SquadFetcher:

    @staticmethod
    def fetch_season_squads(comp_id, season, driver=None):
        try:
            if (driver is None):
                driver_manager = DriverManager()
                driver = DriverManager.get_driver(driver_manager)

            season_overview_page = SeasonOverviewPage(driver)
            driver.get(season_overview_page.url_for_season(comp_id, season))

            team_profiles = season_overview_page.get_team_ids_and_names_tuples()
            driver.close()
            return team_profiles
        except Exception as e:
            print(str(e))



