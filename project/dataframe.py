from result_finder import ResultFinder
import pandas as pd

class DataframeAnalysis:

    def __init__(self):

        self.result_finder = ResultFinder()

    def get_dataframe(self, football_league: str, year: int):
        
        result: str = self.result_finder.get_results(football_league, year)
            
        try:

            df = pd.read_csv(fr"/home/jason2001/Football-Match-Outcome-Predictor/project/Football/Results/{football_league}/{result}")

            print(df)

        except FileNotFoundError:

            print("The football league or annual results cannot be found. Please check the league name is correct or year is correct.")

    


if __name__ == "__main__":

    dataframe = DataframeAnalysis()
    dataframe.get_dataframe("premier_league", 20)