# Datos

## Origen

`raw/rendimiento_2005_2023.csv` y `raw/rendimiento_2024.csv` son extractos de datos
públicos de rendimientos de establecimientos de salud de la Provincia de Buenos
Aires: consultas médicas, odontológicas, paramédicas, interconsultas, camas
disponibles, pacientes-día, egresos y defunciones por establecimiento y año
(2005–2024, 43.725 filas en total).

Este es un dataset público de terceros (Gobierno de la Provincia de Buenos Aires),
no propiedad de este repositorio — ver la nota de licencia en el [`README`](../README.md)
principal.

## Cómo se usan

Los scripts en [`../sql/`](../sql/) cargan estos CSV a SQL Server (`BULK INSERT`),
los separan en tablas de staging y arman las tablas finales que alimenta el modelo
semántico de Power BI en [`../dashboard/`](../dashboard/). El detalle de columnas
calculadas y medidas DAX está en [`../docs/methodology.md`](../docs/methodology.md).

## Nota sobre los scripts SQL

Los pasos `05.` y `07.` en `sql/` usan `BULK INSERT ... FROM '<path>'` con una ruta
de archivo absoluta del entorno original de construcción — es una limitación de
T-SQL (`BULK INSERT` necesita una ruta del lado del servidor, no puede ser relativa
al repositorio). Para reproducir el proceso, editá esa ruta para que apunte a donde
hayas copiado estos CSV antes de ejecutar el script.

## Limitaciones conocidas

Ver [`../docs/data-quality.md`](../docs/data-quality.md) para el detalle completo:
identidad de establecimientos no persistente antes de 2018, códigos reasignados
entre años, y cobertura variable de campos de internación.
