import tkinter as tk
from producto import Producto
from categoria import Categoria
from bodega import Bodega
from cliente import Cliente

def open_producto_window(vent):
    app.withdraw()
    Producto(vent)

def open_categoria_window(vent):
    app.withdraw()
    Categoria(vent)

def open_bodega_window(vent):
    app.withdraw()
    Bodega(vent)

def open_cliente_window(vent):
    app.withdraw()
    Cliente(vent)              

if __name__ == "__main__":
    app = tk.Tk()
    app.title("INVENTARIO")
    app.geometry("800x600+250-100")

    logo_original = tk.PhotoImage(file="logo.gif")
    ancho_original = logo_original.width()
    alto_original = logo_original.height()
    factor_ajuste = 0.5  # Puedes ajustar este valor según tus necesidades

    ancho_ajustado = int(ancho_original * factor_ajuste)
    alto_ajustado = int(alto_original * factor_ajuste)

    logo = logo_original.subsample(int(ancho_original / ancho_ajustado), int(alto_original / alto_ajustado))

    # Mostrar el logo en la ventana
    logo_label = tk.Label(app, image=logo)
    logo_label.pack()
    logo_label.image = logo
    
    button_categoria = tk.Button(app, text="PRODUCTOS", command=lambda: open_producto_window(app), width=30, height=2, bg="#4DE973")
    button_categoria.pack(pady=20)

    button_categoria = tk.Button(app, text="CATEGORIAS", command=lambda: open_categoria_window(app), width=30, height=2, bg="#4DE973")
    button_categoria.pack(pady=20)

    button_bodega = tk.Button(app, text="BODEGA", command=lambda: open_bodega_window(app), width=30, height=2, bg="#4DE973")
    button_bodega.pack(pady=20)
    
    button_provee = tk.Button(app, text="PROVEEDORES", command=lambda: open_cliente_window(app), width=30, height=2, bg="#4DE973")
    button_provee.pack(pady=20)

    app.mainloop()
