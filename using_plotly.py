''' modélisation avec plotly '''

""" importation """

from typing import List, Any
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.datasets import make_blobs
import random as rd

from plotly.offline import download_plotlyjs, init_notebook_mode, plot,iplot # pour travailler en offline!
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Fonctions utiles

def distance(x, y):  # distance entre 2 points du plan cartésien
    x1 = x[0]
    x2 = x[1]
    y1 = y[0]
    y2 = y[1]
    return (abs(np.sqrt((y1 - x1) ** 2 + (y2 - x2) ** 2)))


def remove_(a, l): # enlever les éléments de l dans a
    for i in range(len(l)):
        a.remove(l[i])
    return (list(a))


def chance_infecte(p):  # return True si il devient infecté avec une proba p
    proba = int(p * 100)
    if rd.randint(0, 100) <= proba:
        return (True)
    else:
        return (False)


def immuniser(l, l2, p):  # l: infectés; l2: immunisés précédents
    coord_immu = []
    l_p = l[:]  # création d'une copie pour éviter d'erreur d'indice
    for i in range(len(l_p)):
        proba = int(p * 100)
        if rd.randint(0, 100) <= proba:
            coord_immu.append(l_p[i])
            l.remove(l_p[i])
    coord_immu += l2  # on ajoute les immunisés précédents
    return list(l), coord_immu


def deces(l, l2, l3, p):  # l: infectés; l2: décès précédents; l3: immunisés
    coord_deces = []
    l_p = l[:]  # création d'une copie pour éviter d'erreur d'indice
    for i in range(len(l_p)):
        proba = int(p * 100)
        if rd.randint(0, 100) <= proba and l_p[i] not in l3:
            coord_deces.append(l_p[i])
            l.remove(l_p[i])
    coord_deces += l2  # on ajoute les décès précédents
    return list(l), coord_deces


# Afficher les 4 premières vagues avec proportions

