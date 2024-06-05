import tkinter as tk
from tkinter import messagebox, ttk
from db import conectar_db

class Producto:
    def listar(self):
        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            cursor.execute("SELECT nombre FROM categoria")
            rows = cursor.fetchall()
            conn.close()
            return [fila[0] for fila in rows]
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def __init__(self, ventana):
        self.ventana = ventana
        self.window = tk.Toplevel()
        self.window.title("Inventario")
        self.window.geometry("800x600+250-100")
        self.window.minsize(900, 600)
        self.window.maxsize(900, 600)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Cargar el logo y ajustar su tamaño
        logo_original = tk.PhotoImage(file="logo.gif")
        ancho_original = logo_original.width()
        alto_original = logo_original.height()
        factor_ajuste = 0.2  # Puedes ajustar este valor según tus necesidades

        ancho_ajustado = int(ancho_original * factor_ajuste)
        alto_ajustado = int(alto_original * factor_ajuste)

        logo = logo_original.subsample(int(ancho_original / ancho_ajustado), int(alto_original / alto_ajustado))

        # Mostrar el logo en la ventana
        logo_label = tk.Label(self.window, image=logo)
        logo_label.pack()
        logo_label.image = logo

        # Título de la ventana
        title_frame = tk.Frame(self.window, bg="#f0f0f0")
        title_frame.pack(fill=tk.X)
        title_label = tk.Label(title_frame, text="GESTION DE PRODUCTOS", font=("Arial", 16), bg="#f0f0f0")
        title_label.pack(pady=10)

        frame = tk.Frame(self.window)
        frame.pack(pady=20)

        tk.Label(frame, text="Nombre").grid(row=0, column=0, padx=10)
        tk.Label(frame, text="Cantidad").grid(row=1, column=0, padx=10)
        tk.Label(frame, text="Precio").grid(row=2, column=0, padx=10)
        tk.Label(frame, text="Categoria").grid(row=3, column=0, padx=10)
        tk.Label(frame, text="Descripcion").grid(row=4, column=0, padx=10)

        self.entry_nombre = tk.Entry(frame)
        self.entry_nombre.grid(row=0, column=1, padx=10)

        self.entry_cantidad = tk.Entry(frame)
        self.entry_cantidad.grid(row=1, column=1, padx=10)

        self.entry_precio = tk.Entry(frame)
        self.entry_precio.grid(row=2, column=1, padx=10)

        datos = ["Seleccione"]
        datos.extend(self.listar())
        self.list_categoria = ttk.Combobox(frame, state="readonly")
        self.list_categoria.grid(row=3, column=1, padx=10)
        self.list_categoria['values'] = datos
        self.list_categoria.set("Seleccione")

        self.box_descrip=tk.Text(frame, width=30, height=5)
        self.box_descrip.grid(column=1, row=4,  padx=10, sticky="we")
        #self.box_descrip.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        self.scrollVert=ttk.Scrollbar(frame, command=self.box_descrip.yview)
        #self.scrollVert.pack(fill=tk.Y, side=tk.RIGHT)
        self.box_descrip.config(yscrollcommand=self.scrollVert.set)

        btn_agregar = tk.Button(frame, text="Agregar", command=self.agregar_item, bg="#008CBA", fg="white")
        btn_agregar.grid(row=5, column=0, pady=10)

        btn_actualizar = tk.Button(frame, text="Actualizar", command=self.actualizar_item, bg="#008CBA", fg="white")
        btn_actualizar.grid(row=5, column=1)

        btn_eliminar = tk.Button(frame, text="Eliminar", command=self.eliminar_item, bg="#008CBA", fg="white")
        btn_eliminar.grid(row=5, column=3)

        btn_limpiar = tk.Button(frame, text="Limpiar", command=self.limpiar_campos, bg="#008CBA", fg="white")
        btn_limpiar.grid(row=6, column=1)

        # Configuración del estilo para la tabla
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), foreground="blue")
        style.configure("Treeview", font=("Arial", 10), rowheight=25, background="#f0f0f0", foreground="black")
        style.map("Treeview", background=[("selected", "green")], foreground=[("selected", "white")])

        # Añadir tabla con scrollbar
        tree_frame = tk.Frame(self.window)
        tree_frame.pack(pady=10)

        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Nombre", "Cantidad", "Precio", "Categoria", "Valor Total", "Descripcion"), show="headings", yscrollcommand=tree_scroll.set)
        self.tree.pack()

        tree_scroll.config(command=self.tree.yview)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.heading("Precio", text="Precio")
        self.tree.heading("Categoria", text="Categoria")
        self.tree.heading("Valor Total", text="Valor Total")
        self.tree.heading("Descripcion", text="Descripcion")

        self.tree.column("ID", anchor=tk.CENTER, width=50)
        self.tree.column("Nombre", anchor=tk.CENTER, width=150)
        self.tree.column("Cantidad", anchor=tk.CENTER, width=100)
        self.tree.column("Precio", anchor=tk.CENTER, width=100)
        self.tree.column("Categoria", anchor=tk.CENTER, width=150)
        self.tree.column("Valor Total", anchor=tk.CENTER, width=100)
        self.tree.column("Descripcion", anchor=tk.CENTER, width=200)

        self.tree.bind("<ButtonRelease-1>", self.seleccionar_item)

        self.listar_items()

    def on_closing(self):
        self.window.destroy()
        self.ventana.deiconify()    

    def conectar_db(self):
        return conectar_db()

    def agregar_item(self):
        nombre = self.entry_nombre.get()
        cantidad = self.entry_cantidad.get()
        precio = self.entry_precio.get()
        categoria = self.list_categoria.get()
        if categoria == "Seleccione": categoria = "N/A"
        descripcion = self.box_descrip.get(1.0, "end-1c")

        if nombre and cantidad and precio and categoria and descripcion:
            try:
                conn = self.conectar_db()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO items (nombre, cantidad, precio, categoria, descripcion) VALUES (%s, %s, %s, %s, %s)", (nombre, cantidad, precio, categoria, descripcion))
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
            cursor.execute("SELECT * FROM items")
            rows = cursor.fetchall()
            for row in rows:   
                valor_total = f"{row[2] * row[3]:,}"  # Calcular el valor total (cantidad * precio)
                cont = f"{row[3]:,}"
                self.tree.insert("", "end", values=(row[0], row[1], row[2], cont, row[4], valor_total, row[5]))
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
            cursor.execute("DELETE FROM items WHERE id = %s", (item_id,))
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
        cantidad = self.entry_cantidad.get()
        precio = self.entry_precio.get()
        categoria = self.list_categoria.get()
        if categoria == "Seleccione": categoria = "N/A"
        descripcion = self.box_descrip.get(1.0, "end-1c")

        if nombre and cantidad and precio and categoria and descripcion:
            try:
                conn = self.conectar_db()
                cursor = conn.cursor()
                cursor.execute("UPDATE items SET nombre = %s, cantidad = %s, precio = %s, categoria = %s, descripcion = %s WHERE id = %s", (nombre, cantidad, precio, categoria, descripcion, item_id))
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
                cursor.execute("SELECT * FROM items WHERE id = %s", (item_id,))
                item = cursor.fetchone()
                conn.close()
                self.entry_nombre.delete(0, tk.END)
                self.entry_nombre.insert(0, item[1])
                self.entry_cantidad.delete(0, tk.END)
                self.entry_cantidad.insert(0, item[2])
                self.entry_precio.delete(0, tk.END)
                self.entry_precio.insert(0, item[3])
                if item[4] == "N/A": self.list_categoria.set("Seleccione")
                else: self.list_categoria.set(item[4])
                self.box_descrip.delete(1.0, tk.END)
                self.box_descrip.insert(1.0, item[5])
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def limpiar_campos(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_cantidad.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)
        self.list_categoria.set("Seleccione")
        self.box_descrip.delete(1.0, tk.END)

        self.tree.selection_remove(*self.tree.selection())
                
