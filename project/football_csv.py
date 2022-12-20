from football_dataframe import FootballDataframe
from typing import Type
import pandas as pd

class MakeCSV:

    def __init__(self) -> None:

        self.football_dataframe = FootballDataframe()


    def convert_to_csv(self, football_league: str, year: int) -> None:

        df: Type[pd.DataFrame] = self.football_dataframe.clean_dataframe(football_league, year)

        df.to_csv(fr"/home/jason2001/Football-Match-Outcome-Predictor/project/{football_league}_{year}_cleaned_dataset.csv")


if __name__ == "__main__":

    csv = MakeCSV()
    csv.convert_to_csv("premier_league", 2021)