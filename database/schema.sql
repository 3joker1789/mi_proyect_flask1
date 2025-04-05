-- Crear base de datos
CREATE DATABASE IF NOT EXISTS desarrollo_web;
USE desarrollo_web;

-- Tabla usuarios (para autenticación)
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL
);

-- Tabla productos
CREATE TABLE IF NOT EXISTS productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL
);

-- Datos de prueba (opcional)
INSERT INTO productos (nombre, precio, stock) VALUES
('Laptop HP', 899.99, 5),
('Teclado mecánico', 75.50, 20),
('Monitor 24"', 150.00, 8);