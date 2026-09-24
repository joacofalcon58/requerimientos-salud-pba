# Handoff — Auditoría del informe de establecimientos de salud

Fecha: 18 de septiembre de 2026.

Proyecto: `C:\Users\joaco\Documents\Porfolio\Requerimientos de establecimientos de Salud.pbip`.

HTML informado por el usuario: https://claude.ai/artifact/NEGpzwuRoYTWtn4tu721Bf

## Resumen para quien retome el trabajo

El dashboard está bien organizado en tres preguntas, pero necesita corregir comparabilidad territorial, identidad de establecimientos, períodos y cohortes antes de presentar rankings como conclusiones de gestión. La demanda total fue reconciliada; las clasificaciones hospitalarias deben interpretarse con las limitaciones detalladas abajo.

**Actualización 18-sep-2026 (tarde): las 4 prioridades acordadas con el usuario ya se aplicaron** en Power BI y en el HTML — ver `docs/dashboard-powerbi-build.md`, sección "Auditoría de comparabilidad". Resumen: geografía constante en el gráfico de regiones de P1 (nueva tabla de participación municipal/regional 2005-2024 reemplazó la de crecimiento por establecimiento 2018-2024); tarjeta de ocupación de P2 recalculada a agudos + ventana 2022-2024 (69,9%, antes 75,5% con todos los establecimientos); cohorte de P3 unificada (mismo filtro base en tarjeta/tabla/gráfico/línea, sin umbrales de mortalidad distintos no declarados); "ocupación sostenida" renombrada a "agregada". El resto de las prioridades propuestas más abajo (validar 372 identidades reasignadas, alerta de ocupación >100% año por año, medianas anuales por dependencia) quedan **pendientes**, fueron señaladas al usuario pero no elegidas para esta pasada. El resto de este documento es el detalle original de la auditoría; los números de ejemplo que cita ya no reflejan las tarjetas corregidas arriba, pero sí los datos crudos subyacentes.

**Actualización 18-sep-2026 (noche): se retiraron de pantalla los 4 carteles de advertencia** que mostraban estas mismas salvedades (límite de datos pre-2018, 25 establecimientos con ocupación >100%, IDs no persistentes/372 códigos reasignados, casemix en mortalidad) — pedido explícito del usuario: un gerente/director no necesita ver estas notas en el dashboard, solo los números ya corregidos por la auditoría. Las notas de este documento (y la sección 6 de `docs/dashboard-powerbi-build.md`) son ahora el único lugar donde constan; **siguen siendo válidas como limitaciones de los datos**, solo se sacaron de la interfaz. En Power BI se borraron los 4 textbox y se agrandaron las tablas siguientes para ocupar el espacio; en el HTML se borraron los 4 `<div class="callout">` (el layout de flujo se reacomodó solo) y se publicó como Versión 4. El pie de página del HTML ("Notas metodológicas y de calidad de datos") ya contenía estas mismas limitaciones en prosa y no se modificó.

