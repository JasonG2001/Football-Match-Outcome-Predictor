from dataframe import DataframeAnalysis
import pandas as pd

class FootballDataframe:

    def __init__(self, football_league: str):

        self.football_league: str = football_league
        self.dataframe = DataframeAnalysis(football_league)


    def make_dataframe(self):

        indexed_teams: dict[int:str] = self.dataframe.get_teams_indexed()

        df = pd.DataFrame.from_dict(indexed_teams, orient="index")

        win_board: dict[str:int] = self.dataframe.get_win_board_over_all_years()
        wins = list(win_board.values())
        df["wins"] = wins

        streak_board: dict[str:int] = self.dataframe.get_largest_streak_board_over_all_years()
        streaks = list(streak_board.values())
        df["streaks"] = streaks

        goal_board: dict[str:int] = self.dataframe.get_goal_board_over_all_years()
        goals = list(goal_board.values())
        df["goals"] = goals

        return df


if __name__ == "__main__":

    football_dataframe = FootballDataframe("premier_league")
    print(football_dataframe.make_dataframe())