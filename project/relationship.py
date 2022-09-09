import os
import pandas as pd

class ResultFinder:

    def go_to_football_league(self, football_league: str) -> None:

        try:

            os.chdir(fr"/home/jason2001/Football-Match-Outcome-Predictor/project/Football/Results/{football_league}")

        except FileNotFoundError:

            print("This football league results cannot be found, please check the spelling.")

    def get_results(self, football_league: str, year: int):

        self.go_to_football_league(football_league)



if __name__ == "__main__":

    PATH = r"/home/jason2001/Football-Match-Outcome-Predictor/project/Football/Results"
    result_finder = ResultFinder()
    result_finder.go_to_football_league("2_lig")


