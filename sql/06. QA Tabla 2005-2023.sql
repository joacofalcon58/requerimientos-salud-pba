USE GBA_Rendimientos;
GO

-- Cantidad de registros --

SELECT COUNT(*) AS cantidad_registros
FROM stg.rendimiento_2005_2023;

-- Cobertura de años --

SELECT
    MIN(anio) AS anio_minimo,
    MAX(anio) AS anio_maximo,
    COUNT(DISTINCT anio) AS cantidad_anios
FROM stg.rendimiento_2005_2023;

-- Top 20 para control visual --

SELECT TOP 20 *
FROM stg.rendimiento_2005_2023;

-- Campos identificadores vacios --

SELECT
    SUM(CASE WHEN anio IS NULL OR LTRIM(RTRIM(anio)) = '' THEN 1 ELSE 0 END) AS anio_vacio,
    SUM(CASE WHEN region_sanitaria IS NULL OR LTRIM(RTRIM(region_sanitaria)) = '' THEN 1 ELSE 0 END) AS region_vacia,
    SUM(CASE WHEN municipio_id IS NULL OR LTRIM(RTRIM(municipio_id)) = '' THEN 1 ELSE 0 END) AS municipio_id_vacio,
    SUM(CASE WHEN municipio_nombre IS NULL OR LTRIM(RTRIM(municipio_nombre)) = '' THEN 1 ELSE 0 END) AS municipio_vacio,
    SUM(CASE WHEN establecimiento_id IS NULL OR LTRIM(RTRIM(establecimiento_id)) = '' THEN 1 ELSE 0 END) AS establecimiento_id_vacio,
    SUM(CASE WHEN establecimiento_nombre IS NULL OR LTRIM(RTRIM(establecimiento_nombre)) = '' THEN 1 ELSE 0 END) AS establecimiento_vacio
FROM stg.rendimiento_2005_2023;

-- Dublicados exactos --

SELECT
    *,
    COUNT(*) AS cantidad
FROM stg.rendimiento_2005_2023
GROUP BY
    anio,
    region_sanitaria,
    municipio_id,
    municipio_nombre,
    establecimiento_id,
    establecimiento_nombre,
    dependencia,
    consultas_odontologicas,
    consultas_medicas,
    consultas_paramedicas,
    interconsultas,
    egresos,
    dias_camas_disponible,
    promedio_camas_disponibles,
    pacientes_dias,
    porcentaje_ocupacion,
    dias_estadia,
    promedio_dias_estadia,
    defunciones,
    giro_de_camas,
    tasa_mortalidad_hospitalaria,
    columna_extra
HAVING COUNT(*) > 1;

-- Columna extra --

SELECT
    columna_extra,
    COUNT(*) AS registros
FROM stg.rendimiento_2005_2023
GROUP BY columna_extra;