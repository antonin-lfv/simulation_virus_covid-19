''' modélisation avec utilisation de plotly '''

from sklearn.datasets import make_blobs
import random as rd
import time
from scipy.spatial import distance
from plotly.offline import plot
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

def distance_e(x, y):  # distance entre 2 points du plan cartésien
    return distance.euclidean([x[0],x[1]],[y[0],y[1]])

def remove_(a, l): # enlever les éléments de l dans a
    for i in range(len(l)):
        a.remove(l[i])
    return a

def chance_infecte(p):  # return True si il devient infecté avec une proba p
    proba = int(p * 100)
    return rd.randint(0, 100) <= proba

def immuniser(l, l2, p):  # l: infectés; l2: immunisés précédents
    drop = 0
    for i in range(len(l)):
        proba = int(p * 100)
        if rd.randint(0, 100) <= proba:
            l2.append(l[i-drop])
            l.remove(l[i-drop])
            drop+=1
    return l, l2

def deces(l, l2, l3, p):  # l: infectés; l2: décès précédents; l3: immunisés
    l_p = l[:]  # création d'une copie pour éviter erreur d'indice
    for i in range(len(l_p)):
        proba = int(p * 100)
        if rd.randint(0, 100) <= proba and l_p[i] not in l3:
            l2.append(l_p[i])
            l.remove(l_p[i])
    return l, l2


