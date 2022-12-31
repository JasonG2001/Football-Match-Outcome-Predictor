from new_results import NewResult
from pipeline import Model
from sklearn.pipeline import Pipeline
from typing import Type
import pandas as pd

if __name__ == "__main__":
    model = Model()
    new_result = NewResult()

    rfc, _ = model.random_forest_classifier(2021)

    df: Type[pd.DataFrame] = pd.read_csv("/home/jason2001/Football-Match-Outcome-Predictor/project/results_for_prediction.csv")
    new_df: Type[pd.DataFrame] = new_result.combine_features(df)
    cleaned_df: Type[pd.DataFrame] = new_result.clean_dataframe(new_df)
    print(new_result.make_prediction(cleaned_df, rfc))