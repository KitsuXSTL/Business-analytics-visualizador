# Business Analytics – Visualizador de datos (Guía 9)

Aplicación de escritorio en **Python** (Tkinter + Matplotlib) para ingresar, validar, guardar y graficar los resultados de una encuesta. Se distribuye como **ejecutable portable para Windows**: no necesita instalar Python ni ninguna librería.

Trabajo de la asignatura *Fundamentos de la Inteligencia de Negocios y Gestión de Datos*, Universidad Manuela Beltrán (2026), Guía 9 – Business Analytics e Inteligencia Artificial.

## Funcionalidades

- Ingreso de categorías y cantidades con validación: no se aceptan categorías vacías o repetidas, textos, decimales ni números negativos.
- Tabla de registros con el **total de estudiantes**: aparece en verde si suma 100 y en naranja si no coincide.
- **Gráfico de barras** y **gráfico circular** generados automáticamente.
- **Guardar y abrir archivos CSV**. Al abrir un archivo, las filas inválidas se descartan y se informa cuántas fueron.
- Botón para cargar los datos de ejemplo de la guía.

## Ejecución portable (Windows)

1. Descargue [`dist/BusinessAnalytics_Guia9.exe`](dist/BusinessAnalytics_Guia9.exe).
2. Ábralo con doble clic. La primera vez puede tardar unos segundos.
3. Si Windows muestra *"Windows protegió su PC"*, pulse **Más información** y luego **Ejecutar de todas formas**, porque el archivo no está firmado digitalmente.

> El `.exe` solo funciona en Windows. En macOS o Linux, ejecute el código fuente.

## Ejecución desde el código fuente

```bash
python -m pip install matplotlib
python Aplicacion_Guia9_Business_Analytics.py
```

Requiere Python 3 con Tkinter, que viene incluido en el instalador oficial de python.org.

## Generar el ejecutable

```bash
python -m pip install pyinstaller matplotlib
python -m PyInstaller --onefile --windowed --name BusinessAnalytics_Guia9 Aplicacion_Guia9_Business_Analytics.py
```

El archivo queda en la carpeta `dist`. También puede usarse `generar_exe.bat`.

## Formato del CSV

```csv
Actividad,Estudiantes
Ver series o películas,28
Escuchar música,22
Practicar deporte,18
Jugar videojuegos,15
Leer,10
Otras actividades,7
```

## Estructura del repositorio

| Archivo | Descripción |
|---|---|
| `Aplicacion_Guia9_Business_Analytics.py` | Código fuente documentado (docstrings PEP 257). |
| `dist/BusinessAnalytics_Guia9.exe` | Ejecutable portable para Windows. |
| `encuesta_tiempo_libre.csv` | Datos de la encuesta de la guía. |
| `generar_exe.bat` | Script para volver a generar el ejecutable. |
| `BusinessAnalytics_Guia9.spec` | Configuración de PyInstaller. |
| `README_Aplicacion_Guia9.txt` | Manual de uso en texto plano. |

## Autores

- Nelson Julián Martínez Bedoya
- Samuel Nieto Pardo
- Juan Sebastián Torres Agudelo
- Mauricio Esteban Varela Cañón

Docente: Juan José Osorio Tabares
