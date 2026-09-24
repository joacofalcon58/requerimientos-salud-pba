# Handoff: Dashboard nativo en Power BI — "Requerimientos de establecimientos de Salud"

## Contexto y objetivo

Proyecto PBIP en `C:\Users\joaco\Documents\Porfolio\Requerimientos de establecimientos de Salud.pbip` (no es un repo git). El pedido original: construir un dashboard ejecutivo **dentro del propio informe de Power BI** (no solo como HTML aparte) que responda 3 preguntas de negocio sobre datos de salud de la Provincia de Buenos Aires (2005–2024):

1. Evolución de la demanda 2005–2024 por municipio/región/establecimiento.
2. Señales de saturación/subutilización de capacidad hospitalaria.
3. Peor desempeño relativo de internación (estadía, mortalidad) y su evolución.

Ya existe un dashboard HTML publicado (con diseño en base al manual de marca de la Provincia, Anexo III) que responde las 3 preguntas — ese quedó bien. Lo que falta es la parte nativa en Power BI Desktop, que quedó a mitad de camino.

## Estado actual en disco (confirmado, es la fuente de verdad)

- **Medidas DAX: OK, persistidas.** La tabla `GBA_Rendimientos.tmdl` en `.../Requerimientos de establecimientos de Salud.SemanticModel/definition/tables/` tiene las **20 medidas** creadas y guardadas (confirmado con `grep -c "^\s*measure "` = 20). Ver detalle completo abajo.
- **Páginas del reporte: NO se llegó a aplicar.** Se generaron 3 páginas nuevas vía archivos PBIR (JSON) directamente en disco, pero al intentar cargarlas en Power BI Desktop (flujo "Apply external changes") la app terminó cerrándose y, al cerrar, **sobrescribió los archivos del reporte con su estado en memoria anterior** (1 sola página, la que ya existía, con un visual placeholder vacío tipo "anio"). O sea: **hoy `pages.json` en disco vuelve a tener solo 1 página** ("5dd4ac40977d4030d72e"), y el trabajo de generación de las 3 páginas se perdió del `.Report` folder (pero el código generador quedó documentado abajo, así que es 100% reproducible).
- **Backup manual disponible**: `C:\Users\joaco\Documents\Porfolio\_backup_20260908_142713\` — copia completa de `.Report` y `.SemanticModel` de antes de tocar nada. Útil como red de seguridad, aunque a esta altura lo más simple es regenerar desde cero con el script.
- El proyecto **no está bajo git**, así que no hay historial de versiones aparte del backup manual.

## Lo que quedó bloqueado (para que Claude Code no repita el mismo camino)

Automatizar Power BI Desktop por UI (clicks/teclado remoto) resultó muy poco confiable:

- `computer_open_application "Power BI Desktop"` casi siempre abre una instancia nueva en blanco en vez de enfocar la existente → hay que revisar `ListLocalInstances` y cerrar duplicados todo el tiempo.
- Una app externa (el propio cliente de Claude) le roba el foco a la ventana de Windows todo el tiempo entre llamadas, así que un screenshot inmediatamente después de una acción no siempre refleja el resultado real.
- El diálogo nativo "¿Desea guardar los cambios?" que aparece al usar "Apply external changes" **no respondía a clicks de mouse** (probado con coordenadas verificadas por zoom, en distintos intentos) pero **sí respondía al teclado** (Tab/Enter/Escape funcionaban). Aun así, en el intento final, el flujo terminó cerrando Power BI Desktop por completo y **al cerrar, la app re-escribió los archivos PBIR con su versión vieja (en memoria)**, pisando las 3 páginas nuevas generadas en disco.

**Conclusión / recomendación para Claude Code:** no intentar aplicar cambios de archivo con Power BI Desktop *abierto* (el flujo "Apply external changes" es frágil y puede revertir todo al cerrar). El camino más seguro es:

1. Power BI Desktop **completamente cerrado** (verificar con `ListLocalInstances` → 0 instancias, o simplemente pedirle al usuario que lo cierre).
2. Escribir/editar los archivos PBIR directamente en disco (edición de texto, no requiere Desktop abierto).
3. Recién ahí abrir el `.pbip` de cero (doble click o "Recientes" en Desktop) — así carga los archivos frescos del disco sin pasar por ningún diálogo de conflicto.
4. Verificar visualmente que las páginas/visuales carguen sin errores, y ahí sí guardar (Ctrl+S) para fijar el estado.

## Modelo de datos (confirmado vía MCP powerbi-modeling)

**Tabla de hechos `GBA_Rendimientos`** — columnas: `anio` (Int64), `dependencia` (String), `establecimiento_id` (String), `region_sanitaria` (String), `municipio_id` (String), `municipio_nombre` (String), `establecimiento_nombre` (String), `consultas_odontologicas`, `consultas_medicas`, `consultas_paramedicas`, `interconsultas`, `egresos`, `dias_camas_disponible`, `promedio_camas_disponibles`, `pacientes_dias` (Int64), `porcentaje_ocupacion`, `giro_de_camas` (Double), `dias_estadia` (Int64), `promedio_dias_estadia`, `tasa_mortalidad_hospitalaria` (Double), `defunciones` (Int64), `columna_extra` (String), `Fecha` (DateTime).

**Dimensiones:**
- `Calendario`: Fecha, Anio, MesNro, Mes, AnioMes, TrimestreNro, Trimestre, AnioTrimestre, Dia, DiaSemanaNro, DiaSemana, Decada.
- `DIM_Establecimientos`: establecimiento_id, establecimiento_nombre.
- `DIM_Geografia`: municipio_id, municipio_nombre, region_sanitaria, latitud, longitud.
- `DIM_Dependencia`: dependencia_id, dependencia.

**Relaciones**: todas `OneDirection`, `Many→One`, desde `GBA_Rendimientos` hacia cada dimensión (por `dependencia`, `establecimiento_id`, `municipio_id`) y hacia `Calendario` (por `Fecha`).

⚠️ **Advertencia de calidad de datos** (ya detectada y documentada en el HTML): el campo `establecimiento_id` está vacío en el 100% de las filas 2005–2017 (solo hay `municipio` y `región sanitaria` disponibles en ese tramo). El desglose por establecimiento recién es confiable desde 2018. Cualquier tabla/gráfico por establecimiento debería aclarar esto o filtrar 2018–2024.

## Las 20 medidas DAX (tabla `GBA_Rendimientos`, 3 carpetas de visualización)

### 01. Demanda
```
Total Consultas Médicas = SUM(GBA_Rendimientos[consultas_medicas])
Total Consultas Odontológicas = SUM(GBA_Rendimientos[consultas_odontologicas])
Total Consultas Paramédicas = SUM(GBA_Rendimientos[consultas_paramedicas])
Total Interconsultas = SUM(GBA_Rendimientos[interconsultas])

