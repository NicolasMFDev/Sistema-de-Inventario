import tkinter as tk
from tkinter import ttk, messagebox
from db import conectar_db
from consulta_producto import Consulta_Producto

class Bodega:

    def listar(self):
        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            cursor.execute("SELECT nombre FROM items")
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
        title_label = tk.Label(title_frame, text="CREAR BODEGA", font=("Arial", 16), bg="#f0f0f0")
        title_label.pack(pady=10)

        self.frame = tk.Frame(self.window)
        self.frame.pack(pady=10)

        tk.Label(self.frame, text="Nombre").grid(row=0, column=0, padx=10)
        tk.Label(self.frame, text="Ubicacion").grid(row=1, column=0, padx=10)
        tk.Label(self.frame, text="Capacidad Maxima").grid(row=2, column=0, padx=10)
        tk.Label(self.frame, text="Producto").grid(row=3, column=0, padx=10)

        self.entry_nombre = tk.Entry(self.frame)
        self.entry_nombre.grid(row=0, column=1, padx=10)

        self.entry_ubica = tk.Entry(self.frame)
        self.entry_ubica.grid(row=1, column=1, padx=10)

        self.entry_cap_max = tk.Entry(self.frame)
        self.entry_cap_max.grid(row=2, column=1, padx=10)

        datos = ["Seleccione"]
        datos.extend(self.listar())
        self.list_producto = ttk.Combobox(self.frame, state="readonly")
        self.list_producto.grid(row=3, column=1, padx=10)
        self.list_producto['values'] = datos
        self.list_producto.set("Seleccione")

        btn_agregar = tk.Button(self.frame, text="Agregar", command=self.agregar_item, bg="#008CBA", fg="white")
        btn_agregar.grid(row=4, column=0, pady=10)

        btn_actualizar = tk.Button(self.frame, text="Actualizar", command=self.actualizar_item, bg="#008CBA", fg="white")
        btn_actualizar.grid(row=4, column=1)

        btn_eliminar = tk.Button(self.frame, text="Eliminar", command=self.eliminar_item, bg="#008CBA", fg="white")
        btn_eliminar.grid(row=4, column=2)

        btn_consulta = tk.Button(self.frame, text="Consultar Productos", command=lambda:self.mostrar_consulta(self.window), bg="#008CBA", fg="white")
        btn_consulta.grid(row=5, column=2)

        btn_limpiar = tk.Button(self.frame, text="Limpiar", command=self.limpiar_campos, bg="#008CBA", fg="white")
        btn_limpiar.grid(row=5, column=1)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), foreground="blue")
        style.configure("Treeview", font=("Arial", 10), rowheight=25, background="#f0f0f0", foreground="black")
        style.map("Treeview", background=[("selected", "green")], foreground=[("selected", "white")])

        tree_frame = tk.Frame(self.window)
        tree_frame.pack(pady=10)

        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Nombre", "Ubicacion", "Capacidad Maxima","Producto"), show="headings", yscrollcommand=tree_scroll.set)
        self.tree.pack()

        tree_scroll.config(command=self.tree.yview)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Ubicacion", text="Ubicacion")
        self.tree.heading("Capacidad Maxima", text="Capacidad Maxima")
        self.tree.heading("Producto", text="Producto")

        self.tree.column("ID", anchor=tk.CENTER, width=50)
        self.tree.column("Nombre", anchor=tk.CENTER, width=150)
        self.tree.column("Ubicacion", anchor=tk.CENTER, width=150)
        self.tree.column("Capacidad Maxima", anchor=tk.CENTER, width=200)
        self.tree.column("Producto", anchor=tk.CENTER, width=150)

        self.tree.bind("<ButtonRelease-1>", self.seleccionar_item)

        self.listar_items()

    def on_closing(self):
        self.window.destroy()
        self.ventana.deiconify()

    def conectar_db(self):
        return conectar_db()
    
    def mostrar_consulta(self,vent):
        Consulta_Producto(vent)

    def agregar_item(self):
        nombre = self.entry_nombre.get()
        ubicacion = self.entry_ubica.get()
        cap_max = self.entry_cap_max.get()
        producto = self.list_producto.get()
        if producto == "Seleccione": producto = "N/A"

        if nombre and ubicacion and cap_max and producto:
            try:
                conn = self.conectar_db()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO bodega (nombre, ubicacion, capa_max, producto) VALUES (%s, %s, %s, %s)", (nombre, ubicacion, cap_max, producto))
                conn.commit()
                conn.close()
                self.listar_items()
                self.limpiar_campos()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")

    def listar_items(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM bodega")
            rows = cursor.fetchall()

            for row in rows:
                self.tree.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4]))
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar_item(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Selecciona un elemento para eliminar")
            return

        item_id = self.tree.item(selected_item[0])["values"][0]

        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM bodega WHERE id = %s", (item_id,))
            conn.commit()
            conn.close()
            self.listar_items()
            self.limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizar_item(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Selecciona un elemento para actualizar")
            return

        item_id = self.tree.item(selected_item[0])["values"][0]
        nombre = self.entry_nombre.get()
        ubicacion = self.entry_ubica.get()
        cap_max = self.entry_cap_max.get()
        producto = self.list_producto.get()
        if producto == "Seleccione": producto = "N/A"

        if nombre and ubicacion and cap_max and producto:
            try:
                conn = self.conectar_db()
                cursor = conn.cursor()
                cursor.execute("UPDATE bodega SET nombre = %s, ubicacion = %s, capa_max = %s, producto = %s WHERE id = %s", (nombre, ubicacion, cap_max, producto, item_id))
                conn.commit()
                conn.close()
                self.listar_items()
                self.limpiar_campos()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")

    def seleccionar_item(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item_id = self.tree.item(selected_item[0])["values"][0]
            try:
                conn = self.conectar_db()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM bodega WHERE id = %s", (item_id,))
                item = cursor.fetchone()
                conn.close()
                self.entry_nombre.delete(0, tk.END)
                self.entry_nombre.insert(0, item[1])
                self.entry_ubica.delete(0, tk.END)
                self.entry_ubica.insert(0, item[2])
                self.entry_cap_max.delete(0, tk.END)
                self.entry_cap_max.insert(0, item[3])
                if item[4] == "N/A": self.list_producto.set("Seleccione")
                else: self.list_producto.set(item[4])
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def limpiar_campos(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_ubica.delete(0, tk.END)
        self.entry_cap_max.delete(0, tk.END)
        self.list_producto.set("Seleccione")

        self.tree.selection_remove(*self.tree.selection())
       

