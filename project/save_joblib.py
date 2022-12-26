from joblib import dump, load
from pipeline import Model

class JoblibSave:

    def dump_model(self, model, name: str) -> None:

        dump(model, f"/home/jason2001/Football-Match-Outcome-Predictor/project/{name}.joblib")


    def load_model(self, name: str) -> None:

        load(f"/home/jason2001/Football-Match-Outcome-Predictor/project/{name}.joblib")


if __name__ == "__main__":
    joblib = JoblibSave()
    model_class = Model()
    model = model_class.random_forest_classifier(2021)
    joblib.dump_model(model, "baseline")
    joblib.dump_model(model, "model")
