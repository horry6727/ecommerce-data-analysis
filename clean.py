import pandas as pd


def clean_data(input_path):
    df = pd.read_csv(input_path, encoding="utf-8-sig")

    df.drop(columns='url', inplace=True)
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)

    df['price'] = df['price'].str.replace('£', '').astype(float)

    return df