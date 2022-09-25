from football_dataframe import FootballDataframe

class FootballCSV:

    def __init__(self, football_league: str):

        self.football_dataframe = FootballDataframe(football_league)


    def convert_to_csv(self):

        df = self.football_dataframe.make_dataframe()

        return df.to_csv(r"/home/jason2001/Football-Match-Outcome-Predictor/project/cleaned_dataset.csv")


if __name__ == "__main__":

    csv = FootballCSV("championship")
    csv.convert_to_csv()