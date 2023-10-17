import pandas as pd


def read_data(path):
    """Helper function to read data"""
    if path.endswith('.csv'):
        data = pd.read_csv(path)
    elif path.endswith('.parquet'):
        data = pd.read_parquet(path)
    else:
        data = pd.read_csv(path)
    return data
