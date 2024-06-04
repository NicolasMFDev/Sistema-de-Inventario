import tkinter as tk
from tkinter import ttk, messagebox
from db import conectar_db

class Bodega:
    def __init__(self, ventana):
        self.ventana = ventana
        self.window = tk.Toplevel()
        self.window.title("Bodega")
        self.window.geometry("800x600+250-100")
        self.window.minsize(800, 600)
        self.window.maxsize(800, 600)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        logo_original = tk.PhotoImage(file="logo.gif")
        ancho_original = logo_original.width()
        alto_original = logo_original.height()
        factor_ajuste = 0.2

        ancho_ajustado = int(ancho_original * factor_ajuste)
        alto_ajustado = int(alto_original * factor_ajuste)

        logo = logo_original.subsample(int(ancho_original / ancho_ajustado), int(alto_original / alto_ajustado))

        logo_label = tk.Label(self.window, image=logo)
        logo_label.pack()
        logo_label.image = logo

        title_frame = tk.Frame(self.window, bg="#f0f0f0")
        title_frame.pack(fill=tk.X)
        title_label = tk.Label(title_frame, text="Bodega", font=("Arial", 16), bg="#f0f0f0")
        title_label.pack(pady=10)

        frame = tk.Frame(self.window)
        frame.pack(pady=20)

        btn_productos = tk.Button(frame, text="Productos Agregados", command=self.mostrar_productos, bg="#4CAF50", fg="white")
        btn_productos.grid(row=0, column=0, padx=10, pady=10)

        btn_clientes = tk.Button(frame, text="Clientes Agregados", command=self.mostrar_clientes, bg="#4CAF50", fg="white")
        btn_clientes.grid(row=0, column=1, padx=10, pady=10)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), foreground="blue")
        style.configure("Treeview", font=("Arial", 10), rowheight=25, background="#f0f0f0", foreground="black")
        style.map("Treeview", background=[("selected", "green")], foreground=[("selected", "white")])

        self.tree_frame = tk.Frame(self.window)
        self.tree_frame.pack(pady=10)

        self.tree_scroll = tk.Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(self.tree_frame, yscrollcommand=self.tree_scroll.set)
        self.tree.pack()

        self.tree_scroll.config(command=self.tree.yview)

    def on_closing(self):
        self.window.destroy()
        self.ventana.deiconify()

    def conectar_db(self):
        return conectar_db()

    def mostrar_productos(self):
        for widget in self.tree_frame.winfo_children():
            widget.destroy()

        self.tree = ttk.Treeview(self.tree_frame, columns=("ID", "Nombre", "Cantidad", "Precio", "Descripción", "Categoría"), show="headings")
        self.tree.pack()

        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.heading("Precio", text="Precio")
        self.tree.heading("Descripción", text="Descripción")
        self.tree.heading("Categoría", text="Categoría")

        self.tree.column("ID", anchor=tk.CENTER, width=50)
        self.tree.column("Nombre", anchor=tk.CENTER, width=150)
        self.tree.column("Cantidad", anchor=tk.CENTER, width=100)
        self.tree.column("Precio", anchor=tk.CENTER, width=100)
        self.tree.column("Descripción", anchor=tk.CENTER, width=200)
        self.tree.column("Categoría", anchor=tk.CENTER, width=150)

        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT items.id, items.nombre, items.cantidad, items.precio, items.descripcion, categoria.nombre
                FROM items
                LEFT JOIN categoria ON items.categoria_id = categoria.id
            """)
            rows = cursor.fetchall()
            conn.close()
            
            for row in rows:
                self.tree.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def mostrar_clientes(self):
        for widget in self.tree_frame.winfo_children():
            widget.destroy()

        self.tree = ttk.Treeview(self.tree_frame, columns=("ID", "Nombre", "Apellido", "Dirección", "Teléfono"), show="headings")
        self.tree.pack()

        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Apellido", text="Apellido")
        self.tree.heading("Dirección", text="Dirección")
        self.tree.heading("Teléfono", text="Teléfono")

        self.tree.column("ID", anchor=tk.CENTER, width=50)
        self.tree.column("Nombre", anchor=tk.CENTER, width=150)
        self.tree.column("Apellido", anchor=tk.CENTER, width=150)
        self.tree.column("Dirección", anchor=tk.CENTER, width=200)
        self.tree.column("Teléfono", anchor=tk.CENTER, width=100)

        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clientes")
            rows = cursor.fetchall()
            conn.close()
            
            for row in rows:
                self.tree.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))

