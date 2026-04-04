import pandas as pd
from typing import Optional, Dict, Any


def load_idol_data(csv_path: str = "data/idols.csv") -> pd.DataFrame:
    return pd.read_csv(csv_path)


def clean_empty(value):
    if pd.isna(value):
        return None
    value = str(value).strip()
    if value == "":
        return None
    return value

def find_idol(name: str, csv_path: str = "data/idols.csv") -> Optional[Dict[str, Any]]:
    df = load_idol_data(csv_path)

    target = df[df["name"].str.lower() == name.strip().lower()]
    if target.empty:
        target = df[df["name"].str.contains(name.strip(), case=False, na=False)]

    if target.empty:
        return None

    row = target.iloc[0]
    return {
        "name": clean_empty(row["name"]),
        "birth_date": clean_empty(row["birth_date"]),
        "birth_time": clean_empty(row["birth_time"]),
        "gender": clean_empty(row["gender"]),
        "group": clean_empty(row["group"]),
    }