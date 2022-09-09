import os
import pandas as pd

class ResultFinder:

    def get_football_leagues(self, path) -> list:

        football_leagues: list[str] = [] 

        for football_league in os.listdir(path):
            
            football_leagues.append(football_league)

        return football_leagues

if __name__ == "__main__":

    result_finder = ResultFinder()
    result_finder.get_football_leagues(r"/home/jason2001/Football-Match-Outcome-Predictor/project/Football/Results")


