from result_finder import ResultFinder
import os
import pandas as pd
import pickle

class DataframeAnalysis:

    def __init__(self, football_league: str):

        self.football_league: str = football_league
        self.result_finder = ResultFinder(football_league)
        self.INDEX_OF_HOME_TEAM_SCORE: int = 0
        self.INDEX_OF_AWAY_TEAM_SCORE: int = 2


    def get_dataframe(self, year: int):
        
        result: str = self.result_finder.get_results(year)
            
        df = pd.read_csv(fr"/home/jason2001/Football-Match-Outcome-Predictor/project/Football/Results/{self.football_league}/{result}")

        return df


    def get_elo(self) -> dict:

        elo: dict[str,dict[str,float]] = pickle.load(open('/home/jason2001/Football-Match-Outcome-Predictor/project/elo_dict.pkl', 'rb'))

        return elo


    def get_team_template(self, year: int):

        home_teams = self.get_dataframe(year)["Home_Team"]
        away_teams = self.get_dataframe(year)["Away_Team"]

        teams: set(str) = set(home_teams)
        
        teams.update(set(away_teams))

        empty_dictionary: dict[str,int] = {}

        for team in teams:

            empty_dictionary[team] = 0

        return empty_dictionary


    def get_home_and_away_elos(self, year: int):

        links = self.get_dataframe(year).loc[:, "Link"]
        elo: dict[str,dict[str,float]] = self.get_elo()
        home_elos: list[float] = []
        away_elos: list[float] = []

        link: str
        for _, link in enumerate(links):

            home_elos.append(elo[link]["Elo_home"])
            away_elos.append(elo[link]["Elo_away"])
            
        return home_elos, away_elos


    def get_home_and_away_goals_so_far(self, year: int):

        team_template: dict[str,int] = self.get_team_template(year)

        df = self.get_dataframe(year).loc[:, ["Home_Team", "Away_Team", "Result"]]
        home_goals_so_far: list[int] = []
        away_goals_so_far: list[int] = []

        for _, record in df.iterrows():

            home_team: str = record.loc["Home_Team"]
            away_team: str = record.loc["Away_Team"]

            home_team_score: int = int(record.loc["Result"][self.INDEX_OF_HOME_TEAM_SCORE])
            away_team_score: int = int(record.loc["Result"][self.INDEX_OF_AWAY_TEAM_SCORE])

            team_template[home_team] += home_team_score
            team_template[away_team] += away_team_score

            home_goals_so_far.append(team_template[home_team])
            away_goals_so_far.append(team_template[away_team])

        return home_goals_so_far, away_goals_so_far

            

            
        
        #for record in 

        


    def get_wins_so_far(self):

        pass


    def get_streak_so_far(self):

        pass

        





if __name__ == "__main__":

    dataframe1 = DataframeAnalysis("premier_league")
    dataframe2 = DataframeAnalysis("championship")
    #print(dataframe1.get_home_and_away_elos("2021"))
    print(dataframe1.get_home_and_away_goals_so_far("2021"))