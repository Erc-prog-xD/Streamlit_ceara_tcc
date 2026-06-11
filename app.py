import streamlit as st
import pandas as pd
import json
import base64
import os


st.set_page_config(layout="wide")
st.title("Mapa Interativo do Ceará")

PATH_GEOJSON = "app/components/ceara.geojson.json"
PATH_HTML = "app/components/mapa_d3.html"
PATH_POPULATION = "data/ibge_csv/populacao_ceara_ibge_2022.json"
PATH_CSV_CATEGORIAS = "data/contratos_classificados_final.csv"

with open(PATH_GEOJSON, "r", encoding="utf-8") as f:
    ceara_geo = json.load(f)

with open(PATH_HTML, "r", encoding="utf-8") as f:
    html_template = f.read()

with open(PATH_POPULATION, "r", encoding="utf-8") as f:
    population = json.load(f)

population_por_codigo = {
    item["codigo_ibge"]: item
    for item in population.values()
}


df = pd.read_csv(PATH_CSV_CATEGORIAS)

# Garante que valorGlobal seja numérico
df["valorGlobal"] = pd.to_numeric(df["valorGlobal"], errors="coerce")

# Describe por município
describe_municipios = (
    df.groupby("unidadeOrgao.municipioNome")["valorGlobal"]
    .describe()
    .fillna(0)
    .round(2)
    .to_dict(orient="index")
)

# Valor usado para pintar o mapa: soma por município
dados_municipios = (
    df.groupby("unidadeOrgao.municipioNome")["valorGlobal"]
    .sum()
    .fillna(0)
    .round(2)
    .to_dict()
)

html_final = html_template.replace(
    "const dataFromStreamlit = {};",
    f"const dataFromStreamlit = {json.dumps(dados_municipios, ensure_ascii=False)};"
).replace(
    "const describeFromStreamlit = {};",
    f"const describeFromStreamlit = {json.dumps(describe_municipios, ensure_ascii=False)};"
).replace(
    "const geojson = {};",
    f"const geojson = {json.dumps(ceara_geo, ensure_ascii=False)};"
).replace(
    "const populacaoFromIBGE = {};",
    f"const populacaoFromIBGE = {json.dumps(population_por_codigo, ensure_ascii=False)};"
)

b64_html = base64.b64encode(html_final.encode("utf-8")).decode("utf-8")
data_url = f"data:text/html;base64,{b64_html}"

st.iframe(data_url, height=700)