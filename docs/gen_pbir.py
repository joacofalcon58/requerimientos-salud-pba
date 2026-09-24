# -*- coding: utf-8 -*-
"""Genera las 3 paginas PBIR del informe 'Requerimientos de establecimientos de Salud'.
Replica la logica del dashboard HTML (artefacto abea55bf) de forma nativa en Power BI.
Reproducible: borra y regenera pages/ completo.
"""
import json, os, secrets, shutil

BASE = r"C:\Users\joaco\Documents\Porfolio\Requerimientos de establecimientos de Salud.Report\definition"
PAGES_DIR = os.path.join(BASE, "pages")
SCHEMA_VC = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.12.0/schema.json"
SCHEMA_PAGE = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json"
SCHEMA_PAGES = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.1.0/schema.json"

FACT = "GBA_Rendimientos"
DIME = "DIM_Establecimientos"
DIMG = "DIM_Geografia"

def hexid(n=20):
    return secrets.token_hex(n // 2)

def gid():
    return secrets.token_hex(10)

# ---------- field builders ----------
def col_field(entity, prop):
    return {"Column": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": prop}}

def measure_field(entity, prop):
    return {"Measure": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": prop}}

def proj_col(entity, prop, active=False):
    p = {"field": col_field(entity, prop),
         "queryRef": f"{entity}.{prop}", "nativeQueryRef": prop}
    if active:
        p["active"] = True
    return p

def proj_measure(entity, prop):
    return {"field": measure_field(entity, prop),
            "queryRef": f"{entity}.{prop}", "nativeQueryRef": prop}

def title_obj(text):
    return {"title": [{"properties": {
        "show": {"expr": {"Literal": {"Value": "true"}}},
        "text": {"expr": {"Literal": {"Value": f"'{text}'"}}}}}]}

def base_container(name, x, y, w, h, z, tab):
    return {"$schema": SCHEMA_VC, "name": name,
            "position": {"x": x, "y": y, "z": z, "height": h, "width": w, "tabOrder": tab}}

# ---------- visuals ----------
def v_card(x, y, w, h, z, tab, measure_name, title, entity=FACT):
    c = base_container(hexid(), x, y, w, h, z, tab)
    c["visual"] = {
        "visualType": "card",
        "query": {"queryState": {"Values": {"projections": [proj_measure(entity, measure_name)]}}},
        "objects": {
            "labels": [{"properties": {"labelDisplayUnits": {"expr": {"Literal": {"Value": "0D"}}},
                                        "fontSize": {"expr": {"Literal": {"Value": "22D"}}}}}],
            "categoryLabels": [{"properties": {"show": {"expr": {"Literal": {"Value": "false"}}}}}],
        },
        "visualContainerObjects": title_obj(title),
    }
    return c

def v_line(x, y, w, h, z, tab, cat_entity, cat_prop, measures, title, legend=None,
           cat_is_measure_axis=False):
    c = base_container(hexid(), x, y, w, h, z, tab)
    qs = {"Category": {"projections": [proj_col(cat_entity, cat_prop, active=True)]},
          "Y": {"projections": [proj_measure(e, m) for (e, m) in measures]}}
    if legend:
        qs["Series"] = {"projections": [proj_col(legend[0], legend[1], active=True)]}
    c["visual"] = {
        "visualType": "lineChart",
        "query": {"queryState": qs},
        "objects": {"lineStyles": [{"properties": {"showMarker": {"expr": {"Literal": {"Value": "true"}}},
                                                   "strokeWidth": {"expr": {"Literal": {"Value": "2D"}}}}}]},
        "visualContainerObjects": title_obj(title),
        "drillFilterOtherVisuals": True,
    }
    return c

def v_bar(x, y, w, h, z, tab, cat_entity, cat_prop, measures, title, stacked=False,
          column=False):
    c = base_container(hexid(), x, y, w, h, z, tab)
    if column and stacked:
        vt = "columnChart"
    elif column:
        vt = "clusteredColumnChart"
    elif stacked:
        vt = "barChart"
    else:
        vt = "clusteredBarChart"
    c["visual"] = {
        "visualType": vt,
        "query": {"queryState": {
            "Category": {"projections": [proj_col(cat_entity, cat_prop, active=True)]},
            "Y": {"projections": [proj_measure(e, m) for (e, m) in measures]},
        }},
        "objects": {"labels": [{"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}}}]},
        "visualContainerObjects": title_obj(title),
        "drillFilterOtherVisuals": True,
    }
    return c

def v_scatter(x, y, w, h, z, tab, cat_entity, cat_prop, xm, ym, sizem, title):
    c = base_container(hexid(), x, y, w, h, z, tab)
    c["visual"] = {
        "visualType": "scatterChart",
        "query": {"queryState": {
            "Category": {"projections": [proj_col(cat_entity, cat_prop, active=True)]},
            "X": {"projections": [proj_measure(*xm)]},
            "Y": {"projections": [proj_measure(*ym)]},
            "Size": {"projections": [proj_measure(*sizem)]},
        }},
        "objects": {
            "categoryLabels": [{"properties": {"show": {"expr": {"Literal": {"Value": "false"}}}}}],
            "categoryAxis": [{"properties": {"showAxisTitle": {"expr": {"Literal": {"Value": "true"}}}}}],
            "valueAxis": [{"properties": {"showAxisTitle": {"expr": {"Literal": {"Value": "true"}}}}}],
        },
        "visualContainerObjects": title_obj(title),
        "drillFilterOtherVisuals": True,
    }
    return c

def v_table(x, y, w, h, z, tab, cols, title):
    """cols: list of (kind, entity, name) kind in {'col','measure'}"""
    projections = []
    for kind, entity, name in cols:
        projections.append(proj_col(entity, name) if kind == "col" else proj_measure(entity, name))
    c = base_container(hexid(), x, y, w, h, z, tab)
    c["visual"] = {
        "visualType": "tableEx",
        "query": {"queryState": {"Values": {"projections": projections}}},
        "objects": {"grid": [{"properties": {"gridVertical": {"expr": {"Literal": {"Value": "true"}}}}}],
                    "total": [{"properties": {"totals": {"expr": {"Literal": {"Value": "false"}}}}}]},
        "visualContainerObjects": title_obj(title),
        "drillFilterOtherVisuals": True,
    }
    return c

def v_textbox(x, y, w, h, z, tab, runs, bg=None, border=None, flush=False, align="left"):
    """runs: list of (text, style_dict). style keys: bold(bool), color(hex), size(px int).
    flush=True: full-bleed color band, no border/radius/shadow (for the brand header/topbar)."""
    trs = []
    for text, st in runs:
        ts = {}
        if st.get("bold"):
            ts["fontWeight"] = "bold"
        if st.get("italic"):
            ts["fontStyle"] = "italic"
        if st.get("color"):
            ts["color"] = st["color"]
        if st.get("size"):
            ts["fontSize"] = f"{st['size']}px"
        trs.append({"value": text, "textStyle": ts})
    c = base_container(hexid(), x, y, w, h, z, tab)
    vco = {}
    if not bg:
        vco["background"] = [{"properties": {"show": {"expr": {"Literal": {"Value": "false"}}}}}]
        vco["border"] = [{"properties": {"show": {"expr": {"Literal": {"Value": "false"}}}}}]
        vco["dropShadow"] = [{"properties": {"show": {"expr": {"Literal": {"Value": "false"}}}}}]
    if bg:
        vco["background"] = [{"properties": {
            "show": {"expr": {"Literal": {"Value": "true"}}},
            "color": {"solid": {"color": {"expr": {"Literal": {"Value": f"'{bg}'"}}}}},
            "transparency": {"expr": {"Literal": {"Value": "0D"}}}}}]
    if flush:
        vco["border"] = [{"properties": {"show": {"expr": {"Literal": {"Value": "false"}}}}}]
        vco["dropShadow"] = [{"properties": {"show": {"expr": {"Literal": {"Value": "false"}}}}}]
    elif border:
        vco["border"] = [{"properties": {
            "show": {"expr": {"Literal": {"Value": "true"}}},
            "color": {"solid": {"color": {"expr": {"Literal": {"Value": f"'{border}'"}}}}},
            "radius": {"expr": {"Literal": {"Value": "8D"}}}}}]
    c["visual"] = {
        "visualType": "textbox",
        "objects": {"general": [{"properties": {"paragraphs": [
            {"textRuns": trs, "horizontalTextAlignment": align}]}}]},
    }
    if vco:
        c["visual"]["visualContainerObjects"] = vco
    return c

# ---------- filters ----------
def f_categorical_in(entity, prop, values):
    return {"name": gid(), "field": col_field(entity, prop), "type": "Categorical",
            "filter": {"Version": 2, "From": [{"Name": "e", "Entity": entity, "Type": 0}],
                       "Where": [{"Condition": {"In": {
                           "Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "e"}}, "Property": prop}}],
                           "Values": [[{"Literal": {"Value": f"'{v}'"}}] for v in values]}}}]}}

def f_col_ge(entity, prop, value):
    return {"name": gid(), "field": col_field(entity, prop), "type": "Advanced",
            "filter": {"Version": 2, "From": [{"Name": "e", "Entity": entity, "Type": 0}],
                       "Where": [{"Condition": {"Comparison": {"ComparisonKind": 2,
                           "Left": {"Column": {"Expression": {"SourceRef": {"Source": "e"}}, "Property": prop}},
                           "Right": {"Literal": {"Value": f"{value}L"}}}}}]}}

def f_measure_ge(entity, measure_name, value):
    return {"name": gid(), "field": measure_field(entity, measure_name), "type": "Advanced",
            "filter": {"Version": 2, "From": [{"Name": "m", "Entity": entity, "Type": 0}],
                       "Where": [{"Condition": {"Comparison": {"ComparisonKind": 2,
                           "Left": {"Measure": {"Expression": {"SourceRef": {"Source": "m"}}, "Property": measure_name}},
                           "Right": {"Literal": {"Value": f"{value}D"}}}}}]}}

def attach_filters(container, filters):
    container["filterConfig"] = {"filters": filters}

# ---------- page assembly ----------
def write_page(page_id, display_name, order, visuals):
    pdir = os.path.join(PAGES_DIR, page_id)
    vdir = os.path.join(pdir, "visuals")
    os.makedirs(vdir, exist_ok=True)
    page = {"$schema": SCHEMA_PAGE, "name": page_id, "displayName": display_name,
            "displayOption": "FitToPage", "height": 1080, "width": 1920}
    with open(os.path.join(pdir, "page.json"), "w", encoding="utf-8") as f:
        json.dump(page, f, indent=2, ensure_ascii=False)
    for v in visuals:
        d = os.path.join(vdir, v["name"])
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "visual.json"), "w", encoding="utf-8") as f:
            json.dump(v, f, indent=2, ensure_ascii=False)

# =========================================================================
# LAYOUT CONSTANTS
M = 40                      # margin
PW = 1920
KPI_Y = 150
KPI_H = 132
KPI_GAP = 16
ROW1_Y = 300
CALLOUT_H = 70
Z = 1000

def kpi_row(measures_titles, y=KPI_Y, n=None, entity=FACT):
    n = n or len(measures_titles)
    total = PW - 2 * M
    w = (total - (n - 1) * KPI_GAP) // n
    out = []
    for i, (mname, mtitle, ent) in enumerate(measures_titles):
        x = M + i * (w + KPI_GAP)
        out.append(v_card(x, y, w, KPI_H, Z, i, mname, mtitle, entity=ent))
    return out

def header_block(kicker, title, question):
    """Topbar navy + banda turquesa de marca (replica el header del HTML), mismo
    footprint vertical (0-144) que la version anterior asi el resto del layout no se mueve."""
    topbar = v_textbox(0, 0, PW, 24, Z, 85, [
        ("GOBIERNO DE LA PROVINCIA DE BUENOS AIRES   ·   Grupo COBER   ·   Requerimientos de Establecimientos de Salud",
         {"color": "#CAE7EA", "size": 10}),
    ], bg="#1F3464", flush=True)
    header_band = v_textbox(0, 24, PW, 70, Z, 86, [
        (kicker + "   ·   ", {"bold": True, "color": "#0B2E3A", "size": 13}),
        (title, {"bold": True, "color": "#FFFFFF", "size": 22}),
    ], bg="#00AEC3", flush=True)
    tb_q = v_textbox(M, 100, 1500, 40, Z, 91, [
        (question, {"color": "#52514E", "size": 12}),
    ])
    return [topbar, header_band, tb_q]

def callout(y, kind, runs):
    palette = {"info": ("#EAF7F9", "#BFE8EE"), "warn": ("#FFF6E6", "#FFE1A8"),
               "critical": ("#FDECEC", "#F6C3C3")}
    bg, bd = palette[kind]
    return v_textbox(M, y, PW - 2 * M, CALLOUT_H, Z, 80, runs, bg=bg, border=bd)

pages_order = []

# -------------------- PAGE 1: DEMANDA --------------------
P1 = "5dd4ac40977d4030d72e"   # reutiliza id existente
pages_order.append(P1)
v = []
v += header_block("P1", "Evolucion de la demanda de atencion (2005-2024)",
                  "Como evoluciono la demanda entre 2005 y 2024 y que municipios y regiones concentraron el crecimiento. Se suman consultas medicas, odontologicas, paramedicas e interconsultas.")
v += kpi_row([
    ("Demanda Año Actual (2024)", "Demanda total 2024", FACT),
    ("Crecimiento Demanda 2005-2024 %", "Crecimiento 2005-2024", FACT),
    ("CAGR Demanda 2005-2024 %", "CAGR anual", FACT),
    ("Crecimiento Demanda Absoluto 2005-2024", "Prestaciones adicionales vs 2005", FACT),
])
v.append(v_line(M, ROW1_Y, 1100, 380, Z, 10, FACT, "anio",
                [(FACT, "Demanda Total de Atención")],
                "Demanda total de atencion, 2005-2024 (caida en 2020 por COVID-19)"))
v.append(v_bar(M + 1116, ROW1_Y, PW - 2 * M - 1116, 380, Z, 11, FACT, "anio",
               [(FACT, "Total Consultas Médicas"), (FACT, "Total Consultas Odontológicas"),
                (FACT, "Total Consultas Paramédicas"), (FACT, "Total Interconsultas")],
               "Composicion de la demanda por tipo de prestacion", stacked=True, column=True))
ROW2_Y = ROW1_Y + 396
b_muni = v_bar(M, ROW2_Y, 1100, 330, Z, 12, DIMG, "municipio_nombre",
               [(FACT, "Crecimiento Demanda Absoluto 2005-2024")],
               "Municipios con mayor crecimiento absoluto de demanda (2005 - 2024)")
attach_filters(b_muni, [f_measure_ge(FACT, "Crecimiento Demanda Absoluto 2005-2024", 1200000)])
v.append(b_muni)
v.append(v_bar(M + 1116, ROW2_Y, PW - 2 * M - 1116, 330, Z, 13, FACT, "region_sanitaria",
               [(FACT, "Demanda Año Base (2005)"), (FACT, "Demanda Año Actual (2024)")],
               "Regiones sanitarias: 2005 vs 2024", column=True))
CO_Y = ROW2_Y + 344
v.append(callout(CO_Y, "warn", [
    ("Limite de datos por establecimiento:  ", {"bold": True, "color": "#7A4D06", "size": 12}),
    ("establecimiento_id esta vacio en el 100% de las filas 2005-2017 (solo municipio y region sanitaria). El desglose por establecimiento recien es confiable desde 2018; la tabla siguiente compara 2018 vs 2024.",
     {"color": "#7A4D06", "size": 12}),
]))
T_Y = CO_Y + CALLOUT_H + 12
t1 = v_table(M, T_Y, PW - 2 * M, 1060 - T_Y, Z, 14, [
    ("col", DIME, "establecimiento_nombre"), ("col", DIME, "Municipio"),
    ("measure", FACT, "Demanda Año 2018"), ("measure", FACT, "Demanda Año Actual (2024)"),
    ("measure", FACT, "Crecimiento Demanda 2018-2024"),
], "Establecimientos con mayor crecimiento de demanda (2018 - 2024)")
attach_filters(t1, [f_measure_ge(FACT, "Crecimiento Demanda 2018-2024", 300000)])
v.append(t1)
write_page(P1, "01 · Demanda de atencion", 0, v)

# -------------------- PAGE 2: CAPACIDAD --------------------
P2 = hexid()
pages_order.append(P2)
v = []
v += header_block("P2", "Saturacion y subutilizacion de capacidad hospitalaria",
                  "Que establecimientos de agudos muestran senales de saturacion o subutilizacion. Se cruzan camas, pacientes-dia, % de ocupacion, egresos y giro de camas (promedio 2022-2024).")
v += kpi_row([
    ("% Ocupación 2024", "Ocupacion 2024", FACT),
    ("Hospitales Saturados", "Hospitales saturados (>=90%)", FACT),
    ("Camas Subutilizadas", "Camas subutilizadas (<=40%)", FACT),
    ("Establecimientos Anomalía Ocupación", "Anomalias de datos (>100%)", FACT),
])
v.append(callout(KPI_Y + KPI_H + 14, "info", [
    ("Segmentacion:  ", {"bold": True, "color": "#0A5560", "size": 12}),
    ("los establecimientos de estadia prolongada (geriatricos, media > 30 dias) se excluyen del analisis de saturacion porque su logica de ocupacion y rotacion no es comparable con internacion aguda.",
     {"color": "#0A5560", "size": 12}),
]))
SC_Y = KPI_Y + KPI_H + 14 + CALLOUT_H + 14
ROW1_H2 = 320
sc = v_scatter(M, SC_Y, 1100, ROW1_H2, Z, 10, DIME, "establecimiento_nombre",
               (FACT, "Ocupación Prom (estab)"), (FACT, "Giro Prom (estab)"),
               (FACT, "Camas 22-24 (estab)"),
               "Ocupacion vs giro de camas - establecimientos de agudos")
attach_filters(sc, [f_categorical_in(DIME, "Segmento", ["Agudos"])])
v.append(sc)
ts = v_table(M + 1116, SC_Y, PW - 2 * M - 1116, ROW1_H2, Z, 11, [
    ("col", DIME, "establecimiento_nombre"), ("col", DIME, "Municipio"),
    ("measure", FACT, "Camas 22-24 (estab)"), ("measure", FACT, "Ocupación Prom (estab)"),
    ("measure", FACT, "Giro Prom (estab)"),
], "Establecimientos saturados (ocupacion sostenida >= 90%)")
attach_filters(ts, [f_categorical_in(DIME, "Clasificacion Capacidad", ["Saturado"])])
v.append(ts)
# callout critico a todo el ancho (se saco el grafico de region sanitaria para dejarle
# espacio real a la tabla de subutilizados, que antes quedaba con ~38px de alto)
CO_Y2 = SC_Y + ROW1_H2 + 14
v.append(callout(CO_Y2, "critical", [
    ("Hallazgo de calidad de datos:  ", {"bold": True, "color": "#7A1414", "size": 12}),
    ("25 establecimientos (UPA y Unidades de Diagnostico Precoz) muestran ocupacion > 100% - hasta 242% - imposible con la formula estandar. Probablemente informan camas de observacion/guardia de alta rotacion, no de internacion. Excluidos del ranking.",
     {"color": "#7A1414", "size": 12}),
]))
T_Y = CO_Y2 + CALLOUT_H + 14
tsub = v_table(M, T_Y, PW - 2 * M, 1060 - T_Y, Z, 13, [
    ("col", DIME, "establecimiento_nombre"), ("col", DIME, "Municipio"), ("col", DIME, "Dependencia"),
    ("measure", FACT, "Camas 22-24 (estab)"), ("measure", FACT, "Ocupación Prom (estab)"),
    ("measure", FACT, "Giro Prom (estab)"),
], "Establecimientos subutilizados - candidatos a revision de dotacion de camas")
attach_filters(tsub, [f_categorical_in(DIME, "Clasificacion Capacidad", ["Subutilizado"])])
v.append(tsub)
write_page(P2, "02 · Capacidad hospitalaria", 1, v)

# -------------------- PAGE 3: CALIDAD --------------------
P3 = hexid()
pages_order.append(P3)
v = []
v += header_block("P3", "Desempeno relativo en internacion",
                  "Que establecimientos muestran peor desempeno relativo y como evolucionaron. Se comparan dias de estadia y mortalidad hospitalaria contra la mediana de su misma dependencia (banda de referencia).")
v += kpi_row([
    ("Promedio Días de Estadía 2024", "Dias de estadia 2024", FACT),
    ("Tasa de Mortalidad Hospitalaria 2024 %", "Mortalidad hospitalaria 2024", FACT),
    ("Total Defunciones 2024", "Defunciones 2024", FACT),
    ("Establecimientos Peor Desempeño", "Establecimientos sobre banda", FACT),
])
BW_Y = ROW1_Y
bw = v_bar(M, BW_Y, 1100, 380, Z, 10, DIME, "establecimiento_nombre",
           [(FACT, "Estadía relativa a banda (x)"), (FACT, "Mortalidad relativa a banda (x)")],
           "Peor desempeno relativo vs. banda de referencia (multiplo)")
attach_filters(bw, [f_categorical_in(DIME, "Desempeno Internacion", ["Peor desempeno"]),
                    f_measure_ge(FACT, "Mortalidad relativa a banda (x)", 2.5)])
v.append(bw)
ln = v_line(M + 1116, BW_Y, PW - 2 * M - 1116, 380, Z, 11, FACT, "anio",
            [(FACT, "Tasa de Mortalidad Hospitalaria %")],
            "Evolucion de la mortalidad 2018-2024 - peores desempenos",
            legend=(DIME, "establecimiento_nombre"))
attach_filters(ln, [f_categorical_in(DIME, "Desempeno Internacion", ["Peor desempeno"]),
                    f_col_ge(FACT, "anio", 2018),
                    f_measure_ge(FACT, "Mortalidad relativa a banda (x)", 4)])
v.append(ln)
C1_Y = BW_Y + 396
v.append(callout(C1_Y, "critical", [
    ("El ID de establecimiento no es persistente en el tiempo:  ", {"bold": True, "color": "#7A1414", "size": 12}),
    ("hay codigos de establecimiento_id reasignados a instituciones distintas entre anios. No comparar una serie temporal por ID sin validar que el nombre se mantuvo estable en todos los anios.",
     {"color": "#7A1414", "size": 12}),
]))
C2_Y = C1_Y + CALLOUT_H + 10
v.append(callout(C2_Y, "warn", [
    ("Cuidado con el casemix:  ", {"bold": True, "color": "#7A4D06", "size": 12}),
    ("un centro oncologico especializado tiene mortalidad mas alta por la severidad de sus pacientes, no por falla de calidad. Todo ranking de mortalidad deberia segmentarse por especialidad antes de usarse para gestion.",
     {"color": "#7A4D06", "size": 12}),
]))
T_Y = C2_Y + CALLOUT_H + 12
tw = v_table(M, T_Y, PW - 2 * M, 1060 - T_Y, Z, 12, [
    ("col", DIME, "establecimiento_nombre"), ("col", DIME, "Municipio"), ("col", DIME, "Dependencia"),
    ("measure", FACT, "Promedio Días de Estadía"), ("measure", FACT, "Estadía relativa a banda (x)"),
    ("measure", FACT, "Tasa de Mortalidad Hospitalaria %"), ("measure", FACT, "Mortalidad relativa a banda (x)"),
    ("measure", FACT, "Total Egresos"),
], "Establecimientos con peor desempeno relativo")
attach_filters(tw, [f_categorical_in(DIME, "Desempeno Internacion", ["Peor desempeno"]),
                    f_measure_ge(FACT, "Mortalidad relativa a banda (x)", 2)])
v.append(tw)
write_page(P3, "03 · Calidad de internacion", 2, v)

# -------------------- pages.json --------------------
with open(os.path.join(PAGES_DIR, "pages.json"), "w", encoding="utf-8") as f:
    json.dump({"$schema": SCHEMA_PAGES, "pageOrder": pages_order, "activePageName": P1},
              f, indent=2, ensure_ascii=False)

print("PAGINAS:", pages_order)
print("OK - archivos escritos en", PAGES_DIR)
