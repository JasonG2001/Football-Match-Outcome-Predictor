from dataframe import DataframeAnalysis
import pandas as pd

class FootballDataframe:

    def __init__(self, football_league: str):

        self.dataframe = DataframeAnalysis(football_league)


    def make_dataframe(self, year: int):

        df = self.dataframe.get_dataframe(year)
        df = df.drop(["Result", "Link", "League"], axis=1)

        home_elos, away_elos = self.dataframe.get_home_and_away_elos(year)
        home_goals_so_far, away_goals_so_far = self.dataframe.get_home_and_away_goals_so_far(year)
        home_wins_so_far, away_wins_so_far, home_losses_so_far, away_losses_so_far, home_draws_so_far, away_draws_so_far = self.dataframe.get_wins_losses_draws_so_far(year)
        current_home_streak, current_away_streak = self.dataframe.get_current_streak(year)

        df["Home_Elos"] = home_elos
        df["Away_Elos"] = away_elos
        df["Home_Goals"] = home_goals_so_far
        df["Away_Goals"] = away_goals_so_far
        df["Home_Wins"] = home_wins_so_far
        df["Away_Wins"] = away_wins_so_far
        df["Home_Losses"] = home_losses_so_far
        df["Away_Losses"] = away_losses_so_far
        df["Home_Draws"] = home_draws_so_far
        df["Away_Draws"] = away_draws_so_far
        df["Home_Streak"] = current_home_streak
        df["Away_Streak"] = current_away_streak

        return df


if __name__ == "__main__":

    football_dataframe = FootballDataframe("premier_league")
    print(football_dataframe.make_dataframe("2021"))