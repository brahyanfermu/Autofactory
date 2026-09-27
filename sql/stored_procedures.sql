-- =====================================================
--  STORED PROCEDURES - AUTOfactory
--  Base de datos: Autofactory
--  Autor: Brahyan Fernández Múnera
-- =====================================================

USE Autofactory;

-- =====================================================
--  MÓDULO 1: VEHÍCULOS (modelo_vehiculo)
-- =====================================================

DROP PROCEDURE IF EXISTS sp_listar_modelos;
DELIMITER //
CREATE PROCEDURE sp_listar_modelos()
BEGIN
    SELECT codigo_modelo, nombre, categoria,
           especificaciones_tecnicas, tiempo_ensamble
    FROM modelo_vehiculo
    ORDER BY codigo_modelo DESC;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS sp_insertar_modelo;
DELIMITER //
CREATE PROCEDURE sp_insertar_modelo(
    IN p_nombre VARCHAR(100),
    IN p_categoria VARCHAR(100),
    IN p_especificaciones VARCHAR(250),
    IN p_tiempo_ensamble INT
)
BEGIN
    INSERT INTO modelo_vehiculo
        (nombre, categoria, especificaciones_tecnicas, tiempo_ensamble)
    VALUES
        (p_nombre, p_categoria, p_especificaciones, p_tiempo_ensamble);
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS sp_actualizar_modelo;
DELIMITER //
CREATE PROCEDURE sp_actualizar_modelo(
    IN p_codigo INT,
    IN p_nombre VARCHAR(100),
    IN p_categoria VARCHAR(100),
    IN p_especificaciones VARCHAR(250),
    IN p_tiempo_ensamble INT
)
BEGIN
    UPDATE modelo_vehiculo
    SET nombre = p_nombre,
        categoria = p_categoria,
        especificaciones_tecnicas = p_especificaciones,
        tiempo_ensamble = p_tiempo_ensamble
    WHERE codigo_modelo = p_codigo;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS sp_eliminar_modelo;
DELIMITER //
CREATE PROCEDURE sp_eliminar_modelo(IN p_codigo INT)
BEGIN
    DELETE FROM modelo_vehiculo WHERE codigo_modelo = p_codigo;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS sp_buscar_modelo;
DELIMITER //
CREATE PROCEDURE sp_buscar_modelo(IN p_codigo INT)
BEGIN
    SELECT codigo_modelo, nombre, categoria,
           especificaciones_tecnicas, tiempo_ensamble
    FROM modelo_vehiculo
    WHERE codigo_modelo = p_codigo;
END //
DELIMITER ;


-- =====================================================
--  MÓDULO 2: PRODUCCIÓN (orden_produccion)
-- =====================================================

DROP PROCEDURE IF EXISTS sp_listar_ordenes;
DELIMITER //
CREATE PROCEDURE sp_listar_ordenes()
BEGIN
    SELECT op.numero_produccion, op.fecha_emision,
           mv.nombre AS modelo, op.cantidad_producir,
           op.fecha_inicio, op.fecha_finalizacion,
           op.prioridad, op.estado_actual
    FROM orden_produccion op
    INNER JOIN modelo_vehiculo mv ON op.codigo_modelo = mv.codigo_modelo
    ORDER BY op.numero_produccion DESC;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS sp_insertar_orden;
