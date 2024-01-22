import streamlit as st
import plotly.graph_objects as go 
import pandas as pd 
import json
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout='wide')

st.title("Presupuesto General de la Nación")

tab1, tab2 = st.tabs(['SCruzada', 'Histórico'])

df = pd.read_csv('data/gastos_2013_2024_const.csv')


df['PGN'] = 'PGN'

with tab1:

  year = st.select_slider("Seleccione un año", df['year'].unique())

  df = df[df['year'] == year]



  with open('info.json', 'r') as js:
      dic_info = json.load(js)

  dic_info2 = dic_info.copy()

  for key, values in dic_info2.items():
      try:
        dic_info[int(key)] = values
      except:
         print('cannot convert')
  dif_info = dic_info2.copy()

  dic_info['PGN'] = max(dic_info.values()) + 1

  rel_sec_ent = (df
  .groupby(['year', 'sector_code', 'entidad'])['cop']
  .sum()
  .reset_index()
  .rename(columns={'sector_code': 'col0',
                    'entidad': 'col1'}))

  rel_ent_it = (df
  .groupby(['year', 'entidad', 'cuenta'])['cop']
  .sum()
  .reset_index()
  .rename(columns={'entidad': 'col0',
                    'cuenta': 'col1'}))

  rels = pd.concat([rel_sec_ent, rel_ent_it])

  rels['col0'] = rels['col0'].map(dic_info)
  rels['col1'] = rels['col1'].map(dic_info)

  df = df[df['year'] == year]
  rels = rels[rels['year'] == year]

  st.header('Treemap')

  fig = px.treemap(df, 
                  path=[px.Constant("PGN"), 'sector_code', 'entidad', 'cuenta'], 
                  values='cop',
                  width=1200,
                  height=800)
  fig.update_traces(root_color="lightgrey")
  fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))

  st.plotly_chart(fig)

  st.header('Presupuesto general')

  
  test1 = (df
          .groupby(['year', 'sector_code', 'cuenta'])['cop']
          .sum()
          .reset_index()
          .rename(columns={'sector_code':'col0',
                            'cuenta':'col1'}))
  st.dataframe(test1)
  test2 = (df
          .groupby(['year','PGN', 'sector_code'])['cop']
          .sum()
          .reset_index()
          .rename(columns={'sector_code':'col1',
                            'PGN':'col0'}))
  st.dataframe(test2)
  
  test = pd.concat([test1, test2], ignore_index=True)
  test['col0'] = test['col0'].map(dic_info)
  test['col1'] = test['col1'].map(dic_info)
  test = test[test['year'] == year]
  st.dataframe(test)

  st.json(dic_info)

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
                        df['sector_code'].unique())

  df = df[df['sector_code'] == sector]
  rel_sec_ent = (df
  .groupby(['year', 'sector_code', 'entidad'])['cop']
  .sum()
  .reset_index()
  .rename(columns={'sector_code': 'col0',
                    'entidad': 'col1'}))

  rel_ent_it = (df
  .groupby(['year', 'entidad', 'cuenta'])['cop']
  .sum()
  .reset_index()
  .rename(columns={'entidad': 'col0',
                    'cuenta': 'col1'}))

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



with tab2:
  df = pd.read_csv('data/gastos_2013_2024_const.csv')


  pivot = df.pivot_table(index='sector_code',
                         columns='year',
                         values='cop_5',
                         aggfunc='sum')

    
  fig, ax = plt.subplots(1, 1, figsize=(14,8))

  sns.heatmap(pivot)

  st.pyplot(fig)

  sector = st.selectbox("Seleccione el sector", df['sector_code'].unique())

  filtro = df[df['sector_code'] == sector]

  pivot2 = filtro.pivot_table(index='year',
                              columns='entidad',
                              values='cop_5',
                              aggfunc='sum')

  fig, ax = plt.subplots(1, 1, figsize=(14, 8))

  pivot2.plot(kind='area',
              ax=ax,
              cmap='Blues')
  
  st.pyplot(fig)




