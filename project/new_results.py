from collections import defaultdict
from result_finder import ResultFinder
from typing import Dict, List, Type
import os
import pandas as pd
import pickle

class NewResult:

    def __init__(self) -> None:
        self.result_finder: ResultFinder = ResultFinder()
        self.INDEX_OF_HOME_TEAM_SCORE: int = 0
        self.INDEX_OF_AWAY_TEAM_SCORE: int = 2


    def get_results(self, league: str, path: str) -> Type[pd.DataFrame]:

        os.chdir(path)
        os.chdir(league)

        df: Type[pd.DataFrame] = pd.read_csv(os.listdir()[1])
        elo: Dict[str,Dict[str,str]] = pickle.load(open(os.listdir()[0], "rb"))

        home_elo: List[int] = []
        away_elo: List[int] = []

        link: str
        for link in df.loc[:, "Link"]:
            home_elo.append(int(elo[link]["Elo_home"]))
            away_elo.append(int(elo[link]["Elo_away"]))
        
        df["Home_Elo"]: List[int] = home_elo
        df["Away_Elo"]: List[int] = away_elo
        
        return df


    def combine_all_dataframes(self, path: str) -> type[pd.DataFrame]:

        leagues: List[str] = os.listdir(path)
        leagues: List[str] = [league for league in leagues if league != "previous_elo_dict.pkl"]
        all_data: List[Type[pd.DataFrame]] = []

        all_data: List[Type[pd.DataFrame]] = [self.get_results(league, path) for league in leagues]
        
        df: Type[pd.DataFrame] = pd.concat(all_data)
        
        return df.drop(df.columns[0], axis=1)


    def get_cumulative_home_and_away_goals(self, df: Type[pd.DataFrame]) -> List[int]:

        cumulative_home_goals: List[int] = []
        cumulative_away_goals: List[int] = []

        df: Type[pd.DataFrame] = df.loc[:, ["Home_Team", "Away_Team", "Result"]]
        goals: Dict[str,int] = defaultdict(int)

        record: Type[pd.DataFrame]
        for _, record in df.iterrows():
            home_team: str = record.loc["Home_Team"]
            away_team: str = record.loc["Away_Team"]

            cumulative_home_goals.append(goals[home_team])
            cumulative_away_goals.append(goals[away_team])

            goals[home_team] += int(record.loc["Result"][self.INDEX_OF_HOME_TEAM_SCORE])
            goals[away_team] += int(record.loc["Result"][self.INDEX_OF_AWAY_TEAM_SCORE])

        return cumulative_home_goals, cumulative_away_goals


    def get_cumulative_home_and_away_wins(self, df: Type[pd.DataFrame]) -> List[int]:

        cumulative_home_wins: List[int] = []
        cumulative_away_wins: List[int] = []
        cumulative_home_losses: List[int] = []
        cumulative_away_losses: List[int] = []
        cumulative_home_draws: List[int] = []
        cumulative_away_draws: List[int] = []

        df: Type[pd.DataFrame] = df.loc[:, ["Home_Team", "Away_Team", "Result"]]
        wins: Dict[str,int] = defaultdict(int)
        losses: Dict[str,int] = defaultdict(int)
        draws: Dict[str,int] = defaultdict(int)

        record: Type[pd.DataFrame]
        for _, record in df.iterrows():
            home_team: str = record.loc["Home_Team"]
            away_team: str = record.loc["Away_Team"]

            cumulative_home_wins.append(wins[home_team])
            cumulative_away_wins.append(wins[away_team])
            cumulative_home_losses.append(losses[home_team])
            cumulative_away_losses.append(losses[away_team])
            cumulative_home_draws.append(draws[home_team])
            cumulative_away_draws.append(draws[away_team])

            home_score: int = int(record.loc["Result"][self.INDEX_OF_HOME_TEAM_SCORE])
            away_score: int = int(record.loc["Result"][self.INDEX_OF_AWAY_TEAM_SCORE])

            if home_score > away_score:
                wins[home_team] += 1
                losses[away_team] += 1

            elif home_score < away_score:
                wins[away_team] += 1
                losses[home_team] += 1

            else: 
                draws[home_team] += 1
                draws[away_team] += 1

        return cumulative_home_wins, cumulative_away_wins, cumulative_home_losses, cumulative_away_losses, \
            cumulative_home_draws, cumulative_away_draws


    def get_current_streak(self, df: Type[pd.DataFrame]) -> List[int]:

        current_home_streak: List[int] = []
        current_away_streak: List[int] = []

        df: Type[pd.DataFrame] = df.loc[:, ["Home_Team", "Away_Team", "Result"]]
        current_streak: Dict[str,int] = defaultdict(int)

        record: Type[pd.DataFrame]
        for _, record in df.iterrows():
            home_team: str = record.loc["Home_Team"]
            away_team: str = record.loc["Away_Team"]

            current_home_streak.append(current_streak[home_team])
            current_away_streak.append(current_streak[away_team])

            home_score: int = int(record.loc["Result"][self.INDEX_OF_HOME_TEAM_SCORE])
            away_score: int = int(record.loc["Result"][self.INDEX_OF_AWAY_TEAM_SCORE])

            if home_score > away_score:
                current_streak[home_team] += 1
                current_streak[away_team] = 0

            elif home_score < away_score:
                current_streak[away_team] += 1
                current_streak[home_team] = 0

            else:
                current_streak[home_team] = 0
                current_streak[away_team] = 0

        return current_home_streak, current_away_streak


    def get_results(self, df: Type[pd.DataFrame]) -> List[str]:

        home_result: List[str] = []
        away_result: List[str] = []

        for result in df["Result"]:

            home_score: int = int(result[self.INDEX_OF_HOME_TEAM_SCORE])
            away_score: int = int(result[self.INDEX_OF_AWAY_TEAM_SCORE])

            if home_score > away_score:
                home_result.append("win")
                away_result.append("lose")

            elif home_score < away_score:
                home_result.append("lose")
                away_result.append("win")

            else:
                home_result.append("draw")
                away_result.append("draw")

        return home_result, away_result


    def combine_features(self, df: Type[pd.DataFrame]) -> Type[pd.DataFrame]:

        cumulative_home_goals, cumulative_away_goals = self.get_cumulative_home_and_away_goals(df)
        cumulative_home_wins, cumulative_away_wins, cumulative_home_losses, cumulative_away_losses, \
            cumulative_home_draws, cumulative_away_draws = self.get_cumulative_home_and_away_wins(df)
        current_home_streak, current_away_streak = self.get_current_streak(df)
        home_result, away_result = self.get_results(df)

        df["Current_Home_Goals"]: List[int] = cumulative_home_goals
        df["Current_Away_Goals"]: List[int] = cumulative_away_goals
        df["Current_Home_Wins"]: List[int] = cumulative_home_wins
        df["Current_Away_Wins"]: List[int] = cumulative_away_wins
        df["Current_Home_Losses"]: List[int] = cumulative_home_losses
        df["Current_Away_Losses"]: List[int] = cumulative_away_losses
        df["Current_Home_Draws"]:List[int] = cumulative_home_draws
        df["Current_Away_Draws"]: List[int] = cumulative_away_draws
        df["Current_Home_Streak"]: List[int] = current_home_streak
        df["Current_Away_Streak"]: List[int] = current_away_streak

        df["Home_Result"]: List[str] = home_result
        df["Away_Result"]: List[str] = away_result

        return df


    def clean_dataframe(self, df: Type[pd.DataFrame]) -> Type[pd.DataFrame]:

        df["Home_Team_Code"]: List[int] = df["Home_Team"].astype("category").cat.codes
        df["Away_Team_Code"]: List[int] = df["Away_Team"].astype("category").cat.codes
        df["Home_Team_Result"]: List[int] = df["Home_Result"].astype("category").cat.codes
        df["Away_Team_Result"]: List[int] = df["Away_Result"].astype("category").cat.codes

        return df


    def save_to_csv(self, df: Type[pd.DataFrame], name: str) -> None:

        df.to_csv(f"/home/jason2001/Football-Match-Outcome-Predictor/project/{name}.csv", 
        index=False)

        