import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from io import BytesIO
from datetime import datetime

# Crea carpeta si no existe
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