Demanda Total de Atención =
    [Total Consultas Médicas] + [Total Consultas Odontológicas] +
    [Total Consultas Paramédicas] + [Total Interconsultas]

Demanda Año Base (2005) =
    CALCULATE([Demanda Total de Atención], GBA_Rendimientos[anio] = 2005)

Demanda Año Actual (2024) =
    CALCULATE([Demanda Total de Atención], GBA_Rendimientos[anio] = 2024)

Crecimiento Demanda 2005-2024 % =
    DIVIDE([Demanda Año Actual (2024)] - [Demanda Año Base (2005)], [Demanda Año Base (2005)])

CAGR Demanda 2005-2024 % =
    IF([Demanda Año Base (2005)] > 0,
       (DIVIDE([Demanda Año Actual (2024)], [Demanda Año Base (2005)]) ^ (1/19)) - 1)

Demanda YoY % =
    VAR AnioActual = MAX(GBA_Rendimientos[anio])
    VAR DemandaActual = [Demanda Total de Atención]
    VAR DemandaAnterior =
        CALCULATE([Demanda Total de Atención], GBA_Rendimientos[anio] = AnioActual - 1)
    RETURN DIVIDE(DemandaActual - DemandaAnterior, DemandaAnterior)
```

### 02. Capacidad Hospitalaria
```
Total Camas Disponibles (prom) = SUM(GBA_Rendimientos[promedio_camas_disponibles])
Total Días Cama Disponible = SUM(GBA_Rendimientos[dias_camas_disponible])
Total Pacientes-Día = SUM(GBA_Rendimientos[pacientes_dias])
Total Egresos = SUM(GBA_Rendimientos[egresos])

% Ocupación = DIVIDE([Total Pacientes-Día], [Total Días Cama Disponible])

Giro de Camas (anual) = DIVIDE([Total Egresos], [Total Camas Disponibles (prom)])

Establecimientos con Internación =
    CALCULATE(
        DISTINCTCOUNT(GBA_Rendimientos[establecimiento_id]),
        GBA_Rendimientos[promedio_camas_disponibles] > 0
    )
```

### 03. Calidad de Internación
```
Total Defunciones = SUM(GBA_Rendimientos[defunciones])

Promedio Días de Estadía = DIVIDE(SUM(GBA_Rendimientos[dias_estadia]), [Total Egresos])

