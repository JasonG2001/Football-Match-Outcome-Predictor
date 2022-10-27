from football_dataframe import FootballDataframe
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import RepeatedKFold
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt


class Model:

    def __init__(self, football_league: str):

        self.football_dataframe = FootballDataframe(football_league)


    def train_test_split(self):

        df = self.football_dataframe.make_dataframe()
        X = df[["Wins", "Streaks"]]
        y = df["Goals"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

        return X_train, X_test, y_train, y_test
        

    def simple_linear_regression(self):

        X_train, X_test, y_train, y_test = self.train_test_split()
        
        model = LinearRegression(n_jobs=-1)
        trained_model = model.fit(X_train, y_train)

        return trained_model # r2 = 0.9850585149465104


    def linear_regression_pipeline(self):

        X_train, X_test, y_train, y_test = self.train_test_split()

        pipe = make_pipeline(

            StandardScaler(), # Scaling the data
            LinearRegression() # Type of prediction

        )

        trained_pipe = pipe.fit(X_train, y_train)

        return trained_pipe # 0.9850585149465104 


    def decision_tree_regressor(self):

        X_train, X_test, y_train, y_test = self.train_test_split()

        model = DecisionTreeRegressor(random_state=0)
        trained_model = model.fit(X_train, y_train)

        return trained_model # 0.9820554696946081 


    def gradient_boosting_regressor(self):

        X_train, X_test, y_train, y_test = self.train_test_split()

        model = GradientBoostingRegressor(random_state=0)

        trained_model = model.fit(X_train, y_train)

        return trained_model # 0.986401522797169

    
    def plot_model(self, model):

        X_train, X_test, y_train, y_test = self.train_test_split()

        y_pred = model.predict(X_test)

        plt.scatter(y_pred, y_test)
        plt.xlabel("prediction")
        plt.ylabel("true value")

        return plt.show()


    def score_model(self, model):

        X_train, X_test, y_train, y_test = self.train_test_split()

        y_pred = model.predict(X_test)

        return r2_score(y_pred, y_test)


if __name__ == "__main__":

    model = Model("premier_league")
    model2 = Model("ligue_2")

    mod = model.linear_regression_pipeline()
    print(model.score_model(mod))
    model.plot_model(mod)

