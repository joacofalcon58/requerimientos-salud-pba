# Metodología — Dashboard "Requerimientos de establecimientos de Salud"

Documenta cómo está construido el informe nativo de Power BI (3 páginas) y la vista
HTML standalone que replica el mismo modelo de datos: las columnas calculadas y
medidas DAX agregadas, las definiciones de cada KPI, y las decisiones de cálculo que
mantienen ambos tableros reconciliados número por número.

El dashboard está organizado en tres preguntas de negocio (P1 demanda, P2 capacidad,
P3 desempeño relativo). Ambas vistas —el reporte nativo y el HTML— comparten el mismo
modelo semántico como fuente única de verdad; los cambios de diseño y las
correcciones de cálculo se aplican a los dos en paralelo. El historial detallado de
esas correcciones (bug de cálculo de camas, auditoría de comparabilidad geográfica y
de cohortes, ajustes de escala en el scatter de P2) queda documentado sección por
sección más abajo, y las limitaciones de identidad y comparabilidad de los datos
están en [`data-quality.md`](data-quality.md).

Backups: `_backup_20260908_122719/` (Report + SemanticModel, previo a la construcción
inicial).

---

## 1. Modelo semántico — lo que se agregó

No se tocaron las 20 medidas originales. Se agregaron **16 columnas calculadas** a
`DIM_Establecimientos` y **22 medidas** a `GBA_Rendimientos`.

### 16 columnas calculadas en `DIM_Establecimientos`

Toda la clasificación por establecimiento vive acá (se evalúa una vez al refrescar, no
por-visual). Ventana de referencia fija **2022–2024** para suavizar variación anual.

| Columna | Qué es |
|---|---|
| `Dependencia` | Municipal/Provincial/Nacional del establecimiento (2024, con reserva a la última disponible) |
| `Municipio` | Municipio del establecimiento (2024, con reserva) |
| `Egresos 22_24` | Egresos acumulados 2022–2024 |
| `Egresos Anual 22_24` | `Egresos 22_24 / 3` |
| `Estadia Media 22_24` | Σ días estadía / Σ egresos (razón de sumas) |
| `Mortalidad 22_24` | Σ defunciones / Σ egresos |
| `Camas 22_24` | Camas disponibles promedio anual |
| `Ocupacion 22_24` | Σ pacientes-día / Σ días-cama disponible |
| `Giro 22_24` | Σ egresos / Σ camas disponibles |
| `Segmento` | `Agudos` \| `Estadia prolongada` (estadía media > 30 d) \| `Sin internacion` |
| `Mediana LOS Dep` | Mediana de estadía media de la banda = agudos de la misma dependencia con ≥100 egresos/año |
| `Mediana Mort Dep` | Ídem para tasa de mortalidad |
| `LOS Ratio` | `Estadia Media 22_24 / Mediana LOS Dep` (múltiplo vs. banda) |
| `Mort Ratio` | `Mortalidad 22_24 / Mediana Mort Dep` |
| `Clasificacion Capacidad` | `Saturado` (ocup ≥90%) \| `Subutilizado` (ocup ≤40% y ≥50 egr/año) \| `Anomalia de datos` (ocup >100%) \| `Normal` \| `Excluido (no agudo)` |
| `Desempeno Internacion` | `Peor desempeno` si ≥100 egr/año y (LOS Ratio ≥1,6 o Mort Ratio ≥2,0), si no `Dentro de banda` |

### 22 medidas nuevas en `GBA_Rendimientos`

- **01. Demanda:** `Crecimiento Demanda Absoluto 2005-2024`, `Demanda Año 2018`,
  `Crecimiento Demanda 2018-2024`.
- **02. Capacidad Hospitalaria:** `% Ocupación 2024`, `Camas Informadas 2024`,
  `Establecimientos Agudos`, `Establecimientos Estadía Prolongada`, `Hospitales Saturados`,
  `Camas Saturadas`, `Establecimientos Subutilizados`, `Camas Subutilizadas`,
  `Establecimientos Anomalía Ocupación`, `Ocupación Prom (estab)`, `Giro Prom (estab)`,
  `Camas 22-24 (estab)`.
- **03. Calidad de Internación:** `Tasa de Mortalidad Hospitalaria 2024 %`,
  `Promedio Días de Estadía 2024`, `Establecimientos Peor Desempeño`,
  `Estadía relativa a banda (x)`, `Mortalidad relativa a banda (x)`,
  `Total Defunciones 2024`, `Total Egresos 2024`.

Se mantuvo el patrón del handoff: todos los ratios son `DIVIDE` de numerador y
denominador agregados (razón de sumas), nunca promedio de porcentajes fila a fila
(evita la paradoja de Simpson al agrupar).

---

## 2. Informe — 3 páginas

Formato 1920×1080, `FitToPage`. Tema de marca propio en
`Report/StaticResources/RegisteredResources/PBA-Salud.json` (paleta del Anexo III:
turquesa `#00AEC3`, navy `#1F3464`, semáforo verde/ámbar/rojo, fondo `#F2F5F6`,
tarjetas blancas con borde redondeado). Registrado en `report.json` como `customTheme`.
Los colores de las 8 series (`dataColors`) son los mismos `s1..s8` que usa Chart.js en
el HTML, así los gráficos de barras/líneas quedan del mismo color en ambos tableros.

