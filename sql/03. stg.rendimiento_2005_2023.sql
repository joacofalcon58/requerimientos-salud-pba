USE GBA_Rendimientos;
GO

CREATE TABLE stg.rendimiento_2005_2023 (

    anio VARCHAR(10),
    region_sanitaria VARCHAR(10),
    municipio_id VARCHAR(20),
    municipio_nombre NVARCHAR(150),

    establecimiento_id VARCHAR(50),
    establecimiento_nombre NVARCHAR(250),

    dependencia NVARCHAR(100),

    consultas_odontologicas VARCHAR(50),
    consultas_medicas VARCHAR(50),
    consultas_paramedicas VARCHAR(50),
    interconsultas VARCHAR(50),
    egresos VARCHAR(50),

    dias_camas_disponible VARCHAR(50),
    promedio_camas_disponibles VARCHAR(50),
    pacientes_dias VARCHAR(50),

    porcentaje_ocupacion VARCHAR(50),

    dias_estadia VARCHAR(50),
    promedio_dias_estadia VARCHAR(50),

    defunciones VARCHAR(50),

    giro_de_camas VARCHAR(50),
    tasa_mortalidad_hospitalaria VARCHAR(50),

    columna_extra VARCHAR(50)

);
GO