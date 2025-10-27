-- Script de inicialización de la base de datos
-- Este archivo se ejecuta automáticamente al crear el contenedor PostgreSQL

-- Crear usuario con permisos limitados
CREATE USER hdcruser WITH PASSWORD 'localpass';

-- Conceder permisos básicos
GRANT CONNECT ON DATABASE hidrodb TO hdcruser;
GRANT USAGE ON SCHEMA public TO hdcruser;

-- Crear tablas de ejemplo para la industria petrolera
CREATE TABLE IF NOT EXISTS pozos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    campo VARCHAR(100) NOT NULL,
    profundidad DECIMAL(10,2),
    fecha_perforacion DATE,
    estado VARCHAR(50) DEFAULT 'activo'
);

CREATE TABLE IF NOT EXISTS produccion_pozos (
    id SERIAL PRIMARY KEY,
    pozo_id INTEGER REFERENCES pozos(id),
    fecha_produccion DATE NOT NULL,
    produccion_diaria DECIMAL(12,2) NOT NULL,
    campo VARCHAR(100) NOT NULL,
    tipo_fluido VARCHAR(50) DEFAULT 'petroleo'
);

CREATE TABLE IF NOT EXISTS contratos (
    id SERIAL PRIMARY KEY,
    numero_contrato VARCHAR(50) UNIQUE NOT NULL,
    empresa VARCHAR(200) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    valor_total DECIMAL(15,2),
    estado VARCHAR(50) DEFAULT 'activo'
);

CREATE TABLE IF NOT EXISTS fracturas_hidraulicas (
    id SERIAL PRIMARY KEY,
    pozo_id INTEGER REFERENCES pozos(id),
    fecha_fractura DATE NOT NULL,
    volumen_fluido DECIMAL(10,2),
    presion_maxima DECIMAL(8,2),
    resultado VARCHAR(50),
    costo DECIMAL(12,2)
);

-- Insertar datos de ejemplo
INSERT INTO pozos (nombre, campo, profundidad, fecha_perforacion, estado) VALUES
('Pozo-001', 'Campo Norte', 2500.50, '2023-01-15', 'activo'),
('Pozo-002', 'Campo Norte', 2800.75, '2023-02-20', 'activo'),
('Pozo-003', 'Campo Sur', 2200.25, '2023-03-10', 'activo'),
('Pozo-004', 'Campo Este', 3000.00, '2023-04-05', 'mantenimiento'),
('Pozo-005', 'Campo Oeste', 2600.80, '2023-05-12', 'activo');

INSERT INTO produccion_pozos (pozo_id, fecha_produccion, produccion_diaria, campo, tipo_fluido) VALUES
(1, '2024-01-01', 150.50, 'Campo Norte', 'petroleo'),
(1, '2024-01-02', 148.75, 'Campo Norte', 'petroleo'),
(1, '2024-01-03', 152.25, 'Campo Norte', 'petroleo'),
(2, '2024-01-01', 200.00, 'Campo Norte', 'petroleo'),
(2, '2024-01-02', 198.50, 'Campo Norte', 'petroleo'),
(2, '2024-01-03', 201.75, 'Campo Norte', 'petroleo'),
(3, '2024-01-01', 120.25, 'Campo Sur', 'petroleo'),
(3, '2024-01-02', 118.50, 'Campo Sur', 'petroleo'),
(3, '2024-01-03', 122.00, 'Campo Sur', 'petroleo'),
(5, '2024-01-01', 180.75, 'Campo Oeste', 'petroleo'),
(5, '2024-01-02', 179.25, 'Campo Oeste', 'petroleo'),
(5, '2024-01-03', 182.50, 'Campo Oeste', 'petroleo');

INSERT INTO contratos (numero_contrato, empresa, fecha_inicio, fecha_fin, valor_total, estado) VALUES
('CT-2024-001', 'PetroEnergy Corp', '2024-01-01', '2024-12-31', 5000000.00, 'activo'),
('CT-2024-002', 'OilMax Industries', '2024-02-01', '2025-01-31', 7500000.00, 'activo'),
('CT-2024-003', 'DrillTech Solutions', '2024-03-01', '2024-11-30', 3200000.00, 'activo'),
('CT-2023-004', 'EnergyPlus Ltd', '2023-06-01', '2023-12-31', 2800000.00, 'finalizado');

INSERT INTO fracturas_hidraulicas (pozo_id, fecha_fractura, volumen_fluido, presion_maxima, resultado, costo) VALUES
(1, '2023-12-15', 500.00, 8500.00, 'exitoso', 150000.00),
(2, '2023-11-20', 750.00, 9200.00, 'exitoso', 200000.00),
(3, '2024-01-10', 400.00, 7800.00, 'exitoso', 120000.00),
(4, '2023-10-05', 600.00, 8800.00, 'parcial', 180000.00),
(5, '2023-12-28', 550.00, 8600.00, 'exitoso', 160000.00);

-- Conceder permisos SELECT al usuario hdcruser
GRANT SELECT ON ALL TABLES IN SCHEMA public TO hdcruser;

-- Configurar permisos por defecto para futuras tablas
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO hdcruser;





