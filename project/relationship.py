import os
import pandas as pd

class ResultFinder:

    def get_football_league(self, path):

        for football_league in os.listdir(path):
            
            return football_league
        

df = pd.read_csv(r"/home/jason2001/Football-Match-Outcome-Predictor/project/Football/Results/2_liga/Results_1990_2_liga.csv")
home_team = set(df["Home_Team"])
away_team = set(df["Away_Team"])
home_team.update(away_team)

print(len(home_team))

if __name__ == "__main__":

    result_finder = ResultFinder()
    result_finder.get_football_league(r"/home/jason2001/Football-Match-Outcome-Predictor/project/Football/Results")




