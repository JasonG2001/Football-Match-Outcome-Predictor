from joblib import dump, load
from pipeline import Model

class JoblibSave:

    def __init__(self, football_league: str):

        self.model = Model(football_league)


    def dump_model(self):

        clf = self.model.SVR_tuned()

        return dump(clf, "/home/jason2001/Football-Match-Outcome-Predictor/project/baseline.joblib")


    def load_model(self):

        clf = load("/home/jason2001/Football-Match-Outcome-Predictor/project/baseline.joblib")

        return clf


if __name__ == "__main__":

    joblib = JoblibSave("premier_league")
    # joblib.dump_model()
    print(joblib.load_model())