from datetime import date
import datetime
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import pandas as pd
import numpy as np
from fastdist import fastdist
import random as rd
from sklearn.datasets import make_blobs
import itertools

st.set_page_config(layout="wide", )
# streamlit run StreamLit/streamlit.py
st.markdown("""
<style>
.first_titre {
    font-size:40px !important;
    font-weight: bold;
    box-sizing: border-box;
    text-align: center;
    width: 100%;
    border: solid #008000 4px;
    padding: 4px;
}
.intro{
    text-align: justify;
    font-size:20px !important;
}
.grand_titre {
    font-size:30px !important;
    font-weight: bold;
    text-decoration: underline;
    text-decoration-color: #2782CD;
    text-decoration-thickness: 5px;
}
.section{
    font-size:20px !important;
    font-weight: bold;
    text-decoration: underline;
    text-decoration-color: #258813;
    text-decoration-thickness: 3px;
}
.petite_section{
    font-size:16px !important;
    font-weight: bold;
}
.caract{
    font-size:11px !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="first_titre">Simulation épidémiologique</p>', unsafe_allow_html=True)
st.sidebar.title("Options :control_knobs:")


def distance_e(x, y):  # distance entre 2 points du plan cartésien
    return fastdist.euclidean(np.array(x), np.array(y))


def remove_(a, l):  # enlever les éléments de l dans a
    for i in range(len(l)):
        a.remove(l[i])
    return a


def chance_infecte(p):  # return True si il devient infecté avec une proba p
    return rd.randint(0, 100) < int(p * 100)


def immuniser(l, l2, p):  # l: infectés; l2: immunisés précédents
    drop = 0
    for i in range(len(l)):
        if rd.randint(0, 100) < int(p * 100):
            l2.append(l[i - drop])
            l.remove(l[i - drop])
            drop += 1
    return l, l2


def deces(l, l2, l3, p):  # l: infectés; l2: décès précédents; l3: immunisés
    l_p = l[:]  # création d'une copie pour éviter d'erreur d'indice
    for i in range(len(l_p)):
        if rd.randint(0, 100) < int(p * 100) and not any(list == l_p[i] for list in l3):
            l2.append(l_p[i])
            l.remove(l_p[i])
    return l, l2


global list

with st.sidebar.form(key='Parametres de la simulation'):
    nb_individu = st.slider(label="Nombre d'individus", min_value=10, max_value=2500, value=1000)
    variance_pop = st.slider(label="Éloignement des individus", min_value=0.4, max_value=10., step=0.2, value=1.)
    rayon_contamination = st.slider(label="Rayon de contamination", min_value=0.3, max_value=5.9, step=0.2, value=0.5)
    infectiosite = st.slider(label="Taux d'infection", min_value=0., max_value=1., value=0.1, step=0.05)
    p = st.slider(label="Taux de guérison", min_value=0., max_value=1., value=0.1, step=0.05)
    d = st.slider(label="Taux de décès", min_value=0., max_value=1., value=0.05, step=0.05)
    submit_button = st.form_submit_button(label='Lancer la simulation')

st.sidebar.subheader("La simulation prend quelques secondes à s'éxecuter")

# création des figures
fig = make_subplots(rows=2, cols=2, column_widths=[0.8, 0.2], row_heights=[0.5, 0.5],
                    subplot_titles=["population", "", ""],
                    specs=[[{'type': 'xy'}, {'type': 'domain'}], [{'type': 'xy', 'colspan': 2}, None]],
                    horizontal_spacing=0.05, vertical_spacing=0.05)

# dataset
x, y = make_blobs(n_samples=nb_individu, centers=1, cluster_std=variance_pop)
df = pd.DataFrame(dict(x=x[:, 0],
                       y=x[:, 1]))

# création des courbes finales et listes des coordonnées
data = dict(courbe_sains=[], courbe_infectes=[], courbe_immunises=[], courbe_deces=[],
            coord_infectes=[], coord_sains=[], coord_immunises=[], coord_deces=[])

numero_infecte_1 = rd.randint(0, nb_individu - 1)  # on choisit le premier individu infecté au hasard
coord_1er_infecte = [df['x'][numero_infecte_1], df['y'][numero_infecte_1]]  # coordonnées du 1er infecté

# Remplissage des listes

for k in range(nb_individu):
    if k == numero_infecte_1:
        data['coord_infectes'].append(coord_1er_infecte)
    else:
        data['coord_sains'].append([df['x'][k], df['y'][k]])

data['courbe_sains'].append(nb_individu - 1)
data['courbe_infectes'].append(1)
data['courbe_immunises'].append(0)
data['courbe_deces'].append(0)

# Jours 2 à n

while len(data['coord_infectes']) > 0.08 * nb_individu or len(data['courbe_sains']) < 10:  # condition d'arrêt

    for k in range(len(data['coord_infectes'])):
        non_sains = 0
        for j in range(len(data['coord_sains'])):
            if distance_e(data['coord_infectes'][k],
                          data['coord_sains'][j - non_sains]) < rayon_contamination and not any(
                list == data['coord_sains'][j - non_sains] for list in
                data['coord_infectes']) and chance_infecte(infectiosite):
                buf = data['coord_sains'][j - non_sains]
                data['coord_infectes'].append(buf)
                data['coord_sains'].remove(buf)
                non_sains += 1

    coord_infectes1, data['coord_immunises'] = immuniser(data['coord_infectes'], data['coord_immunises'], p)
    data['coord_infectes'], data['coord_deces'] = deces(coord_infectes1, data['coord_deces'],
                                                        data['coord_immunises'], d)

    # pour les courbes finales
    data['courbe_sains'].append(len(data['coord_sains']))
    data['courbe_infectes'].append(len(data['coord_infectes']))
    data['courbe_immunises'].append(len(data['coord_immunises']))
    data['courbe_deces'].append(len(data['coord_deces']))

if data['coord_sains']:
    fig.add_trace(
        go.Scatter(x=np.array(data['coord_sains'])[:, 0], y=np.array(data['coord_sains'])[:, 1], name="sain",
                   mode="markers",
                   marker=dict(
                       color='#636EFA',
                       size=5,
                       line=dict(
                           width=0.4,
                           color='#636EFA')
                   ), marker_line=dict(width=1), showlegend=False), 1, 1)
if data['coord_infectes']:
    fig.add_trace(go.Scatter(x=np.array(data['coord_infectes'])[:, 0], y=np.array(data['coord_infectes'])[:, 1],
                             name="infecté", mode="markers",
                             marker=dict(
                                 color='#EF553B',
                                 size=5,
                                 line=dict(
                                     width=0.4,
                                     color='#EF553B')
                             ), marker_line=dict(width=1), showlegend=False), 1, 1)
if data['coord_immunises']:
    fig.add_trace(
        go.Scatter(x=np.array(data['coord_immunises'])[:, 0], y=np.array(data['coord_immunises'])[:, 1],
                   name='immunisé', mode="markers",
                   marker=dict(
                       color='#00CC96',
                       size=5,
                       line=dict(
                           width=0.4,
                           color='#00CC96')
                   ), marker_line=dict(width=1), showlegend=False), 1, 1)
if data['coord_deces']:
    fig.add_trace(
        go.Scatter(x=np.array(data['coord_deces'])[:, 0], y=np.array(data['coord_deces'])[:, 1], name="décédé",
                   mode="markers",
                   marker=dict(
                       color='#AB63FA',
                       size=5,
                       line=dict(
                           width=0.4,
                           color='#AB63FA')
                   ), marker_line=dict(width=1), showlegend=False), 1, 1)
fig.update_traces(hoverinfo="name")
fig.update_xaxes(showgrid=False, visible=False, row=1, col=1)
fig.update_yaxes(showgrid=False, visible=False, row=1, col=1)
labels = ["sains", "infectés", "immunisés", "décédés"]
fig.add_trace(go.Pie(
    values=[len(data['coord_sains']), len(data['coord_infectes']), len(data['coord_immunises']),
            len(data['coord_deces'])], labels=labels, sort=False,
    marker_colors=['#636EFA', '#EF553B', '#00CC96', '#AB63FA']), 1, 2)

x_courbe = list(np.arange(0, len(data['courbe_sains'])))
fig.add_trace(
    go.Scatter(x=x_courbe, y=data['courbe_sains'], marker=dict(color='#636EFA'), marker_line=dict(width=2),
               showlegend=False, name="sains", yaxis="y", ), 2, 1)
fig.add_trace(
    go.Scatter(x=x_courbe, y=data['courbe_infectes'], marker=dict(color='#EF553B'), marker_line=dict(width=1),
               showlegend=False, name="infectés", yaxis="y2", ), 2, 1)
fig.add_trace(
    go.Scatter(x=x_courbe, y=data['courbe_immunises'], marker=dict(color='#00CC96'), marker_line=dict(width=1),
               showlegend=False, name="immunisés", yaxis="y3", ), 2, 1)
fig.add_trace(
    go.Scatter(x=x_courbe, y=data['courbe_deces'], marker=dict(color='#AB63FA'), marker_line=dict(width=1),
               showlegend=False, name="décédés", yaxis="y4", ), 2, 1)
fig.update_xaxes(title_text="jours", row=2, col=1)
fig.update_yaxes(title_text="nombre d'individus", row=2, col=1)
fig.add_annotation(text="Maximum d'infectés", x=data['courbe_infectes'].index(max(data['courbe_infectes'])),
                   # ajouter un texte avec une flèche
                   y=max(data['courbe_infectes']) + 0.03 * nb_individu, arrowhead=1, showarrow=True, row=2,
                   col=1)
fig.update_traces(
    hoverinfo="name+x+y",
    line={"width": 1.3},
    marker={"size": 2},
    mode="lines+markers",
    showlegend=False, row=2, col=1)

fig.update_layout(hovermode="x")
fig.update_layout(
    template='simple_white',
    font=dict(size=10),
    autosize=False,
    width=1600, height=1000,
    margin=dict(l=40, r=500, b=40, t=40),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
)
st.plotly_chart(fig)
