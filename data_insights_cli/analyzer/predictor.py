from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd

def predict_values(df, target_column, x_column, future_values):
    """Entrena un modelo y predice valores futuros basados en una relación lineal simple"""
    model = LinearRegression()
    X = df[[x_column]].dropna()
    y = df[target_column].loc[X.index]

    model.fit(X, y)
    predicts = model.predict(np.array(future_values).reshape(-1, 1))

    return list(zip(future_values, predicts))