DELIMITER //
CREATE PROCEDURE sp_insertar_orden(
    IN p_fecha_emision DATE,
    IN p_codigo_modelo INT,
    IN p_cantidad INT,
    IN p_fecha_inicio DATE,
    IN p_fecha_fin DATE,
    IN p_prioridad VARCHAR(100),
    IN p_estado VARCHAR(100)
)
BEGIN
    INSERT INTO orden_produccion
        (fecha_emision, codigo_modelo, cantidad_producir,
         fecha_inicio, fecha_finalizacion, prioridad, estado_actual)
    VALUES
        (p_fecha_emision, p_codigo_modelo, p_cantidad,
         p_fecha_inicio, p_fecha_fin, p_prioridad, p_estado);
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS sp_actualizar_orden;
DELIMITER //
CREATE PROCEDURE sp_actualizar_orden(
    IN p_numero INT,
    IN p_fecha_emision DATE,
    IN p_codigo_modelo INT,
    IN p_cantidad INT,
    IN p_fecha_inicio DATE,
    IN p_fecha_fin DATE,
    IN p_prioridad VARCHAR(100),
    IN p_estado VARCHAR(100)
)
BEGIN
    UPDATE orden_produccion
    SET fecha_emision = p_fecha_emision,
        codigo_modelo = p_codigo_modelo,
        cantidad_producir = p_cantidad,
        fecha_inicio = p_fecha_inicio,
        fecha_finalizacion = p_fecha_fin,
        prioridad = p_prioridad,
        estado_actual = p_estado
    WHERE numero_produccion = p_numero;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS sp_eliminar_orden;
DELIMITER //
CREATE PROCEDURE sp_eliminar_orden(IN p_numero INT)
BEGIN
    DELETE FROM orden_produccion WHERE numero_produccion = p_numero;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS sp_buscar_orden;
DELIMITER //
CREATE PROCEDURE sp_buscar_orden(IN p_numero INT)
BEGIN
    SELECT numero_produccion, fecha_emision, codigo_modelo,
           cantidad_producir, fecha_inicio, fecha_finalizacion,
           prioridad, estado_actual
    FROM orden_produccion
    WHERE numero_produccion = p_numero;
END //
DELIMITER ;


-- =====================================================
--  MÓDULO 3: INVENTARIO (componente)
-- =====================================================

DROP PROCEDURE IF EXISTS sp_listar_componentes;
DELIMITER //
CREATE PROCEDURE sp_listar_componentes()
BEGIN
    SELECT c.codigo_componente, c.descripcion, c.categoria,
           c.especificaciones_tecnicas, c.costo_unitario,
           c.stock_minimo, p.razon_social AS proveedor
    FROM componente c
    LEFT JOIN proveedores p ON c.codigo_proveedor = p.codigo_proveedor
    ORDER BY c.codigo_componente DESC;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS sp_insertar_componente;
DELIMITER //
CREATE PROCEDURE sp_insertar_componente(
    IN p_descripcion VARCHAR(255),
    IN p_categoria VARCHAR(100),
    IN p_especificaciones TEXT,
    IN p_codigo_proveedor INT,
    IN p_tiempo_entrega INT,
    IN p_costo_unitario DECIMAL(10,2),
    IN p_stock_minimo INT
)
BEGIN
    INSERT INTO componente
        (descripcion, categoria, especificaciones_tecnicas,
         codigo_proveedor, tiempo_entrega, costo_unitario, stock_minimo)
    VALUES
        (p_descripcion, p_categoria, p_especificaciones,
         p_codigo_proveedor, p_tiempo_entrega, p_costo_unitario, p_stock_minimo);
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS sp_actualizar_componente;
DELIMITER //
CREATE PROCEDURE sp_actualizar_componente(
    IN p_codigo INT,
    IN p_descripcion VARCHAR(255),
    IN p_categoria VARCHAR(100),
    IN p_especificaciones TEXT,
    IN p_codigo_proveedor INT,
    IN p_tiempo_entrega INT,
    IN p_costo_unitario DECIMAL(10,2),
    IN p_stock_minimo INT
)
BEGIN
    UPDATE componente
    SET descripcion = p_descripcion,
        categoria = p_categoria,
        especificaciones_tecnicas = p_especificaciones,
        codigo_proveedor = p_codigo_proveedor,
        tiempo_entrega = p_tiempo_entrega,
        costo_unitario = p_costo_unitario,
        stock_minimo = p_stock_minimo
    WHERE codigo_componente = p_codigo;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS sp_eliminar_componente;