**Banda de marca (18-sep-2026):** cada página abre con la misma cabecera de marca que
el HTML — franja navy angosta ("GOBIERNO DE LA PROVINCIA DE BUENOS AIRES · Grupo COBER
· Requerimientos de Establecimientos de Salud") y debajo una banda turquesa a todo el
ancho con el número de sección ("P1"/"P2"/"P3") y el título en blanco. Implementada
como dos `textbox` a ancho completo (`flush=True`: sin borde/radius/sombra, para que no
se vean como una tarjeta redondeada sino como una franja de punta a punta), ocupando el
mismo espacio vertical (0–144px) que el título simple anterior, así no hizo falta
recalcular el resto del layout de ninguna página.

### 01 · Demanda de atención  (`pages/5dd4ac40977d4030d72e`)
KPIs: Demanda total 2024 · Crecimiento 2005–2024 · CAGR anual · Prestaciones adicionales vs 2005.
Visuales: línea demanda total 2005–2024 · columna apilada composición por tipo ·
barras municipios con mayor crecimiento absoluto · columnas región sanitaria 2005 vs 2024 ·
callout límite de datos 2005–2017 · tabla establecimientos con mayor crecimiento 2018→2024.

### 02 · Capacidad hospitalaria  (`pages/1b3902ad5838b2b7a8e8`)
KPIs: Ocupación 2024 · Hospitales saturados (≥90%) · Camas subutilizadas (≤40%) · Anomalías (>100%).
Visuales: callout segmentación agudos/estadía prolongada · dispersión ocupación vs giro
(solo agudos, tamaño = camas) · tabla saturados · callout crítico anomalías >100% ·
tabla subutilizados (ancho completo).

**Fix 17-sep-2026 (tarde):** la tabla de subutilizados quedaba con ~38px de alto (no
entraba en la página) porque el layout apilaba scatter+tabla saturados (360px) + gráfico
de región sanitaria (250px) antes de calcular el espacio restante para la última tabla.
Se sacó el gráfico de % ocupación por región sanitaria (no estaba en el HTML original de
todos modos) y el callout crítico pasó a ancho completo — la tabla de subutilizados ahora
tiene 262px reales, visible sin recortes.

### 03 · Calidad de internación  (`pages/1cd2a9963f2a78d63974`)
KPIs: Días de estadía 2024 · Mortalidad hospitalaria 2024 · Defunciones 2024 · Establecimientos sobre banda.
Visuales: barras múltiplo estadía/mortalidad vs. banda · línea evolución mortalidad 2018–2024
(peores desempeños) · callout ID no persistente · callout casemix oncológico ·
tabla establecimientos con peor desempeño relativo.

---

## 3. Reconciliación con el artefacto HTML (17-sep-2026)

**Estado actual: los dos tableros muestran los mismos números.** El HTML fue
actualizado (misma URL del artefacto, versión 2) para igualar al modelo de Power BI,
que pasó a ser la única fuente de verdad — se conectó en vivo vía MCP
`powerbi-modeling` y se recalcularon todas las cifras compartidas desde ahí.

### Bug encontrado y corregido: camas infladas ~3x

La primera pasada de reconciliación detectó que **`Camas 22_24` estaba mal
calculada**: dividía la suma de `promedio_camas_disponibles` (2022–2024) por la
cantidad de años presentes en el rango, pero muchos establecimientos solo informan
esa columna en 1 de los 3 años → dividía por 3 cuando debía dividir por 1.
Verificado fila por fila contra el origen (ej. Hosp. Munic. E. Dudignac: camas=13
todos los años → mi cálculo daba 13/3=4,3 en vez de 13).

Un segundo hallazgo, más relevante: **el HTML original no tenía este bug — tenía uno
peor.** Sus cifras de "camas" resultaron ser la *suma* de los 3 años (no el promedio
que su propio texto decía usar) — ej. Hosp. Munic. Dr. D. E. Thompson: camas 2022=261,
2023=218, 2024=159 → el HTML mostraba "638" (261+218+159), un número físicamente no
creíble para un solo hospital. Se corrigió `Camas 22_24` en el modelo (divide por los
años que realmente informan camas, no por el total de años del rango) y se
regeneraron con esos valores tanto el HTML (mismo artefacto, republicado) como las
tablas nativas de PBI.

### Tabla final reconciliada (ambos tableros, misma fuente)

| Métrica | Valor | Nota |
|---|---|---|
| Ocupación 2024 (todos, ese año) | 75,5% | sigue existiendo como concepto, pero la tarjeta de P2 ya no usa este alcance — ver sección 5 |
| Ocupación agudos 2022–24 (tarjeta P2) | 69,9% | nueva medida `% Ocupación Agudos 22-24`, ver sección 5 |
| Mortalidad 2024 | 2,75% | sin cambios |
| Crecimiento demanda 2005–2024 | +141,4% | sin cambios |
| Establecimientos de agudos (2022–24) | 278 | antes 267/269 (HTML) |
| Estadía prolongada / crónicos | 150 | antes 157 (HTML) |
| Hospitales saturados (≥90%) | 20 | antes 19 (HTML) |
| Camas saturadas | 1.807 | antes 5.106 (HTML, bug de suma) |
| Establecimientos subutilizados (≤40%) | 50 | antes 51 (HTML) |
| Camas subutilizadas | 1.977 | antes 5.924 (HTML, bug de suma) |
| Anomalías de datos (>100%) | 25 | antes 23 (HTML) |
| Establecimientos peor desempeño (≥1,6x LOS o ≥2,0x mortalidad) | 90 | antes 73 (HTML, ver nota) |

`Establecimientos Peor Desempeño` (90) sigue siendo el número más alto vs. la
curaduría manual original del HTML (73): el modelo en vivo no excluye a mano los
IDs reciclados (mismo código de establecimiento reasignado a otra institución entre
años) ni el caso del hospital oncológico (mortalidad más alta esperable por casemix,
no por falla de calidad) — el HTML sí los excluía uno por uno. Esa curaduría manual
no es reproducible en DAX puro; queda documentada como advertencia en los callouts
de ambos tableros (Q3), no como filtro activo.

Un `#N/D` aparece en los cortes por región/dependencia por filas con
`region_sanitaria` nula en el origen — es real, no un bug.

### Cómo se reconcilió (para repetir el proceso si el modelo cambia)

1. Conectar `powerbi-modeling` MCP al `.pbip` abierto (`ListLocalInstances` → `Connect`).
2. Correr consultas DAX de diagnóstico (`SUMMARIZECOLUMNS` por `Clasificacion
   Capacidad` / `Segmento` / `Desempeno Internacion`) y comparar contra los números
   del HTML.
3. Ante una discrepancia grande, verificar fila por fila contra `GBA_Rendimientos`
   crudo (no contra las columnas calculadas) — así se encontró el bug real.
4. Corregir la columna/medida en el modelo vía `column_operations`/`measure_operations`
   Update, `Refresh` (`Calculate`), re-verificar.
5. Extraer las listas/valores finales con `dax_query_operations Execute` a CSV
   (`%LOCALAPPDATA%\PowerBIModelingMCP\QueryResults\`), reconstruir los `const DATA_*`
   del HTML y los textos estáticos con números embebidos, republicar el artefacto
   (mismo `url`), y guardar el `.pbip` (`Ctrl+S`).

---

## 5. Auditoría de comparabilidad (18-sep-2026)

Un handoff externo (`data-quality.md` en la raíz del proyecto, con evidencia en
`docs/revision-20260918/`) revisó el informe con consultas DAX independientes y
encontró 4 problemas reales de comparabilidad — no errores de cifras, sino de
**qué se está comparando contra qué**. El usuario aprobó 4 correcciones concretas
(de una lista de 7 prioridades propuestas); se aplicaron en Power BI y en el HTML
por igual.

### 5.1 Geografía variable en el gráfico de regiones (P1)

El gráfico "Regiones sanitarias: 2005 vs 2024" agrupaba por
`GBA_Rendimientos[region_sanitaria]` — la región **tal como estaba registrada cada
año**. Un municipio que cambió de región administrativa entre 2005 y 2024 (ej. La
Matanza: región VII → XII) aparecía como "crecimiento" de una región y "pérdida" de
otra, sin haber cambiado la demanda real. Se corrigió a `DIM_Geografia[region_sanitaria]`
(la región vigente en 2024, constante para ambos años). Los números cambian:
por ejemplo la región V pasa de +21,5M a +22,4M de crecimiento porque ahora agrupa
consistentemente los mismos municipios en 2005 y en 2024.

### 5.2 Tabla de crecimiento por establecimiento fuera de escala (P1)

La tabla "Establecimientos con mayor crecimiento de demanda (2018→2024)" comparaba
un período de 6 años cuando el resto de la página compara 2005-2024 (19 años) — y
dependía de `establecimiento_id`, vacío antes de 2018 y con identidad inestable
después (ver `data-quality.md` §1). Se reemplazó por una tabla de
**participación municipal y regional en el crecimiento 2005-2024** (misma ventana
que el resto de P1, geografía constante, medida nueva `% Participación en
Crecimiento` = crecimiento del municipio / crecimiento total provincial). Top 5:
Lomas de Zamora 9,8%, General San Martín 8,2%, Pilar 5,6%, Berazategui 5,0%,
La Plata 4,6% — acumulan 33,2% del crecimiento, tal como reconciliaron
independientemente el modelo vivo y la auditoría.

### 5.3 Tarjeta de ocupación de P2 con universo distinto al resto de la página

La tarjeta "Ocupación 2024" usaba **todos** los establecimientos y **solo** 2024
(75,5%), mientras el resto de P2 (dispersión, tablas de saturados/subutilizados)
analiza **solo agudos** en la ventana **2022-2024**. Convivían dos poblaciones
distintas en la misma página sin aclararlo. Se creó la medida
`% Ocupación Agudos 22-24` (razón de sumas, agudos, 2022-2024) — la tarjeta ahora
muestra **69,9%**, no 75,5%. La medida vieja quedó renombrada in place (mismo
`lineageTag`, sin dejar huérfanos); nada más la referenciaba.

### 5.4 Cohorte de "peor desempeño" (P3) inconsistente entre visuales

La clasificación base `Desempeno Internacion = "Peor desempeno"` (LOS≥1,6x o
mortalidad≥2x la mediana de su dependencia) da 90 establecimientos, y esa es la
cifra que muestra la tarjeta KPI. Pero la tabla, el gráfico de barras y la línea de
evolución aplicaban además umbrales de mortalidad **distintos y no declarados**
(≥2x, ≥2,5x y ≥4x respectivamente) — cada visual mostraba un subconjunto diferente
sin decirlo, y ninguno coincidía con el "90" del KPI. Se corrigió a un único criterio
base en los tres:

- **Tabla y barras**: sin umbral extra — cohorte completa (90), con scroll nativo.
- **Línea de evolución**: mantiene un recorte a **Top 7 de 90 por mortalidad
  relativa (≥3x mediana)** porque 90 series simultáneas en un gráfico de líneas no
  se pueden leer — pero ahora el título lo dice explícitamente ("Top 7 de 90"), en
  vez de ser un umbral silencioso. Dos de los 7 (U.S. Nº 28, Unid. Sanit. Dr. René
  Favaloro) solo informan 2024, así que su "evolución" es un único punto — también
  aclarado en el HTML.

Además: `Promedio Días de Estadía` y `Tasa de Mortalidad Hospitalaria %` en la
tabla de P3 eran medidas **sin filtro de año** (todo 2005-2024) mostradas junto a
ratios de la ventana 2022-2024 — mezclaban períodos en la misma fila. Se
reemplazaron por las columnas `Estadia Media 22_24` / `Mortalidad 22_24` de
`DIM_Establecimientos`, que ya son de la misma ventana que los ratios.

### 5.5 Cambios de redacción (sin tocar números)

- "Ocupación sostenida 90-100%" → "Ocupación agregada 90-100%", en la tarjeta y en
  la tabla de saturados de P2. La palabra "sostenida" implicaba que los 20
  establecimientos estuvieron ≥90% *todos* los años de la ventana; en realidad es
  un agregado de 2022-2024 y 11 de los 20 tuvieron al menos un año individual >100%
  (oculto en el agregado). No se construyó la alerta año-por-año que propone la
  auditoría — quedó fuera del alcance aprobado por el usuario.
- El callout "ID no persistente en el tiempo" (P3) ahora cita los 3 ejemplos
  concretos que verificó la auditoría (códigos 27400051, 59500191, 86100073) en vez
  de solo describir el problema en general.

### 5.6 Lo que quedó pendiente (fuera del alcance aprobado)

La auditoría propuso 7 prioridades; el usuario aprobó las 4 de arriba. Quedan sin
aplicar (documentadas en `data-quality.md` para quien retome):

- Validar contra la fuente original los 372 códigos de establecimiento con más de
  un nombre en 2022-2024 (identidad, no solo comparabilidad).
- Alerta de ocupación >100% **año por año** (hoy solo existe el flag "Anomalía de
  datos" sobre el agregado de la ventana).
- Medianas de referencia **por año**, en vez de una mediana fija 2022-2024 por
  dependencia, para medir evolución relativa (no solo absoluta) en P3.

### 5.7 Errores propios cometidos al aplicar esto (para no repetirlos)

Al escribir `sortDefinition` directamente en el PBIR de dos tablas (la nueva de
participación en P1 y la de P3), el primer intento lo anidó dentro de
`query.queryState.Values` — Power BI lo rechaza como propiedad no reconocida. El
segundo intento lo movió a `query.queryState` (un nivel de más). El esquema correcto
es `query.sortDefinition`, **hermano** de `queryState`, no anidado dentro de él —
así estaba en todos los visuales generados originalmente por `gen_pbir.py`. Cuando
además ya existía un `sortDefinition` viejo en esa posición (referenciando una
medida que la edición había quitado de la proyección), quedaron dos
`sortDefinition` contradictorios y el informe no cargaba ("No se pudo cargar el
informe", sin más detalle). Verificar con `grep -n "sortDefinition"` cuántas
apariciones hay y a qué nivel de indentación antes de reabrir Desktop.

## 6. Retiro de los carteles de advertencia (18-sep-2026, tarde)

El usuario pidió sacar los 4 cuadros de advertencia (cartel con fondo de color +
ícono de alerta) de ambos tableros — decisión de audiencia: un gerente/director que
lee el dashboard no necesita ver en pantalla las salvedades de calidad de datos o
casemix, solo los números ya corregidos. Las notas quedan **solo en la
documentación** (`data-quality.md` y esta sección), no en el HTML ni en el PBI.

Cuadros eliminados (4):

| Página | Contenido del cuadro |
|---|---|
| P1 · Demanda | "Límite de datos por establecimiento": establecimiento_id vacío 2005-2017 |
| P2 · Capacidad | "Hallazgo de calidad de datos": 25 establecimientos (UPA/UDP) con ocupación >100% |
| P3 · Calidad | "El ID de establecimiento no es persistente en el tiempo" (los 372 códigos reasignados) |
| P3 · Calidad | "Cuidado con el casemix" (mortalidad de centros oncológicos) |

No se tocó el cuadro "Segmentación aplicada"/"Segmentación" de P2 y P3 (geriátricos
y estadía prolongada excluidos del análisis) porque son alcance del análisis, no
salvedades de calidad de datos: sin ellos el lector no entendería por qué el
universo de establecimientos no coincide con el total del modelo.

**Power BI**: se borraron las 4 carpetas de visual (textbox) y se agrandó la tabla
que quedaba justo debajo de cada una para ocupar el espacio liberado, manteniendo
el margen inferior de página (~20px a 1080px de alto) que ya usaban las otras
páginas:

| Página | Tabla reubicada | y anterior -> nueva | alto anterior -> nuevo |
|---|---|---|---|
| P1 | Participación municipal/regional | 858.3 -> 795.8 | 201.6 -> 264.0 |
| P2 | Establecimientos subutilizados | 798 -> 714 | 262 -> 346 |
| P3 | Establecimientos con peor desempeño | 858 -> 698 | 202 -> 362 |

Verificado reabriendo el `.pbip` de cero: las 3 páginas cargan sin error, sin
huecos vacíos donde estaban los carteles, sin recortes ni superposiciones.
Guardado con `Ctrl+S`.

**HTML**: al ser layout de flujo (no canvas absoluto como PBI), alcanzó con borrar
los 4 `<div class="callout ...">` — el elemento siguiente ya traía su propio
`margin-top:16px` y el navegador reordena solo, sin necesidad de recalcular
posiciones. Publicado como **Versión 4** del artefacto. El pie de página
("Notas metodológicas y de calidad de datos") no se tocó: ya listaba estas mismas
limitaciones en prosa discreta al final del documento, que es el lugar de
documentación que el usuario pidió conservar.

## 7. Cambios de formato/color del usuario, trasladados al HTML (19-sep-2026)

El usuario reformateó el PBI directamente en Desktop (sin pasar por mí) y pidió
"actualiza el html en base a los cambios que hice". Como el proyecto no tiene git,
detecté los cambios por `mtime` de archivos y comparación manual contra lo que ya
sabía del proyecto, no por diff. Encontrado:

1. **Página nueva "Presentación"** (primera del `pageOrder`): una imagen de portada
   de ancho completo (`Imagen de Presentación.png`, 1920x1080) con franja navy +
   franja turquesa arriba, título grande turquesa, bajada gris, línea de acento,
   leyenda "GOBIERNO DE LA PROVINCIA DE BUENOS AIRES", 4 íconos circulares
   (hospital/personas/diente/estetoscopio), ilustración de línea+barras ascendente
   de fondo y el isotipo de GPBA abajo a la derecha.
2. **Paleta de gráficos explícita** en 7 visuales (antes usaban rotación de color
   por defecto del tema): navy `#1F3464` como color primario/serie base, rojo
   `#BE1717` como serie de contraste (año actual vs. base), celeste claro
   `#A3D8E7` (ThemeDataColor id 9) como color terciario. Aplicado en: gráfico de
   regiones (2005 navy / 2024 rojo), composición de demanda (Médicas navy / Odont.
   rojo / Param. `#74C9E3` / Interc. turquesa `#00AEC3`), municipios (navy, serie
   única), demanda total (línea navy), tabla P2/gráfico P3 "peor desempeño"
   (Estadía navy / Mortalidad celeste), y la línea de evolución P3 (2 de los 7
   establecimientos resaltados a mano: Espigas=navy, Villa Iris=celeste).
3. Tarjeta de ocupación P2: `fontSize` del valor a 22pt — no se replicó 1:1 en el
   HTML (unidades de medida distintas entre PBI y CSS, sin una base de comparación
   confiable para saber si eso es más grande o más chico que antes).

**HTML**: se agregó una sección `.hero` nueva arriba de todo (franjas navy/turquesa,
título, bajada, línea de acento, leyenda, 4 íconos SVG inline dibujados a mano en el
mismo estilo minimalista — no una réplica pixel del isotipo oficial de GPBA, que ya
existía como marca abstracta simplificada en el header del proyecto — más una
ilustración decorativa de línea+barras). Los 7 `new Chart(...)` de Chart.js se
recolorearon con la misma regla navy/rojo/celeste descripta arriba, reutilizando
`COLORS.navy` (`--pba-navy`, ya existía) y agregando el celeste `#a3d8e7`
(`--pba-l2`, ya existía como variable pero no se usaba en gráficos). Verificado
visualmente sirviendo el archivo con un servidor local (`python -m http.server`) en
el navegador embebido antes de publicar — la Versión 3/4 del artefacto no se podía
inspeccionar así porque `claude.ai` requiere sesión iniciada. Publicado como
**Versión 5**.

## 8. Scatter P2 y gráfico de regiones — verificación punto por punto (19-sep-2026)

Preguntado por qué el scatter "Ocupación vs. giro de camas" se veía distinto entre
PBI y HTML, en vez de asumir que los datos diferían se verificó cada capa por
separado — la lección quedó documentada porque casi todo terminó siendo config de
gráfico, no de datos:

- **Los datos ya coincidían.** El array `DATA_SCATTER` del HTML tiene los mismos
  278 establecimientos de agudos, con el mismo máximo de ocupación (242%) que
  Power BI. No era un problema de cálculo.
- **El eje del HTML tenía un tope fijo que recortaba puntos.** `max:110` en X y
  `max:200` en Y ocultaban 18 y 17 puntos respectivamente (los mismos "anomalía de
  datos" ya documentados) que Power BI sí mostraba por su autoescalado. Se sacaron
  los `max` fijos y se dejó que Chart.js autoescale iguale a PBI.
- **El color era una decisión de diseño distinta, no un bug.** PBI ya tenía (lo
  agregó el usuario) un degradado continuo de 3 puntos sobre `Ocupación Prom
  (estab)` — verde `#1BAF7A` → amarillo `#F2A100` → rojo `#E34948`, con el mínimo y
  máximo tomados del propio rango de datos. Se replicó ese mismo degradado en el
  HTML (mismos 3 colores, mismo mínimo/máximo/punto medio calculados sobre
  `DATA_SCATTER`), reemplazando las 5 categorías discretas que tenía antes. Se
  sacó también la leyenda categórica (PBI tampoco muestra una para este gráfico).
  Bug propio en el primer intento: la función de interpolación devolvía
  `rgb(r,g,b)` y después se le pegaba un sufijo de alfa tipo `'CC'` — eso arma un
  string inválido (`rgb(27,175,122)CC`) que el canvas no puede parsear y cae a
  negro. Corregido devolviendo hex (`#RRGGBB`) para que el sufijo de alfa forme un
  hex de 8 dígitos válido, igual que el resto de los colores del proyecto
  (`COLORS.s1+'99'`, etc.).

Para el gráfico "Regiones sanitarias: 2005 vs 2024 (geografía constante 2024)":
consulta DAX en vivo confirmó que los 12 valores por región ya coincidían
exactamente entre PBI y HTML — pero el **orden de las barras no coincidía**. El
HTML ordenaba por crecimiento absoluto descendente; Power BI (con un
`sortDefinition` que ya estaba puesto en el visual, sobre "Demanda Año Actual
(2024)" descendente) ordenaba por demanda 2024. Se cambió el `.sort()` del HTML
para usar el mismo criterio (`d2024` descendente) — no fue necesario tocar nada en
Power BI, el `sortDefinition` correcto ya estaba ahí. Verificado visualmente:
ambos quedan en el mismo orden (V, VI, XI, VII, VIII, XII, IX, I, X, IV, III, II).
Publicado como **Versión 6**.

## 9. "Composición de la demanda" reconstruido en Power BI (19-sep-2026)

El visual de PBI y el de HTML se llamaban parecido pero mostraban cosas distintas:
PBI graficaba las 4 prestaciones **por año** (2005-2024 completo, eje X = año, un
color por prestación); el HTML compara **2005 vs 2024** por tipo de prestación (eje
Y = tipo, 2 barras de color por fila). No era un desajuste de formato — la
estructura del visual era otra. Se reconstruyó el de PBI para igualar al HTML:

- **Modelo**: se agregó la tabla calculada `DIM_TipoPrestacion` (4 filas fijas:
  Consultas médicas/odontológicas/paramédicas, Interconsultas, con una columna
  `orden` para mantener ese orden en el eje) vía `UNION(ROW(...), ...)` — no existía
  ninguna dimensión de "tipo de prestación" en el modelo porque esos 4 tipos viven
  como columnas separadas (formato ancho) en `GBA_Rendimientos`, no como filas.
  Se agregaron 2 medidas nuevas en `GBA_Rendimientos`: `Cantidad por Tipo (2005)` y
  `Cantidad por Tipo (2024)`, cada una con un `SWITCH` sobre
  `SELECTEDVALUE(DIM_TipoPrestacion[tipo_prestacion])` que resuelve a la medida
  correspondiente (`Total Consultas Médicas`, etc.) filtrada al año fijo. Verificado
  contra el HTML con una consulta DAX en vivo antes de tocar el visual — coinciden
  exacto (ej. Consultas médicas 2005: 41.626.204 en ambos).
- **Visual**: reconstruido de cero como `clusteredBarChart` (barras horizontales,
  igual que el `indexAxis:'y'` del HTML) con Category=`DIM_TipoPrestacion[tipo_prestacion]`,
  Y=`[Cantidad por Tipo (2005), Cantidad por Tipo (2024)]`, colores navy/rojo
  (mismo criterio que el resto de los 2005-vs-2024 del proyecto), y un
  `sortDefinition` (en `query.sortDefinition`, ya con el esquema correcto de
  entrada) ordenando por `DIM_TipoPrestacion[orden]` para que las 4 filas queden en
  el mismo orden que en el HTML.
- Editado con Power BI Desktop cerrado, revalidado con `python -m json.load`,
  reabierto de cero: carga sin error, sin ícono de advertencia en el visual, 4 filas
  con sus 2 barras cada una tal como se esperaba. Guardado.

No hizo falta tocar el HTML — ya tenía la estructura correcta; el desajuste era
enteramente del lado de Power BI.

## 10. "Peor desempeño relativo" (P3) — capado a 12 filas + hallazgo de identidad (19-sep-2026)

Título, subtítulo, colores (navy/celeste), cohorte de 90 y orden (mortalidad
descendente) ya coincidían entre PBI y HTML. La diferencia real: el HTML
(`chartWorst`, `.slice(0,12)`) muestra un canvas fijo de 12 barras sin scroll;
el visual de PBI, sin límite de filas, mostraba las 90 con scrollbar — una
diferencia puramente visual (más denso/con barra de desplazamiento vs. compacto).
Se agregó un filtro Advanced sobre "Mortalidad relativa a banda (x)" **>= 2,7**
(el mismo patrón "umbral en vez de TopN" ya usado en el gráfico de evolución de
P3) para capar a las mismas 12 filas que muestra el HTML, y se agrandó la fila de
gráficos (bar + línea, 380→420px) porque con el espaciado por defecto de barras
de Power BI 11 filas ocupaban lo que en el HTML ocupan 12 — la tabla de abajo se
corrió para mantener el margen inferior de la página.

**Hallazgo real encontrado en el camino (no buscado, pero confirmado con DAX en
vivo):** al calcular el umbral se detectó que "Hosp. Zonal Esp. Odontología y
Ortodoncia Dr. J. U. Carrea" — que en los datos limpios por establecimiento
(columna `DIM_Establecimientos[Mort Ratio]`) califica con mortalidad relativa
2,89x (entraría en el top 12) — desaparecía del gráfico. La causa: ese nombre
identifica **46 `establecimiento_id` distintos** en el modelo (Villarino, Vicente
López, Villa Gesell), de los cuales **dos** califican independientemente como
"Peor desempeño" (uno por mortalidad 2,89x, otro por estadía 13,6x con mortalidad
1,29x). El gráfico de barras agrupa por `establecimiento_nombre` (no por ID), así
que la medida `AVERAGE(DIM_Establecimientos[Mort Ratio])` termina promediando esos
dos establecimientos distintos en una sola barra (2,09x), que ya no llega al
umbral — y por eso "desaparece" en vez de simplemente ocupar el puesto 13. La
tabla de abajo (`b9d187645049112683d3`) no tiene este problema porque lista filas
individuales en vez de agrupar por nombre.

**No se corrigió** — es exactamente la misma clase de problema que el punto 5 de
`data-quality.md` ("372 códigos con más de un nombre"), que el usuario dejó fuera de
alcance el 18-sep-2026. Se deja documentado acá como un caso concreto y verificado
de esa limitación ya conocida, no como una tarea nueva. El umbral 2,7 quedó fijado
usando el cálculo *tal como lo hace el propio gráfico* (agrupado/promediado), no
el valor limpio por establecimiento, para que el conteo de filas sea estable y
consistente con lo que el visual realmente calcula.

## 11. Tabla "Establecimientos subutilizados" — el HTML estaba mal, no Power BI (19-sep-2026)

El usuario preguntó cuál de los dos tenía razón. Verificado con DAX en vivo antes
de tocar nada:

- **Cifra correcta y confirmada:** `COUNTROWS` sobre `Clasificacion Capacidad =
  "Subutilizado"` da **50 establecimientos, 1.977,33 camas** — coincide exacto
  con el subtítulo que ya tenían ambos tableros ("50 establecimientos, 1.977
  camas"). Ese número siempre fue correcto.
- **Power BI: casi correcto.** La tabla (`b80becd9e6f980b0b2ce`) usa las medidas
  wrapper de `GBA_Rendimientos` (`Camas 22-24 (estab)`, `Ocupación Prom (estab)`,
  `Giro Prom (estab)`) agrupadas por `establecimiento_nombre` — el mismo patrón
  del punto 10. Como "Hosp. Zonal Esp. Odontología y Ortodoncia Dr. J. U. Carrea"
  tiene **3 códigos de establecimiento distintos** que califican como
  Subutilizado (12, 28 y 11 camas), Power BI los agrupa en una sola fila
  ("51 camas", ocupación promediada entre los 3 — mezclando establecimientos
  reales distintos). Resultado: la tabla muestra **47 filas** en vez de 50 (la
  suma de camas total sigue dando 1.977 porque `SUM` no se ve afectado, solo el
  conteo de filas y la ocupación/giro de esa fila mezclada). No se tocó — mismo
  alcance que el punto 10, ya documentado como pendiente.
- **HTML: mal, y por una razón distinta.** El array `DATA_CAPACIDAD.top_subutilizados`
  solo tenía **12 filas cargadas (264 camas)** — muy por debajo de las 50/1.977
  que su propio subtítulo ya anunciaba. No era un problema de agrupación como en
  Power BI: era un array viejo, incompleto, nunca terminado de poblar con el
  universo completo, con las filas además sin ningún orden consistente.

**Corregido el HTML**, no Power BI: se reconstruyó `top_subutilizados` con los 50
establecimientos completos desde una consulta DAX en vivo sobre las columnas
limpias de `DIM_Establecimientos` (no las medidas wrapper — el HTML lista filas
directamente, no necesita agrupar por nombre, así que no hereda el problema de
identidad de Power BI). Orden: ocupación descendente, igual que el
`sortDefinition` de la tabla de PBI. Total verificado: 50 filas, 1.977 camas
exacto. Esto deja al HTML **más preciso que la tabla de Power BI** en este punto
particular (muestra los 3 "Carrea" como establecimientos separados en vez de
mezclarlos) — una asimetría menor, aceptable, y de la misma naturaleza que el
punto 10. Publicado como **Versión 7** del artefacto.

**Adenda (mismo día):** faltaba la columna Egresos en la tabla de Power BI — tenía
Giro en su lugar, que el HTML no muestra en esta tabla. Se reconstruyó la tabla de
PBI (`b80becd9e6f980b0b2ce`) cambiando las 3 medidas wrapper de `GBA_Rendimientos`
(Camas/Ocupación/Giro "Prom (estab)") por las columnas limpias de
`DIM_Establecimientos` (`Camas 22_24`, `Ocupacion 22_24`, `Egresos 22_24`) — mismo
patrón que ya se usó en la tabla de P3. Esto no solo agrega Egresos, sino que de
paso **cierra la asimetría del punto anterior**: al dejar de agrupar por
`establecimiento_nombre` con medidas promediadas, los 3 "Carrea" ya no se mezclan,
y la tabla de PBI ahora también muestra las 50 filas reales (no 47). Verificado
reabriendo de cero: columnas correctas, valores sensatos, scrollbar con las 50
filas. Guardado.

## 12. Toggle Mortalidad/Estadía en el gráfico de evolución + aclaración tabla-vs-gráfico (19-sep-2026)

El HTML tenía 2 botones (Mortalidad % / Días de estadía) para elegir qué serie
mostrar en "Evolución 2018–2024: casos destacados"; el visual de PBI no tenía
equivalente, solo mostraba mortalidad fija. **El usuario lo armó directamente en
Power BI Desktop** usando el mecanismo nativo correcto para esto — un **parámetro
de campo** ("Métrica", con las opciones "Mortalidad %" y "Días de estadía"
apuntando a `Tasa de Mortalidad Hospitalaria %` y `Promedio Días de Estadía`),
mostrado como una segmentación en formato mosaico (2 botones) junto al título del
gráfico. Verificado: ambas opciones cambian el eje Y y los valores correctamente.

**Segunda consulta el mismo día:** el usuario notó que, filtrando por "Unid.
Sanit. La Dulce", la tabla de abajo decía 24,1 días de estadía pero el gráfico de
líneas (en "Días de estadía") mostraba 32,0 — y sospechaba que tampoco coincidía
con el HTML. Verificado con DAX en vivo antes de asumir nada:

- Tabla (`Estadia Media 22_24`): **24,09 días** — promedio ponderado (razón de
  sumas) de la ventana completa 2022-2024, el número usado para clasificar la
  cohorte.
- Gráfico, año por año (`Promedio Días de Estadía`, un año a la vez): 2022=8,30 ·
  2023=38,9 · **2024=31,95** ("≈32,0", el punto que vio el usuario).
- El HTML tiene guardados exactamente los mismos 7 valores por año (172,508 ·
  102,739 · 88,966 · 8,169 · 8,299 · 38,9 · 31,95) — coincide byte a byte con la
  consulta en vivo.

**Conclusión: no hay ningún bug.** Son dos estadísticas distintas y las dos son
correctas — 24,1 es el promedio de 3 años; 32,0 es el valor real de 2024 nada más.
Con solo ~38 egresos/año en este establecimiento (volumen muy bajo), el promedio
anual varía muchísimo de un año a otro (8,3 → 38,9 → 32,0) — eso es señal real,
no ruido de cálculo. PBI y HTML ya estaban de acuerdo entre sí; lo único que
faltaba era dejarlo explícito para que no se lea como una inconsistencia. Se
agregó el mismo subtítulo aclaratorio en los dos: *"Valor real de cada año (no el
promedio 2022-2024 de la tabla de abajo) · en establecimientos de bajo volumen
puede variar mucho año a año"*. Publicado como **Versión 8** del artefacto.

---

## 4. Cómo regenerar las páginas

Script: `docs/gen_pbir.py`. Reproduce las 3 páginas completas.

1. Cerrar Power BI Desktop por completo.
2. `rm -rf ".../Report/definition/pages" && mkdir` y correr el script.
3. Validar JSON (`json.load` sobre cada archivo).
4. Abrir el `.pbip` **de cero** (no usar "Aplicar cambios externos" con PBI abierto —
   es frágil y puede revertir todo al cerrar).
5. Clic en "Actualizar ahora" (las columnas calculadas se recalculan manual la 1ª vez).
6. `Ctrl+S`.

Notas de esquema PBIR (Power BI 2.157):
- `visualContainer` 2.12.0, `page` 2.1.0, `pagesMetadata` 1.1.0.
- `customTheme` en `report.json` **requiere** el bloque `reportVersionAtImport`
  (si falta, PBI rechaza abrir el informe).
- Tipos de visual usados: `card`, `lineChart`, `columnChart` (apilado),
  `clusteredColumnChart`, `clusteredBarChart`, `scatterChart`, `tableEx`, `textbox`.
- Filtros de visual: se evitó `TopN` (JSON frágil); se usan filtros `Advanced` de
  comparación sobre medida/columna para acotar los rankings.
