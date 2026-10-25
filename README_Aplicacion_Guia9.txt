APLICACIÓN GUÍA 9 - BUSINESS ANALYTICS
Manual de uso y ejecución
=====================================================================

1. CONTENIDO DE LA CARPETA
   - BusinessAnalytics_Guia9.exe ........ programa portable para Windows
                                           (no requiere instalación).
   - Aplicacion_Guia9_Business_Analytics.py  código fuente documentado.
   - generar_exe.bat .................... script para volver a generar el .exe.
   - encuesta_tiempo_libre.csv .......... datos de la guía (opcional).

2. EJECUCIÓN PORTABLE (recomendada, Windows)
   1. Copie BusinessAnalytics_Guia9.exe a cualquier carpeta o memoria USB.
   2. Haga doble clic sobre el archivo. No necesita Python ni instalar nada.
      La primera vez puede tardar unos segundos en abrir.
   3. Si Windows muestra "Windows protegió su PC", pulse "Más información"
      y luego "Ejecutar de todas formas" (el archivo no está firmado).
   Nota: el .exe solo funciona en Windows. Para macOS o Linux se debe
   generar el ejecutable en ese sistema o ejecutar el código fuente.

3. EJECUCIÓN DESDE EL CÓDIGO FUENTE (cualquier sistema)
   1. Tener Python 3 con Tkinter.
   2. Instalar Matplotlib:  python -m pip install matplotlib
   3. Ejecutar:            python Aplicacion_Guia9_Business_Analytics.py

4. CÓMO GENERAR EL .EXE
   Doble clic en generar_exe.bat (o ejecutar en la terminal):
     python -m pip install pyinstaller matplotlib
     python -m PyInstaller --onefile --windowed --clean --name BusinessAnalytics_Guia9 Aplicacion_Guia9_Business_Analytics.py
   El archivo queda en la carpeta dist.

5. USO DE LA APLICACIÓN
   - Agregar: escriba la categoría y la cantidad y pulse "Agregar" (o Enter).
     La cantidad debe ser un número entero mayor o igual que cero.
     No se permiten categorías vacías ni repetidas.
   - Cargar ejemplo: llena la tabla con los 6 datos de la guía.
   - Eliminar seleccionado: quita la fila marcada en la tabla.
   - Total: debajo de la tabla se muestra la suma. En verde si es 100
     (coincide con la encuesta) y en naranja si es diferente.
   - Gráfico de barras / Gráfico circular: abre la gráfica en otra ventana.
     Si la suma no es 100, el programa pregunta antes de graficar.
     Desde la ventana de la gráfica se puede guardar como imagen (icono disco).
   - Guardar CSV: guarda la tabla en un archivo .csv (se abre en Excel).
   - Abrir CSV: carga un archivo .csv guardado antes. Las filas con datos
     inválidos se omiten y se informa cuántas fueron.
   - Limpiar todo: deja la tabla vacía.

6. FORMATO DEL ARCHIVO CSV
   Actividad,Estudiantes
   Ver series o películas,28
   Escuchar música,22
   ...
