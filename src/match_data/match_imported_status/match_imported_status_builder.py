from src.database_connector.postgres_connector import PostgresConnector

#todo add more status saving around match importing
class MatchImportStatusTableUtil:

    @staticmethod
    def save_match_status(match_id: str, match_import_status: str, postgres_connector: PostgresConnector=None):
        try:
            if(postgres_connector is None):
                postgres_connector = PostgresConnector()
                postgres_connector.open_connection_cursor("premier_league_stats")
        finally:
            postgres_connector.close_connection()