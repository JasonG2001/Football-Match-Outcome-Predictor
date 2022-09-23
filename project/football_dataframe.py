from dataframe import DataframeAnalysis
import pandas as pd

class FootballDataframe:

    def __init__(self, football_league: str):

        self.football_league = football_league
        self.dataframe = DataframeAnalysis(football_league)


    def make_dataframe(self):

        wins: dict[str:int] = self.dataframe.get_win_board_over_all_years()

        return pd.DataFrame.from_dict(wins, orient="index")


if __name__ == "__main__":

    football_dataframe = FootballDataframe("premier_league")
    print(football_dataframe.make_dataframe())