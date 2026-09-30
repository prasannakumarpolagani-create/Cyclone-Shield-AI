import pandas as pd


def load_infrastructure():

    return pd.read_csv(
        "data/infrastructure.csv"
    )


def load_cyclone():

    return pd.read_csv(
        "data/cyclone_data.csv"
    )