import streamlit as st
import json
import base64

st.set_page_config(layout="wide")
st.title("Mapa Interativo do Ceará")

# Caminhos exatos da sua estrutura
PATH_GEOJSON = "app/components/ceara.geojson.json"
PATH_HTML = "app/components/mapa_d3.html"

# 1. Carregar arquivos
with open(PATH_GEOJSON, "r", encoding="utf-8") as f:
    ceara_geo = json.load(f)

with open(PATH_HTML, "r", encoding="utf-8") as f:
    html_template = f.read()

# 2. Seus dados de ML/Estatística
dados_municipios = {
    "Fortaleza": 100,
    "Sobral": 70,
    "Juazeiro do Norte": 85,
    "Abaiara": 30,
    "Crateús": 50
}

# 3. Injetar dados no template HTML
html_final = html_template.replace(
    "const dataFromStreamlit = {};", 
    f"const dataFromStreamlit = {json.dumps(dados_municipios)};"
).replace(
    "const geojson = {};", 
    f"const geojson = {json.dumps(ceara_geo)};"
)

# 4. Converter para Base64 para usar no st.iframe (padrão 2026)
b64_html = base64.b64encode(html_final.encode("utf-8")).decode("utf-8")
data_url = f"data:text/html;base64,{b64_html}"

# Renderizar o mapa
st.iframe(data_url, height=700)