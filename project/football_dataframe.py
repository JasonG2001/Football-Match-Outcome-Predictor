from dataframe import DataframeAnalysis
import pandas as pd

class FootballDataframe:

    def __init__(self, football_league: str):

        self.football_league = football_league
        self.dataframe = DataframeAnalysis(football_league)


    def