def virus_px():
    
    #paramètres
    nb_individu = 300
    variance_population = 7
    rayon_contamination = 5
    infectiosite = 0.7
    p = 0.2 #proba immunisé
    d = 0.2 #proba de décès

    fig = go.Figure() #création de la figure
    
    x, y = make_blobs(n_samples=nb_individu, centers=2, cluster_std=variance_population, shuffle=True) #dataset population
    taille_pop = len(x)
    
    # création des subplots - 'xy' pour des courbes et 'domain' pour des pies | colspan pour étendre un subplot sur 2 colonnes
    fig = make_subplots(rows=6, cols=2,column_widths=[0.8, 0.2],specs=[[{'type':'xy'},{'type':'domain'}],[{'type':'xy'},{'type':'domain'}],[{'type':'xy'},{'type':'domain'}],[{'type':'xy'},{'type':'domain'}],[{'type':'xy'},{'type':'domain'}],[{'type':'xy', "colspan": 2},None]])
    
    # initialisation des courbes finales
    courbe_sains = []
    courbe_infectes = []
    courbe_immunises = []
    courbe_deces = []
    
    "1er infecté"
    numero_infecte_1 = rd.randint(0, taille_pop) # au hasard un individu dans la population
    coord_1er_infecte = [x[:, 0][numero_infecte_1], x[:, 1][numero_infecte_1]]
    fig.add_trace(go.Scatter(x=x[:, 0],y=x[:, 1],mode="markers",marker=dict(color='#636EFA'),showlegend=False),1,1) # on trace les individus sains
    fig.add_trace(go.Scatter(x=[x[:, 0][numero_infecte_1]],y=[x[:, 1][numero_infecte_1]],mode="markers",marker=dict(color="Red"),showlegend=False),1,1) # on trace l'individu infecté
    
    "pie"
    labels = ["sains","infectés","immunisés","décédés"]
    fig.add_trace(go.Pie(labels=labels, values=[taille_pop-1,1,0,0],sort=False),1,2) # création du pie (graphe fromage)
    fig.update_xaxes(showgrid=False, visible= False, row=1, col=1)
    fig.update_yaxes(showgrid=False, visible= False, row=1, col=1)
    #actualisation des courbes
    courbe_sains.append(taille_pop - 1)
    courbe_infectes.append(1)
    courbe_immunises.append(0)
    courbe_deces.append(0)
    
    "1er vague"
    coord_infectes = []  # cette liste sera implémentée des nouveaux cas
    coord_sains = []  # liste des cas sains
    for k in range(taille_pop):
        if [x[:, 0][k], x[:, 1][k]] == coord_1er_infecte:
            coord_infectes.append(coord_1er_infecte)
        elif distance(coord_1er_infecte, [x[:, 0][k], x[:, 1][k]]) < rayon_contamination and chance_infecte(infectiosite):
            fig.add_trace(go.Scatter(x=[x[:, 0][k]], y=[x[:, 1][k]], mode="markers", marker=dict(color='#EF553B'), showlegend=False),2,1)
            coord_infectes.append([x[:, 0][k], x[:, 1][k]])
        else:
            fig.add_trace(go.Scatter(x=[x[:, 0][k]], y=[x[:, 1][k]], mode="markers", marker=dict(color='#636EFA'), showlegend=False),2,1)
            coord_sains.append([x[:, 0][k], x[:, 1][k]])
            fig.add_trace(go.Scatter(x=[x[:, 0][numero_infecte_1]], y=[x[:, 1][numero_infecte_1]], mode="markers",marker=dict(color='#EF553B'), showlegend=False),2,1)
    fig.update_xaxes(showgrid=False, visible=False, row=1, col=1) # on supprime les axes
    fig.update_yaxes(showgrid=False, visible=False, row=1, col=1)
    
    "pie"
    labels = ["sains","infectés","immunisés","décédés"]
    fig.add_trace(go.Pie(values=[ len(coord_sains),len(coord_infectes),0,0], labels=labels,sort=False),2,2)
    courbe_sains.append(len(coord_sains))
    courbe_infectes.append(len(coord_infectes))
    courbe_immunises.append(0)
    courbe_deces.append(0)
    
    "2e vague"
    non_sains = []
    coord_infectes1, coord_immunises = immuniser(coord_infectes, [], p)
    coord_infectes, coord_deces = deces(coord_infectes1, [], coord_immunises, d)
    for k in range(len(coord_infectes)):
        for j in range(len(coord_sains)):
            if distance(np.array(coord_infectes)[k, :], np.array(coord_sains)[j, :]) < rayon_contamination and list(np.array(coord_sains)[j, :]) not in coord_infectes:
                coord_infectes.append(list(np.array(coord_sains)[j, :]))
                non_sains.append(list(np.array(coord_sains)[j, :]))

    coord_sains = remove_(coord_sains, non_sains)
    if coord_sains != []:
        fig.add_trace(go.Scatter(x=np.array(coord_sains)[:, 0], y=np.array(coord_sains)[:, 1], mode="markers", marker=dict(color='#636EFA'), showlegend=False),3,1)
    if coord_infectes != []:
        fig.add_trace(go.Scatter(x=np.array(coord_infectes)[:, 0], y=np.array(coord_infectes)[:, 1], mode="markers",marker=dict(color='#EF553B'), showlegend=False),3,1)
    if coord_immunises != []:
        fig.add_trace(go.Scatter(x=np.array(coord_immunises)[:, 0], y=np.array(coord_immunises)[:, 1], mode="markers",marker=dict(color='#00CC96'), showlegend=False),3,1)
    if coord_deces != []:
        fig.add_trace(go.Scatter(x=np.array(coord_deces)[:, 0], y=np.array(coord_deces)[:, 1], mode="markers",marker=dict(color='#AB63FA'), showlegend=False),3,1)
    fig.update_xaxes(showgrid=False, visible=False, row=2, col=1)
    fig.update_yaxes(showgrid=False, visible=False, row=2, col=1)
    
    "pie"
    labels = ["sains","infectés","immunisés","décédés"]
    fig.add_trace(go.Pie(values=[len(coord_sains),len(coord_infectes) ,len(coord_immunises), len(coord_deces)], labels=labels,sort=False),3,2)
    courbe_sains.append(len(coord_sains))
    courbe_infectes.append(len(coord_infectes))
    courbe_immunises.append(len(coord_immunises))
    courbe_deces.append(len(coord_deces))
    
    "3e vague"
    non_sains = []
    coord_infectes1, coord_immunises = immuniser(coord_infectes, coord_immunises, p)
    coord_infectes, coord_deces = deces(coord_infectes1, coord_deces, coord_immunises, d)
    for k in range(len(coord_infectes)):
        for j in range(len(coord_sains)):
            if distance(np.array(coord_infectes)[k, :], np.array(coord_sains)[j, :]) < rayon_contamination and list(
                    np.array(coord_sains)[j, :]) \
                    not in coord_infectes and chance_infecte(infectiosite):
                coord_infectes.append(list(np.array(coord_sains)[j, :]))
                non_sains.append(list(np.array(coord_sains)[j, :]))
    coord_sains = remove_(coord_sains, non_sains) # on enlève les individus sains qui sont maintenant infectés
    if coord_sains != []:
        fig.add_trace(go.Scatter(x=np.array(coord_sains)[:, 0], y=np.array(coord_sains)[:, 1], mode="markers", marker=dict(color='#636EFA'), showlegend=False),4,1)
    if coord_infectes != []:
        fig.add_trace(go.Scatter(x=np.array(coord_infectes)[:, 0], y=np.array(coord_infectes)[:, 1], mode="markers",marker=dict(color='#EF553B'), showlegend=False),4,1)
    if coord_immunises != []:
        fig.add_trace(go.Scatter(x=np.array(coord_immunises)[:, 0], y=np.array(coord_immunises)[:, 1], mode="markers",marker=dict(color='#00CC96'), showlegend=False),4,1)
    if coord_deces != []:
        fig.add_trace(go.Scatter(x=np.array(coord_deces)[:, 0], y=np.array(coord_deces)[:, 1], mode="markers",marker=dict(color='#AB63FA'), showlegend=False),4,1)
    fig.update_xaxes(showgrid=False, visible=False, row=3, col=1)
    fig.update_yaxes(showgrid=False, visible=False, row=3, col=1)
    
    "pie"
    labels = ["sains","infectés","immunisés","décédés"]
    fig.add_trace(go.Pie(values=[len(coord_sains),len(coord_infectes) ,len(coord_immunises), len(coord_deces)], labels=labels,sort=False),4,2)
    courbe_sains.append(len(coord_sains))
    courbe_infectes.append(len(coord_infectes))
    courbe_immunises.append(len(coord_immunises))
    courbe_deces.append(len(coord_deces))
    
    "4e vague"
    non_sains = []
    coord_infectes1, coord_immunises = immuniser(coord_infectes, coord_immunises, p)
    coord_infectes, coord_deces = deces(coord_infectes1, coord_deces, coord_immunises, d)
    for k in range(len(coord_infectes)):
        for j in range(len(coord_sains)):
            if distance(np.array(coord_infectes)[k, :], np.array(coord_sains)[j, :]) < rayon_contamination and list(
                    np.array(coord_sains)[j, :]) not in \
                    coord_infectes and chance_infecte(infectiosite):
                coord_infectes.append(list(np.array(coord_sains)[j, :]))
                non_sains.append(list(np.array(coord_sains)[j, :]))
    coord_sains = remove_(coord_sains, non_sains)
    if coord_sains != []:
        fig.add_trace(go.Scatter(x=np.array(coord_sains)[:, 0], y=np.array(coord_sains)[:, 1], mode="markers", marker=dict(color='#636EFA'), showlegend=False),5,1)
    if coord_infectes != []:
        fig.add_trace(go.Scatter(x=np.array(coord_infectes)[:, 0], y=np.array(coord_infectes)[:, 1], mode="markers",marker=dict(color='#EF553B'), showlegend=False),5,1)
    if coord_immunises != []:
        fig.add_trace(go.Scatter(x=np.array(coord_immunises)[:, 0], y=np.array(coord_immunises)[:, 1], mode="markers",marker=dict(color='#00CC96'), showlegend=False),5,1)
    if coord_deces != []:
        fig.add_trace(go.Scatter(x=np.array(coord_deces)[:, 0], y=np.array(coord_deces)[:, 1], mode="markers",marker=dict(color='#AB63FA'), showlegend=False),5,1)
    fig.update_xaxes(showgrid=False, visible=False, row=4, col=1)
    fig.update_yaxes(showgrid=False, visible=False, row=4, col=1)
    
    "pie"
    labels = ["sains","infectés","immunisés","décédés"]
    fig.add_trace(go.Pie(values=[len(coord_sains),len(coord_infectes) ,len(coord_immunises), len(coord_deces)], labels=labels,sort=False),5,2)
    courbe_sains.append(len(coord_sains))
    courbe_infectes.append(len(coord_infectes))
    courbe_immunises.append(len(coord_immunises))
    courbe_deces.append(len(coord_deces))
    
    "courbes"
    x_courbe = list(np.arange(0, len(courbe_sains)))
    # on trace les courbes finales
    fig.add_trace(go.Scatter(x=x_courbe,y=courbe_sains,marker=dict(color='#636EFA'), name="sain",showlegend=False),6,1)
    fig.add_trace(go.Scatter(x=x_courbe,y=courbe_infectes,marker=dict(color='#EF553B'), name="infecté",showlegend=False),6,1)
    fig.add_trace(go.Scatter(x=x_courbe,y=courbe_immunises,marker=dict(color='#00CC96'), name="immunisé", showlegend=False),6,1)
    fig.add_trace(go.Scatter(x=x_courbe,y=courbe_deces,marker=dict(color='#AB63FA'),name="décédé",showlegend=False),6,1)
    fig.update_traces(
        hoverinfo="name+x+y", # affichage du curseur avec la souris
        line={"width": 1.2},
        marker={"size": 6},
        mode="lines+markers",
        showlegend=False, row=2, col=1) 
    fig.update_layout(hovermode="x")
    
    plot(fig)


