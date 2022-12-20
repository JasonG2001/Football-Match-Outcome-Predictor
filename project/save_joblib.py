from joblib import dump, load
from pipeline import Model

class JoblibSave:

    def dump_model(self, model) -> None:

        dump(model, "/home/jason2001/Football-Match-Outcome-Predictor/project/baseline.joblib")


    def load_model(self) -> None:

        load("/home/jason2001/Football-Match-Outcome-Predictor/project/baseline.joblib")


if __name__ == "__main__":
    joblib = JoblibSave()
    model_class = Model()
    model = model_class.decision_tree_classifier(2021)
    joblib.dump_model(model)
