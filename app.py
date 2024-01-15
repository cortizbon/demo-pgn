import streamlit as st
import plotly.graph_objects as go 
import pandas as pd 
import json
import plotly.express as px

st.set_page_config(layout='wide')

st.title("Presupuesto General de la Nación")

df = pd.read_csv('data/gastos.csv')
df['PGN'] = 'PGN'

year = st.select_slider("Seleccione un año", df['year'].unique())

df = df[df['year'] == year]



with open('data/dic_info.json', 'r') as js:
    dic_info = json.load(js)

dic_info['PGN'] = max(dic_info.values()) + 1

rel_sec_ent = (df
 .groupby(['year', 'sector name', 'entity name'])['cop']
 .sum()
 .reset_index()
 .rename(columns={'sector name': 'col0',
                  'entity name': 'col1'}))

rel_ent_it = (df
 .groupby(['year', 'entity name', 'item'])['cop']
 .sum()
 .reset_index()
 .rename(columns={'entity name': 'col0',
                  'item': 'col1'}))

rels = pd.concat([rel_sec_ent, rel_ent_it])

rels['col0'] = rels['col0'].map(dic_info)
rels['col1'] = rels['col1'].map(dic_info)

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

st.header('Presupuesto general')

dic_info['PGN'] = 327
test1 = (df
         .groupby(['year', 'sector name', 'item'])['cop']
         .sum()
         .reset_index()
         .rename(columns={'sector name':'col0',
                          'item':'col1'}))
test2 = (df
         .groupby(['year','PGN', 'sector name'])['cop']
         .sum()
         .reset_index()
         .rename(columns={'sector name':'col1',
                          'PGN':'col0'}))
test = pd.concat([test1, test2], ignore_index=True)
test = test[test['year'] == year]

test['col1'] = test['col1'].map(dic_info)
test['col0'] = test['col0'].map(dic_info)

fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(color = "black", width = 0.5),
      label = list(dic_info.keys()),
      color = "blue"
    ),
    link = dict(
      source = test['col0'], # indices correspond to labels, eg A1, A2, A1, B1, ...
      target = test['col1'],
      value = test['cop']
  ))])

fig.update_layout(title_text="Presupuesto general", font_size=10, width=1000, height=700)
st.plotly_chart(fig)



sector = st.selectbox("Seleccione el sector", 
                       df['sector name'].unique())

df = df[df['sector name'] == sector]
rel_sec_ent = (df
 .groupby(['year', 'sector name', 'entity name'])['cop']
 .sum()
 .reset_index()
 .rename(columns={'sector name': 'col0',
                  'entity name': 'col1'}))

rel_ent_it = (df
 .groupby(['year', 'entity name', 'item'])['cop']
 .sum()
 .reset_index()
 .rename(columns={'entity name': 'col0',
                  'item': 'col1'}))

rels = pd.concat([rel_sec_ent, rel_ent_it])

rels['col0'] = rels['col0'].map(dic_info)
rels['col1'] = rels['col1'].map(dic_info)





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

fig.update_layout(title_text="Presupueso por sector", font_size=10, width=1000, height=800)
st.header('Presupuesto por sector')
st.plotly_chart(fig)






