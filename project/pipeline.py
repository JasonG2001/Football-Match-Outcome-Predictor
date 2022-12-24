from football_dataframe import FootballDataframe
from result_finder import ResultFinder
from sklearn.ensemble import RandomForestClassifier as sklearn_random_forest
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import RandomizedSearchCV, train_test_split as sklearn_train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from typing import Dict, List, Type, Union
import pandas as pd


class Model:

    def __init__(self) -> None:

        self.football_dataframe = FootballDataframe()
        self.result_finder = ResultFinder()


    def split_into_train_and_test(self, football_league: str, year: int):

        df: Type[pd.DataFrame] = self.football_dataframe.clean_dataframe(football_league, year)

        X = df.drop(["Home_Team", "Away_Team", "Home_Result", "Away_Result", "Home_Result_Code", 
        "Away_Result_Code", "Round", "Home_Team_Code", "Away_Team_Code", "Home_Draws", 
        "Away_Draws", "Home_Streak", "Away_Streak"], axis=1)

        y = df["Home_Result_Code"]
        
        X_train, X_test, y_train, y_test = sklearn_train_test_split(X, y, test_size=0.2, random_state=0)

        return X_train, X_test, y_train, y_test


    def random_forest_classifier(self, year: int) -> float:

        leagues: List[str] = self.result_finder.get_list_of_leagues()
        pipeline = make_pipeline(StandardScaler(), sklearn_random_forest())

        param_grid: Dict[str,List[Union[str,float]]] = {
            'randomforestclassifier__n_estimators': [10, 50, 100, 200], # 50
            'randomforestclassifier__max_depth': [None, 5, 10, 15], # 5
            'randomforestclassifier__min_samples_split': [2, 5, 10], # 5/10
            'randomforestclassifier__min_samples_leaf': [1, 2, 4], # 2
            'randomforestclassifier__max_features': ["auto", "sqrt", "log2"]},
        grid_search = RandomizedSearchCV(estimator=pipeline, param_distributions=param_grid, cv=5, scoring="accuracy")

        league: str
        for league in leagues:
            X_train, X_test, y_train, y_test = self.split_into_train_and_test(league, year)
            grid_search = grid_search.fit(X_train, y_train)
        
        y_pred = grid_search.predict(X_test)
        acc = accuracy_score(y_test, y_pred)

        return grid_search.best_params_, acc


    def logistic_regressor(self, year: int) -> float:

        leagues: List[str] = self.result_finder.get_list_of_leagues()
        trained_model = make_pipeline(StandardScaler(), LogisticRegression())

        league: str
        for league in leagues:
            X_train, X_test, y_train, y_test = self.split_into_train_and_test(league, year)
            trained_model = trained_model.fit(X_train, y_train)

        y_pred = trained_model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)

        return trained_model, acc


    def k_nearest_neighbour(self, year: int) -> float:

        leagues: List[str] = self.result_finder.get_list_of_leagues()
        trained_model = make_pipeline(StandardScaler(), KNeighborsClassifier())

        league: str
        for league in leagues:
            X_train, X_test, y_train, y_test = self.split_into_train_and_test(league, year)
            trained_model = trained_model.fit(X_train, y_train)

        y_pred = trained_model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)

        return trained_model, acc


    def decision_tree_classifier(self, year: int) -> float:

        leagues: List[str] = self.result_finder.get_list_of_leagues()
        trained_model = make_pipeline(StandardScaler(), DecisionTreeClassifier())

        league: str
        for league in leagues:
            X_train, X_test, y_train, y_test = self.split_into_train_and_test(league, year)
            trained_model = trained_model.fit(X_train, y_train)

        y_pred = trained_model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)

        return trained_model, acc


    def gaussiannb(self, year: int) -> float:

        leagues: List[str] = self.result_finder.get_list_of_leagues()
        trained_model = make_pipeline(StandardScaler(), GaussianNB())

        league: str
        for league in leagues:
            X_train, X_test, y_train, y_test = self.split_into_train_and_test(league, year)
            trained_model = trained_model.fit(X_train, y_train)

        y_pred = trained_model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)

        return trained_model, acc


    def svm(self, year: int) -> float:

        leagues: List[str] = self.result_finder.get_list_of_leagues()
        trained_model = make_pipeline(StandardScaler(), SVC())

        league: str
        for league in leagues:
            X_train, X_test, y_train, y_test = self.split_into_train_and_test(league, year)
            trained_model = trained_model.fit(X_train, y_train)

        y_pred = trained_model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)

        return trained_model, acc


if __name__ == "__main__":

    model = Model()
    print("random forest:", model.random_forest_classifier(2021))
    print("logistic regressor:", model.logistic_regressor(2021))
    print("knn:", model.k_nearest_neighbour(2021))
    print("decision tree:", model.decision_tree_classifier(2021))
    print("gaussiannd:", model.gaussiannb(2021))
    print("svm:", model.svm(2021))
    