Tasa de Mortalidad Hospitalaria % = DIVIDE([Total Defunciones], [Total Egresos])
```

**Nota de diseño importante**: todas las medidas de ratio/porcentaje usan `DIVIDE` de numerador y denominador agregados (no promedio de porcentajes por fila), justamente para evitar la paradoja de Simpson al filtrar/agrupar por distintas dimensiones. Mantené ese patrón si se agregan medidas nuevas.

**Sanity check ya verificado con `dax_query_operations Execute`** (útil para confirmar que las medidas siguen bien si se recrean): Demanda Total ≈ 1.549.481.211; Demanda 2005 ≈ 50.466.975; Demanda 2024 ≈ 121.826.050; Crecimiento % ≈ 141,4%; CAGR % ≈ 4,75%; % Ocupación ≈ 73,1%; Giro Camas ≈ 37,3; Mortalidad % ≈ 3,18%; Días Estadía ≈ 6,84.

## Diseño de las 3 páginas del reporte (plan completo, listo para regenerar)

Formato de página: 1920×1080, `displayOption: FitToPage`.

**Layout común** (constantes de posición usadas en las 3 páginas):
- 3 tarjetas KPI arriba: `y=24, h=130, w=360`, en `x = [24, 404, 784]`.
- Gráfico principal (izquierda): `x=24, y=174, w=1120, h=460`.
- Gráfico secundario (derecha): `x=1164, y=174, w=732, h=460`.
- Tabla de detalle (abajo, ancho completo): `x=24, y=654, w=1872, h=400`.

**Página 1 — "01. Demanda de Atención"**
- Tarjetas: `Demanda Año Actual (2024)`, `Crecimiento Demanda 2005-2024 %`, `CAGR Demanda 2005-2024 %`.
- Gráfico de línea: Categoría = `anio`, Y = `Demanda Total de Atención`.
- Gráfico de barras: Categoría = `DIM_Geografia.municipio_nombre`, Y = `Demanda Total de Atención`.
- Tabla: columnas `establecimiento_nombre`, `municipio_nombre` + medidas `Demanda Total de Atención`, `Total Consultas Médicas`, `Crecimiento Demanda 2005-2024 %`.

**Página 2 — "02. Capacidad Hospitalaria"**
- Tarjetas: `% Ocupación`, `Giro de Camas (anual)`, `Establecimientos con Internación`.
- Gráfico de dispersión (scatter): Categoría = `establecimiento_nombre`, X = `% Ocupación`, Y = `Giro de Camas (anual)`, Tamaño = `Total Egresos`.
- Gráfico de barras: Categoría = `municipio_nombre`, Y = `% Ocupación`.
- Tabla: columnas `establecimiento_nombre`, `municipio_nombre` + medidas `Total Camas Disponibles (prom)`, `Total Pacientes-Día`, `% Ocupación`, `Giro de Camas (anual)`.

**Página 3 — "03. Calidad de Internación"**
- Tarjetas: `Promedio Días de Estadía`, `Tasa de Mortalidad Hospitalaria %`, `Total Defunciones`.
- Gráfico de dispersión: Categoría = `establecimiento_nombre`, X = `Promedio Días de Estadía`, Y = `Tasa de Mortalidad Hospitalaria %`, Tamaño = `Total Egresos`.
- Gráfico de barras: Categoría = `municipio_nombre`, Y = `Tasa de Mortalidad Hospitalaria %`.
- Tabla: columnas `establecimiento_nombre`, `municipio_nombre`, `dependencia` + medidas `Promedio Días de Estadía`, `Tasa de Mortalidad Hospitalaria %`, `Total Defunciones`.

## Detalle técnico PBIR (formato de reporte de Power BI, "Enhanced Report Format")

Rutas dentro de `Requerimientos de establecimientos de Salud.Report/definition/`:
- `pages/pages.json` → `{"$schema": ".../pagesMetadata/1.1.0/schema.json", "pageOrder": [...ids...], "activePageName": "<id>"}`
- `pages/<pageId>/page.json` → `{"$schema": ".../page/2.1.0/schema.json", "name": "<pageId>", "displayName": "...", "displayOption": "FitToPage", "height": 1080, "width": 1920}`
- `pages/<pageId>/visuals/<visualId>/visual.json` → un archivo por visual.

Esquema de `visual.json` confirmado (schema `visualContainer/2.4.0`, `https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.4.0/schema.json`):

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.4.0/schema.json",
  "name": "<hexId>",
  "position": {"x": 0, "y": 0, "z": 2001, "height": 130, "width": 360, "tabOrder": 0},
  "visual": {
    "visualType": "card | lineChart | barChart | scatterChart | tableEx",
    "query": {"queryState": { "...roles...": {"projections": [ ... ]} }},
    "objects": { ... formato específico del tipo de visual ... },
    "visualContainerObjects": {"title": [{"properties": {
        "show": {"expr": {"Literal": {"Value": "true"}}},
        "text": {"expr": {"Literal": {"Value": "'Texto del título'"}}}
    }}]}
  },
  "filterConfig": {"filters": [{"name": "<hexId>", "field": {...}, "type": "Categorical"}]}
}
```

