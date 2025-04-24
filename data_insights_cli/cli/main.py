import click
import pandas as pd
import requests
import os
from io import BytesIO

from data_insights_cli.analyzer.visualizer import plot_histogram, plot_scatter, plot_correlation, plot_with_stats, plot_prediction

API_URL = "http://127.0.0.1:8000/api/datasets/"  # TODO: Cambiar en deploy

def get_dataset_by_id(id=None, name=None):
    """Descarga el dataset y lo convierte en un DataFrame."""
    if id:
        res = requests.get(f"{API_URL}{id}/")
    elif name:
        res = requests.get(f"{API_URL}by_name/?name={name}")
    else:
        click.echo("[❌] Debes proporcionar --id o --name")
        return None

    if res.status_code != 200:
        click.echo(f"[❌] Dataset no encontrado ({res.status_code})")
        return None

    file_url = res.json()["file"]
    click.echo(f"[📥] Descargando CSV desde: {file_url}")
    file_res = requests.get(file_url)
    if file_res.status_code != 200:
        click.echo("[❌] Error al descargar CSV")
        return None

    return pd.read_csv(BytesIO(file_res.content))

@click.group()
def cli():
    """Data Insights CLI"""
    pass

@cli.command()
@click.option('--file', required=True, type=click.Path(exists=True), help="Ruta al archivo CSV")
@click.option('--name', help="Nombre del dataset (opcional)")
def upload(file, name):
    """Sube un archivo CSV al servidor"""
    with open(file, 'rb') as f:
        files = {'file': f}
        data = {'name': name or os.path.basename(file)}
        click.echo(f"[⏫] Subiendo archivo '{file}'...")
        response = requests.post(API_URL, files=files, data=data)

    if response.status_code == 201:
        data = response.json()
        click.echo(f"[✅] Archivo subido exitosamente.\n   ➤ Nombre: {data['name']}\n   ➤ ID: {data['id']}\n   ➤ URL: {data['file']}")
    else:
        click.echo(f"[❌] Error al subir archivo: {response.status_code}\n{response.text}")

@cli.command()
@click.option('--id', required=True, type=int, help="ID del dataset")
def analyze(id):
    """Obtiene el análisis exploratorio desde el backend"""
    click.echo(f"[🔎] Solicitando análisis para el dataset con ID {id}...")

    res = requests.get(f"{API_URL}{id}/analyze/")
    if res.status_code != 200:
        click.echo(f"[❌] Error al obtener análisis ({res.status_code})")
        click.echo(res.text)
        return

    analysis = res.json()

    click.echo(f"\n🔢 Dimensiones: {analysis['shape']}")
    click.echo(f"📄 Columnas: {analysis['columns']}")
    click.echo(f"🔤 Tipos de datos: {analysis['dtypes']}")
    click.echo(f"⚠️ Valores nulos: {analysis['nulls']}")

    click.echo("\n📈 Estadísticas:")
    for columna, estadisticas in analysis['describe'].items():
        click.echo(f"\n📊 Estadísticas para la columna: {columna}")
        for nombre_estadistica, valor in estadisticas.items():
            valor = valor if valor is not None else "N/A"
            click.echo(f"   - {nombre_estadistica.capitalize()}: {valor}")

@cli.command()
@click.option('--id', required=False, type=int, help="ID del dataset")
@click.option('--name', required=False, help="Nombre del dataset (alternativa a ID)")
@click.option('--type', required=True, type=click.Choice(['histogram', 'scatter', 'correlation', 'stats']), help="Tipo de gráfico")
@click.option('--column', required=False, help="Columna para histograma")
@click.option('--x', required=False, help="Columna X (scatter)")
@click.option('--y', required=False, help="Columna Y (scatter)")
def visualize(id, name, type, column, x, y):
    """Genera visualizaciones a partir del dataset"""
    df = get_dataset_by_id(id, name)
    if df is None:
        return

    if type == "histogram":
        if not column:
            click.echo("[⚠️] Debes especificar --column para histogramas")
            return
        plot_histogram(df, column)

    elif type == "scatter":
        if not x or not y:
            click.echo("[⚠️] Debes especificar --x y --y para scatter")
            return
        plot_scatter(df, x, y)

    elif type == "correlation":
        plot_correlation(df)
    
    elif type == "stats":
        if not x or not y:
            click.echo("[⚠️] Debes especificar --x y --y para tipo 'stats'")
            return
        plot_with_stats(df, x, y)

@cli.command()
@click.option('--id', type=int, help="ID del dataset")
@click.option('--name', help="Nombre del dataset")
def delete(id, name):
    """Elimina un dataset por ID o nombre"""
    if id:
        url = f"{API_URL}{id}/"
    elif name:
        res = requests.get(f"{API_URL}by_name/?name={name}")
        if res.status_code != 200:
            click.echo(f"[❌] Dataset con nombre '{name}' no encontrado")
            return
        id = res.json()["id"]
        url = f"{API_URL}{id}/"
    else:
        click.echo("[⚠️] Debes proporcionar --id o --name para borrar un dataset")
        return

    res = requests.delete(url)
    if res.status_code in (204, 200):
        click.echo(f"[🗑️] Dataset eliminado correctamente (ID: {id})")
    else:
        click.echo(f"[❌] Error al eliminar dataset: {res.status_code}\n{res.text}")

@cli.command()
@click.option('--id', required=True, type=int, help="ID del dataset")
@click.option('--feature', required=True, help="Columna independiente (feature)")
@click.option('--target', required=True, help="Columna objetivo (target)")
@click.option('--future', required=True, multiple=True, type=float, help="Valores futuros de la variable independiente")
@click.option('--degree', default=2, required=False, type=int, help="Grado del polínomio. Por defecto es 2.")
@click.option('--plot', is_flag=True, help="Generar una visualización con los resultados")
def predict(id, feature, target, future, plot, degree):
    """
    Predice valores futuros usando regresión lineal.
    """
    future_params = "&".join([f"future={val}" for val in future])
    url = f"{API_URL}{id}/predict/?feature={feature}&target={target}&{future_params}&degree={degree}"

    click.echo(f"[🔮] Solicitando predicción desde el backend...")
    res = requests.get(url)

    if res.status_code != 200:
        click.echo(f"[❌] Error al obtener predicciones ({res.status_code})")
        click.echo(res.text)
        return

    data = res.json()
    click.echo(f"\n🔮 Predicciones para target '{target}' según '{feature}':")
    if plot:
        df = get_dataset_by_id(id)
        if df is not None:
            plot_prediction(df, feature, target, data["predicciones"])
    for pred in data["predicciones"]:
        click.echo(f"   ➤ Si {feature} = {pred['x']} ➜ {target} ≈ {round(pred['y'], 2)}")
if __name__ == '__main__':
    cli()