# Revisión del informe de establecimientos de salud

Estado: necesita revisión. Cobertura parcial: modelo vivo consultado mediante Power BI Modeling MCP 0.4.0 en modo de solo lectura, 43.725 filas recuperadas y reconciliadas con COUNTROWS; 42 medidas y columnas del modelo inspeccionadas. Páginas y filtros revisados en el PBIR guardado. No se verificó el renderizado ni las interacciones de la ventana de Power BI; los cambios visuales no guardados podrían diferir. No se modificó el informe ni el modelo.

## Conclusiones respaldadas

### Demanda registrada

La suma de consultas médicas, odontológicas, paramédicas e interconsultas creció de 50.466.975 en 2005 a 121.826.050 en 2024: +71.359.075, +141,4%, CAGR 4,75%. En 2019 hubo 95.361.530; en 2020, 75.081.975 (-21,3%); en 2023, 120.295.395; en 2024, +1,27%. El aumento de 2024 se explica aritméticamente por paramédicas (+1.257.482), odontológicas (+677.554) e interconsultas (+320.257), mientras médicas disminuyen 724.638.

Los cinco municipios de mayor contribución absoluta son Lomas de Zamora (+6.972.476), General San Martín (+5.842.897), Pilar (+3.994.259), Berazategui (+3.598.381) y La Plata (+3.255.527). Juntos explican 33,16% del aumento neto provincial. Se agrupa por municipio_id y DIM_Geografia para normalizar nombres.

Con regionalización constante de DIM_Geografia, V aporta +22.358.180 (31,33% del aumento); VI +19.000.159 (26,63%); XI +6.957.225 (9,75%); VIII +6.246.151 (8,75%). V y VI reúnen 57,96%. Esta comparación difiere deliberadamente del gráfico guardado, que usa la región registrada cada año. La Matanza está en VII en 2005 y XII en 2024; ese traslado no es crecimiento. Hay 29.720 atenciones de 2024 sin correspondencia en la dimensión geográfica (0,024% del total de ese año), retenidas en el denominador provincial.

Estos son servicios registrados, no personas únicas, necesidad sanitaria total ni demanda insatisfecha. La cobertura también cambia: 1.945 registros en 2005 y 2.371 en 2024. La serie no es un panel fijo de establecimientos; 2005–2017 no tienen establecimiento_id.

### Capacidad 2022–2024

La clasificación existente identifica 278 agudos, 20 saturados (ocupación agregada 90–100%), 50 subutilizados (≤40%, al menos 50 egresos por año informado), 25 con ocupación agregada >100%, y 183 restantes normales. Los saturados reúnen 1.807,3 camas promedio informadas; subutilizados 1.977,3. No son camas automáticamente reasignables.

Ejemplos con identidad nominal compatible en la ventana, recalculados desde las filas:

| Establecimiento | Camas promedio | Pacientes-día/año | Egresos/año | Ocupación agregada | Giro anual |
|---|---:|---:|---:|---:|---:|
| Ntra. Sra. del Carmen, Chacabuco | 203,3 | 71.210 | 19.389 | 96,0% | 95,4 |
| Raúl F. Larcade, San Miguel | 224,3 | 74.328 | 24.538 | 90,8% | 109,4 |
| Juan E. de la Fuente, General Belgrano | 73,0 | 25.480 | 3.342 | 95,5% | 45,8 |
| Eduardo Oller, Quilmes | 116,3 | 12.790 | 3.129 | 30,1% | 26,9 |
| Dra. Germani, La Matanza | 102,0 | 10.291 | 3.228 | 27,6% | 31,6 |
| A. Elicagaray, A. Gonzales Chaves | 94,3 | 11.559 | 1.550 | 33,5% | 16,4 |

Ocupación = suma pacientes-día / suma días-cama disponibles. Giro = suma egresos / suma camas promedio anuales. En los seis ejemplos existen los tres años, por lo que los promedios son sumas / 3. Son señales operativas según umbrales del informe, no validación externa de suficiencia de recursos.

