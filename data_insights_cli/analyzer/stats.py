import pandas as pd
import math
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

def sanitize_for_json(data):
    if isinstance(data, dict):
        return {k: sanitize_for_json(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_for_json(i) for i in data]
    elif isinstance(data, float):
        if math.isnan(data) or math.isinf(data):
            return None  # o podés devolver 'NaN' como string
        return data
    return data
