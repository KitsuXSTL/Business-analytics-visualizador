"""
Aplicación Guía 9 - Business Analytics e Inteligencia Artificial.

Programa de escritorio para registrar los resultados de una encuesta
(categoría y número de estudiantes), validarlos, guardarlos en un archivo
CSV y generar gráficos de barras y circulares de forma automática.

Asignatura: Fundamentos de la Inteligencia de Negocios y Gestión de Datos
Universidad Manuela Beltrán - 2026

Requisitos para ejecutar el código fuente: Python 3 con Tkinter y Matplotlib.
La versión .exe (generada con PyInstaller) no necesita ninguna instalación.

Estructura del código:
    - Constantes de configuración (total esperado, datos de la guía).
    - Clase App: interfaz gráfica, validación, almacenamiento y gráficas.
    - Bloque principal: crea la ventana y arranca la aplicación.
"""

import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

#: Número de estudiantes encuestados según la guía. Se usa para comprobar
#: que la suma de las categorías sea coherente con la población.
TOTAL_ESPERADO = 100

#: Datos originales entregados en la guía de laboratorio.
DATOS_GUIA = [
    ("Ver series o películas", 28),
    ("Escuchar música", 22),
    ("Practicar deporte", 18),
    ("Jugar videojuegos", 15),
    ("Leer", 10),
    ("Otras actividades", 7),
]

#: Encabezados que se escriben y se esperan en los archivos CSV.
ENCABEZADOS_CSV = ("Actividad", "Estudiantes")


