from football_dataframe import FootballDataframe

class MakeCSV:

    def __init__(self, football_league: str):

        self.football_league: str = football_league 
        self.football_dataframe = FootballDataframe(football_league)


    def convert_to_csv(self, year: int):

        df = self.football_dataframe.clean_dataframe(year)

        return df.to_csv(fr"/home/jason2001/Football-Match-Outcome-Predictor/project/{self.football_league}_{year}_cleaned_dataset.csv")


if __name__ == "__main__":

    csv = MakeCSV("premier_league")
    csv.convert_to_csv(2021)