Once de los 20 saturados tienen al menos un año con ocupación >100%. Thompson, por ejemplo, pasa de 91,8% en 2022 a 95,9% en 2023 y 115,2% en 2024, mientras la ventana agregada queda en 99,0%. La regla de anomalía sólo sobre el agregado oculta esos años. Nueve de los 20 tienen ≥90% los tres años, contando años >100%; ello no prueba por sí solo saturación operativa válida. Larcade pasa 84,9%→93,5%→94,5%, por lo que “sostenida durante todo 2022–2024” tampoco lo describe.

### Desempeño relativo y evolución

Medianas recalculadas de la cohorte del modelo (agudos, ≥100 egresos por año informado): municipal 3,1076 días / 2,5671% mortalidad (189 centros); provincial 5,5496 días / 4,4472% (71); nacional 8,7414 días / 8,9621% (2). La referencia nacional es particularmente pequeña. Son medianas puntuales, no bandas estadísticas ni ajuste de riesgo.

| Caso municipal | Estadía 2022–24 | Veces mediana | Mortalidad 2022–24 | Veces mediana | Evolución 2022→2024 |
|---|---:|---:|---:|---:|---|
| Pte. Néstor C. Kirchner, Escobar | 6,58 días | 2,12 | 12,01% | 4,68 | Estadía 5,88→7,70; mortalidad 11,28%→13,68% |
| Dr. A. Drozdowski, Malvinas Argentinas | 8,45 días | 2,72 | 15,69% | 6,11 | Estadía 5,76→14,43; mortalidad 8,67%→33,51% |
| Quijano, Lezama | 26,17 días | 8,42 | 7,03% | 2,74 | En 2023: 34,91 días / 8,65%; en 2024: 22,58 / 5,66%, mejora reciente |
| Juan E. de la Fuente, General Belgrano | 8,64 días | 2,78 | 3,43% | 1,34 | Estadía 8,35→8,48; mortalidad 4,02%→3,19% |

Drozdowski está nombrado como rehabilitación, pero entra a agudos porque la regla usa estadía ≤30 días. Su comparación requiere validar tipología y mezcla de pacientes. Kirchner tiene ocupación anual 2023 de 101,1%, alerta adicional de calidad/capacidad. Quijano y La Dulce cruzan 30 días en años particulares: segmentar por promedio puede ocultar perfiles cambiantes.

La etiqueta actual marca 90 establecimientos: 69 agudos y 21 de estadía prolongada comparados contra agudos. Cuarenta de los 69 agudos disparan sólo por estadía y quedan fuera de la tabla que exige además mortalidad ≥2 veces la mediana. Estos resultados identifican prioridades de revisión; no demuestran mala calidad asistencial ni causas clínicas. La evolución anterior es absoluta; el informe no implementa medianas anuales comparables para medir evolución relativa.

## Prioridades propuestas

1. Validar identidad antes de publicar nombres/rankings. Código 27400051: Mi Pueblo en 2022–23, Zeballos II en 2024; 59500191: Oncología L. Fortabat versus Espigas; 86100073: Maternidad Santa Rosa versus Cetrángolo. Los datos no permiten decidir si son reasignaciones, nombres incorrectos u otro problema. Hay 372 códigos con más de un texto de nombre durante 2022–24; este conteo incluye variaciones ortográficas y no equivale a 372 identidades erróneas.
2. Unificar ventana de P3. La tabla mezcla medidas históricas sin filtro de año con ratios fijos 2022–24. Mostrar valores de la misma ventana y cobertura.
3. Unificar cohorte de P3 y selección visual. Clasificación aplica LOS≥1,6 o mortalidad≥2, pero tabla/barras/línea exigen además mortalidad≥2/2,5/4. Añadir agudos al criterio o construir referentes específicos para otros tipos. Mostrar ambas trayectorias y mediana anual de la misma dependencia, con cohorte/criterio explícitos.
4. Corregir comparación regional a geografía constante, o separar explícitamente reasignaciones administrativas de cambios asistenciales.
5. Detectar ocupación >100% por año además de la ventana. Mostrar pacientes-día, egresos, años reportados y consistencia entre camas y días-cama. Reemplazar “sostenida” por “agregada” cuando no se comprueba persistencia.
6. Alinear tarjeta de ocupación 2024 (todos los segmentos) con universo y período de las demás vistas de capacidad, o rotular la diferencia.
7. Diferenciar ausencia y cero. Camas/egresos anuales se dividen por cantidad de años positivos, no siempre por tres. Once agudos tienen menos de tres años registrados, entre ellos U.S. N°28 con sólo 2024. Su etiqueta 2022–24 no representa tres observaciones.

