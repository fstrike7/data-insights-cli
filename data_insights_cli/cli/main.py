import argparse
from io import BytesIO
import pandas as pd
import requests
import os
from data_insights_cli.analyzer.stats import analyze_csv
from data_insights_cli.analyzer.visualizer import plot_histogram, plot_scatter, plot_correlation


API_URL = "http://127.0.0.1:8000/api/datasets/"  # TODO: Cambiar en deploy

def upload_file(file_path, name=None):
    if not os.path.isfile(file_path):
        print(f"[❌] El archivo no existe: {file_path}")
        return

    with open(file_path, 'rb') as f:
        files = {'file': f}
        data = {'name': name or os.path.basename(file_path)}
        print(f"[⏫] Subiendo archivo '{file_path}'...")
        response = requests.post(API_URL, files=files, data=data)

    if response.status_code == 201:
        data = response.json()
        print(f"[✅] Archivo subido exitosamente.")
        print(f"   ➤ Nombre: {data['name']}")
        print(f"   ➤ ID: {data['id']}")
        print(f"   ➤ URL: {data['file']}")
    else:
        print(f"[❌] Error al subir archivo: {response.status_code}")
        print(response.text)


def analyze_dataset(dataset_id):
    print(f"[🔎] Buscando dataset con ID {dataset_id}...")
    res = requests.get(f"{API_URL}{dataset_id}/")

    if res.status_code != 200:
        print(f"[❌] Dataset no encontrado ({res.status_code})")
        return

    dataset = res.json()
    file_url = dataset["file"]
    print(f"[📥] Descargando archivo desde: {file_url}")
    file_response = requests.get(file_url)

    if file_response.status_code != 200:
        print(f"[❌] Error al descargar archivo")
        return

    print("[📊] Analizando datos...\n")
    analysis = analyze_csv(file_response.content)

    print(f"🔢 Dimensiones: {analysis['shape']}")
    print(f"📄 Columnas: {analysis['columns']}")
    print(f"🔤 Tipos de datos: {analysis['dtypes']}")
    print(f"⚠️ Valores nulos: {analysis['nulls']}")
    print(f"📈 Estadísticas:\n")

    for col, stats in analysis['describe'].items():
        print(f"📌 {col}:")
        for stat_name, value in stats.items():
            print(f"   {stat_name}: {value}")
        print("")

def delete_dataset(dataset_id=None, name=None):
    if dataset_id:
        url = f"{API_URL}{dataset_id}/"
    elif name:
        # Buscar primero el dataset por nombre
        res = requests.get(f"{API_URL}by_name/?name={name}")
        if res.status_code != 200:
            print(f"[❌] Dataset con nombre '{name}' no encontrado")
            return
        dataset_id = res.json()["id"]
        url = f"{API_URL}{dataset_id}/"
    else:
        print("[⚠️] Debes proporcionar --id o --name para borrar un dataset")
        return

    res = requests.delete(url)
    if res.status_code in (204, 200):
        print(f"[🗑️] Dataset eliminado correctamente (ID: {dataset_id})")
    else:
        print(f"[❌] Error al eliminar dataset: {res.status_code}")
        print(res.text)


def main():
    parser = argparse.ArgumentParser(description="Data Insights CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # upload
    upload_parser = subparsers.add_parser("upload", help="Subir un dataset")
    upload_parser.add_argument("--file", type=str, required=True, help="Ruta al archivo CSV")
    upload_parser.add_argument("--name", type=str, help="Nombre del dataset (opcional)")

    # analyze
    analyze_parser = subparsers.add_parser("analyze", help="Analizar un dataset")
    analyze_parser.add_argument("--id", type=int, required=True, help="ID del dataset")

    # visualize
    visualize_parser = subparsers.add_parser("visualize", help="Generar visualización")
    visualize_parser.add_argument("--id", type=int, required=True, help="ID del dataset")
    visualize_parser.add_argument("--type", type=str, required=True, choices=["histogram", "scatter", "correlation"], help="Tipo de gráfico")
    visualize_parser.add_argument("--column", type=str, help="Columna para histograma")
    visualize_parser.add_argument("--x", type=str, help="Columna X (scatter)")
    visualize_parser.add_argument("--y", type=str, help="Columna Y (scatter)")
    visualize_parser.add_argument("--name", type=str, help="Nombre del dataset (opcional en lugar de --id)")

    # delete
    delete_parser = subparsers.add_parser("delete", help="Eliminar un dataset")
    delete_parser.add_argument("--id", type=int, help="ID del dataset")
    delete_parser.add_argument("--name", type=str, help="Nombre del dataset")

    args = parser.parse_args()

    if args.command == "upload":
        upload_file(args.file, args.name)
    elif args.command == "analyze":
        analyze_dataset(args.id)
    elif args.command == "visualize":
        # Dataset por ID o nombre
        if args.id:
            res = requests.get(f"{API_URL}{args.id}/")
        elif args.name:
            res = requests.get(f"{API_URL}by_name/?name={args.name}")
        else:
            print("[❌] Debes proporcionar --id o --name")
            return
        res = requests.get(f"{API_URL}{args.id}/")
        if res.status_code != 200:
            print(f"[❌] Dataset no encontrado ({res.status_code})")
            return

        file_url = res.json()["file"]
        print(f"[📥] Descargando CSV desde: {file_url}")
        file_res = requests.get(file_url)

        if file_res.status_code != 200:
            print(f"[❌] Error al descargar CSV")
            return

        df = pd.read_csv(BytesIO(file_res.content))

        if args.type == "histogram":
            if not args.column:
                print("[⚠️] Debes especificar --column para histogramas")
                return
            plot_histogram(df, args.column)

        elif args.type == "scatter":
            if not args.x or not args.y:
                print("[⚠️] Debes especificar --x y --y para scatter")
                return
            plot_scatter(df, args.x, args.y)

        elif args.type == "correlation":
            plot_correlation(df)
    elif args.command == "delete":
        delete_dataset(dataset_id=args.id, name=args.name)
        
if __name__ == "__main__":
    main()