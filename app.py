import streamlit as st
import plotly.graph_objects as go 
import pandas as pd 
import json
import plotly.express as px

st.set_page_config(layout='wide')

st.title("Presupuesto General de la Nación")



df = pd.read_csv('data/gastos.csv')
rels_or = pd.read_csv('data/relationships_or.csv')
rels = pd.read_csv('data/relationships.csv')

with open('data/dic_info.json', 'r') as js:
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

sector = st.selectbox("Seleccione el sector", 
                       df['sector name'].unique())

df = df[df['sector name'] == sector]
rels = rels[(rels['col0'] == dic_info[sector])]


col1, col2 = st.columns(2)

with col1:
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

    fig.update_layout(title_text="PGN", font_size=10, width=500, height=350)
    st.header('Sankey diagram')
    st.plotly_chart(fig)

with col2:
    st.header('Second sankey')

    test = df.groupby(['year', 'sector name', 'item'])['cop'].sum().reset_index()
    test['PGN'] = 'PGN'
    test = test[test['year'] == year]

    test['sector name'] = test['sector name'].map(dic_info)
    test['item'] = test['item'].map(dic_info)

    fig = go.Figure(data=[go.Sankey(
        node = dict(
        pad = 15,
        thickness = 20,
        line = dict(color = "black", width = 0.5),
        label = list(dic_info.keys()),
        color = "blue"
        ),
        link = dict(
        source = test['sector name'], # indices correspond to labels, eg A1, A2, A1, B1, ...
        target = test['item'],
        value = test['cop']
    ))])

    fig.update_layout(title_text="Basic Sankey Diagram", font_size=10, width=500, height=450)
    st.plotly_chart(fig)



