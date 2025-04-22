import pandas as pd
from io import BytesIO

def analyze_csv(file_bytes):
    df = pd.read_csv(BytesIO(file_bytes))

    analysis = {
        "shape": df.shape,
        "columns": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "nulls": df.isnull().sum().to_dict(),
        "describe": df.describe(include='all').to_dict()
    }

    return analysis
