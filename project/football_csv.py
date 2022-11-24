from football_dataframe import FootballDataframe

class FootballCSV:

    def __init__(self, football_league: str):

        self.football_dataframe = FootballDataframe(football_league)

    
    def clean_dataset(self, year: int):

        df = self.football_dataframe.make_dataframe(year)
        df["Home_Team_Code"] = df["Home_Team"].astype("category").cat.codes
        df["Away_Team_Code"] = df["Away_Team"].astype("category").cat.codes
        df["Home_Result_Code"] = df["Home_Result"].astype("category").cat.codes
        df["Away_Result_Code"] = df["Away_Result"].astype("category").cat.codes

        return df


    def convert_to_csv(self, year: int):

        df = self.clean_dataset(year)

        return df.to_csv(r"/home/jason2001/Football-Match-Outcome-Predictor/project/cleaned_dataset.csv")


if __name__ == "__main__":

    csv = FootballCSV("premier_league")
    csv.convert_to_csv()