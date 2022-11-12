from result_finder import ResultFinder
import os
import pandas as pd
import pickle

class DataframeAnalysis:

    def __init__(self, football_league: str):

        self.football_league: str = football_league
        self.result_finder = ResultFinder(football_league)
        self.INDEX_OF_AWAY_TEAM = 2


    def get_dataframe(self, year: int):
        
        result: str = self.result_finder.get_results(year)
            
        df = pd.read_csv(fr"/home/jason2001/Football-Match-Outcome-Predictor/project/Football/Results/{self.football_league}/{result}")

        return df


    def get_elo(self) -> dict:

        elo: dict[str,dict[str,float]] = pickle.load(open('/home/jason2001/Football-Match-Outcome-Predictor/project/elo_dict.pkl', 'rb'))

        return elo


    def add_elo_feature(self, year: int):

        links = self.get_dataframe(year).loc[:, "Link"]
        elo: dict[str,dict[str,float]] = self.get_elo()
        home_elos: list[float] = []
        away_elos: list[float] = []

        for _, link in enumerate(links):

            home_elos.append(elo[link]["Elo_home"])
            away_elos.append(elo[link]["Elo_away"])

        





if __name__ == "__main__":

    dataframe1 = DataframeAnalysis("premier_league")
    dataframe2 = DataframeAnalysis("championship")
    print(dataframe1.add_elo_feature("2021"))