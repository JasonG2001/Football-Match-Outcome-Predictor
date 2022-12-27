import os
import pandas as pd
import pickle
from typing import Dict, List, Type

class NewResult:

    def __init__(self) -> None:
        pass

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
        