def vague_seuil_px_opti2():

    print('Début de la simulation ... \n')
    start = time.time()

    nb_individu = 2000  # recommandé : 500 à 10000
    variance_pop = 1  # recommandé : 1
    rayon_contamination = 0.5  # recommandé : 0.5
    infectiosite = 0.17  # recommandé : 10%
    p = 0.1  # recommandé : 10%
    d = 0.05  # recommandé : 5%

    # NOTE : si les courbes restent constantes, augmentez le rayon de contamination
    # si le virus est trés mortel il n'y aura pas beaucoup de propagation

    # Bleu : '#636EFA'
    # Rouge : '#EF553B'
    # Vert : '#00CC96'
    # Violet : '#AB63FA'

    if nb_individu < 10 or rayon_contamination <= 0:
        return 'error, nb_individu and var_population and rayon_contamination must be >=10 and > 0'
    if infectiosite < 0 or infectiosite > 1:
        return 'error, infectiosité must be in [0,1]'
    if p < 0 or p > 1:
        return 'error, p must be in [0,1]'
    if d < 0 or p > 1:
        return 'error, d must be in [0,1]'

    # création des figures
    fig = make_subplots(rows=2, cols=2, column_widths=[0.8, 0.2], row_heights=[0.5, 0.5],
                        subplot_titles=["population", "", ""],
                        specs=[[{'type': 'xy'}, {'type': 'domain'}], [{'type': 'xy', 'colspan': 2}, None]],
                        horizontal_spacing=0.05, vertical_spacing=0.05)

    # dataset
    x, y = make_blobs(n_samples=nb_individu, centers=1, cluster_std=variance_pop)
    df = pd.DataFrame(dict(x=x[:,0],
                           y=x[:,1]))

    # création des courbes finales et listes des coordonnées
    data = dict(courbe_sains = [],courbe_infectes = [],courbe_immunises = [],courbe_deces = [],courbe_removed = [],coord_infectes=[],coord_sains=[],coord_immunises=[],coord_deces=[])

    numero_infecte_1 = rd.randint(0, nb_individu - 1)  # on choisit le premier individu infecté au hasard
    coord_1er_infecte = [df['x'][numero_infecte_1], df['y'][numero_infecte_1]]  # coordonnées du 1er infecté

    # Remplissage des listes

    for k in range(nb_individu):
        if k==numero_infecte_1 :
            data['coord_infectes'].append(coord_1er_infecte)
        else:
            data['coord_sains'].append([df['x'][k], df['y'][k]])

    data['courbe_sains'].append(nb_individu-1)
    data['courbe_infectes'].append(1)
    data['courbe_immunises'].append(0)
    data['courbe_deces'].append(0)
    data['courbe_removed'].append(0)

    # Jours 2 à n

    while len(data['coord_infectes']) > 0.08*nb_individu or len(data['courbe_sains']) < 10: #condition d'arrêt

        for k in range(len(data['coord_infectes'])):
            non_sains = 0
            for j in range(len(data['coord_sains'])):
                if distance_e(data['coord_infectes'][k],data['coord_sains'][j-non_sains]) < rayon_contamination and data['coord_sains'][j-non_sains] not in data['coord_infectes'] and chance_infecte(infectiosite):
                    data['coord_infectes'].append(data['coord_sains'][j-non_sains])
                    data['coord_sains'].remove(data['coord_sains'][j-non_sains])
                    non_sains+=1

        coord_infectes1, data['coord_immunises'] = immuniser(data['coord_infectes'], data['coord_immunises'], p)
        data['coord_infectes'], data['coord_deces'] = deces(coord_infectes1, data['coord_deces'], data['coord_immunises'], d)

        # pour les courbes finales
        data['courbe_sains'].append(len(data['coord_sains']))
        data['courbe_infectes'].append(len(data['coord_infectes']))
        data['courbe_immunises'].append(len(data['coord_immunises']))
        data['courbe_deces'].append(len(data['coord_deces']))
        data['courbe_removed'].append(len(data['coord_immunises']) + len(data['coord_deces']))

    if data['coord_sains']:
        fig.add_trace(go.Scatter(x=np.array(data['coord_sains'])[:, 0], y=np.array(data['coord_sains'])[:, 1], name="sain", mode="markers",
                                 marker=dict(
                                     color='#636EFA',
                                     size=5,
                                     line=dict(
                                         width=0.4,
                                         color='#636EFA')
                                 ),marker_line=dict(width=1), showlegend=False), 1, 1)
    if data['coord_infectes']:
        fig.add_trace(go.Scatter(x=np.array(data['coord_infectes'])[:, 0], y=np.array(data['coord_infectes'])[:, 1], name="infecté",mode="markers",
                                 marker=dict(
                                     color='#EF553B',
                                     size=5,
                                     line=dict(
                                         width=0.4,
                                         color='#EF553B')
                                 ),marker_line=dict(width=1), showlegend=False), 1, 1)
    if data['coord_immunises']:
        fig.add_trace(go.Scatter(x=np.array(data['coord_immunises'])[:, 0], y=np.array(data['coord_immunises'])[:, 1], name='immunisé',mode="markers",
                                 marker=dict(
                                     color='#00CC96',
                                     size=5,
                                     line=dict(
                                         width=0.4,
                                         color='#00CC96')
                                 ), marker_line=dict(width=1),showlegend=False), 1, 1)
    if data['coord_deces'] :
        fig.add_trace(go.Scatter(x=np.array(data['coord_deces'])[:, 0], y=np.array(data['coord_deces'])[:, 1], name="décédé", mode="markers",
                                 marker=dict(
                                     color='#AB63FA',
                                     size=5,
                                     line=dict(
                                         width=0.4,
                                         color='#AB63FA')
                                 ), marker_line=dict(width=1),showlegend=False), 1, 1)
    fig.update_traces(hoverinfo="name")
    fig.update_xaxes(showgrid=False, visible=False, row=1, col=1)
    fig.update_yaxes(showgrid=False, visible=False, row=1, col=1)
    labels = ["sains", "infectés", "immunisés", "décédés"]
    fig.add_trace(go.Pie(values=[len(data['coord_sains']), len(data['coord_infectes']), len(data['coord_immunises']), len(data['coord_deces'])], labels=labels, sort=False), 1, 2)

    x_courbe = list(np.arange(0, len(data['courbe_sains'])))
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_sains'], marker=dict(color='#636EFA'), marker_line=dict(width=2),showlegend=False, name="sains",yaxis="y", ), 2, 1)
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_infectes'], marker=dict(color='#EF553B'), marker_line=dict(width=1),showlegend=False, name="infectés",yaxis="y2", ), 2, 1)
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_immunises'], marker=dict(color='#00CC96'), marker_line=dict(width=1),showlegend=False, name="immunisés",yaxis="y3", ), 2, 1)
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_deces'], marker=dict(color='#AB63FA'), marker_line=dict(width=1),showlegend=False, name="décédés",yaxis="y4", ), 2, 1)
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_removed'], marker=dict(color='#000000'), marker_line=dict(width=1), showlegend=False, name="removed",yaxis="y5", ), 2, 1)
    fig.update_xaxes(title_text="jours", row=2, col=1)
    fig.update_yaxes(title_text="nombre d'individus", row=2, col=1)
    fig.add_annotation(text="Maximum d'infectés", x=data['courbe_infectes'].index(max(data['courbe_infectes'])),# ajouter un texte avec une flèche
                       y=max(data['courbe_infectes']) + 0.03 * nb_individu, arrowhead=1, showarrow=True, row=2, col=1)
    fig.update_traces(
        hoverinfo="name+x+y",
        line={"width": 1.3},
        marker={"size": 2},
        mode="lines+markers",
        showlegend=False, row=2, col=1)

    fig.update_layout(hovermode="x")
    fig.update_layout(title_text="simulation virus")
    fig.update_layout(title_font_color='#EF553B')
    t = (time.time()-start)
    min = int(round(t,2)//60)
    sec = round(t-min*60,1)
    print('Simulation terminée en '+str(min)+' minutes \net '+str(sec)+' secondes')
    plot(fig)

