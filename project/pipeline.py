from football_dataframe import FootballDataframe
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

class Model:

    def __init__(self, football_league: str):

        self.football_dataframe = FootballDataframe(football_league)


    def make_pipeline(self):

        pipe = make_pipeline(

            StandardScaler(), # Scaling the data
            LinearRegression() # Type of prediction

        )

        return pipe


    def temp(self):    

        df = self.football_dataframe.make_dataframe()

        X = df[["Wins", "Streaks", "Goals"]]
        y = df["Goals"]




if __name__ == "__main__":

    model = Model("premier_league")
    print(model.make_pipeline())

