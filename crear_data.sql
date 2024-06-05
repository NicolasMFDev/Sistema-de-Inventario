CREATE DATABASE IF NOT EXISTS inventario;

USE inventario;

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
    categoria VARCHAR(255) NOT NULL,
    descripcion TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bodega (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    ubicacion VARCHAR(255) NOT NULL,
    capa_max INT NOT NULL,
    producto VARCHAR(255) NOT NULL
);

INSERT INTO categoria (nombre) VALUES
('Electrónica'),
('Ropa'),
('Comestibles'),
('Hogar'),
('Juguetes');

