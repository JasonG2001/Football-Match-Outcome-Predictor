from football_dataframe import FootballDataframe
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

class Model:

    def __init__(self, football_league: str):

        self.football_dataframe = FootballDataframe(football_league)


    def make_pipeline(self):

        pipe = make_pipeline(

            StandardScaler(), # Scaling the data
            LinearRegression() # Type of prediction

        )

        return pipe


    def get_training_and_testing_set(self):    

        df = self.football_dataframe.make_dataframe()

        X = df[["Wins", "Streaks"]]
        y = df["Goals"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

        return X_train, X_test, y_train, y_test


    def fit_and_predict(self):

        pipe = self.make_pipeline()
        X_train, X_test, y_train, _ = self.get_training_and_testing_set()

        pipe.fit(X_train, y_train)
        return pipe.predict(X_test)

    
    def plot_correlation(self):

        y_pred = self.fit_and_predict()
        _, _, _, y_test = self.get_training_and_testing_set()

        plt.scatter(y_pred, y_test)

        return plt.show()


if __name__ == "__main__":

    model = Model("premier_league")
    # print(model.get_training_and_testing_set())
    # print(model.get_training_and_testing_set())
    # print(model.fit_and_predict())
    model.plot_correlation()

