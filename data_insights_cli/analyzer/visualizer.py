import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from io import BytesIO
from datetime import datetime

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_and_show_plot(fig, filename):
    path = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(path, bbox_inches='tight')
    plt.show()
    print(f"[📁] Gráfico guardado en: {path}")

def plot_histogram(df, column):
    fig, ax = plt.subplots()
    df[column].plot(kind='hist', bins=20, ax=ax, color='skyblue', edgecolor='black')
    ax.set_title(f'Histograma de {column}')
    save_and_show_plot(fig, f"histogram_{column}_{timestamp()}.png")

def plot_scatter(df, x_col, y_col):
    fig, ax = plt.subplots()
    df.plot(kind='scatter', x=x_col, y=y_col, ax=ax, alpha=0.6)
    ax.set_title(f'Scatter: {x_col} vs {y_col}')
    save_and_show_plot(fig, f"scatter_{x_col}_vs_{y_col}_{timestamp()}.png")

def plot_correlation(df):
    fig, ax = plt.subplots(figsize=(10, 8))
    corr = df.corr(numeric_only=True)
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    ax.set_title("Mapa de correlación")
    save_and_show_plot(fig, f"correlation_matrix_{timestamp()}.png")

def timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

import matplotlib.pyplot as plt
import numpy as np

def plot_with_stats(df, x_col, y_col):
    """Genera un gráfico de dispersión con líneas de media y desviación estándar del eje Y"""
    x = df[x_col]
    y = df[y_col]

    media = y.mean()
    std = y.std()

    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, label='Datos')
    plt.axhline(media, color='green', linestyle='--', label=f'Media ({media:.2f})')
    plt.axhline(media + std, color='orange', linestyle=':', label=f'Media + 1 STD ({(media + std):.2f})')
    plt.axhline(media - std, color='orange', linestyle=':', label=f'Media - 1 STD ({(media - std):.2f})')

    plt.title(f'{y_col} vs {x_col} con media y desviación estándar')
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    filename = f"outputs/stats_{x_col}_vs_{y_col}.png"
    plt.savefig(filename)
    plt.close()

    print(f"[📊] Gráfico guardado en: {filename}")

def plot_prediction(df, feature, target, predicciones):
    """Genera un gráfico con datos históricos y predicciones sobre el eje X"""
    import matplotlib.pyplot as plt

    # Datos históricos
    x = df[feature]
    y = df[target]

    # Datos de predicción
    x_pred = [p['x'] for p in predicciones]
    y_pred = [p['y'] for p in predicciones]

    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, label='Datos reales', color='blue')
    plt.plot(x, y, linestyle='dashed', alpha=0.5)

    plt.scatter(x_pred, y_pred, color='red', label='Predicciones', marker='x')
    plt.plot(x_pred, y_pred, linestyle='solid', color='red', alpha=0.7)

    plt.title(f'Predicción de {target} en función de {feature}')
    plt.xlabel(feature)
    plt.ylabel(target)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    filename = f"outputs/predict_{target}_vs_{feature}.png"
    plt.savefig(filename)
    plt.close()

    print(f"[📊] Gráfico de predicción guardado en: {filename}")
