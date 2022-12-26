from football_dataframe import FootballDataframe
from result_finder import ResultFinder
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, train_test_split as sklearn_train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline, Pipeline
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
        "Away_Result_Code", "Home_Team_Code", "Away_Team_Code", "Home_Draws", "Away_Draws"], axis=1)

        y = df["Home_Result_Code"]
        
        X_train, X_test, y_train, y_test = sklearn_train_test_split(X, y, test_size=0.2, random_state=0)

        return X_train, X_test, y_train, y_test


    def random_forest_classifier(self, year: int) -> Union[float,Pipeline]:

        leagues: List[str] = self.result_finder.get_list_of_leagues()
        pipeline: Pipeline = make_pipeline(StandardScaler(), RandomForestClassifier(n_estimators=250, min_samples_split=2, 
            min_samples_leaf=12, max_features="auto", max_depth=40))
        '''
        param_grid: Dict[str,List[Union[str,float]]] = {
            'randomforestclassifier__n_estimators': [10, 50, 100, 200, 250, 300, 350], # 200
            'randomforestclassifier__max_depth': [None, 5, 10, 15, 20, 30, 40], # 20
            'randomforestclassifier__min_samples_split': [2, 5, 10, 15, 20], # 10
            'randomforestclassifier__min_samples_leaf': [1, 2, 4, 6, 8, 10, 12, 15], # 2
            'randomforestclassifier__max_features': ["auto", "sqrt", "log2"]} # auto
        pipeline = RandomizedSearchCV(estimator=pipeline, param_distributions=param_grid, cv=5, scoring="accuracy")
        '''
        league: str
        for league in leagues:
            X_train, X_test, y_train, y_test = self.split_into_train_and_test(league, year)
            pipeline = pipeline.fit(X_train, y_train)
        
        y_pred = pipeline.predict(X_test)
        acc: float = accuracy_score(y_test, y_pred)

        return pipeline, acc # 0.4, 0.5


    def logistic_regressor(self, year: int) -> Union[float,Pipeline]:

        leagues: List[str] = self.result_finder.get_list_of_leagues()
        pipeline: Pipeline = make_pipeline(StandardScaler(), LogisticRegression(C=0.5, tol=0.1, solver="sag"))
        '''
        param_grid: Dict[str,List[Union[str,float]]] = {
            'logisticregression__C': [0.5, 1.0, 2.0, 3.0, 4.0, 5.0], # 0.5
            'logisticregression__tol': [0.00001, 0.0001, 0.001, 0.01, 0.1, 1], # 0.1
            'logisticregression__solver': ['lbfgs', 'liblinear', 'newton-cg', 'sag', 'saga'] # sag
        }
        pipeline = GridSearchCV(estimator=pipeline, param_grid=param_grid, cv=10, scoring="accuracy", n_jobs=-1)
        '''
        league: str
        for league in leagues:
            X_train, X_test, y_train, y_test = self.split_into_train_and_test(league, year)
            pipeline = pipeline.fit(X_train, y_train)

        y_pred = pipeline.predict(X_test)
        acc: float = accuracy_score(y_test, y_pred)

        return pipeline, acc # 4.4e-1, 0.42


    def k_nearest_neighbour(self, year: int) -> Union[float,Pipeline]:

        leagues: List[str] = self.result_finder.get_list_of_leagues()
        pipeline: Pipeline = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=6, 
            weights="uniform", algorithm="ball_tree", leaf_size=29, p=7))
        '''
        param_grid: Dict[str,List[Union[str,float]]] = {
            'kneighborsclassifier__n_neighbors': range(1, 11), # 6
            'kneighborsclassifier__weights': ["uniform", "distance"], # uniform
            'kneighborsclassifier__algorithm': ["brute", "kd_tree", "ball_tree", "auto"], # ball_tree
            'kneighborsclassifier__leaf_size': range(10, 50), # 29
            'kneighborsclassifier__p': range(1, 15) # 7
        }
        pipeline = RandomizedSearchCV(estimator=pipeline, param_distributions=param_grid, cv=10, scoring="accuracy", n_jobs=-1)
        '''
        league: str
        for league in leagues:
            X_train, X_test, y_train, y_test = self.split_into_train_and_test(league, year)
            pipeline = pipeline.fit(X_train, y_train)

        y_pred = pipeline.predict(X_test)
        acc: float = accuracy_score(y_test, y_pred)

        return pipeline, acc # 0.44, 0.44


    def decision_tree_classifier(self, year: int) -> Union[float,Pipeline]:

        leagues: List[str] = self.result_finder.get_list_of_leagues()
        pipeline: Pipeline = make_pipeline(StandardScaler(), DecisionTreeClassifier(max_depth=5, min_samples_split=5,
            min_samples_leaf=8, criterion="entropy", splitter="random", max_features="log2"))
        '''
        param_grid: Dict[str,List[Union[str,float]]] = {
            'decisiontreeclassifier__max_depth': [None, 0, 2, 5, 10, 15], # 5
            'decisiontreeclassifier__min_samples_split': [2, 5, 10], # 5
            'decisiontreeclassifier__min_samples_leaf': [1, 2, 4, 6, 8, 10], # 8
            'decisiontreeclassifier__criterion': ["gini", "entropy", "log_loss"], # gini
            'decisiontreeclassifier__splitter': ["best", "random"], # random
            'decisiontreeclassifier__max_features': ["auto", "sqrt", "log2", None] # log2
        }

        pipeline = RandomizedSearchCV(estimator=pipeline, param_distributions=param_grid, cv=10, scoring="accuracy", n_jobs=-1)
        '''
        league: str
        for league in leagues:
            X_train, X_test, y_train, y_test = self.split_into_train_and_test(league, year)
            pipeline = pipeline.fit(X_train, y_train)

        y_pred = pipeline.predict(X_test)
        acc: float = accuracy_score(y_test, y_pred)

        return pipeline, acc # 0.4, 0.5


    def gaussiannb(self, year: int) -> Union[float,Pipeline]:

        leagues: List[str] = self.result_finder.get_list_of_leagues()
        pipeline: Pipeline = make_pipeline(StandardScaler(), GaussianNB(var_smoothing=1e-6))
        '''
        param_grid: Dict[str,List[Union[str,float]]] = {
            'gaussiannb__var_smoothing': [1e-9, 1e-8, 1e-7, 1e-6, 1e-5]
        }

        pipeline = RandomizedSearchCV(estimator=pipeline, param_distributions=param_grid, cv=10, scoring="accuracy", n_jobs=-1)
        '''
        league: str
        for league in leagues:
            X_train, X_test, y_train, y_test = self.split_into_train_and_test(league, year)
            pipeline = pipeline.fit(X_train, y_train)

        y_pred = pipeline.predict(X_test)
        acc: float = accuracy_score(y_test, y_pred)

        return pipeline, acc # 0.4, 0.4


    def svm(self, year: int) -> Union[float,Pipeline]:

        leagues: List[str] = self.result_finder.get_list_of_leagues()
        pipeline: Pipeline = make_pipeline(StandardScaler(), SVC(C=0.1, kernel="linear", degree=6, 
            gamma="scale", tol=1, cache_size=200))
        '''
        param_grid: Dict[str,List[Union[str,float]]] = {
            'svc__C': [0.01, 0.1, 1, 10, 100], # 0.1
            'svc__kernel': ['linear', 'poly', 'rbf', 'sigmoid'], # "linear"
            'svc__degree': range(10), # 6
            'svc__gamma': ['scale', 'auto'],
            'svc__tol': [1e-4, 1e-3, 1e-2, 1e-1, 1, 10, 100], # 1
            'svc__cache_size': [50, 100, 150, 200, 250, 300, 350] # 200
        }

        pipeline = RandomizedSearchCV(estimator=pipeline, param_distributions=param_grid, cv=10, scoring="accuracy", n_jobs=-1)
        '''
        league: str
        for league in leagues:
            X_train, X_test, y_train, y_test = self.split_into_train_and_test(league, year)
            pipeline = pipeline.fit(X_train, y_train)

        y_pred = pipeline.predict(X_test)
        acc: float = accuracy_score(y_test, y_pred)

        return pipeline, acc # 0.4, 0.42


if __name__ == "__main__":

    model = Model()
    print("random forest:", model.random_forest_classifier(2021))
    print("logistic regressor:", model.logistic_regressor(2021))
    print("knn:", model.k_nearest_neighbour(2021))
    print("decision tree:", model.decision_tree_classifier(2021))
    print("gaussiannd:", model.gaussiannb(2021))
    print("svm:", model.svm(2021))
    