from football_dataframe import FootballDataframe
import psycopg2

class database:

    def __init__(self, football_league: str):

        self.dataframe = FootballDataframe(football_league)

    