Binding de un campo **medida**:
```json
{
  "field": {"Measure": {"Expression": {"SourceRef": {"Entity": "GBA_Rendimientos"}}, "Property": "Total Egresos"}},
  "queryRef": "GBA_Rendimientos.Total Egresos",
  "nativeQueryRef": "Total Egresos"
}
```

Binding de un campo **columna** (agregar `"active": true` en el campo principal/categoría):
```json
{
  "field": {"Column": {"Expression": {"SourceRef": {"Entity": "DIM_Geografia"}}, "Property": "municipio_nombre"}},
  "queryRef": "DIM_Geografia.municipio_nombre",
  "nativeQueryRef": "municipio_nombre",
  "active": true
}
```

`queryState` usa roles según el tipo de visual: `Values` (card, tableEx), `Category`/`Y` (lineChart, barChart), `Category`/`X`/`Y`/`Size` (scatterChart).

## Script generador (ya escrito y probado — reusar tal cual)

Hay un script Python completo y ya validado (corrió sin errores, generó JSON sintácticamente válido) en `/tmp/generate_pbir.py` de esta sesión — contiene las funciones helper (`hexid`, `col_proj`, `measure_proj`, `title_obj`, `base_container`, `make_card`, `make_line_chart`, `make_bar_chart`, `make_scatter`, `make_table`, `write_page`) y arma las 3 páginas completas con el layout y contenido de arriba. Pídanle a Claude Code que lo tome como base — es prácticamente el generador PBIR completo, solo faltaría:

1. **Antes de correrlo de nuevo**: borrar el visual placeholder viejo que quedó en la página 1 (`pages/5dd4ac40977d4030d72e/visuals/d0def68c119cc2339394/`), porque el script no limpia visuales viejos, solo agrega nuevos.
2. Confirmar que Power BI Desktop esté **cerrado** antes de escribir/aplicar los archivos (ver sección de bloqueos arriba).
3. Validar el JSON resultante (`json.load` sobre cada archivo) antes de abrir el `.pbip`.
4. Abrir el `.pbip` de cero y verificar visualmente que las 3 páginas y sus 18 visuales carguen sin "campo no encontrado" ni placeholders rojos de error.
5. Guardar (Ctrl+S) una vez confirmado.

## Referencias de esquema PBIR usadas (por si hace falta volver a consultarlas)

Las plantillas de visual reales que sirvieron de base para el generador vienen del repo público `cn-dataworks/pbir-visuals` (rama `master`, no `main`):
- `https://raw.githubusercontent.com/cn-dataworks/pbir-visuals/master/skills/pbir-visual-creator/SKILL.md`
- `https://cdn.jsdelivr.net/gh/cn-dataworks/pbir-visuals@master/visual-templates/card-single-measure.json`
- `https://cdn.jsdelivr.net/gh/cn-dataworks/pbir-visuals@master/visual-templates/line-chart-category-y.json`
- `https://cdn.jsdelivr.net/gh/cn-dataworks/pbir-visuals@master/visual-templates/bar-chart-category-y.json`
- `https://cdn.jsdelivr.net/gh/cn-dataworks/pbir-visuals@master/visual-templates/table-basic.json`
- `https://cdn.jsdelivr.net/gh/cn-dataworks/pbir-visuals@master/visual-templates/scatter-bubble-chart.json`

(`github.com/.../tree/...` y la API de GitHub están bloqueados por robots/perm404 en algunos entornos — el mirror de `raw.githubusercontent.com` / `cdn.jsdelivr.net` funciona.)

## Próximo paso sugerido

Dado que la edición de archivos PBIR no depende de tener Power BI Desktop abierto, el camino de menor fricción para Claude Code es: (1) pedir que se cierre Power BI Desktop, (2) limpiar el visual placeholder viejo y volver a correr el generador, (3) abrir el `.pbip` de cero y verificar, (4) guardar. Si Claude Code tiene acceso a MCP de Power BI modeling, las medidas ya están OK y no hace falta tocarlas — solo hay que regenerar las páginas del reporte.
