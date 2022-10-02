from football_dataframe import FootballDataframe
import psycopg2

class database:

    def __init__(self, football_league: str):

        self.dataframe = FootballDataframe(football_league)

    
    def connect_to_rds(self, host: str, user: str, password: str, dbname: str, port: int):

        pass
    
    def give_sql_input(self):

        pass

    