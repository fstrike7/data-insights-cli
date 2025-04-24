# Data Insights CLI

**Data Insights CLI** es una herramienta de línea de comandos desarrollada en Python que permite subir datasets, analizarlos y generar visualizaciones simples. Combina desarrollo backend con Django REST Framework, análisis de datos con Pandas y Matplotlib, y una interfaz CLI profesional, instalable con `pip`.

---

## 🚀 Características

- Carga de datasets en formato CSV.
- Análisis exploratorio de datos (EDA) desde el backend:
  - Estadísticas descriptivas
  - Detección de valores nulos
  - Matriz de correlación
- Generación de visualizaciones desde el CLI:
  - Histogramas
  - Gráficos de dispersión
  - Mapa de calor de correlación
- Predicciones de valores futuros mediante regresión polinómica configurable desde el backend (`data-insights predict`)
- Exportación como imágenes (`.png`)
- Interfaz por consola instalada como comando: `data-insights`
- Backend en Django + Django REST Framework para gestión de archivos, análisis y predicción.

---

## 🧰 Tecnologías

- Python 3.10+
- Django 4.x + Django REST Framework
- Pandas
- Matplotlib / Seaborn
- scikit-learn
- requests
- SQLite
- CLI con `setuptools`, `click` y `pyproject.toml`

---

## 📦 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/fstrike7/data-insights-cli.git
cd data-insights-cli

# Crear entorno virtual
python -m venv venv
.\venv\Scripts\activate  # (Windows) o source venv/bin/activate

# Instalar backend y dependencias
pip install -r requirements.txt

# Instalar el CLI como paquete editable
pip install -e .
```

## ⚙️ Backend (Django)
```bash
cd data_insights
python manage.py migrate
python manage.py runserver
```

## 🧪 Uso del CLI
```bash
# Subir un dataset CSV
data-insights upload --file path/al/archivo.csv --name "Ventas Abril"

# Obtener análisis básico (desde el backend)
data-insights analyze --id 1

# Generar visualización y exportarla como imagen
data-insights visualize --id 1 --type histogram --column edad

# Predecir valores futuros con regresión polinómica (desde el backend)
data-insights predict --id 1 --feature año --target ventas --future 2026 --future 2027 --degree 2
```
- El parámetro `--degree` es opcional y permite especificar el grado del polinomio para la regresión. Por defecto es 2, pero puede ajustarse para mejorar el ajuste del modelo según los datos.

Los archivos se guardarán en la carpeta `outputs/` automáticamente.


## ✅ Ejemplos de uso

```bash
# Histograma de una columna
data-insights visualize --id 1 --type histogram --column edad

# Scatter entre dos columnas
data-insights visualize --id 1 --type scatter --x edad --y ingresos

# Mapa de correlación
data-insights visualize --id 1 --type correlation

# Predicción de valores para años futuros (desde backend)
data-insights predict --id 1 --feature año --target ventas --future 2026 --future 2027
```

## 📁 Estructura del proyecto
```bash
data-insights-cli/
data-insights-cli/
├── data_insights_cli/
│   ├── analyzer/
│   │   ├── reader.py
│   │   ├── predictor.py
│   │   ├── stats.py
│   │   ├── visualizer.py
│   ├── cli/
│   │   └── main.py
│
├── ├──data_insights/      # Backend Django
│   │   ├── api/
│   │   ├── data_insights/
│   │   └── manage.py
├── pyproject.toml
├── requirements.txt
├── README.md
├── outputs/            # Carpeta generada automáticamente para guardar los gráficos
├── tests/
```

## 📌 Roadmap

- [x] Backend Django funcional con API REST
- [x] CLI instalable como comando global (data-insights)
- [x] Subida de datasets
- [x] Análisis exploratorio (EDA) desde el backend
- [x] Visualizaciones exportables (.png)
- [x] Eliminación de datasets (delete)
- [x] Buscar por nombre (--name)
- [x] Migración de argparse a click
- [x] Predicciones con regresión lineal desde backend (`data-insights predict`)
- [ ] Exportar análisis como JSON
- [ ] Validaciones más específicas
- [ ] Tests automatizados
- [ ] Documentación de API con Swagger
- [ ] UI Web (opcional)

## 📝 Licencia
MIT
