from dataframe import DataframeAnalysis
import pandas as pd

class FootballDataframe:

    def __init__(self, football_league: str):

        self.football_league: str = football_league
        self.dataframe = DataframeAnalysis(football_league)


    def make_dataframe(self):

        indexed_teams: dict[int:str] = self.dataframe.get_teams_indexed()

        return pd.DataFrame.from_dict(indexed_teams, orient="index")


if __name__ == "__main__":

    football_dataframe = FootballDataframe("premier_league")
    print(football_dataframe.make_dataframe())