# affiche la vague pour laquelle le virus ne se propage plus, avec les proportions et courbes évolutives

def vague_seuil_px():

    nb_individu = 1000 # recommandé : 1000
    variance_population = 5
    rayon_contamination = 2
    infectiosite = 0.8 # proba d'être infecté
    p = 0.35 # proba d'être immunisé
    d = 0.2 # proba de décès

    # NOTE : si les courbes restent constantes, augmentez le rayon de contamination
    # si le virus est trés mortel il n'y aura pas beaucoup de propagation

    # Bleu : '#636EFA'
    # Rouge : '#EF553B'
    # Vert : '#00CC96'
    # Violet : '#AB63FA'

    # création des figures
    fig = go.Figure()
    fig = make_subplots(rows=2, cols=2,column_widths=[0.8, 0.2],row_heights=[0.5,0.5],subplot_titles=["population","",""],specs=[[{'type': 'xy'},{'type': 'domain'}],[{'type': 'xy', 'colspan' : 2},None]],horizontal_spacing = 0.05,vertical_spacing=0.05)

    # création des courbes finales
    courbe_sains = []
    courbe_infectes = []
    courbe_immunises = []
    courbe_deces = []
    courbe_removed = [] # somme des immunisés + décès

    # dataset
    x, y = make_blobs(n_samples=nb_individu, centers=2, cluster_std=variance_population)  # création du dataset
    taille_pop = len(x)

    numero_infecte_1 = rd.randint(0, taille_pop-1)  # on choisit le premier individu infecté au hasard
    coord_1er_infecte = [x[:, 0][numero_infecte_1], x[:, 1][numero_infecte_1]]  # coordonnées du 1er infecté
    courbe_sains.append(taille_pop - 1)
    courbe_infectes.append(1)
    courbe_immunises.append(0)
    courbe_deces.append(0)
    courbe_removed.append(0)

    # 1er vague
    coord_infectes = []  # cette liste sera implémentée des nouveaux cas
    coord_sains = []  # liste des cas sains
    for k in range(taille_pop):
        if [x[:, 0][k], x[:, 1][k]] == coord_1er_infecte:
            coord_infectes.append(coord_1er_infecte)
        elif distance(coord_1er_infecte, [x[:, 0][k], x[:, 1][k]]) < rayon_contamination and chance_infecte(
                infectiosite):
            coord_infectes.append([x[:, 0][k], x[:, 1][k]])
        else:
            coord_sains.append([x[:, 0][k], x[:, 1][k]])
    # actualisation des courbes finales
    courbe_sains.append(len(coord_sains))
    courbe_infectes.append(len(coord_infectes))
    courbe_immunises.append(0)
    courbe_deces.append(0)
    courbe_removed.append(0)

    # vagues 2 à la fin
    coord_immunises = []  # on initialise
    coord_deces = []
    i = 1
    while len(courbe_infectes)!=0 and  len(coord_infectes)>0.05*taille_pop : # conditions d'état stationnaire
        non_sains = []
        coord_infectes1, coord_immunises = immuniser(coord_infectes, coord_immunises, p) # on sépare immunisés et infectés
        coord_infectes, coord_deces = deces(coord_infectes1, coord_deces, coord_immunises, d) # on sépare les décès des infectés qu'ils restent

        for k in range(len(coord_infectes)):
            for j in range(len(coord_sains)):
                if distance(np.array(coord_infectes)[k, :],
                            np.array(coord_sains)[j, :]) < rayon_contamination and np.array(coord_sains)[j,:] not in np.array(coord_infectes) and chance_infecte(infectiosite):
                    coord_infectes.append(list(np.array(coord_sains)[j, :]))
                    non_sains.append(list(np.array(coord_sains)[j, :]))
        coord_sains = remove_(coord_sains, non_sains)
        # pour les courbes finales
        courbe_sains.append(len(coord_sains))
        courbe_infectes.append(len(coord_infectes))
        courbe_immunises.append(len(coord_immunises))
        courbe_deces.append(len(coord_deces))
        courbe_removed.append(len(coord_deces)+len(coord_immunises))
        i += 1 # vague suivante
        
    # on trace les individus de la dernière vague si il y en a 
    if coord_sains != []:
        fig.add_trace(go.Scatter(x=np.array(coord_sains)[:, 0], y=np.array(coord_sains)[:, 1],name="sain", mode="markers", marker=dict(color='#636EFA'), showlegend=False),1,1)
    if coord_infectes != []:
        fig.add_trace(go.Scatter(x=np.array(coord_infectes)[:, 0], y=np.array(coord_infectes)[:, 1],name="infecté", mode="markers",marker=dict(color='#EF553B'), showlegend=False),1,1)
    if coord_immunises != []:
        fig.add_trace(go.Scatter(x=np.array(coord_immunises)[:, 0], y=np.array(coord_immunises)[:, 1],name='immunisé', mode="markers",marker=dict(color='#00CC96'), showlegend=False),1,1)
    if coord_deces != []:
        fig.add_trace(go.Scatter(x=np.array(coord_deces)[:, 0], y=np.array(coord_deces)[:, 1],name="décédé", mode="markers", marker=dict(color='#AB63FA'), showlegend=False),1,1)
    
    fig.update_traces(hoverinfo="name") # affichage du curseur de la souris
    fig.update_xaxes(showgrid=False, visible=False, row=1, col=1) # on supprime les axes
    fig.update_yaxes(showgrid=False, visible=False, row=1, col=1)

    # Pie finale
    labels = ["sains","infectés","immunisés","décédés"]
    fig.add_trace(go.Pie(values=[len(coord_sains),len(coord_infectes) ,len(coord_immunises), len(coord_deces)], labels=labels, sort=False),1,2)
    
    # on trace les courbes finales
    x_courbe = list(np.arange(0, len(courbe_sains))) # abscisses, correspond aux vagues
    fig.add_trace(go.Scatter(x=x_courbe, y=courbe_sains, marker=dict(color='#636EFA'), showlegend=False, name="sains", yaxis="y",),2,1)
    fig.add_trace(go.Scatter(x=x_courbe, y=courbe_infectes,  marker=dict(color='#EF553B'), showlegend=False, name="infectés", yaxis="y2",),2,1)
    fig.add_trace(go.Scatter(x=x_courbe, y=courbe_immunises, marker=dict(color='#00CC96'), showlegend=False, name="immunisés", yaxis="y3",),2,1)
    fig.add_trace(go.Scatter(x=x_courbe, y=courbe_deces, marker=dict(color='#AB63FA'), showlegend=False, name="décédés", yaxis="y4",),2,1)
    fig.add_trace(go.Scatter(x=x_courbe, y=courbe_removed, marker=dict(color='#000000'), showlegend=False, name="removed", yaxis="y5",),2,1)
    fig.update_xaxes(title_text="vague", row=2, col=1) # nom abscisses
    fig.update_yaxes(title_text="nombre d'individus", row=2, col=1) # nom ordonnées
    fig.add_annotation(text="Maximum d'infectés", x=courbe_infectes.index(max(courbe_infectes)), # ajouter un texte avec une flèche au pic d'infectés
                   y=max(courbe_infectes)+0.03*taille_pop, arrowhead=1, showarrow=True,row=2,col=1)
    fig.update_traces(
        hoverinfo="name+x+y", # affichage du curseur de la souris sur le point
        line={"width": 1.2},
        marker={"size": 6},
        mode="lines+markers",
        showlegend=False, row=2, col=1)
    fig.update_layout(hovermode="x")
    fig.update_layout(title_text="simulation virus") # titre du plot
    fig.update_layout(title_font_color='#EF553B',) # couleur du titre
    
    plot(fig)