## Qué conservar y simplificar

Conservar la organización en tres páginas; suma de las cuatro prestaciones; línea anual de demanda; contribución municipal absoluta; razones de sumas para tasas; cruce ocupación/giro/camas; referencia por dependencia como primera aproximación y avisos de comparabilidad.

Mover a detalle la tabla de crecimiento por establecimiento 2018–24 en P1, que responde otra escala y período y enfrenta problemas de identidad. Reemplazar su espacio por participación municipal/regional en el aumento. CAGR puede ir en tooltip. Defunciones totales 2024 es menos útil para desempeño relativo que egresos y cobertura de la cohorte. No llamar “banda” a una sola mediana: renombrar o añadir un intervalo explícito.

## Cobertura de revisión

Los denominadores siguientes son preguntas/páginas dentro del alcance, no porcentaje de exactitud ni verificación de todos los visuales. N/E significa denominador completo no establecido.

| Categoría | Defectos observados | Evaluación |
|---|---|---|
| Utilidad y completitud | 3 / 3 | P1 comparación regional heterogénea; P2 faltan pacientes-día/egresos visibles; P3 falta evolución relativa y estadía. |
| Claridad analítica | 3 / 3 | Crecimiento regional sin geografía constante; saturación “sostenida”; banda y períodos P3. |
| Consistencia visual/interacción | N/E | Se inspeccionó PBIR; no render ni interacción en Desktop. |

| Categoría | Defectos observados | Evaluación |
|---|---|---|
| Autoridad/confianza de fuente | N/E | Fuente viva solicitada verificada; identidad y nombres requieren validación aguas arriba. |
| Exactitud de cifras | N/E | Demanda global, referencias y ejemplos seleccionados reconciliados; no se certifica cada visual. |
| Acuerdo dentro de gráficos | N/E | Períodos incompatibles constatados en tabla P3; no lectura visual de valores renderizados. |
| Detalle completo de fuentes | N/E | Consultas y extractos conservados; origen primario no contrastado externamente. |
| Consistencia entre componentes | N/E | Cohortes P3 y tarjeta P2 difieren. |
| Controles de calidad | N/E | Identidad, cobertura y anomalías anuales no resueltas por el diseño actual. |
| Soporte de conclusiones | 2 / 3 | Demanda global sustentada; rankings de capacidad/desempeño precisan salvedades y reparación. |

## Evidencia reproducible

- `008.csv`: extracto completo de GBA_Rendimientos obtenido por MCP, 43.725 filas.
- `009.csv`: DIM_Establecimientos con clasificaciones, métricas y referencias.
- `006.csv`, `007.csv`: columnas y medidas del modelo vivo.
- `010.csv`: geografía del modelo; `012.csv`: comparación regional homogénea ejecutada en DAX.
- `011.csv`: control independiente DAX de conteo y demanda 2005/2024.
- `analysis.json`, `details.txt`, `analyze.py`, `detail.py`, `selected.py`: cálculos independientes desde extractos. Los decimales del CSV usan coma y se normalizan antes del cálculo.

Los ID vacíos antes de 2018 son falta de identificador, no duplicados probados de registros; no se deduplicaron. Los resultados corresponden al contenido importado que estaba abierto, sin actualizar fuentes. No se verificaron causas epidemiológicas ni ajuste de riesgo clínico.