class App:
    """Ventana principal del visualizador de datos.

    Atributos:
        root (tk.Tk): ventana raíz de Tkinter.
        data (list[tuple[str, int]]): registros en memoria (categoría, cantidad).
        cat (tk.StringVar): texto del campo "Categoría".
        val (tk.StringVar): texto del campo "Cantidad".
        tree (ttk.Treeview): tabla donde se muestran los registros.
        total_var (tk.StringVar): texto con el total de estudiantes.
        status (tk.StringVar): mensaje de estado de la última acción.
    """

    def __init__(self, root):
        """Construye la interfaz: formulario, tabla, total y botones."""
        self.root = root
        self.root.title("Business Analytics - Visualizador de datos")
        self.root.geometry("900x560")
        self.root.minsize(860, 520)
        self.data = []

        main = ttk.Frame(root, padding=15)
        main.pack(fill="both", expand=True)
        ttk.Label(main, text="Ingreso y visualización de datos",
                  font=("Arial", 16, "bold")).pack(anchor="w")

        # --- Formulario de ingreso -------------------------------------
        form = ttk.LabelFrame(main, text="Nuevo registro", padding=10)
        form.pack(fill="x", pady=10)
        ttk.Label(form, text="Categoría:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.cat = tk.StringVar()
        entrada_cat = ttk.Entry(form, textvariable=self.cat, width=32)
        entrada_cat.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(form, text="Cantidad:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.val = tk.StringVar()
        entrada_val = ttk.Entry(form, textvariable=self.val, width=12)
        entrada_val.grid(row=0, column=3, padx=5, pady=5)
        ttk.Button(form, text="Agregar", command=self.add).grid(row=0, column=4, padx=5)
        ttk.Button(form, text="Cargar ejemplo", command=self.example).grid(row=0, column=5, padx=5)
        # Permite agregar el registro presionando Enter en cualquiera de los campos.
        entrada_cat.bind("<Return>", lambda _e: self.add())
        entrada_val.bind("<Return>", lambda _e: self.add())

        # --- Tabla de registros ----------------------------------------
        self.tree = ttk.Treeview(main, columns=("cat", "val"), show="headings", height=11)
        self.tree.heading("cat", text="Actividad")
        self.tree.heading("val", text="Estudiantes")
        self.tree.column("cat", width=520)
        self.tree.column("val", width=160, anchor="center")
        self.tree.pack(fill="both", expand=True)

        # --- Total de estudiantes --------------------------------------
        self.total_var = tk.StringVar()
        self.total_label = tk.Label(main, textvariable=self.total_var,
                                    font=("Arial", 10, "bold"), anchor="w")
        self.total_label.pack(fill="x", pady=(6, 0))

        # --- Botones de acciones ---------------------------------------
        buttons = ttk.Frame(main)
        buttons.pack(fill="x", pady=10)
        ttk.Button(buttons, text="Eliminar seleccionado", command=self.delete).pack(side="left", padx=4)
        ttk.Button(buttons, text="Gráfico de barras",
                   command=lambda: self.plot("bar")).pack(side="left", padx=4)
        ttk.Button(buttons, text="Gráfico circular",
                   command=lambda: self.plot("pie")).pack(side="left", padx=4)
        ttk.Button(buttons, text="Limpiar todo", command=self.clear).pack(side="right", padx=4)
        ttk.Button(buttons, text="Abrir CSV", command=self.load_csv).pack(side="right", padx=4)
        ttk.Button(buttons, text="Guardar CSV", command=self.save_csv).pack(side="right", padx=4)

        # --- Línea de estado -------------------------------------------
        self.status = tk.StringVar(value="Listo para ingresar datos.")
        ttk.Label(main, textvariable=self.status).pack(anchor="w")
        self.refresh()

    # ------------------------------------------------------------------
    # Validación e ingreso
    # ------------------------------------------------------------------
    def validate(self, cat, raw):
        """Valida una categoría y una cantidad escritas por el usuario.

        Args:
            cat (str): nombre de la categoría (ya sin espacios al inicio/fin).
            raw (str): cantidad tal como se escribió.

        Returns:
            int | None: la cantidad convertida a entero si los datos son
            válidos; None si hay un error (en ese caso se muestra un aviso).
        """
        if not cat:
            messagebox.showwarning("Validación", "Escriba una categoría.")
            return None
        if any(c.lower() == cat.lower() for c, _ in self.data):
            messagebox.showwarning("Validación", f"La categoría «{cat}» ya está registrada.")
            return None
        try:
            val = int(raw)  # int() rechaza textos y decimales como "2.5"
        except ValueError:
            messagebox.showwarning("Validación",
                                   "La cantidad debe ser un número entero (sin decimales).")
            return None
        if val < 0:
            messagebox.showwarning("Validación", "La cantidad no puede ser negativa.")
            return None
        return val

    def add(self):
        """Agrega el registro del formulario si pasa la validación."""
        cat = self.cat.get().strip()
        val = self.validate(cat, self.val.get().strip())
        if val is None:
            return
        self.data.append((cat, val))
        self.refresh()
        self.cat.set("")
        self.val.set("")
        self.status.set("Registro agregado correctamente.")

    # ------------------------------------------------------------------
    # Gestión de la tabla
    # ------------------------------------------------------------------
    def refresh(self):
        """Vuelve a dibujar la tabla y actualiza el total de estudiantes.

        Si la suma no coincide con TOTAL_ESPERADO, el total se muestra en
        color naranja con una advertencia.
        """
        for item in self.tree.get_children():
            self.tree.delete(item)
        for cat, val in self.data:
            self.tree.insert("", "end", values=(cat, val))

        total = sum(v for _, v in self.data)
        if not self.data:
            self.total_var.set("Total: 0 estudiantes")
            self.total_label.config(fg="black")
        elif total == TOTAL_ESPERADO:
            self.total_var.set(f"Total: {total} estudiantes ✔ coincide con la encuesta")
            self.total_label.config(fg="#1e7b34")
        else:
            self.total_var.set(f"Total: {total} estudiantes ⚠ la encuesta tiene "
                               f"{TOTAL_ESPERADO}; revise los datos")
            self.total_label.config(fg="#c55a11")

    def example(self):
        """Carga los seis datos originales de la guía."""
        self.data = list(DATOS_GUIA)
        self.refresh()
        self.status.set("Se cargaron los datos de la guía.")

    def delete(self):
        """Elimina la fila seleccionada en la tabla."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Eliminar", "Seleccione una fila.")
            return
        idx = self.tree.index(selected[0])
        self.data.pop(idx)
        self.refresh()
        self.status.set("Registro eliminado.")

    def clear(self):
        """Borra todos los registros de la tabla."""
        self.data = []
        self.refresh()
        self.status.set("Tabla vacía.")

    # ------------------------------------------------------------------
    # Almacenamiento en CSV
    # ------------------------------------------------------------------
    def save_csv(self):
        """Guarda los registros actuales en un archivo CSV elegido por el usuario.

        Se usa la codificación utf-8-sig para que Excel muestre bien las tildes.
        """
        if not self.data:
            messagebox.showinfo("Guardar", "No hay datos para guardar.")
            return
        ruta = filedialog.asksaveasfilename(
            title="Guardar datos", defaultextension=".csv",
            initialfile="encuesta_tiempo_libre.csv",
            filetypes=[("Archivo CSV", "*.csv")])
        if not ruta:
            return  # el usuario canceló
        try:
            with open(ruta, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow(ENCABEZADOS_CSV)
                writer.writerows(self.data)
        except OSError as e:
            messagebox.showerror("Guardar", f"No se pudo guardar el archivo:\n{e}")
            return
        self.status.set(f"Datos guardados en {ruta}")

    def load_csv(self):
        """Carga registros desde un archivo CSV y valida cada fila.

        Las filas con categoría vacía, cantidad no entera o negativa se
        omiten y se informa cuántas fueron descartadas.
        """
        ruta = filedialog.askopenfilename(
            title="Abrir datos", filetypes=[("Archivo CSV", "*.csv")])
        if not ruta:
            return
        nuevos, omitidas = [], 0
        try:
            with open(ruta, newline="", encoding="utf-8-sig") as f:
                for i, fila in enumerate(csv.reader(f)):
                    if i == 0 and tuple(fila[:2]) == ENCABEZADOS_CSV:
                        continue  # se salta la fila de encabezados
                    try:
                        cat, val = fila[0].strip(), int(fila[1])
                        if not cat or val < 0:
                            raise ValueError
                        nuevos.append((cat, val))
                    except (ValueError, IndexError):
                        omitidas += 1
        except OSError as e:
            messagebox.showerror("Abrir", f"No se pudo leer el archivo:\n{e}")
            return
        self.data = nuevos
        self.refresh()
        mensaje = f"Se cargaron {len(nuevos)} registros desde el archivo."
        if omitidas:
            mensaje += f" Se omitieron {omitidas} filas con datos inválidos."
            messagebox.showwarning("Abrir", mensaje)
        self.status.set(mensaje)

    # ------------------------------------------------------------------
    # Visualización
    # ------------------------------------------------------------------
    def plot(self, kind):
        """Genera una gráfica con los registros actuales.

        Args:
            kind (str): "bar" para gráfico de barras o "pie" para circular.
        """
        if not self.data:
            messagebox.showinfo("Visualización", "Agregue datos antes de generar la gráfica.")
            return
        total = sum(v for _, v in self.data)
        if total == 0:
            messagebox.showinfo("Visualización", "Todas las cantidades son cero; no hay nada que graficar.")
            return
        if total != TOTAL_ESPERADO and not messagebox.askyesno(
                "Visualización",
                f"La suma de los datos es {total} y la encuesta tiene {TOTAL_ESPERADO} "
                "estudiantes.\n¿Desea generar la gráfica de todas formas?"):
            return

        cats = [c for c, _ in self.data]
        vals = [v for _, v in self.data]
        plt.figure(figsize=(8, 5))
        if kind == "bar":
            bars = plt.bar(cats, vals, color="#2e75b6")
            plt.ylabel("Cantidad")
            plt.title("Resultados por categoría")
            plt.xticks(rotation=25, ha="right")
            # Escribe el valor encima de cada barra.
            for b, v in zip(bars, vals):
                plt.text(b.get_x() + b.get_width() / 2, v + max(vals) * .02, str(v), ha="center")
        else:
            plt.pie(vals, labels=cats, autopct="%1.1f%%", startangle=90)
            plt.title("Distribución porcentual")
        plt.tight_layout()
        plt.show()
        self.status.set("Gráfica generada.")


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
