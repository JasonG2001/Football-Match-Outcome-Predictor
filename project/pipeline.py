from football_dataframe import FootballDataframe
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import RepeatedKFold
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split as sklearn_train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt



class Model:

    def __init__(self, football_league: str):

        self.football_dataframe = FootballDataframe(football_league)


    def split_into_train_and_test(self, year: int):

        df = self.football_dataframe.clean_dataframe(year)
        X = df.drop(["Home_Team", "Away_Team", "Home_Result", "Away_Result"], axis=1)
        y = df.loc[:, ["Home_Result_Code", "Away_Result_Code"]]
        
        X_train, X_test, y_train, y_test = sklearn_train_test_split(X, y, test_size=0.2, random_state=0)

        return X_train, X_test, y_train, y_test

    '''
    def simple_linear_regression(self):

        X_train, X_test, y_train, y_test = self.train_test_split()
        
        model = LinearRegression(n_jobs=-1)
        trained_model = model.fit(X_train, y_train)

        return trained_model # 0.9850585149465104


    def linear_regression_pipeline(self):

        X_train, X_test, y_train, y_test = self.train_test_split()

        pipe = make_pipeline(

            StandardScaler(),
            LinearRegression()

        )

        trained_pipe = pipe.fit(X_train, y_train)

        return trained_pipe # 0.9850585149465104 

    @property
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


    def SVR(self):

        X_train, X_test, y_train, y_test = self.train_test_split()

        model = SVR()
        trained_model = model.fit(X_train, y_train)

        return trained_model # -9447.089006984184


    def SVR_tuned(self):

        X_train, X_test, y_train, y_test = self.train_test_split()

        model = SVR()

        kernel = ["linear", "rbf", "sigmoid", "poly"]
        tol = [1e-3, 1e-4, 1e-5]
        C = [1, 1.5, 2, 2.5]

        grid = dict(kernel = kernel, tol = tol, C = C)
        cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)

        grid_search = GridSearchCV(estimator=model, param_grid=grid, n_jobs=-1, cv=cv, scoring="neg_mean_squared_error")

        trained_grid_search = grid_search.fit(X_train, y_train)
        best_model = trained_grid_search.best_estimator_

        return best_model # 0.989734139462195 
    

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
    '''

if __name__ == "__main__":

    model = Model("premier_league")
    print(model.split_into_train_and_test(2021))
    