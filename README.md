# SOFTWARE DE GESTION DE INVENTARIO

Sistema para la gestion de inventarios de una empresa.

## Descripcion del Software

El sistema cuenta con 4 funcionalidades como: gestion de bodega, gestion de productos, gestion de categoria y gestion de proveedores(clientes). El sistema posee varias interfaces amables con el usuario capaz de entender con facilidad el manejo de cada una sin ningun tipo de problema y logrando asi satisfacer sus necesidades

## Requerimientos

Las funcionalidades del sistema se basan en lo requerimientos planteados como:
- Registro, actualizacion, eliminacion y consulta de productos
- Registro, actualizacion, eliminacion y consulta de categorias
- Registro, actualizacion, eliminacion y consulta de proveedores (clientes)
- Registro, actualizacion, eliminacion y consulta de bodegas

## Instalacion

Para ejecutar el proyecto primero debera descargar la carpeta con los archivos

Abrir el editor de codigo ya sea Visual Studio Code o cualquier otra de preferencia y abrir el terminal

Use el admnistrador de paquetes [pip](https://pip.pypa.io/en/stable/) para instalar la libreria.

```bash
pip install mysql-connector-python
```

Debera tener instalado una base de datos ya sea `MySQL WorkBench` con `Xammp` o cualquier otra de preferencia

Cree la base de datos conforme se muestra en el archivo `crear_data.sql`

### Uso

La libreria `mysql-conector-python` se usa para hacer la conexion con la base de datos

```python
import mysql.connector

def conectar_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="datebase-name"
    )

```

La libreria `tkinter` permite diseñar la interfaz y los componentes que iran en la interfaz

```python
import tkinter as tk

ventana = tk.Tk() #creacion de la ventana
ventana.title("NOMBRE_VENTANA") #titulo de la ventana
ventana.geometry("800x600+250-100") #tamaño de la ventana

label = tk.Label(ventana, text="texto-label").place(x=posicion eje x, y=posicion eje y) # texto que ira en la ventana
entrada = tk.Entry(ventana).place(x=posicion eje x, y=posicion eje y) # campo de texto para capturar datos de usuario

ventana.pack()
ventana.mainloop()

```

## Autores

Nicolas Martinez - Desarrollador

Carlos Hernan Ruiz - Desarrollador

## Diagrama de Clases

![Diagrama de Clases](diagrama_clase.jpg)

`Main`: Es el controlador principal que maneja la interfaz gráfica y las ventanas de Producto, Cliente, Bodega y Categoria.

`Producto, Cliente, Bodega y Categoria`: Cada una de estas clases maneja su propia ventana y las interacciones con la base de datos correspondientes a su dominio específico.

`DB`: Este módulo proporciona la conexión a la base de datos y es utilizado por las clases Producto, Cliente, Bodega y Categoria.

`Relaciones`:

- Main: Contiene métodos que crean instancias de Producto, Cliente, Bodega y Categoria.

- Producto, Cliente, Bodega y Categoria: Utilizan el módulo DB para realizar operaciones en la base de datos.