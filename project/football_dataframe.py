from dataframe import DataframeAnalysis
from typing import List, Type
import pandas as pd

class FootballDataframe:

    def __init__(self) -> None:

        self.dataframe = DataframeAnalysis()


    def make_dataframe(self, football_league: str, year: int) -> Type[pd.DataFrame]:

        df: Type[pd.DataFrame] = self.dataframe.get_dataframe(football_league, year)
        df: Type[pd.DataFrame] = df.drop(["Result", "Link", "League"], axis=1)

        home_elos, away_elos = self.dataframe.get_home_and_away_elos(football_league, year)
        home_goals_so_far, away_goals_so_far = self.dataframe.get_home_and_away_goals_so_far(football_league, year)
        home_wins_so_far, away_wins_so_far, home_losses_so_far, away_losses_so_far, home_draws_so_far, \
            away_draws_so_far = self.dataframe.get_wins_losses_draws_so_far(football_league, year)
        current_home_streak, current_away_streak = self.dataframe.get_current_streak(football_league, year)
        home_results, away_results = self.dataframe.get_result(football_league, year)

        df["Home_Elos"]: List[float] = home_elos
        df["Away_Elos"]: List[float] = away_elos
        df["Home_Goals"]: List[int] = home_goals_so_far
        df["Away_Goals"]: List[int] = away_goals_so_far
        df["Home_Wins"]: List[int] = home_wins_so_far
        df["Away_Wins"]: List[int] = away_wins_so_far
        df["Home_Losses"]: List[int] = home_losses_so_far
        df["Away_Losses"]: List[int] = away_losses_so_far
        df["Home_Draws"]: List[int] = home_draws_so_far
        df["Away_Draws"]: List[int] = away_draws_so_far
        df["Home_Streak"]: List[int] = current_home_streak
        df["Away_Streak"]: List[int] = current_away_streak

        df["Home_Result"]: List[str] = home_results
        df["Away_Result"]: List[str] = away_results

        return df


    def clean_dataframe(self, football_league: str, year: int) -> Type[pd.DataFrame]:

        df: Type[pd.DataFrame] = self.make_dataframe(football_league, year)
        df["Home_Team_Code"]: List[int] = df["Home_Team"].astype("category").cat.codes
        df["Away_Team_Code"]: List[int] = df["Away_Team"].astype("category").cat.codes
        df["Home_Result_Code"]: List[int] = df["Home_Result"].astype("category").cat.codes
        df["Away_Result_Code"]: List[int] = df["Away_Result"].astype("category").cat.codes

        return df


if __name__ == "__main__":

    football_dataframe = FootballDataframe()
    print(football_dataframe.make_dataframe("premier_league", 2021))
    print(football_dataframe.clean_dataframe("premier_league", 2021))