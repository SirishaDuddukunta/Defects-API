import pandas as pd

def load_defect_data(path="defects_data.csv"):
    df = pd.read_csv(path, parse_dates=["defect_date"])
    return df