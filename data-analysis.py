import pandas as pd
import streamlit as st
import plotly.express as px
import altair as alt

# load datasets
df_shoots = pd.read_csv('2024-shoots.csv', sep=',')
df_possession = pd.read_csv('2024-possession.csv', sep=',')
df_defense = pd.read_csv('2024-defense.csv', sep=',')
df_defensive_actions = pd.read_csv('2024-defensive-actions.csv', sep=',')
df_passes = pd.read_csv('2024-passes.csv', sep=',')

# Shoots
data_shoots = {'team': [], 'type': [], 'amount': []}

for item in df_shoots.values:
    data_shoots['team'].append(item[0])
    data_shoots['type'].append('Gol')
    data_shoots['amount'].append(item[3])
    data_shoots['team'].append(item[0])
    data_shoots['type'].append('No alvo')
    data_shoots['amount'].append(item[5] - item[3])
    data_shoots['team'].append(item[0])
    data_shoots['type'].append('Pra fora')
    data_shoots['amount'].append(item[4] - item[5])

df_data_shoots = pd.DataFrame(data=data_shoots)


# Possession
data_possession = {'team': [], 'type': [], 'amount': []}

for item in df_possession.values:
    data_possession['team'].append(item[0])
    data_possession['type'].append('Defesa')
    data_possession['amount'].append(item[5]+item[6])
    data_possession['team'].append(item[0])
    data_possession['type'].append('Meio do campo')
    data_possession['amount'].append(item[7])
    data_possession['team'].append(item[0])
    data_possession['type'].append('Ataque')
    data_possession['amount'].append(item[9]+item[8])


# Passes
data_passes = {'team': [], 'type': [], 'amount': []}
data_completed_passes = {'team': [], 'amount': []}
data_passes_types = {'team': [], 'type': [], 'amount': []}

for item in df_passes.values:
    data_passes['team'].append(item[0])
    data_passes['type'].append('Passes certos')
    data_passes['amount'].append(item[3])
    data_passes['team'].append(item[0])
    data_passes['type'].append('Passes errados')
    data_passes['amount'].append(item[4] - item[3])
    data_completed_passes['team'].append(item[0])
    data_completed_passes['amount'].append(item[5]/100)
    data_passes_types['team'].append(item[0])
    data_passes_types['type'].append('Lançamentos')
    data_passes_types['amount'].append(item[15])
    data_passes_types['team'].append(item[0])
    data_passes_types['type'].append('Curto')
    data_passes_types['amount'].append(item[9])
    data_passes_types['team'].append(item[0])
    data_passes_types['type'].append('Médio')
    data_passes_types['amount'].append(item[12])

# Defense
data_defense = {'team': [], 'type': [], 'amount': []}

for item in df_defense.values:
    data_defense['team'].append(item[0])
    data_defense['type'].append('Gols sofridos')
    data_defense['amount'].append(item[1])
    data_defense['team'].append(item[0])
    data_defense['type'].append('Chutes no gol')
    data_defense['amount'].append(item[2])

df_data_shoots = pd.DataFrame(data=data_shoots)
df_data_possession = pd.DataFrame(data=data_possession)
df_data_passes = pd.DataFrame(data=data_passes)
df_data_completed_passes = pd.DataFrame(data=data_completed_passes)
df_data_passes_types = pd.DataFrame(data=data_passes_types)
df_data_defense = pd.DataFrame(data=data_defense)

chart_shoot = alt.Chart(df_data_shoots, title='Chutes ao gol', width=500).mark_bar().encode(
    x=alt.X('amount', title=None),
    y=alt.Y("team", title='Clubes', axis=alt.Axis(labels=True)),
    color=alt.Color('type', scale=alt.Scale(range=['lightgreen', 'dodgerblue', 'tomato'])).legend(
        orient='bottom', title=None)
)

chart_possession = alt.Chart(df_data_possession, title='Posse de bola', width=500).mark_bar().encode(
    x=alt.X('sum(amount)', title=None),
    y=alt.Y("team", title='Clubes', axis=alt.Axis(labels=True)),
    color=alt.Color('type', scale=alt.Scale(range=['lightgreen', 'dodgerblue', 'gold'])).legend(
        orient='bottom', title=None)
)

chart_passes = alt.Chart(df_data_passes, title='Passes', width=500).mark_bar().encode(
    x=alt.X('sum(amount)', title=None),
    y=alt.Y("team", title='Clubes', axis=alt.Axis(labels=True)),
    color=alt.Color('type', scale=alt.Scale(range=['lightgreen', 'tomato'])).legend(
        orient='bottom', title=None)
)

chart_percent_passes = alt.Chart(df_data_completed_passes, title='Precisão nos passes', width=500).mark_bar().encode(
    x=alt.X('sum(amount)', title=None),
    y=alt.Y("team", title='Clubes', axis=alt.Axis(labels=True))
)

text_max = alt.Chart(df_data_completed_passes).mark_text(align='left', dx=5, color='white').encode(
    x=alt.X('amount'),
    y=alt.Y('team'),
    text=alt.Text('amount', format='.0%')
)

chart_passes_types = alt.Chart(df_data_passes_types, title='Tipos de passe', width=500).mark_bar().encode(
    x=alt.X('sum(amount)', title=None),
    y=alt.Y("team", title='Clubes', axis=alt.Axis(labels=True)),
    color=alt.Color('type', scale=alt.Scale(range=['lightgreen', 'dodgerblue', 'gold'])).legend(
        orient='bottom', title=None)
)

chart_defense = alt.Chart(df_data_defense, title='Chutes do adversário', width=500).mark_bar().encode(
    x=alt.X('amount', title=None),
    y=alt.Y("team", title='Clubes', axis=alt.Axis(labels=True)),
    color=alt.Color('type', scale=alt.Scale(range=['lightgreen', 'dodgerblue'])).legend(
        orient='bottom', title=None)
)

st.set_page_config(layout='wide')

st.write(
    """
    # Campeonato Brasileiro 2024
    """
)


first_1, second_1 = st.columns(2)
first_2, second_2 = st.columns(2)
first_3, second_3 = st.columns(2)
# first_4, second_4 = st.columns(2)

first_1.write(chart_shoot)
second_1.write(chart_percent_passes + text_max)
first_2.write(chart_passes)
second_2.write(chart_passes_types)
first_3.write(chart_defense)
second_3.write(chart_possession)
