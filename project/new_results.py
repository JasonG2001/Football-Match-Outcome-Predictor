from result_finder import ResultFinder
from typing import Dict, List, Type
import os
import pandas as pd
import pickle

class NewResult:

    def __init__(self) -> None:
        self.result_finder: ResultFinder = ResultFinder()


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


    def save_to_csv(self, dataframe: Type[pd.DataFrame]) -> None:

        dataframe.to_csv("/home/jason2001/Football-Match-Outcome-Predictor/project/results_for_prediction.csv", 
        index=False)

        