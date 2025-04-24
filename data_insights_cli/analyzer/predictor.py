from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import numpy as np

def predict_values(df, target_column, x_column, future_values, degree):
    """
    Entrena un modelo de regresión polinómica y predice valores futuros.

    Args:
        df (pd.DataFrame): Dataset con los datos históricos.
        target_column (str): Nombre de la columna objetivo (variable dependiente).
        x_column (str): Nombre de la columna de entrada (variable independiente).
        future_values (list): Lista de valores futuros de la variable independiente.
        degree (int, opcional): Grado del polinomio. Por defecto es 2.

    Returns:
        list of tuple: Lista de pares (valor futuro, predicción).
    """
    # Crear características polinómicas
    poly = PolynomialFeatures(degree)
    X = df[[x_column]].dropna()
    y = df[target_column].loc[X.index]

    X_poly = poly.fit_transform(X)

    # Ajustar el modelo
    model = LinearRegression()
    model.fit(X_poly, y)

    # Predecir valores futuros
    future_values_poly = poly.transform(np.array(future_values).reshape(-1, 1))
    predicts = model.predict(future_values_poly)

    return list(zip(future_values, predicts))