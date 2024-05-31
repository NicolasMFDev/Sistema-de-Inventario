# Sistema de Inventario

Software para la gestion de inventarios de una empresa.

## Descripcion del Software

El sistema cuenta con diferentes funcionalidades como: manejo de bodega, registro de productos, gestion de proveedores y registro de categorias.

La  Bodega

## Instalacion

Para ejecutar el proyecto primero debera descargar la carpeta con los archivos

Abra el editor de codigo ya sea Visual Studio Code o cualquier otra de preferencia y abra el terminal

Use el admnistrador de paquetes [pip](https://pip.pypa.io/en/stable/) para instalar las librerias.

```bash
pip install mysql-connector-python
pip install tkinter
```
Debera tener instalado una base de datos ya MySQL u otra y un gestos de datos puede ser phpAdmin con Xammp

Cree la base de datos conforme se muestra en el archivo `crear_data.sql`

### Usage

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

La libreria `tkinter` permite diseñar la interfaz donde se pondran los componentes

```python
import tkinter as tk

ventana = tk.Tk() #creacion de la ventana
ventana.title("NOMBRE_VENTANA") #titulo de la ventana
ventana.geometry("800x600+250-100") #tamaño de la ventana

ventana.pack()
ventana.mainloop()

```

## Autores

Nicolas Martinez - Desarrolladores

Carlos Hernan Ruiz - Desarrolladores

## Diagrama de Clases