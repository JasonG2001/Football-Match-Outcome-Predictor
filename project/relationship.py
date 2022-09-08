import os
import pandas as pd

class ResultFinder:

    def __init__(self, path):

        self.path = path
        
    def get_foot_league(self):
        pass

df = pd.read_csv(r"/home/jason2001/Football-Match-Outcome-Predictor/project/Football/Results/2_liga/Results_1990_2_liga.csv")
home_team = set(df["Home_Team"])
away_team = set(df["Away_Team"])
home_team.update(away_team)

print(len(home_team))




