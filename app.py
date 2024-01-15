import streamlit as st
import plotly.graph_objects as go 
import pandas as pd 
import json
import plotly.express as px

st.set_page_config(layout='wide')

st.title("Presupuesto General de la Nación")



df = pd.read_csv('gastos.csv')
rels_or = pd.read_csv('relationships_or.csv')
rels = pd.read_csv('relationships.csv')

with open('dic_info.json', 'r') as js:
    dic_info = json.load(js)

year = st.select_slider("Seleccione un año", df['year'].unique())

df = df[df['year'] == year]
rels = rels[rels['year'] == year]

st.header('Treemap')

fig = px.treemap(df, 
                 path=[px.Constant("PGN"), 'sector name', 'entity name', 'item'], 
                 values='cop',
                 width=1200,
                 height=800)
fig.update_traces(root_color="lightgrey")
fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))

st.plotly_chart(fig)

fig = go.Figure(data=[go.Sankey(
node = dict(
      pad = 15,
      thickness = 30,
      line = dict(color = "black", width = 0.5),
      label = list(dic_info.keys())
    ),
link = dict(
      source = rels['col0'], # indices correspond to labels, eg A1, A2, A1, B1, ...
      target = rels['col1'],
      value = rels['cop']
    ))])

fig.update_layout(title_text="PGN", font_size=10, width=1200, height=800)
st.header('Sankey diagram')
st.plotly_chart(fig)