Respaldo previo a cambios: `C:\Users\joaco\Documents\Porfolio\_backup_20260918_correcciones\` (Report, SemanticModel, PBIP y generador de páginas).

El HTML no pudo inspeccionarse: el enlace requiere iniciar sesión en Claude desde el navegador disponible. No se encontró una copia HTML local dentro del proyecto. Las conclusiones sobre su implementación exacta quedan pendientes; no debe afirmarse que ya se auditó o corrigió ese artefacto.

## Objetivo acordado

1. Explicar la evolución de la demanda 2005–2024 y los municipios/regiones que concentran el crecimiento, sumando las cuatro prestaciones.
2. Detectar señales de saturación/subutilización de agudos con camas, pacientes-día, ocupación, egresos y giro en 2022–2024.
3. Comparar estadía y mortalidad con la mediana de la misma dependencia e interpretar su evolución.

## Alcance y evidencia

Estado: necesita revisión. Cobertura parcial: modelo vivo consultado mediante Power BI Modeling MCP 0.4.0 en modo de solo lectura, 43.725 filas recuperadas y reconciliadas con COUNTROWS; se inspeccionaron las 42 medidas y el esquema de columnas del modelo. Páginas y filtros revisados en el PBIR guardado. Posteriormente se observó la primera página en Desktop y se guardó el estado existente, pero no se realizó una validación visual completa ni una prueba de interacciones de las tres páginas. No se aplicaron correcciones al informe ni al modelo.

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

Todos los archivos de evidencia enumerados arriba están en `C:\Users\joaco\Documents\Porfolio\docs\revision-20260918\`. Los CSV son evidencia de la auditoría, no sustituyen una nueva lectura del modelo si los datos cambian.

## Ubicación de las correcciones en Power BI

Raíz del reporte: `C:\Users\joaco\Documents\Porfolio\Requerimientos de establecimientos de Salud.Report\definition\`.

| Página / componente | Archivo relativo a la raíz del reporte | Corrección pendiente |
|---|---|---|
| Orden de páginas | `pages\pages.json` | Conservar las tres páginas y sus identificadores. |
| P1: regiones | `pages\5dd4ac40977d4030d72e\visuals\e26907092a1b4e8591d6\visual.json` | Cambiar categoría de `GBA_Rendimientos[region_sanitaria]` a `DIM_Geografia[region_sanitaria]` y declarar regionalización constante. |
| P2: dispersión | `pages\1b3902ad5838b2b7a8e8\visuals\8dc6168b6a850abc0d89\visual.json` | Actualmente sólo filtra Agudos; distinguir/excluir anomalías del conjunto comparable, sin ocultarlas del informe. |
| P2: saturados | `pages\1b3902ad5838b2b7a8e8\visuals\2cb01cea4c8dcdd8ad02\visual.json` | Añadir pacientes-día, egresos, cobertura y alerta anual; corregir “sostenida”. |
| P2: subutilizados | `pages\1b3902ad5838b2b7a8e8\visuals\b80becd9e6f980b0b2ce\visual.json` | Añadir denominadores y cobertura; evitar equiparar baja utilización con camas transferibles. |
| P2: tarjeta ocupación | `pages\1b3902ad5838b2b7a8e8\visuals\e80e36dd81a87e7e314d\visual.json` | Alinear universo y período con el análisis de capacidad. |
| P3: tabla | `pages\1cd2a9963f2a78d63974\visuals\b9d187645049112683d3\visual.json` | Usar absolutos de 2022–2024 junto con ratios de esa misma ventana; quitar filtro adicional de mortalidad ≥2. |
| P3: barras | `pages\1cd2a9963f2a78d63974\visuals\570ef0a7ececc61bb96f\visual.json` | Quitar mortalidad ≥2,5 como selección distinta; incluir alertas de estadía. |
| P3: evolución | `pages\1cd2a9963f2a78d63974\visuals\00c8b7256be261865cea\visual.json` | Quitar selección arbitraria ≥4; incorporar estadía y referencia anual comparable. |

Modelo: `C:\Users\joaco\Documents\Porfolio\Requerimientos de establecimientos de Salud.SemanticModel\definition\tables\`.

- `DIM_Establecimientos.tmdl`: criterios de elegibilidad, clasificaciones, promedios, medianas y ratios.
- `GBA_Rendimientos.tmdl`: medidas y formatos. Mantener numeradores y denominadores compatibles; no reemplazar razones de sumas por promedios simples de porcentajes.
- `DIM_Geografia.tmdl`: clasificación territorial para comparación homogénea.
- `..\relationships.tmdl`: relación por establecimiento_id y relaciones geográficas/temporales; revisar impacto antes de introducir una correspondencia histórica.
- `C:\Users\joaco\Documents\Porfolio\docs\gen_pbir.py`: generador previo. No ejecutarlo sin adaptarlo: conserva la lógica auditada, crea nuevos identificadores para P2/P3 y puede reintroducir los errores. Preferir cambios dirigidos sobre archivos actuales y actualizar después el generador.

Los identificadores de visual se verificaron en los archivos guardados al auditar; volver a comprobarlos si alguien edita o regenera el informe.

## Plan concreto de implementación

### 1. Preservar y recuperar el estado vigente

- Confirmar que el PBIP abierto corresponde al proyecto indicado.
- Guardar cambios existentes y conservar un respaldo del Report, SemanticModel y HTML original.
- Comparar contra este handoff; no sobrescribir cambios posteriores del usuario.
- Para editar PBIR en disco, cerrar primero Desktop de forma normal después de guardar. Los handoffs anteriores documentan que la aplicación llegó a sobrescribir cambios externos con su versión en memoria. No forzar el cierre ni descartar cambios sin revisar el estado.

### 2. Resolver calidad sin inventar identidades

- Agregar cobertura 2022–2024 y por métrica: años informados, ceros y faltantes por separado.
- Incorporar alerta de nombre/identidad y listado de revisión con ID, año y nombre original. Una diferencia de texto es una señal de revisión, no evidencia automática de institución distinta.
- Validar correspondencias de los casos materialmente distintos con la fuente original. No reasignar ni corregir nombres por intuición.
- Mientras no se resuelvan, separarlos claramente del ranking atribuible a instituciones y conservarlos en una vista de calidad. Mostrar el número de excluidos y el motivo; no eliminarlos de la demanda agregada provincial.
- Distinguir “agudos inferidos por estadía” de tipología oficial. No presentar esa inferencia como clasificación institucional validada.

### 3. Ajustar definiciones

- Corregir `Dependencia` y `Municipio`: el fallback actual usa SELECTEDVALUE sobre toda la historia, aunque la descripción promete el último dato. Debe seleccionar efectivamente el último año disponible y detectar conflictos dentro de ese año.
- Contar años no vacíos al calcular promedios por año informado; no excluir un cero válido. Si se exige un promedio de tres años, requerir cobertura completa y mantener incompletos como categoría aparte.
- Crear una alerta anual de ocupación >100%, además de la agregada. Definir la prioridad de esa alerta antes de etiquetar saturación/subutilización.
- Aplicar la misma elegibilidad a la referencia de desempeño y a los establecimientos evaluados. Las estadías prolongadas deben tener referencia propia o quedar fuera de la comparación aguda.
- Crear valores de estadía, mortalidad y egresos de la misma ventana 2022–2024 para la tabla. Las columnas fijas no deben aparentar responder a un filtro anual.
- Para evolución, calcular mediana por año y dependencia con elegibilidad explícita; mostrar tamaño de la cohorte y conservar el contexto anual al retirar sólo el filtro de establecimiento. No promediar medianas de distintas dependencias.
- Mantener los umbrales como reglas descriptivas del tablero: ocupación ≥90%, ≤40%, estadía ≥1,6× y mortalidad ≥2×. No presentarlos como estándares clínicos externos validados.

### 4. Modificar páginas conservando el diseño

- **P1:** conservar serie y composición; usar geografía constante; mostrar contribución al aumento; reemplazar la tabla institucional 2018–2024 por detalle municipal/regional 2005–2024. Pasar CAGR a información secundaria si hace falta espacio.
- **P2:** conservar cruce ocupación/giro/camas; sumar pacientes-día, egresos y años informados; separar anomalías e incompletos; alinear tarjetas con período y población. No sostener una explicación causal de ocupación >100% sin comprobarla.
- **P3:** mostrar estadía y mortalidad en relación con la mediana, usando una selección consistente. Añadir evolución de ambos indicadores con su referencia anual. Preferir “alerta relativa” a “peor calidad”. Mantener visibles las limitaciones de identidad, especialidad y ausencia de ajuste de riesgo.
- Conservar la paleta turquesa/navy, las cabeceras y la organización en tres preguntas. No reconstruir todo el reporte si bastan cambios dirigidos.

### 5. Actualizar el HTML original

- Obtener acceso al artefacto o su código HTML exportado. El enlace compartido no permitió acceso anónimo en esta sesión.
- Respaldar y editar la misma fuente, conservando estructura, identidad y controles existentes.
- Aplicar exactamente las definiciones, exclusiones, períodos y cifras finales verificadas en Power BI; actualizar textos estáticos, arrays de datos, tooltips, tablas y gráficos afectados.
- No presentar una copia local como actualización de la URL publicada. Si sólo se puede entregar HTML local, indicar que la publicación original sigue pendiente.
- No enviar datos ni instrucciones a una conversación de Claude como sustituto de editar el código sin autorización específica para esa acción.

### 6. Validar y entregar

- Reconciliar demanda global y regional; no perder las filas sin correspondencia geográfica.
- Comparar conteos de cohortes antes/después y explicar cada cambio por su regla. Los valores 20/50/25/90 son la línea base auditada, no metas que deban preservarse si se corrige la lógica.
- Verificar de forma independiente razones de sumas, promedios anuales y medianas; probar al menos un hospital completo, uno incompleto, una anomalía anual y una alerta sólo de estadía.
- Probar filtros y selección institucional; confirmar que las medidas fijas y las anuales se comportan según sus títulos.
- Abrir las tres páginas en Desktop: sin errores de campo, tablas recortadas ni alturas negativas. Revisar las dos series de evolución.
- Verificar en navegador las tres secciones del HTML, filtros, tablas, tooltips y tamaños de pantalla relevantes.
- Guardar y reabrir el PBIP para comprobar persistencia. Registrar qué quedó efectivamente aplicado, qué se verificó y qué sigue pendiente por acceso o identidad.

## Estado al entregar este handoff

| Elemento | Estado |
|---|---|
| Auditoría del modelo y PBIR | Realizada, con alcance y limitaciones indicados. |
| Cálculos independientes | Conservados en `docs\revision-20260918\`. |
| Respaldo previo | Creado en `_backup_20260918_correcciones\`. |
| Guardado del estado existente en Desktop | Realizado; no equivale a aplicar correcciones. |
| Cambios en Power BI | Pendientes. |
| Acceso/código del HTML original | Pendiente; el enlace requiere autenticación. |
| Cambios/publicación HTML | Pendientes. |

La carpeta `docs\cambios-20260918\` contiene únicamente utilidades preparatorias y descubrimiento de la instancia MCP; no constituye una implementación de las correcciones. La conexión MCP debe redescubrirse con `ListLocalInstances`: no reutilizar un puerto antiguo como si fuera permanente.