DELIMITER //
CREATE PROCEDURE sp_eliminar_componente(IN p_codigo INT)
BEGIN
    DELETE FROM componente WHERE codigo_componente = p_codigo;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS sp_verificar_stock;
DELIMITER //
CREATE PROCEDURE sp_verificar_stock(IN p_codigo INT)
BEGIN
    SELECT c.codigo_componente, c.descripcion, c.stock_minimo,
           IFNULL(SUM(i.cantidad_disponible), 0) AS stock_actual,
           CASE
               WHEN IFNULL(SUM(i.cantidad_disponible), 0) <= c.stock_minimo
               THEN 'BAJO'
               ELSE 'SUFICIENTE'
           END AS estado_stock
    FROM componente c
    LEFT JOIN inventario i ON c.codigo_componente = i.codigo_componente
    WHERE c.codigo_componente = p_codigo
    GROUP BY c.codigo_componente, c.descripcion, c.stock_minimo;
END //
DELIMITER ;


-- =====================================================
--  MÓDULO 4: EMPLEADOS (empleado)
-- =====================================================

DROP PROCEDURE IF EXISTS sp_listar_empleados;
DELIMITER //
CREATE PROCEDURE sp_listar_empleados()
BEGIN
    SELECT numero_empleado, nombres, apellido, DNI,
           puesto, especializacion, numero_linea,
           turno, fecha_contratacion, evaluacion_desempeno
    FROM empleado
    ORDER BY numero_empleado DESC;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS sp_insertar_empleado;
DELIMITER //
CREATE PROCEDURE sp_insertar_empleado(
    IN p_nombres VARCHAR(50),
    IN p_apellido VARCHAR(100),
    IN p_dni VARCHAR(20),
    IN p_puesto VARCHAR(50),
    IN p_especializacion VARCHAR(100),
    IN p_numero_linea INT,
    IN p_turno VARCHAR(50),
    IN p_fecha_contratacion DATE,
    IN p_evaluacion DECIMAL(3,2)
)
BEGIN
    INSERT INTO empleado
        (nombres, apellido, DNI, puesto, especializacion,
         numero_linea, turno, fecha_contratacion, evaluacion_desempeno)
    VALUES
        (p_nombres, p_apellido, p_dni, p_puesto, p_especializacion,
         p_numero_linea, p_turno, p_fecha_contratacion, p_evaluacion);
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS sp_actualizar_empleado;
DELIMITER //
CREATE PROCEDURE sp_actualizar_empleado(
    IN p_numero INT,
    IN p_nombres VARCHAR(50),
    IN p_apellido VARCHAR(100),
    IN p_dni VARCHAR(20),
    IN p_puesto VARCHAR(50),
    IN p_especializacion VARCHAR(100),
    IN p_numero_linea INT,
    IN p_turno VARCHAR(50),
    IN p_fecha_contratacion DATE,
    IN p_evaluacion DECIMAL(3,2)
)
BEGIN
    UPDATE empleado
    SET nombres = p_nombres,
        apellido = p_apellido,
        DNI = p_dni,
        puesto = p_puesto,
        especializacion = p_especializacion,
        numero_linea = p_numero_linea,
        turno = p_turno,
        fecha_contratacion = p_fecha_contratacion,
        evaluacion_desempeno = p_evaluacion
    WHERE numero_empleado = p_numero;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS sp_eliminar_empleado;
DELIMITER //
CREATE PROCEDURE sp_eliminar_empleado(IN p_numero INT)
BEGIN
    DELETE FROM empleado WHERE numero_empleado = p_numero;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS sp_buscar_empleado;
DELIMITER //
CREATE PROCEDURE sp_buscar_empleado(IN p_numero INT)
BEGIN
    SELECT numero_empleado, nombres, apellido, DNI,
           puesto, especializacion, numero_linea,
           turno, fecha_contratacion, evaluacion_desempeno
    FROM empleado
    WHERE numero_empleado = p_numero;
END //
DELIMITER ;