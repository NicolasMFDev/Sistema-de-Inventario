CREATE DATABASE IF NOT EXISTS inventario2;

USE inventario2;

CREATE TABLE IF NOT EXISTS clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    apellido VARCHAR(255) NOT NULL,
    direccion VARCHAR(255) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    empresa VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS categoria (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    cantidad INT NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    descripcion TEXT NOT NULL,
    categoria_id INT,
    FOREIGN KEY (categoria_id) REFERENCES categoria(id)
);

INSERT INTO categoria (nombre) VALUES
('Electrónica'),
('Ropa'),
('Comestibles'),
('Hogar'),
('Juguetes');

