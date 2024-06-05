import tkinter as tk
from tkinter import messagebox, ttk
from db import conectar_db

class Cliente:
    def __init__(self, ventana):
        self.ventana = ventana
        self.window = tk.Toplevel()
        self.window.title("Clientes")
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
        title_label = tk.Label(title_frame, text="GESTION DE CLIENTES", font=("Arial", 16), bg="#f0f0f0")
        title_label.pack(pady=10)

        frame = tk.Frame(self.window)
        frame.pack(pady=20)

        tk.Label(frame, text="Nombre").grid(row=0, column=0, padx=10)
        tk.Label(frame, text="Apellido").grid(row=1, column=0, padx=10)
        tk.Label(frame, text="Dirección").grid(row=2, column=0, padx=10)
        tk.Label(frame, text="Teléfono").grid(row=3, column=0, padx=10)
        tk.Label(frame, text="Empresa").grid(row=4, column=0, padx=10)

        self.entry_nombre = tk.Entry(frame)
        self.entry_nombre.grid(row=0, column=1, padx=10)

        self.entry_apellido = tk.Entry(frame)
        self.entry_apellido.grid(row=1, column=1, padx=10)

        self.entry_direccion = tk.Entry(frame)
        self.entry_direccion.grid(row=2, column=1, padx=10)

        self.entry_telefono = tk.Entry(frame)
        self.entry_telefono.grid(row=3, column=1, padx=10)

        self.entry_empresa = tk.Entry(frame)
        self.entry_empresa.grid(row=4, column=1, padx=10)

        btn_agregar = tk.Button(frame, text="Agregar Cliente", command=self.agregar_cliente, bg="#008CBA", fg="white")
        btn_agregar.grid(row=5, column=0, pady=10)

        btn_actualizar = tk.Button(frame, text="Actualizar", command=self.actualizar_item, bg="#008CBA", fg="white")
        btn_actualizar.grid(row=5, column=1)

        btn_eliminar = tk.Button(frame, text="Eliminar Cliente", command=self.eliminar_cliente, bg="#008CBA", fg="white")
        btn_eliminar.grid(row=5, column=2)

        btn_limpiar = tk.Button(frame, text="Limpiar", command=self.limpiar_campos, bg="#008CBA", fg="white")
        btn_limpiar.grid(row=6, column=1)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), foreground="blue")
        style.configure("Treeview", font=("Arial", 10), rowheight=25, background="#f0f0f0", foreground="black")
        style.map("Treeview", background=[("selected", "green")], foreground=[("selected", "white")])

        tree_frame = tk.Frame(self.window)
        tree_frame.pack(pady=10)

        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Nombre", "Apellido", "Dirección", "Teléfono",  "Empresa"), show="headings", yscrollcommand=tree_scroll.set)
        self.tree.pack()

        tree_scroll.config(command=self.tree.yview)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Apellido", text="Apellido")
        self.tree.heading("Dirección", text="Dirección")
        self.tree.heading("Teléfono", text="Teléfono")
        self.tree.heading("Empresa", text="Empresa")

        self.tree.column("ID", anchor=tk.CENTER, width=50)
        self.tree.column("Nombre", anchor=tk.CENTER, width=150)
        self.tree.column("Apellido", anchor=tk.CENTER, width=150)
        self.tree.column("Dirección", anchor=tk.CENTER, width=200)
        self.tree.column("Teléfono", anchor=tk.CENTER, width=100)
        self.tree.column("Empresa", anchor=tk.CENTER, width=100)

        self.tree.bind("<ButtonRelease-1>", self.seleccionar_cliente)

        self.listar_clientes()

    def on_closing(self):
        self.window.destroy()
        self.ventana.deiconify()

    def conectar_db(self):
        return conectar_db()

    def agregar_cliente(self):
        nombre = self.entry_nombre.get()
        apellido = self.entry_apellido.get()
        direccion = self.entry_direccion.get()
        telefono = self.entry_telefono.get()
        empresa = self.entry_empresa.get()

        if nombre and apellido and direccion and telefono:
            try:
                conn = self.conectar_db()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO clientes (nombre, apellido, direccion, telefono, empresa) VALUES (%s, %s, %s, %s, %s)", (nombre, apellido, direccion, telefono, empresa))
                conn.commit()
                conn.close()
                self.listar_clientes()
                self.limpiar_campos()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

    def listar_clientes(self):
        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clientes")
            rows = cursor.fetchall()
            conn.close()
            
            self.tree.delete(*self.tree.get_children())

            for row in rows:
                self.tree.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizar_item(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Selecciona un elemento para actualizar")
            return

        item_id = self.tree.item(selected_item[0])["values"][0]
        nombre = self.entry_nombre.get()
        apellido = self.entry_apellido.get()
        direccion = self.entry_direccion.get()
        telefono = self.entry_telefono.get()
        empresa = self.entry_empresa.get()

        if nombre and apellido and direccion and telefono and empresa:
            try:
                conn = self.conectar_db()
                cursor = conn.cursor()
                cursor.execute("UPDATE clientes nombre = %s, apellido = %s, direccion = %s, telefono = %s, empresa = %s WHERE id = %s", (nombre, apellido, direccion, telefono, empresa, item_id))
                conn.commit()
                conn.close()
                self.listar_clientes()
                self.limpiar_campos()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")        

    def seleccionar_cliente(self, event):
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion)
            self.id_seleccionado = item["values"][0]
            self.entry_nombre.delete(0, tk.END)
            self.entry_nombre.insert(tk.END, item["values"][1])
            self.entry_apellido.delete(0, tk.END)
            self.entry_apellido.insert(tk.END, item["values"][2])
            self.entry_direccion.delete(0, tk.END)
            self.entry_direccion.insert(tk.END, item["values"][3])
            self.entry_telefono.delete(0, tk.END)
            self.entry_telefono.insert(tk.END, item["values"][4])
            self.entry_empresa.delete(0, tk.END)
            self.entry_empresa.insert(tk.END, item["values"][5])

    def eliminar_cliente(self):
        if self.id_seleccionado:
            try:
                conn = self.conectar_db()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM clientes WHERE id = %s", (self.id_seleccionado,))
                conn.commit()
                conn.close()
                self.listar_clientes()
                self.limpiar_campos()
                self.id_seleccionado = None
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Seleccione un cliente para eliminar")

    def limpiar_campos(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_apellido.delete(0, tk.END)
        self.entry_direccion.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_empresa.delete(0, tk.END)
        self.tree.selection_remove(*self.tree.selection())



