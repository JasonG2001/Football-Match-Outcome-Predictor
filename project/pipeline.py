from football_dataframe import FootballDataframe
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier as sklearn_random_forest
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split as sklearn_train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


class Model:

    def __init__(self, football_league: str):

        self.football_dataframe = FootballDataframe(football_league)


    def split_into_train_and_test(self, year: int):

        df = self.football_dataframe.clean_dataframe(year)
        X = df.drop(["Home_Team", "Away_Team", "Home_Result", "Away_Result", "Home_Result_Code", "Away_Result_Code"], axis=1)
        y = df["Home_Result_Code"]
        
        X_train, X_test, y_train, y_test = sklearn_train_test_split(X, y, test_size=0.2, random_state=0)

        return X_train, X_test, y_train, y_test


    def random_forest_classifier(self, year: int) -> float:

        X_train, X_test, y_train, y_test = self.split_into_train_and_test(year)

        trained_model = make_pipeline(StandardScaler(), sklearn_random_forest()).fit(X_train, y_train)
        y_pred = trained_model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)

        return acc


    def logistic_regressor(self, year: int) -> float:

        X_train, X_test, y_train, y_test = self.split_into_train_and_test(year)

        trained_model = make_pipeline(StandardScaler(), LogisticRegression()).fit(X_train, y_train)

        y_pred = trained_model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)

        return acc


    def k_nearest_neighbour(self, year: int) -> float:

        X_train, X_test, y_train, y_test = self.split_into_train_and_test(year)

        trained_model = make_pipeline(StandardScaler(), KNeighborsClassifier()).fit(X_train, y_train)

        y_pred = trained_model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)

        return acc


    def decision_tree_classifier(self, year) -> float:

        X_train, X_test, y_train, y_test = self.split_into_train_and_test(year)

        trained_model = make_pipeline(StandardScaler(), DecisionTreeClassifier()).fit(X_train, y_train)

        y_pred = trained_model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)

        return acc


    def gaussiannb(self, year) -> float:

        X_train, X_test, y_train, y_test = self.split_into_train_and_test(year)

        trained_model = make_pipeline(StandardScaler(), GaussianNB()).fit(X_train, y_train)

        y_pred = trained_model.predict(X_test)
        acc: float = accuracy_score(y_test, y_pred)

        return acc


    def svm(self, year) -> float:

        X_train, X_test, y_train, y_test = self.split_into_train_and_test(year)

        trained_model = make_pipeline(StandardScaler(), SVC()).fit(X_train, y_train)

        y_pred = trained_model.predict(X_test)
        acc: float = accuracy_score(y_test, y_pred)

        return acc


if __name__ == "__main__":

    model = Model("premier_league")
    print("logistic regressor:", model.logistic_regressor(2021))
    print("knn:", model.k_nearest_neighbour(2021))
    print("decision tree:", model.decision_tree_classifier(2021))
    print("gaussiannd:", model.gaussiannb(2021))
    print("svm:", model.svm(2021))
    