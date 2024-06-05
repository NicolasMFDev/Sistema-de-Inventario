import tkinter as tk
from tkinter import ttk, messagebox
from db import conectar_db

class Consulta_Producto:

    def listar(self):
        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            cursor.execute("SELECT nombre FROM bodega")
            rows = cursor.fetchall()
            conn.close()
            return [fila[0] for fila in rows]
        except Exception as e:
            messagebox.showerror("Error", str(e))       

    def __init__(self, ventana):
        self.ventana = ventana
        self.window = tk.Toplevel()
        self.window.title("Bodega")
        self.window.geometry("800x600+250-100")
        self.window.minsize(800, 600)
        self.window.maxsize(800, 600)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        title_frame = tk.Frame(self.window, bg="#f0f0f0")
        title_frame.pack(fill=tk.X)
        title_label = tk.Label(title_frame, text="LISTA DE PRODUCTOS", font=("Arial", 16), bg="#f0f0f0")
        title_label.pack(pady=10)

        self.frame = tk.Frame(self.window)
        self.frame.pack(pady=10)

        tk.Label(self.frame, text="Bodega").grid(row=0, column=0, padx=10)

        datos = ["Seleccione"]
        datos.extend(self.listar())
        nombres_unicos = list(set(datos))
        self.list_bodega = ttk.Combobox(self.frame, state="readonly")
        self.list_bodega.grid(row=0, column=1, padx=10)
        self.list_bodega['values'] = nombres_unicos
        self.list_bodega.set("Seleccione")

        btn_consultar = tk.Button(self.frame, text="Consultar", command=self.consultar_item, bg="#008CBA", fg="white")
        btn_consultar.grid(row=4, column=0, pady=10)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), foreground="blue")
        style.configure("Treeview", font=("Arial", 10), rowheight=25, background="#f0f0f0", foreground="black")
        style.map("Treeview", background=[("selected", "green")], foreground=[("selected", "white")])

        tree_frame = tk.Frame(self.window)
        tree_frame.pack(pady=10)

        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(tree_frame, columns=("Bodega", "Producto"), show="headings", yscrollcommand=tree_scroll.set)
        self.tree.pack()

        tree_scroll.config(command=self.tree.yview)

        self.tree.heading("Bodega", text="Bodega")
        self.tree.heading("Producto", text="Producto")

        self.tree.column("Bodega", anchor=tk.CENTER, width=50)
        self.tree.column("Producto", anchor=tk.CENTER, width=150)

        self.tree.bind("<ButtonRelease-1>", self.consultar_item)


    def on_closing(self):
        self.window.destroy()

    def conectar_db(self):
        return conectar_db()
        
    def consultar_item(self):
        bodega = self.list_bodega.get()
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            cursor.execute("SELECT nombre, producto FROM bodega WHERE nombre = %s", (bodega,))
            rows = cursor.fetchall()

            for row in rows:
                self.tree.insert("", "end", values=(row[0], row[1]))
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def limpiar_campos(self):
        self.list_bodega.set("Seleccione")     