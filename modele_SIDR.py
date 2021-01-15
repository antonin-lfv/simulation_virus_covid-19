''' modélisation de la propagation d'un virus '''

""" importation """

from typing import List, Any
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
import random as rd
import time
from scipy.spatial import distance
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot  # pour travailler en offline!
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np

""" I) création du dataset """

x, y = make_blobs(n_samples=1000, centers=2, cluster_std=5, shuffle=True)
plt.scatter(x[:, 0], x[:, 1], c='dodgerblue')
plt.title('dataset')
plt.show()

def distance_e(x, y):  # distance entre 2 points du plan cartésien
    return distance.euclidean([x[0],x[1]],[y[0],y[1]])

def first_infect(pop,infec):
    l = []
    for i in range(infec):
        num = rd.randint(0, pop - 1)
        while num in l:
            num = rd.randint(0, pop - 1)
        l.append(num)
    return l

def remove_(a, l): # enlever les éléments de l dans a
    for i in range(len(l)):
        a.remove(l[i])
    return a

def chance_infecte(p):  # return True si il devient infecté avec une proba p
    proba = int(p * 100)
    return rd.randint(0, 100) < proba

def immuniser(l, l2, p):  # l: infectés; l2: immunisés précédents
    drop = 0
    for i in range(len(l)):
        proba = int(p * 100)
        if rd.randint(0, 100) < proba:
            l2.append(l[i-drop])
            l.remove(l[i-drop])
            drop+=1
    return l, l2

def deces(l, l2, l3, p):  # l: infectés; l2: décès précédents; l3: immunisés
    l_p = l[:]  # création d'une copie pour éviter d'erreur d'indice
    for i in range(len(l_p)):
        proba = int(p * 100)
        if rd.randint(0, 100) < proba and l_p[i] not in l3:
            l2.append(l_p[i])
            l.remove(l_p[i])
    return l, l2

""" II) choix de la personne infectée en premier """

taille_pop = len(x)

numero_infecte_1 = rd.randint(0, taille_pop)
coord_1er_infecte = [x[:, 0][numero_infecte_1], x[:, 1][numero_infecte_1]]

# afficher l'individu infecté dans la pop :

plt.scatter(x[:, 0], x[:, 1], c='dodgerblue')
plt.scatter(x[:, 0][numero_infecte_1], x[:, 1][numero_infecte_1], c='r')
plt.scatter(x[:, 0][numero_infecte_1], x[:, 1][numero_infecte_1], c='r')  # , s=3300, alpha=0.2)
plt.title('1er individu contaminé')
plt.show()

""" III) 1er contaminations """

coord_infectes = []
coord_sains = []

# contamination

for k in range(taille_pop):
    if distance_e(coord_1er_infecte, [x[:, 0][k], x[:, 1][k]]) < 0.5:
        plt.scatter(x[:, 0][k], x[:, 1][k], c='firebrick')
        coord_infectes.append([x[:, 0][k], x[:, 1][k]])
    else:
        plt.scatter(x[:, 0][k], x[:, 1][k], c='dodgerblue')
        coord_sains.append([x[:, 0][k], x[:, 1][k]])
    plt.scatter(x[:, 0][numero_infecte_1], x[:, 1][numero_infecte_1], c='r')
    plt.title('1er vague de contamination')
    plt.show()

plt.clf()
plt.pie([len(coord_infectes), len(coord_sains)], labels=('infectés', 'sains'), colors=['firebrick', 'dodgerblue'],
        shadow=True, autopct='%1.1f%%')
plt.title('1er vague de contamination')
plt.show()

""" IV) 2e contamination """

non_sains = []
coord_infectes1, coord_immunises = immuniser(coord_infectes, [], 0.80)
coord_infectes, coord_deces = deces(coord_infectes1, [], coord_immunises, 0.5)
for k in range(len(coord_infectes)):
    for j in range(len(coord_sains)):
        if distance_e(np.array(coord_infectes)[k, :], np.array(coord_sains)[j, :]) < 0.5 and list(
                np.array(coord_sains)[j, :]) not in coord_infectes:
            coord_infectes.append(list(np.array(coord_sains)[j, :]))
            non_sains.append(list(np.array(coord_sains)[j, :]))

coord_sains = remove_(coord_sains, non_sains)
if coord_sains != []:
    plt.scatter(np.array(coord_sains)[:, 0], np.array(coord_sains)[:, 1], c='dodgerblue')
if coord_infectes != []:
    plt.scatter(np.array(coord_infectes)[:, 0], np.array(coord_infectes)[:, 1], c='firebrick')
if coord_immunises != []:
    plt.scatter(np.array(coord_immunises)[:, 0], np.array(coord_immunises)[:, 1], c='g')
if coord_deces != []:
    plt.scatter(np.array(coord_deces)[:, 0], np.array(coord_deces)[:, 1], c='k')
plt.title('2e vague de contamination')
plt.show()

plt.clf()
plt.pie([len(coord_infectes), len(coord_sains), len(coord_immunises), len(coord_deces)],
        colors=['firebrick', 'dodgerblue', 'g', 'dimgrey'], labels=('infectés', 'sains', 'immunisés', 'décès'),
        shadow=True, autopct='%1.1f%%')
plt.title('2er vague de contamination')
plt.show()

""" 3e vague """

non_sains = []
coord_infectes, coord_immunises = immuniser(coord_infectes, coord_immunises, 0.80)
coord_infectes, coord_deces = deces(coord_infectes, coord_deces, coord_immunises, 0.4)
for k in range(len(coord_infectes)):
    for j in range(len(coord_sains)):
        if distance_e(np.array(coord_infectes)[k, :], np.array(coord_sains)[j, :]) < 0.5 and np.array(coord_sains)[j,
                                                                                           :] not in np.array(
            coord_infectes):
            coord_infectes.append(list(np.array(coord_sains)[j, :]))
            non_sains.append(list(np.array(coord_sains)[j, :]))

coord_sains = remove_(coord_sains, non_sains)
if coord_sains != []:
    plt.scatter(np.array(coord_sains)[:, 0], np.array(coord_sains)[:, 1], c='dodgerblue')
if coord_infectes != []:
    plt.scatter(np.array(coord_infectes)[:, 0], np.array(coord_infectes)[:, 1], c='firebrick')
if coord_immunises != []:
    plt.scatter(np.array(coord_immunises)[:, 0], np.array(coord_immunises)[:, 1], c='g')
if coord_deces != []:
    plt.scatter(np.array(coord_deces)[:, 0], np.array(coord_deces)[:, 1], c='k')
plt.title('3e vague de contamination')
plt.show()

plt.clf()
plt.pie([len(coord_infectes), len(coord_sains), len(coord_immunises), len(coord_deces)],
        colors=['firebrick', 'dodgerblue', 'g', 'dimgrey'], labels=('infectés', 'sains', 'immunisés', 'décès'),
        shadow=True, autopct='%1.1f%%')
plt.title('3e vague de contamination')
plt.show()

""" résumé des 4 premières vagues """


def virus(nb_individu, variance_population, rayon_contamination, infectiosite, p, d):
    # recommandé pour petite population :
    # nb_individu = 150, var_population = 150, rayon_contamination = 0.9, infectiosite = 0.25, p = 0.5, d = 0.3
    # recommandé pour grosse population :
    # nb_individu = 1000, var_population = 100, rayon_contamination = 70, infectiosite = 0.6, p = 0.5, d = 0.3
    # variance population correspond à l'espacement moyen des individus
    # infectiosite correspond à la proba d'un infecté de transmettre le virus à l'interieur de son rayon
    # p correspond à la proba d'un infecté de devenir immunisé
    # d correspond à la proba d'un infecté de déceder

    x, y = make_blobs(n_samples=nb_individu, centers=1, cluster_std=variance_population)  # création du dataset
    ax = plt.figure(figsize=(10, 8))
    taille_pop = len(x)

    # création des figures
    ax1 = ax.add_subplot(6, 2, 1)
    ax2 = ax.add_subplot(6, 2, 3)
    ax3 = ax.add_subplot(6, 2, 5)
    ax4 = ax.add_subplot(6, 2, 2)
    ax5 = ax.add_subplot(6, 2, 4)
    ax6 = ax.add_subplot(6, 2, 6)
    ax7 = ax.add_subplot(6, 2, 7)
    ax8 = ax.add_subplot(6, 2, 8)
    ax9 = ax.add_subplot(6, 2, 9)
    ax10 = ax.add_subplot(6, 2, 10)
    ax11 = ax.add_subplot(6, 2, 11)
    ax12 = ax.add_subplot(6, 2, 12)

    # création des courbes finales
    courbe_sains = []
    courbe_infectes = []
    courbe_immunises = []
    courbe_deces = []

    # Afficher 1er individu avec pourcentage infectés/sains
    numero_infecte_1 = rd.randint(0, taille_pop)  # on choisit le premier individu infecté au hasard
    coord_1er_infecte = [x[:, 0][numero_infecte_1], x[:, 1][numero_infecte_1]]  # coordonnées du 1er infecté
    ax1.scatter(x[:, 0], x[:, 1], c='dodgerblue')
    ax1.scatter(x[:, 0][numero_infecte_1], x[:, 1][numero_infecte_1], c='firebrick')
    ax1.set_title('1er individu', fontsize=8)
    ax1.axis('off')
    ax4.pie([1, taille_pop - 1], shadow=True, autopct='%1.1f%%', colors=['firebrick', 'dodgerblue'], pctdistance=1.5,
            counterclock=False)
    courbe_sains.append(taille_pop - 1)
    courbe_infectes.append(1)
    courbe_immunises.append(0)
    courbe_deces.append(0)

    # Afficher 1er vague avec pourcentage infectés/sains
    coord_infectes = []  # cette liste sera implémentée des nouveaux cas
    coord_sains = []  # liste des cas sains
    for k in range(taille_pop):
        if [x[:, 0][k], x[:, 1][k]] == coord_1er_infecte:
            coord_infectes.append(coord_1er_infecte)
        elif distance_e(coord_1er_infecte, [x[:, 0][k], x[:, 1][k]]) < rayon_contamination and chance_infecte(
                infectiosite):
            ax2.scatter(x[:, 0][k], x[:, 1][k], c='firebrick')
            coord_infectes.append([x[:, 0][k], x[:, 1][k]])
        else:
            ax2.scatter(x[:, 0][k], x[:, 1][k], c='dodgerblue')
            coord_sains.append([x[:, 0][k], x[:, 1][k]])
        ax2.scatter(x[:, 0][numero_infecte_1], x[:, 1][numero_infecte_1], c='firebrick')
        ax2.set_title('1er vague', fontsize=8)
    ax2.axis('off')
    ax5.pie([len(coord_infectes), len(coord_sains)], shadow=True, autopct='%1.1f%%',
            colors=['firebrick', 'dodgerblue'], pctdistance=1.5, counterclock=False)
    courbe_sains.append(len(coord_sains))
    courbe_infectes.append(len(coord_infectes))
    courbe_immunises.append(0)
    courbe_deces.append(0)

    # Afficher 2e vague avec pourcentage infectés/sains
    non_sains = []
    coord_infectes1, coord_immunises = immuniser(coord_infectes, [], p)
    coord_infectes, coord_deces = deces(coord_infectes1, [], coord_immunises, d)
    for k in range(len(coord_infectes)):
        for j in range(len(coord_sains)):
            if distance_e(np.array(coord_infectes)[k, :], np.array(coord_sains)[j, :]) < rayon_contamination and \
                    list(np.array(coord_sains)[j, :]) not in coord_infectes:
                coord_infectes.append(list(np.array(coord_sains)[j, :]))
                non_sains.append(list(np.array(coord_sains)[j, :]))

    coord_sains = remove_(coord_sains, non_sains)
    if coord_sains != []:
        ax3.scatter(np.array(coord_sains)[:, 0], np.array(coord_sains)[:, 1], c='dodgerblue')
    if coord_infectes != []:
        ax3.scatter(np.array(coord_infectes)[:, 0], np.array(coord_infectes)[:, 1], c='firebrick')
    if coord_immunises != []:
        ax3.scatter(np.array(coord_immunises)[:, 0], np.array(coord_immunises)[:, 1], c='g')
    if coord_deces != []:
        ax3.scatter(np.array(coord_deces)[:, 0], np.array(coord_deces)[:, 1], c='k')
    ax3.set_title('2e vague', fontsize=8)
    ax3.axis('off')
    ax6.pie([len(coord_infectes), len(coord_sains), len(coord_immunises), len(coord_deces)], shadow=True,
            autopct='%1.1f%%',
            colors=['firebrick', 'dodgerblue', 'g', 'dimgrey'], pctdistance=1.5, counterclock=False)
    courbe_sains.append(len(coord_sains))
    courbe_infectes.append(len(coord_infectes))
    courbe_immunises.append(len(coord_immunises))
    courbe_deces.append(len(coord_deces))

    # Afficher 3e vague avec pourcentage infectés/sains
    non_sains = []
    coord_infectes1, coord_immunises = immuniser(coord_infectes, coord_immunises, p)
    coord_infectes, coord_deces = deces(coord_infectes1, coord_deces, coord_immunises, d)
    for k in range(len(coord_infectes)):
        for j in range(len(coord_sains)):
            if distance_e(np.array(coord_infectes)[k, :], np.array(coord_sains)[j, :]) < rayon_contamination and list(
                    np.array(coord_sains)[j, :]) \
                    not in coord_infectes and chance_infecte(infectiosite):
                coord_infectes.append(list(np.array(coord_sains)[j, :]))
                non_sains.append(list(np.array(coord_sains)[j, :]))
    coord_sains = remove_(coord_sains, non_sains)
    if coord_sains != []:
        ax7.scatter(np.array(coord_sains)[:, 0], np.array(coord_sains)[:, 1], c='dodgerblue')
    if coord_infectes != []:
        ax7.scatter(np.array(coord_infectes)[:, 0], np.array(coord_infectes)[:, 1], c='firebrick')
    if coord_immunises != []:
        ax7.scatter(np.array(coord_immunises)[:, 0], np.array(coord_immunises)[:, 1], c='g')
    if coord_deces != []:
        ax7.scatter(np.array(coord_deces)[:, 0], np.array(coord_deces)[:, 1], c='k')
    ax7.set_title('3e vague', fontsize=8)
    ax7.axis('off')
    ax8.pie([len(coord_infectes), len(coord_sains), len(coord_immunises), len(coord_deces)], shadow=True,
            autopct='%1.1f%%',
            colors=['firebrick', 'dodgerblue', 'g', 'dimgrey'], pctdistance=1, counterclock=False)
    courbe_sains.append(len(coord_sains))
    courbe_infectes.append(len(coord_infectes))
    courbe_immunises.append(len(coord_immunises))
    courbe_deces.append(len(coord_deces))

    # Afficher 4e vague avec pourcentage infectés/sains
    non_sains = []
    coord_infectes1, coord_immunises = immuniser(coord_infectes, coord_immunises, p)
    coord_infectes, coord_deces = deces(coord_infectes1, coord_deces, coord_immunises, d)
    for k in range(len(coord_infectes)):
        for j in range(len(coord_sains)):
            if distance_e(np.array(coord_infectes)[k, :], np.array(coord_sains)[j, :]) < rayon_contamination and list(
                    np.array(coord_sains)[j, :]) not in \
                    coord_infectes and chance_infecte(infectiosite):
                coord_infectes.append(list(np.array(coord_sains)[j, :]))
                non_sains.append(list(np.array(coord_sains)[j, :]))
    coord_sains = remove_(coord_sains, non_sains)
    if coord_sains != []:
        ax9.scatter(np.array(coord_sains)[:, 0], np.array(coord_sains)[:, 1], c='dodgerblue')
    if coord_infectes != []:
        ax9.scatter(np.array(coord_infectes)[:, 0], np.array(coord_infectes)[:, 1], c='firebrick')
    if coord_immunises != []:
        ax9.scatter(np.array(coord_immunises)[:, 0], np.array(coord_immunises)[:, 1], c='g')
    if coord_deces != []:
        ax9.scatter(np.array(coord_deces)[:, 0], np.array(coord_deces)[:, 1], c='k', alpha=0.7)
    ax9.set_title('4e vague', fontsize=8)
    ax9.axis('off')
    ax10.pie([len(coord_infectes), len(coord_sains), len(coord_immunises), len(coord_deces)], shadow=True,
             autopct='%1.1f%%',
             colors=['firebrick', 'dodgerblue', 'g', 'dimgrey'], pctdistance=1, counterclock=False)
    courbe_sains.append(len(coord_sains))
    courbe_infectes.append(len(coord_infectes))
    courbe_immunises.append(len(coord_immunises))
    courbe_deces.append(len(coord_deces))

    ax11.axis('off')
    ax12.axis('off')
    textstr = '\n'.join((
        r'$nombre \ individu=%.2f$' % (nb_individu,),
        r'$variance \ population=%.2f$' % (variance_population,),
        r'$rayon \ de \ contamination=%.2f$' % (rayon_contamination,),
        r'$infectiosité=%.2f$' % (infectiosite,),
        r'$proba \ dêtre \ immunisé=%.2f$' % (p,),
        r'$proba \ de \ décès=%.2f$' % (d,)))
    ax.text(0.12, 0.04, textstr, horizontalalignment='left', verticalalignment='bottom', fontsize=14,
            bbox=dict(boxstyle='round', facecolor='dodgerblue', alpha=0.6))
    plt.figure()
    x_courbe = list(np.arange(0, len(courbe_sains)))
    plt.plot(x_courbe, courbe_sains, label='sains', c='dodgerblue')
    plt.plot(x_courbe, courbe_infectes, label='infectés', c='firebrick')
    plt.plot(x_courbe, courbe_immunises, label='immunisés', c='g')
    plt.plot(x_courbe, courbe_deces, label='décès', c='k')
    plt.legend()
    plt.show()


""" V) Avec n vagues """


def nieme_vague(n, nb_individu, var_population, rayon_contamination, infectiosite, p, d):
    if n < 2:
        return ('error, n must be >= 2')
    if nb_individu <= 0 or var_population <= 0 or rayon_contamination <= 0:
        return ('error, nb_individu and var_population and rayon_contamination must be > 0')
    if infectiosite < 0 or infectiosite > 1:
        return ('error, infectiosité must be in [0,1]')
    if p < 0 or p > 1:
        return ('error, p must be in [0,1]')
    if d < 0 or p > 1:
        return ('error, d must be in [0,1]')

    # on obtient ici le resultat de la n-ieme vague
    # recommandé :
    # n = 7; nb_individu = 150, var_population = 3, rayon_contamination = 3, infectiosite =0.6; p=0.4; d=0.3
    # variance population correspond à l'espacement moyen des individus
    # infectiosité correspond à la proba d'un infectés de transmettre le virus
    # p est la proba de devenir immunisé

    # création des figures
    ax = plt.figure()
    ax1 = ax.add_subplot(1, 2, 1)
    ax2 = ax.add_subplot(1, 2, 2)

    # création des courbes finales
    courbe_sains = []
    courbe_infectes = []
    courbe_immunises = []
    courbe_deces = []

    x, y = make_blobs(n_samples=nb_individu, centers=1, cluster_std=var_population)  # création du dataset
    taille_pop = len(x)

    numero_infecte_1 = rd.randint(0, taille_pop)  # on choisit le premier individu infecté au hasard
    coord_1er_infecte = [x[:, 0][numero_infecte_1], x[:, 1][numero_infecte_1]]  # coordonnées du 1er infecté
    courbe_sains.append(taille_pop - 1)
    courbe_infectes.append(1)
    courbe_immunises.append(0)
    courbe_deces.append(0)

    # 1er vague
    coord_infectes = []  # cette liste sera implémentée des nouveaux cas
    coord_sains = []  # liste des cas sains
    for k in range(taille_pop):
        if [x[:, 0][k], x[:, 1][k]] == coord_1er_infecte:
            coord_infectes.append(coord_1er_infecte)
        elif distance_e(coord_1er_infecte, [x[:, 0][k], x[:, 1][k]]) < rayon_contamination and chance_infecte(
                infectiosite):
            coord_infectes.append([x[:, 0][k], x[:, 1][k]])
        else:
            coord_sains.append([x[:, 0][k], x[:, 1][k]])
    courbe_sains.append(len(coord_sains))
    courbe_infectes.append(len(coord_infectes))
    courbe_immunises.append(0)
    courbe_deces.append(0)

    # vagues 2 à n
    coord_immunises = []  # on initialise
    coord_deces = []
    for i in range(n - 2):
        non_sains = []
        coord_infectes1, coord_immunises = immuniser(coord_infectes, coord_immunises, p)
        coord_infectes, coord_deces = deces(coord_infectes1, coord_deces, coord_immunises, d)
        for k in range(len(coord_infectes)):
            for j in range(len(coord_sains)):
                if distance_e(np.array(coord_infectes)[k, :],
                            np.array(coord_sains)[j, :]) < rayon_contamination and np.array(coord_sains)[j,
                                                                                   :] not in np.array(
                    coord_infectes) and chance_infecte(infectiosite):
                    coord_infectes.append(list(np.array(coord_sains)[j, :]))
                    non_sains.append(list(np.array(coord_sains)[j, :]))
        coord_sains = remove_(coord_sains, non_sains)
        courbe_sains.append(len(coord_sains))
        courbe_infectes.append(len(coord_infectes))
        courbe_immunises.append(len(coord_immunises))
        courbe_deces.append(len(coord_deces))
    if coord_sains != []:
        ax1.scatter(np.array(coord_sains)[:, 0], np.array(coord_sains)[:, 1], c='dodgerblue')
    if coord_infectes != []:
        ax1.scatter(np.array(coord_infectes)[:, 0], np.array(coord_infectes)[:, 1], c='firebrick')
    if coord_immunises != []:
        ax1.scatter(np.array(coord_immunises)[:, 0], np.array(coord_immunises)[:, 1], c='g')
    if coord_deces != []:
        ax1.scatter(np.array(coord_deces)[:, 0], np.array(coord_deces)[:, 1], c='k')
    ax1.set_title('n-ième vague', fontsize=8)
    ax1.axis('off')
    ax2.pie([len(coord_infectes), len(coord_sains), len(coord_immunises), len(coord_deces)],
            colors=['firebrick', 'dodgerblue', 'g', 'dimgrey'], labels=('infectés', 'sains', 'immunisés', 'décès'),
            shadow=True, autopct='%1.1f%%')
    plt.figure()
    x_courbe = list(np.arange(0, len(courbe_sains)))
    plt.plot(x_courbe, courbe_sains, label='sains', c='dodgerblue')
    plt.plot(x_courbe, courbe_infectes, label='infectés', c='firebrick')
    plt.plot(x_courbe, courbe_immunises, label='immunisés', c='g')
    plt.plot(x_courbe, courbe_deces, label='décès', c='k')
    plt.legend()
    plt.show()


""" VI) animation """


def n_vagues_anim(n, nb_individu, var_population, rayon_contamination, infectiosite, p, d):
    x, y = make_blobs(n_samples=nb_individu, centers=1, cluster_std=var_population)  # création du dataset
    taille_pop = len(x)

    # création des courbes finales
    courbe_sains = []
    courbe_infectes = []
    courbe_immunises = []
    courbe_deces = []

    plt.figure()
    numero_infecte_1 = rd.randint(0, taille_pop)  # on choisit le premier individu infecté au hasard
    coord_1er_infecte = [x[:, 0][numero_infecte_1], x[:, 1][numero_infecte_1]]  # coordonnées du 1er infecté
    plt.scatter(x[:, 0], x[:, 1], c='dodgerblue')
    plt.scatter(x[:, 0][numero_infecte_1], x[:, 1][numero_infecte_1], c='firebrick')
    plt.axis('off')
    courbe_sains.append(taille_pop - 1)
    courbe_infectes.append(1)
    courbe_immunises.append(0)
    courbe_deces.append(0)

    # vague 1
    plt.figure()
    coord_infectes = []  # cette liste sera implémentée des nouveaux cas
    coord_sains = []  # liste des cas sains
    for k in range(taille_pop):
        if distance_e(coord_1er_infecte, [x[:, 0][k], x[:, 1][k]]) < rayon_contamination and chance_infecte(infectiosite):
            plt.scatter(x[:, 0][k], x[:, 1][k], c='firebrick')
            coord_infectes.append([x[:, 0][k], x[:, 1][k]])
        else:
            plt.scatter(x[:, 0][k], x[:, 1][k], c='dodgerblue')
            coord_sains.append([x[:, 0][k], x[:, 1][k]])
        plt.scatter(x[:, 0][numero_infecte_1], x[:, 1][numero_infecte_1], c='firebrick')
        plt.title('1er vague')
    plt.axis('off')
    courbe_sains.append(len(coord_sains))
    courbe_infectes.append(len(coord_infectes))
    courbe_immunises.append(0)
    courbe_deces.append(0)

    # vagues 2 à n
    coord_immunises = []  # on initialise
    coord_deces = []
    for i in range(n - 2):
        plt.figure()
        non_sains = []
        coord_infectes, coord_immunises = immuniser(coord_infectes, coord_immunises, p)
        coord_infectes, coord_deces = deces(coord_infectes, coord_deces, coord_immunises, d)
        for k in range(len(coord_infectes)):
            for j in range(len(coord_sains)):
                if distance_e(np.array(coord_infectes)[k, :],
                            np.array(coord_sains)[j, :]) < rayon_contamination and np.array(coord_sains)[j,
                                                                                   :] not in np.array(
                    coord_infectes) and chance_infecte(infectiosite):
                    coord_infectes.append(list(np.array(coord_sains)[j, :]))
                    non_sains.append(list(np.array(coord_sains)[j, :]))
        coord_sains = remove_(coord_sains, non_sains)
        if coord_sains != []:
            plt.scatter(np.array(coord_sains)[:, 0], np.array(coord_sains)[:, 1], c='dodgerblue')
        if coord_infectes != []:
            plt.scatter(np.array(coord_infectes)[:, 0], np.array(coord_infectes)[:, 1], c='firebrick')
        if coord_immunises != []:
            plt.scatter(np.array(coord_immunises)[:, 0], np.array(coord_immunises)[:, 1], c='g')
        if coord_deces != []:
            plt.scatter(np.array(coord_deces)[:, 0], np.array(coord_deces)[:, 1], c='k', alpha=0.7)
        plt.axis('off')
        courbe_sains.append(len(coord_sains))
        courbe_infectes.append(len(coord_infectes))
        courbe_immunises.append(len(coord_immunises))
        courbe_deces.append(len(coord_deces))
    plt.figure()
    x_courbe = list(np.arange(0, len(courbe_sains)))
    plt.plot(x_courbe, courbe_sains, label='sains', c='dodgerblue')
    plt.plot(x_courbe, courbe_infectes, label='infectés', c='firebrick')
    plt.plot(x_courbe, courbe_immunises, label='immunisés', c='g')
    plt.plot(x_courbe, courbe_deces, label='décès', c='k')
    plt.legend()
    plt.show()


""" VII) afficher la vague tq on ai un état stationnaire """


def vague_seuil(nb_individu, var_population, rayon_contamination, infectiosite, p, d):
    # recommandé :
    # nb_individu=500; var_population=2; rayon_contamination=2,infectiosité=0.7;p=0.4;d=0.3
    # cette fonction affiche la vague ou le nombre de personnes saines devient constant ou que le nombre d'infectés est nul
    # c'est à dire que le virus ne circule plus
    # NOTE : si les courbes restent constantes, augmentez le rayon de contamination
    # si le virus est trés mortel il n'y aura pas beaucoup de propagation

    if nb_individu < 10 or var_population <= 0 or rayon_contamination <= 0:
        return 'error, nb_individu and var_population and rayon_contamination must be >=10 and > 0'
    if infectiosite < 0 or infectiosite > 1:
        return 'error, infectiosité must be in [0,1]'
    if p < 0 or p > 1:
        return 'error, p must be in [0,1]'
    if d < 0 or p > 1:
        return 'error, d must be in [0,1]'

    # création des figures
    ax = plt.figure()
    ax1 = ax.add_subplot(1, 2, 1)
    ax2 = ax.add_subplot(1, 2, 2)

    # création des courbes finales
    courbe_sains = []
    courbe_infectes = []
    courbe_immunises = []
    courbe_deces = []

    # dataset
    x, y = make_blobs(n_samples=nb_individu, centers=3, cluster_std=var_population)  # création du dataset
    taille_pop = len(x)

    numero_infecte_1 = rd.randint(0, taille_pop)  # on choisit le premier individu infecté au hasard
    coord_1er_infecte = [x[:, 0][numero_infecte_1], x[:, 1][numero_infecte_1]]  # coordonnées du 1er infecté
    courbe_sains.append(taille_pop - 1)
    courbe_infectes.append(1)
    courbe_immunises.append(0)
    courbe_deces.append(0)

    # 1er vague
    coord_infectes = []  # cette liste sera implémentée des nouveaux cas
    coord_sains = []  # liste des cas sains
    for k in range(taille_pop):
        if [x[:, 0][k], x[:, 1][k]] == coord_1er_infecte:
            coord_infectes.append(coord_1er_infecte)
        elif distance_e(coord_1er_infecte, [x[:, 0][k], x[:, 1][k]]) < rayon_contamination and chance_infecte(
                infectiosite):
            coord_infectes.append([x[:, 0][k], x[:, 1][k]])
        else:
            coord_sains.append([x[:, 0][k], x[:, 1][k]])
    courbe_sains.append(len(coord_sains))
    courbe_infectes.append(len(coord_infectes))
    courbe_immunises.append(0)
    courbe_deces.append(0)

    # vagues 2 à n
    coord_immunises = []  # on initialise
    coord_deces = []
    # for i in range(n - 2):
    i = 1
    while len(courbe_infectes) != 0 and courbe_sains[i - 1] > courbe_sains[i]:
        non_sains = []
        coord_infectes1, coord_immunises = immuniser(coord_infectes, coord_immunises, p)
        coord_infectes, coord_deces = deces(coord_infectes1, coord_deces, coord_immunises, d)
        for k in range(len(coord_infectes)):
            for j in range(len(coord_sains)):
                if distance_e(np.array(coord_infectes)[k, :],
                            np.array(coord_sains)[j, :]) < rayon_contamination and np.array(coord_sains)[j,
                                                                                   :] not in np.array(
                    coord_infectes) and chance_infecte(infectiosite):
                    coord_infectes.append(list(np.array(coord_sains)[j, :]))
                    non_sains.append(list(np.array(coord_sains)[j, :]))
        coord_sains = remove_(coord_sains, non_sains)
        # pour les courbes finales
        courbe_sains.append(len(coord_sains))
        courbe_infectes.append(len(coord_infectes))
        courbe_immunises.append(len(coord_immunises))
        courbe_deces.append(len(coord_deces))
        i += 1  # vague suivante
    if coord_sains != []:
        ax1.scatter(np.array(coord_sains)[:, 0], np.array(coord_sains)[:, 1], c='dodgerblue')
    if coord_infectes != []:
        ax1.scatter(np.array(coord_infectes)[:, 0], np.array(coord_infectes)[:, 1], c='firebrick')
    if coord_immunises != []:
        ax1.scatter(np.array(coord_immunises)[:, 0], np.array(coord_immunises)[:, 1], c='g')
    if coord_deces != []:
        ax1.scatter(np.array(coord_deces)[:, 0], np.array(coord_deces)[:, 1], c='k')
    titre = str(i) + '-ième vague'
    ax1.set_title(titre, fontsize=8)
    ax1.axis('off')
    ax2.pie([len(coord_infectes), len(coord_sains), len(coord_immunises), len(coord_deces)],
            colors=['firebrick', 'dodgerblue', 'g', 'dimgrey'], labels=('infectés', 'sains', 'immunisés', 'décès'),
            shadow=True, autopct='%1.1f%%')
    plt.figure()
    x_courbe = list(np.arange(0, len(courbe_sains)))
    plt.plot(x_courbe, courbe_sains, label='sains', c='dodgerblue')
    plt.plot(x_courbe, courbe_infectes, label='infectés', c='firebrick')
    plt.plot(x_courbe, courbe_immunises, label='immunisés', c='g')
    plt.plot(x_courbe, courbe_deces, label='décès', c='k')
    plt.legend()
    print(i, 'ième vague')
    plt.show()








""" AVEC PLOTLY """

x, y = make_blobs(n_samples=1000, centers=2, cluster_std=5, shuffle=True)
fig = go.Figure()
fig.add_trace(go.Scatter(x=x[:, 0], y=x[:, 1], mode="markers", marker=dict(color="Blue")))
plot(fig)

nb_individu = 1000
variance_population = 5
rayon_contamination = 1.2
infectiosite = 0.7
p = 0.4
d = 0.3
taille_pop = len(x)

# création des courbes finales
courbe_sains = []
courbe_infectes = []
courbe_immunises = []
courbe_deces = []

""" II) choix de la personne infectée en premier """

numero_infecte_1 = rd.randint(0, taille_pop)
coord_1er_infecte = [x[:, 0][numero_infecte_1], x[:, 1][numero_infecte_1]]

# afficher l'individu infecté dans la pop :

fig = go.Figure()
fig.add_trace(go.Scatter(x=x[:, 0], y=x[:, 1], mode="markers", marker=dict(color="Blue")))
fig.add_trace(go.Scatter(x=[x[:, 0][numero_infecte_1]], y=[x[:, 1][numero_infecte_1]], mode="markers",
                         marker=dict(color="DarkOrange")))
fig.update_layout(title_text="1er infecté", showlegend=False, )
plot(fig)

fig = go.Figure()
labels = ["sains", "infectés", "immunisés", "décédés"]
fig.add_trace(go.Pie(values=[taille_pop - 1, 1], labels=labels, ))
fig.update_layout(title_text="Proportions population")
plot(fig)

courbe_sains.append(taille_pop - 1)
courbe_infectes.append(1)
courbe_immunises.append(0)
courbe_deces.append(0)

# subplots
fig = go.Figure()
fig = make_subplots(rows=2, cols=1, subplot_titles=("population", ""), specs=[[{'type': 'xy'}], [{'type': 'domain'}]])
fig.add_trace(go.Scatter(x=x[:, 0], y=x[:, 1], mode="markers", marker=dict(color="Blue"), showlegend=False), 1, 1)
fig.add_trace(go.Scatter(x=[x[:, 0][numero_infecte_1]], y=[x[:, 1][numero_infecte_1]], mode="markers",
                         marker=dict(color="DarkOrange"), showlegend=False), 1, 1)
fig.update_layout(template="simple_white")
labels = ["sains", "infectés", "immunisés", "décédés"]
fig.add_trace(go.Pie(labels=labels, values=[taille_pop - 1, 1, 0, 0], sort=False), 2, 1)
fig.update_xaxes(showgrid=False, visible=False, row=1, col=1)
fig.update_xaxes(showgrid=False, visible=False, row=2, col=1)
fig.update_yaxes(showgrid=False, visible=False, row=1, col=1)
fig.update_yaxes(showgrid=False, visible=False, row=2, col=1)
plot(fig)

""" III) 1er vague """

# Afficher 1er vague avec pourcentage infectés/sains
coord_infectes = []  # cette liste sera implémentée des nouveaux cas
coord_sains = []  # liste des cas sains
fig = go.Figure()
for k in range(taille_pop):
    if [x[:, 0][k], x[:, 1][k]] == coord_1er_infecte:
        coord_infectes.append(coord_1er_infecte)
    elif distance_e(coord_1er_infecte, [x[:, 0][k], x[:, 1][k]]) < rayon_contamination and chance_infecte(infectiosite):
        fig.add_trace(go.Scatter(x=[x[:, 0][k]], y=[x[:, 1][k]], mode="markers", marker=dict(color="DarkOrange"),
                                 showlegend=False))
        coord_infectes.append([x[:, 0][k], x[:, 1][k]])
    else:
        fig.add_trace(
            go.Scatter(x=[x[:, 0][k]], y=[x[:, 1][k]], mode="markers", marker=dict(color="Blue"), showlegend=False))
        coord_sains.append([x[:, 0][k], x[:, 1][k]])
        fig.add_trace(go.Scatter(x=[x[:, 0][numero_infecte_1]], y=[x[:, 1][numero_infecte_1]], mode="markers",
                                 marker=dict(color="DarkOrange"), showlegend=False))
plot(fig)

fig = go.Figure()
labels = ["sains", "infectés", "immunisés", "décédés"]
fig.add_trace(go.Pie(values=[len(coord_sains), len(coord_infectes), 0, 0], labels=labels, sort=False))
fig.update_layout(title_text="Proportions population")
plot(fig)

courbe_sains.append(len(coord_sains))
courbe_infectes.append(len(coord_infectes))
courbe_immunises.append(0)
courbe_deces.append(0)

# Afficher 2e vague avec pourcentage infectés/sains
non_sains = []
coord_infectes1, coord_immunises = immuniser(coord_infectes, [], p)
coord_infectes, coord_deces = deces(coord_infectes1, [], coord_immunises, d)
for k in range(len(coord_infectes)):
    for j in range(len(coord_sains)):
        if distance_e(np.array(coord_infectes)[k, :], np.array(coord_sains)[j, :]) < rayon_contamination and list(
                np.array(coord_sains)[j, :]) not in coord_infectes:
            coord_infectes.append(list(np.array(coord_sains)[j, :]))
            non_sains.append(list(np.array(coord_sains)[j, :]))

coord_sains = remove_(coord_sains, non_sains)
fig = go.Figure()
if coord_sains:
    fig.add_trace(go.Scatter(x=np.array(coord_sains)[:, 0], y=np.array(coord_sains)[:, 1], mode="markers",
                             marker=dict(color="Blue"), showlegend=False))
if coord_infectes:
    fig.add_trace(go.Scatter(x=np.array(coord_infectes)[:, 0], y=np.array(coord_infectes)[:, 1], mode="markers",
                             marker=dict(color="Red"), showlegend=False))
if coord_immunises:
    fig.add_trace(go.Scatter(x=np.array(coord_immunises)[:, 0], y=np.array(coord_immunises)[:, 1], mode="markers",
                             marker=dict(color="Green"), showlegend=False))
if coord_deces:
    fig.add_trace(go.Scatter(x=np.array(coord_deces)[:, 0], y=np.array(coord_deces)[:, 1], mode="markers",
                             marker=dict(color="Purple"), showlegend=False))
plot(fig)

fig = go.Figure()
labels = ["sains", "infectés", "immunisés", "décédés"]
fig.add_trace(
    go.Pie(values=[len(coord_sains), len(coord_infectes), len(coord_immunises), len(coord_deces)], labels=labels,
           sort=False))
fig.update_layout(title_text="Proportions population")
plot(fig)

courbe_sains.append(len(coord_sains))
courbe_infectes.append(len(coord_infectes))
courbe_immunises.append(len(coord_immunises))
courbe_deces.append(len(coord_deces))

# Afficher 3e vague avec pourcentage infectés/sains
non_sains = []
coord_infectes1, coord_immunises = immuniser(coord_infectes, coord_immunises, p)
coord_infectes, coord_deces = deces(coord_infectes1, coord_deces, coord_immunises, d)
for k in range(len(coord_infectes)):
    for j in range(len(coord_sains)):
        if distance_e(np.array(coord_infectes)[k, :], np.array(coord_sains)[j, :]) < rayon_contamination and list(
                np.array(coord_sains)[j, :]) \
                not in coord_infectes and chance_infecte(infectiosite):
            coord_infectes.append(list(np.array(coord_sains)[j, :]))
            non_sains.append(list(np.array(coord_sains)[j, :]))
coord_sains = remove_(coord_sains, non_sains)
fig = go.Figure()
if coord_sains != []:
    fig.add_trace(go.Scatter(x=np.array(coord_sains)[:, 0], y=np.array(coord_sains)[:, 1], mode="markers",
                             marker=dict(color="Blue"), showlegend=False))
if coord_infectes != []:
    fig.add_trace(go.Scatter(x=np.array(coord_infectes)[:, 0], y=np.array(coord_infectes)[:, 1], mode="markers",
                             marker=dict(color="Red"), showlegend=False))
if coord_immunises != []:
    fig.add_trace(go.Scatter(x=np.array(coord_immunises)[:, 0], y=np.array(coord_immunises)[:, 1], mode="markers",
                             marker=dict(color="Green"), showlegend=False))
if coord_deces != []:
    fig.add_trace(go.Scatter(x=np.array(coord_deces)[:, 0], y=np.array(coord_deces)[:, 1], mode="markers",
                             marker=dict(color="Purple"), showlegend=False))
plot(fig)

fig = go.Figure()
labels = ["sains", "infectés", "immunisés", "décédés"]
fig.add_trace(
    go.Pie(values=[len(coord_sains), len(coord_infectes), len(coord_immunises), len(coord_deces)], labels=labels,
           sort=False))
fig.update_layout(title_text="Proportions population")
plot(fig)

courbe_sains.append(len(coord_sains))
courbe_infectes.append(len(coord_infectes))
courbe_immunises.append(len(coord_immunises))
courbe_deces.append(len(coord_deces))

# Afficher 4e vague avec pourcentage infectés/sains
non_sains = []
coord_infectes1, coord_immunises = immuniser(coord_infectes, coord_immunises, p)
coord_infectes, coord_deces = deces(coord_infectes1, coord_deces, coord_immunises, d)
for k in range(len(coord_infectes)):
    for j in range(len(coord_sains)):
        if distance_e(np.array(coord_infectes)[k, :], np.array(coord_sains)[j, :]) < rayon_contamination and list(
                np.array(coord_sains)[j, :]) not in \
                coord_infectes and chance_infecte(infectiosite):
            coord_infectes.append(list(np.array(coord_sains)[j, :]))
            non_sains.append(list(np.array(coord_sains)[j, :]))
coord_sains = remove_(coord_sains, non_sains)
fig = go.Figure()
if coord_sains != []:
    fig.add_trace(go.Scatter(x=np.array(coord_sains)[:, 0], y=np.array(coord_sains)[:, 1], mode="markers",
                             marker=dict(color="Blue"), showlegend=False))
if coord_infectes != []:
    fig.add_trace(go.Scatter(x=np.array(coord_infectes)[:, 0], y=np.array(coord_infectes)[:, 1], mode="markers",
                             marker=dict(color="Red"), showlegend=False))
if coord_immunises != []:
    fig.add_trace(go.Scatter(x=np.array(coord_immunises)[:, 0], y=np.array(coord_immunises)[:, 1], mode="markers",
                             marker=dict(color="Green"), showlegend=False))
if coord_deces != []:
    fig.add_trace(go.Scatter(x=np.array(coord_deces)[:, 0], y=np.array(coord_deces)[:, 1], mode="markers",
                             marker=dict(color="Purple"), showlegend=False))
plot(fig)

fig = go.Figure()
labels = ["sains", "infectés", "immunisés", "décédés"]
fig.add_trace(
    go.Pie(values=[len(coord_sains), len(coord_infectes), len(coord_immunises), len(coord_deces)], labels=labels,
           sort=False))
fig.update_layout(title_text="Proportions population")
plot(fig)

courbe_sains.append(len(coord_sains))
courbe_infectes.append(len(coord_infectes))
courbe_immunises.append(len(coord_immunises))
courbe_deces.append(len(coord_deces))

fig = go.Figure()
x_courbe = list(np.arange(0, len(courbe_sains)))
fig.add_trace(go.Scatter(x=x_courbe, y=courbe_sains, marker=dict(color="Blue")))
fig.add_trace(go.Scatter(x=x_courbe, y=courbe_infectes, marker=dict(color="Red")))
fig.add_trace(go.Scatter(x=x_courbe, y=courbe_immunises, marker=dict(color="Green")))
fig.add_trace(go.Scatter(x=x_courbe, y=courbe_deces, marker=dict(color="Black")))
plot(fig)


def virus_px():
    nb_individu = 500
    variance_population = 5
    rayon_contamination = 4
    infectiosite = 0.7
    p = 0.4
    d = 0.2

    fig = go.Figure()
    x, y = make_blobs(n_samples=nb_individu, centers=2, cluster_std=variance_population, shuffle=True)
    fig.add_trace(go.Scatter(x=x[:, 0], y=x[:, 1], mode="markers", marker=dict(color="Blue")))
    taille_pop = len(x)

    fig = make_subplots(rows=6, cols=2, column_widths=[0.8, 0.2],
                        specs=[[{'type': 'xy'}, {'type': 'domain'}], [{'type': 'xy'}, {'type': 'domain'}],
                               [{'type': 'xy'}, {'type': 'domain'}], [{'type': 'xy'}, {'type': 'domain'}],
                               [{'type': 'xy'}, {'type': 'domain'}], [{'type': 'xy', "colspan": 2}, None]])
    courbe_sains = []
    courbe_infectes = []
    courbe_immunises = []
    courbe_deces = []
    "1er infecté"
    numero_infecte_1 = rd.randint(0, taille_pop)
    coord_1er_infecte = [x[:, 0][numero_infecte_1], x[:, 1][numero_infecte_1]]
    fig.add_trace(go.Scatter(x=x[:, 0], y=x[:, 1], mode="markers", marker=dict(color="Blue"), showlegend=False), 1, 1)
    fig.add_trace(go.Scatter(x=[x[:, 0][numero_infecte_1]], y=[x[:, 1][numero_infecte_1]], mode="markers",
                             marker=dict(color="Red"), showlegend=False), 1, 1)
    "pie"
    labels = ["sains", "infectés", "immunisés", "décédés"]
    fig.add_trace(go.Pie(labels=labels, values=[taille_pop - 1, 1, 0, 0], sort=False), 1, 2)
    fig.update_xaxes(showgrid=False, visible=False, row=1, col=1)
    fig.update_yaxes(showgrid=False, visible=False, row=1, col=1)
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
        elif distance_e(coord_1er_infecte, [x[:, 0][k], x[:, 1][k]]) < rayon_contamination and chance_infecte(
                infectiosite):
            fig.add_trace(
                go.Scatter(x=[x[:, 0][k]], y=[x[:, 1][k]], mode="markers", marker=dict(color="Red"), showlegend=False),
                2, 1)
            coord_infectes.append([x[:, 0][k], x[:, 1][k]])
        else:
            fig.add_trace(
                go.Scatter(x=[x[:, 0][k]], y=[x[:, 1][k]], mode="markers", marker=dict(color="Blue"), showlegend=False),
                2, 1)
            coord_sains.append([x[:, 0][k], x[:, 1][k]])
            fig.add_trace(go.Scatter(x=[x[:, 0][numero_infecte_1]], y=[x[:, 1][numero_infecte_1]], mode="markers",
                                     marker=dict(color="DarkOrange"), showlegend=False), 2, 1)
    fig.update_xaxes(showgrid=False, visible=False, row=1, col=1)
    fig.update_yaxes(showgrid=False, visible=False, row=1, col=1)
    "pie"
    labels = ["sains", "infectés", "immunisés", "décédés"]
    fig.add_trace(go.Pie(values=[len(coord_sains), len(coord_infectes), 0, 0], labels=labels, sort=False), 2, 2)
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
            if distance_e(np.array(coord_infectes)[k, :], np.array(coord_sains)[j, :]) < rayon_contamination and list(
                    np.array(coord_sains)[j, :]) not in coord_infectes:
                coord_infectes.append(list(np.array(coord_sains)[j, :]))
                non_sains.append(list(np.array(coord_sains)[j, :]))

    coord_sains = remove_(coord_sains, non_sains)
    if coord_sains != []:
        fig.add_trace(go.Scatter(x=np.array(coord_sains)[:, 0], y=np.array(coord_sains)[:, 1], mode="markers",
                                 marker=dict(color="Blue"), showlegend=False), 3, 1)
    if coord_infectes != []:
        fig.add_trace(go.Scatter(x=np.array(coord_infectes)[:, 0], y=np.array(coord_infectes)[:, 1], mode="markers",
                                 marker=dict(color="Red"), showlegend=False), 3, 1)
    if coord_immunises != []:
        fig.add_trace(go.Scatter(x=np.array(coord_immunises)[:, 0], y=np.array(coord_immunises)[:, 1], mode="markers",
                                 marker=dict(color="Green"), showlegend=False), 3, 1)
    if coord_deces != []:
        fig.add_trace(go.Scatter(x=np.array(coord_deces)[:, 0], y=np.array(coord_deces)[:, 1], mode="markers",
                                 marker=dict(color="Purple"), showlegend=False), 3, 1)
    fig.update_xaxes(showgrid=False, visible=False, row=2, col=1)
    fig.update_yaxes(showgrid=False, visible=False, row=2, col=1)
    "pie"
    labels = ["sains", "infectés", "immunisés", "décédés"]
    fig.add_trace(
        go.Pie(values=[len(coord_sains), len(coord_infectes), len(coord_immunises), len(coord_deces)], labels=labels,
               sort=False), 3, 2)
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
            if distance_e(np.array(coord_infectes)[k, :], np.array(coord_sains)[j, :]) < rayon_contamination and list(
                    np.array(coord_sains)[j, :]) \
                    not in coord_infectes and chance_infecte(infectiosite):
                coord_infectes.append(list(np.array(coord_sains)[j, :]))
                non_sains.append(list(np.array(coord_sains)[j, :]))
    coord_sains = remove_(coord_sains, non_sains)
    if coord_sains != []:
        fig.add_trace(go.Scatter(x=np.array(coord_sains)[:, 0], y=np.array(coord_sains)[:, 1], mode="markers",
                                 marker=dict(color="Blue"), showlegend=False), 4, 1)
    if coord_infectes != []:
        fig.add_trace(go.Scatter(x=np.array(coord_infectes)[:, 0], y=np.array(coord_infectes)[:, 1], mode="markers",
                                 marker=dict(color="Red"), showlegend=False), 4, 1)
    if coord_immunises != []:
        fig.add_trace(go.Scatter(x=np.array(coord_immunises)[:, 0], y=np.array(coord_immunises)[:, 1], mode="markers",
                                 marker=dict(color="Green"), showlegend=False), 4, 1)
    if coord_deces != []:
        fig.add_trace(go.Scatter(x=np.array(coord_deces)[:, 0], y=np.array(coord_deces)[:, 1], mode="markers",
                                 marker=dict(color="Purple"), showlegend=False), 4, 1)
    fig.update_xaxes(showgrid=False, visible=False, row=3, col=1)
    fig.update_yaxes(showgrid=False, visible=False, row=3, col=1)
    "pie"
    labels = ["sains", "infectés", "immunisés", "décédés"]
    fig.add_trace(
        go.Pie(values=[len(coord_sains), len(coord_infectes), len(coord_immunises), len(coord_deces)], labels=labels,
               sort=False), 4, 2)
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
            if distance_e(np.array(coord_infectes)[k, :], np.array(coord_sains)[j, :]) < rayon_contamination and list(
                    np.array(coord_sains)[j, :]) not in \
                    coord_infectes and chance_infecte(infectiosite):
                coord_infectes.append(list(np.array(coord_sains)[j, :]))
                non_sains.append(list(np.array(coord_sains)[j, :]))
    coord_sains = remove_(coord_sains, non_sains)
    if coord_sains != []:
        fig.add_trace(go.Scatter(x=np.array(coord_sains)[:, 0], y=np.array(coord_sains)[:, 1], mode="markers",
                                 marker=dict(color="Blue"), showlegend=False), 5, 1)
    if coord_infectes != []:
        fig.add_trace(go.Scatter(x=np.array(coord_infectes)[:, 0], y=np.array(coord_infectes)[:, 1], mode="markers",
                                 marker=dict(color="Red"), showlegend=False), 5, 1)
    if coord_immunises != []:
        fig.add_trace(go.Scatter(x=np.array(coord_immunises)[:, 0], y=np.array(coord_immunises)[:, 1], mode="markers",
                                 marker=dict(color="Green"), showlegend=False), 5, 1)
    if coord_deces != []:
        fig.add_trace(go.Scatter(x=np.array(coord_deces)[:, 0], y=np.array(coord_deces)[:, 1], mode="markers",
                                 marker=dict(color="Purple"), showlegend=False), 5, 1)
    fig.update_xaxes(showgrid=False, visible=False, row=4, col=1)
    fig.update_yaxes(showgrid=False, visible=False, row=4, col=1)
    "pie"
    labels = ["sains", "infectés", "immunisés", "décédés"]
    fig.add_trace(
        go.Pie(values=[len(coord_sains), len(coord_infectes), len(coord_immunises), len(coord_deces)], labels=labels,
               sort=False), 5, 2)
    courbe_sains.append(len(coord_sains))
    courbe_infectes.append(len(coord_infectes))
    courbe_immunises.append(len(coord_immunises))
    courbe_deces.append(len(coord_deces))
    "courbes"
    x_courbe = list(np.arange(0, len(courbe_sains)))
    fig.add_trace(go.Scatter(x=x_courbe, y=courbe_sains, marker=dict(color="Blue"), name="sain", showlegend=False), 6,
                  1)
    fig.add_trace(go.Scatter(x=x_courbe, y=courbe_infectes, marker=dict(color="Red"), name="infecté", showlegend=False),
                  6, 1)
    fig.add_trace(
        go.Scatter(x=x_courbe, y=courbe_immunises, marker=dict(color="Green"), name="immunisé", showlegend=False), 6, 1)
    fig.add_trace(go.Scatter(x=x_courbe, y=courbe_deces, marker=dict(color="Black"), name="décédé", showlegend=False),
                  6, 1)
    fig.update_traces(
        hoverinfo="name+x+y",
        line={"width": 1.2},
        marker={"size": 6},
        mode="lines+markers",
        showlegend=False, row=2, col=1)
    fig.update_layout(hovermode="x")
    plot(fig)

# pour 1000 -> 8 minutes et 33.6 secondes
# pour 2000 -> 60 minutes et 12.8 secondes
def vague_seuil_px():

    print('Début de la simulation ... \n')
    start = time.time()

    nb_individu = 2000  # recommandé : 1000
    variance_population = 4
    rayon_contamination = 2
    infectiosite = 0.17
    p = 0.20
    d = 0.05

    # NOTE : si les courbes restent constantes, augmentez le rayon de contamination
    # si le virus est trés mortel il n'y aura pas beaucoup de propagation

    # Bleu : '#636EFA'
    # Rouge : '#EF553B'
    # Vert : '#00CC96'
    # Violet : '#AB63FA'

    if nb_individu < 10 or variance_population <= 0 or rayon_contamination <= 0:
        return 'error, nb_individu and var_population and rayon_contamination must be >=10 and > 0'
    if infectiosite < 0 or infectiosite > 1:
        return 'error, infectiosité must be in [0,1]'
    if p < 0 or p > 1:
        return 'error, p must be in [0,1]'
    if d < 0 or p > 1:
        return 'error, d must be in [0,1]'

    # création des figures
    fig = go.Figure()
    fig = make_subplots(rows=2, cols=2, column_widths=[0.8, 0.2], row_heights=[0.5, 0.5],
                        subplot_titles=["population", "", ""],
                        specs=[[{'type': 'xy'}, {'type': 'domain'}], [{'type': 'xy', 'colspan': 2}, None]],
                        horizontal_spacing=0.05, vertical_spacing=0.05)

    # création des courbes finales
    courbe_sains = []
    courbe_infectes = []
    courbe_immunises = []
    courbe_deces = []
    courbe_removed = []

    # dataset
    x, y = make_blobs(n_samples=nb_individu, centers=1, cluster_std=variance_population)  # création du dataset
    taille_pop = len(x)

    numero_infecte_1 = rd.randint(0, taille_pop - 1)  # on choisit le premier individu infecté au hasard
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
        elif distance_e(coord_1er_infecte, [x[:, 0][k], x[:, 1][k]]) < rayon_contamination and chance_infecte(
                infectiosite):
            coord_infectes.append([x[:, 0][k], x[:, 1][k]])
        else:
            coord_sains.append([x[:, 0][k], x[:, 1][k]])
    courbe_sains.append(len(coord_sains))
    courbe_infectes.append(len(coord_infectes))
    courbe_immunises.append(0)
    courbe_deces.append(0)
    courbe_removed.append(0)

    # vagues 2 à n
    coord_immunises = []  # on initialise
    coord_deces = []
    # for i in range(n - 2):
    i = 1
    while len(coord_infectes) > 0.1 * taille_pop or len(courbe_sains) < 5:
        non_sains = []
        coord_infectes1, coord_immunises = immuniser(coord_infectes, coord_immunises, p)
        coord_infectes, coord_deces = deces(coord_infectes1, coord_deces, coord_immunises, d)

        for k in range(len(coord_infectes)):
            for j in range(len(coord_sains)):
                if distance_e(np.array(coord_infectes)[k, :],
                            np.array(coord_sains)[j, :]) < rayon_contamination and np.array(coord_sains)[j,
                                                                                   :] not in np.array(
                    coord_infectes) and chance_infecte(infectiosite):
                    coord_infectes.append(list(np.array(coord_sains)[j, :]))
                    non_sains.append(list(np.array(coord_sains)[j, :]))
        coord_sains = remove_(coord_sains, non_sains)
        # pour les courbes finales
        courbe_sains.append(len(coord_sains))
        courbe_infectes.append(len(coord_infectes))
        courbe_immunises.append(len(coord_immunises))
        courbe_deces.append(len(coord_deces))
        courbe_removed.append(len(coord_immunises) + len(coord_deces))
        i += 1  # vague suivante
    if coord_sains != []:
        fig.add_trace(
            go.Scatter(x=np.array(coord_sains)[:, 0], y=np.array(coord_sains)[:, 1], name="sain", mode="markers",
                       marker=dict(color='#636EFA'), showlegend=False), 1, 1)
    if coord_infectes != []:
        fig.add_trace(go.Scatter(x=np.array(coord_infectes)[:, 0], y=np.array(coord_infectes)[:, 1], name="infecté",
                                 mode="markers", marker=dict(color='#EF553B'), showlegend=False), 1, 1)
    if coord_immunises != []:
        fig.add_trace(go.Scatter(x=np.array(coord_immunises)[:, 0], y=np.array(coord_immunises)[:, 1], name='immunisé',
                                 mode="markers", marker=dict(color='#00CC96'), showlegend=False), 1, 1)
    if coord_deces != []:
        fig.add_trace(
            go.Scatter(x=np.array(coord_deces)[:, 0], y=np.array(coord_deces)[:, 1], name="décédé", mode="markers",
                       marker=dict(color='#AB63FA'), showlegend=False), 1, 1)
    fig.update_traces(hoverinfo="name")
    fig.update_xaxes(showgrid=False, visible=False, row=1, col=1)
    fig.update_yaxes(showgrid=False, visible=False, row=1, col=1)
    titre = str(i) + '-ième vague'

    labels = ["sains", "infectés", "immunisés", "décédés"]
    fig.add_trace(
        go.Pie(values=[len(coord_sains), len(coord_infectes), len(coord_immunises), len(coord_deces)], labels=labels,
               sort=False), 1, 2)

    x_courbe = list(np.arange(0, len(courbe_sains)))
    fig.add_trace(go.Scatter(x=x_courbe, y=courbe_sains, marker=dict(color='#636EFA'), showlegend=False, name="sains",
                             yaxis="y", ), 2, 1)
    fig.add_trace(
        go.Scatter(x=x_courbe, y=courbe_infectes, marker=dict(color='#EF553B'), showlegend=False, name="infectés",
                   yaxis="y2", ), 2, 1)
    fig.add_trace(
        go.Scatter(x=x_courbe, y=courbe_immunises, marker=dict(color='#00CC96'), showlegend=False, name="immunisés",
                   yaxis="y3", ), 2, 1)
    fig.add_trace(go.Scatter(x=x_courbe, y=courbe_deces, marker=dict(color='#AB63FA'), showlegend=False, name="décédés",
                             yaxis="y4", ), 2, 1)
    fig.add_trace(
        go.Scatter(x=x_courbe, y=courbe_removed, marker=dict(color='#000000'), showlegend=False, name="removed",
                   yaxis="y5", ), 2, 1)
    fig.update_xaxes(title_text="jours", row=2, col=1)
    fig.update_yaxes(title_text="nombre d'individus", row=2, col=1)
    fig.add_annotation(text="Maximum d'infectés", x=courbe_infectes.index(max(courbe_infectes)),
                       # ajouter un texte avec une flèche
                       y=max(courbe_infectes) + 0.03 * taille_pop, arrowhead=1, showarrow=True, row=2, col=1)
    fig.update_traces(
        hoverinfo="name+x+y",
        line={"width": 1.2},
        marker={"size": 6},
        mode="lines+markers",
        showlegend=False, row=2, col=1)
    fig.update_layout(hovermode="x")
    fig.update_layout(title_text="simulation virus")
    fig.update_layout(title_font_color='#EF553B', )
    t = (time.time()-start)
    min = int(round(t,2)//60)
    sec = round(t-min*60,1)
    print('Simulation terminée en '+str(min)+' minutes \net '+str(sec)+' secondes')
    plot(fig)

# pour 1000 -> 16.6 secondes
# pour 2000 -> 51.3 secondes
# pour 10.000 ->
def vague_seuil_px_opti():

    print('Début de la simulation ... \n')
    start = time.time()

    nb_individu = 10000  # recommandé : 500 à 10000
    variance_pop = 1  # recommandé : 1
    rayon_contamination = 0.5  # recommandé : 0.5
    infectiosite = 0.10  # recommandé : 10%
    p = 0.10  # recommandé : 10%
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
    fig = go.Figure()
    fig = make_subplots(rows=2, cols=2, column_widths=[0.8, 0.2], row_heights=[0.5, 0.5],
                        subplot_titles=["population", "", ""],
                        specs=[[{'type': 'xy'}, {'type': 'domain'}], [{'type': 'xy', 'colspan': 2}, None]],
                        horizontal_spacing=0.05, vertical_spacing=0.05)

    # création des courbes finales et listes des coordonnées
    data = dict(courbe_sains = [],courbe_infectes = [],courbe_immunises = [],courbe_deces = [],courbe_removed = [],coord_infectes=[],coord_sains=[],coord_immunises=[],coord_deces=[])

    # dataset
    x, y = make_blobs(n_samples=nb_individu, centers=1, cluster_std=variance_pop)
    df = pd.DataFrame(dict(x=x[:,0],
                           y=x[:,1]))
    taille_pop = len(df['x'])

    numero_infecte_1 = rd.randint(0, taille_pop - 1)  # on choisit le premier individu infecté au hasard
    coord_1er_infecte = [df['x'][numero_infecte_1], df['y'][numero_infecte_1]]  # coordonnées du 1er infecté
    data['courbe_sains'].append(taille_pop-1)
    data['courbe_infectes'].append(1)
    data['courbe_immunises'].append(0)
    data['courbe_deces'].append(0)
    data['courbe_removed'].append(0)

    # 1er vague

    df_sans1erinfecte = df[(df['x'] != df['x'][numero_infecte_1]) & (df['y'] != df['y'][numero_infecte_1])]
    for k in range(taille_pop):
        if [df['x'][k], df['y'][k]] == coord_1er_infecte:
            data['coord_infectes'].append(coord_1er_infecte)
        elif distance_e(coord_1er_infecte, [df_sans1erinfecte['x'][k], df_sans1erinfecte['y'][k]]) < rayon_contamination and chance_infecte(infectiosite):
            data['coord_infectes'].append([df['x'][k], df['y'][k]])
        else:
            data['coord_sains'].append([df['x'][k], df['y'][k]])

    data['courbe_sains'].append(len(data['coord_sains']))
    data['courbe_infectes'].append(len(data['coord_infectes']))
    data['courbe_immunises'].append(0)
    data['courbe_deces'].append(0)
    data['courbe_removed'].append(0)

    # vagues 2 à n

    i = 1
    while len(data['coord_infectes']) > 0.08*taille_pop or len(data['courbe_sains']) < 20: #condition d'arrêt
        non_sains = []
        coord_infectes1, data['coord_immunises'] = immuniser(data['coord_infectes'], data['coord_immunises'], p)
        data['coord_infectes'], data['coord_deces'] = deces(coord_infectes1, data['coord_deces'], data['coord_immunises'], d)

        for k in range(len(data['coord_infectes'])):
            for j in range(len(data['coord_sains'])):
                if distance_e(data['coord_infectes'][k],data['coord_sains'][j]) < rayon_contamination and data['coord_sains'][j] not in data['coord_infectes'] and chance_infecte(infectiosite):
                    data['coord_infectes'].append(data['coord_sains'][j])
                    non_sains.append(data['coord_sains'][j])
        data['coord_sains'] = remove_(data['coord_sains'], non_sains)
        # pour les courbes finales
        data['courbe_sains'].append(len(data['coord_sains']))
        data['courbe_infectes'].append(len(data['coord_infectes']))
        data['courbe_immunises'].append(len(data['coord_immunises']))
        data['courbe_deces'].append(len(data['coord_deces']))
        data['courbe_removed'].append(len(data['coord_immunises']) + len(data['coord_deces']))
        i += 1  # vague suivante

    if data['coord_sains'] != []:
        fig.add_trace(go.Scatter(x=np.array(data['coord_sains'])[:, 0], y=np.array(data['coord_sains'])[:, 1], name="sain", mode="markers",
                                 marker=dict(
                                     color='#636EFA',
                                     line=dict(
                                         width=0.4,
                                         color='#636EFA')
                                 ),marker_line=dict(width=1), showlegend=False), 1, 1)
    if data['coord_infectes'] != []:
        fig.add_trace(go.Scatter(x=np.array(data['coord_infectes'])[:, 0], y=np.array(data['coord_infectes'])[:, 1], name="infecté",mode="markers",
                                 marker=dict(
                                     color='#EF553B',
                                     line=dict(
                                         width=0.4,
                                         color='#EF553B')
                                 ),marker_line=dict(width=1), showlegend=False), 1, 1)
    if data['coord_immunises'] != []:
        fig.add_trace(go.Scatter(x=np.array(data['coord_immunises'])[:, 0], y=np.array(data['coord_immunises'])[:, 1], name='immunisé',mode="markers",
                                 marker=dict(
                                     color='#00CC96',
                                     line=dict(
                                         width=0.4,
                                         color='#00CC96')
                                 ), marker_line=dict(width=1),showlegend=False), 1, 1)
    if data['coord_deces'] != []:
        fig.add_trace(go.Scatter(x=np.array(data['coord_deces'])[:, 0], y=np.array(data['coord_deces'])[:, 1], name="décédé", mode="markers",
                                 marker=dict(
                                     color='#AB63FA',
                                     line=dict(
                                         width=0.4,
                                         color='#AB63FA')
                                 ), marker_line=dict(width=1),showlegend=False), 1, 1)
    fig.update_traces(hoverinfo="name")
    fig.update_xaxes(showgrid=False, visible=False, row=1, col=1)
    fig.update_yaxes(showgrid=False, visible=False, row=1, col=1)
    titre = str(i) + '-ième vague'
    labels = ["sains", "infectés", "immunisés", "décédés"]
    fig.add_trace(go.Pie(values=[len(data['coord_sains']), len(data['coord_infectes']), len(data['coord_immunises']), len(data['coord_deces'])], labels=labels, sort=False), 1, 2)

    x_courbe = list(np.arange(0, len(data['courbe_sains'])))
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_sains'], marker=dict(color='#636EFA'), showlegend=False, name="sains",yaxis="y", ), 2, 1)
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_infectes'], marker=dict(color='#EF553B'), showlegend=False, name="infectés",yaxis="y2", ), 2, 1)
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_immunises'], marker=dict(color='#00CC96'), showlegend=False, name="immunisés",yaxis="y3", ), 2, 1)
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_deces'], marker=dict(color='#AB63FA'), showlegend=False, name="décédés",yaxis="y4", ), 2, 1)
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_removed'], marker=dict(color='#000000'), showlegend=False, name="removed",yaxis="y5", ), 2, 1)
    fig.update_xaxes(title_text="jours", row=2, col=1)
    fig.update_yaxes(title_text="nombre d'individus", row=2, col=1)
    fig.add_annotation(text="Maximum d'infectés", x=data['courbe_infectes'].index(max(data['courbe_infectes'])),# ajouter un texte avec une flèche
                       y=max(data['courbe_infectes']) + 0.03 * taille_pop, arrowhead=1, showarrow=True, row=2, col=1)
    fig.update_traces(
        hoverinfo="name+x+y",
        line={"width": 1.2},
        marker={"size": 6},
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

# pour 1000 -> 11.1 secondes
# pour 2000 -> 50.9 secondes
# pour 10.000 ->
def vague_seuil_px_opti2():

    print('Début de la simulation ... \n')
    start = time.time()

    nb_individu = 50000  # recommandé : 500 à 10000
    variance_pop = 1  # recommandé : 1
    rayon_contamination = 0.5  # recommandé : 0.5
    infectiosite = 0.1  # recommandé : 10%
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
    data = dict(courbe_sains = [nb_individu-1],courbe_infectes = [1],courbe_immunises = [0],courbe_deces = [0],courbe_removed = [0],coord_infectes=[],coord_sains=[],coord_immunises=[],coord_deces=[])

    numero_infecte_1 = rd.randint(0, nb_individu - 1)  # on choisit le premier individu infecté au hasard
    coord_1er_infecte = [df['x'][numero_infecte_1], df['y'][numero_infecte_1]]  # coordonnées du 1er infecté

    # 1er vague

    df_sans1erinfecte = df[(df['x'] != df['x'][numero_infecte_1]) & (df['y'] != df['y'][numero_infecte_1])]
    for k in range(nb_individu):
        if [df['x'][k], df['y'][k]] == coord_1er_infecte:
            data['coord_infectes'].append(coord_1er_infecte)
        elif distance_e(coord_1er_infecte, [df_sans1erinfecte['x'][k], df_sans1erinfecte['y'][k]]) < rayon_contamination and chance_infecte(infectiosite):
            data['coord_infectes'].append([df['x'][k], df['y'][k]])
        else:
            data['coord_sains'].append([df['x'][k], df['y'][k]])

    data['courbe_sains'].append(len(data['coord_sains']))
    data['courbe_infectes'].append(len(data['coord_infectes']))
    data['courbe_immunises'].append(0)
    data['courbe_deces'].append(0)
    data['courbe_removed'].append(0)

    # vagues 2 à n

    while len(data['coord_infectes']) > 0.08*nb_individu or len(data['courbe_sains']) < 10: #condition d'arrêt
        coord_infectes1, data['coord_immunises'] = immuniser(data['coord_infectes'], data['coord_immunises'], p)
        data['coord_infectes'], data['coord_deces'] = deces(coord_infectes1, data['coord_deces'], data['coord_immunises'], d)

        for k in range(len(data['coord_infectes'])):
            non_sains = 0
            for j in range(len(data['coord_sains'])):
                if distance_e(data['coord_infectes'][k],data['coord_sains'][j-non_sains]) < rayon_contamination and data['coord_sains'][j-non_sains] not in data['coord_infectes'] and chance_infecte(infectiosite):
                    data['coord_infectes'].append(data['coord_sains'][j-non_sains])
                    data['coord_sains'].remove(data['coord_sains'][j-non_sains])
                    non_sains+=1
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
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_sains'], marker=dict(color='#636EFA',size=1), marker_line=dict(width=1),showlegend=False, name="sains",yaxis="y", ), 2, 1)
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_infectes'], marker=dict(color='#EF553B',size=1), marker_line=dict(width=1),showlegend=False, name="infectés",yaxis="y2", ), 2, 1)
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_immunises'], marker=dict(color='#00CC96',size=1), marker_line=dict(width=1),showlegend=False, name="immunisés",yaxis="y3", ), 2, 1)
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_deces'], marker=dict(color='#AB63FA',size=1), marker_line=dict(width=1),showlegend=False, name="décédés",yaxis="y4", ), 2, 1)
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_removed'], marker=dict(color='#000000',size=1), marker_line=dict(width=1), showlegend=False, name="removed",yaxis="y5", ), 2, 1)
    fig.update_xaxes(title_text="jours", row=2, col=1)
    fig.update_yaxes(title_text="nombre d'individus", row=2, col=1)
    fig.add_annotation(text="Maximum d'infectés", x=data['courbe_infectes'].index(max(data['courbe_infectes'])),# ajouter un texte avec une flèche
                       y=max(data['courbe_infectes']) + 0.03 * nb_individu, arrowhead=1, showarrow=True, row=2, col=1)
    fig.update_traces(
        hoverinfo="name+x+y",
        line={"width": 1.2},
        marker={"size": 6},
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


# simulation avec seulement les courbes
# pour 10.000 -> 14 min
def vague_seuil_px_courbes():

    print('Début de la simulation ... \n')
    start = time.time()

    nb_individu = 10000 # recommandé : 1000
    variance_population = 1
    rayon_contamination = 0.5
    infectiosite = 0.6
    p = 0.3
    d = 0.12

    # NOTE : si les courbes restent constantes, augmentez le rayon de contamination
    # si le virus est trés mortel il n'y aura pas beaucoup de propagation

    # Bleu : '#636EFA'
    # Rouge : '#EF553B'
    # Vert : '#00CC96'
    # Violet : '#AB63FA'

    if nb_individu < 10 or variance_population <= 0 or rayon_contamination <= 0:
        return 'error, nb_individu and var_population and rayon_contamination must be >=10 and > 0'
    if infectiosite < 0 or infectiosite > 1:
        return 'error, infectiosité must be in [0,1]'
    if p < 0 or p > 1:
        return 'error, p must be in [0,1]'
    if d < 0 or p > 1:
        return 'error, d must be in [0,1]'

    # création des figures
    fig = go.Figure()

    # création des courbes finales
    data = dict(courbe_sains = [nb_individu-1],courbe_infectes = [1],courbe_immunises = [0],courbe_deces = [0],courbe_removed = [0],coord_infectes=[],coord_sains=[],coord_immunises=[],coord_deces=[])


    # dataset
    x, y = make_blobs(n_samples=nb_individu, centers=1, cluster_std=variance_population)  # création du dataset
    df = pd.DataFrame(dict(x=x[:,0],
                           y=x[:,1]))
    taille_pop = len(x)

    numero_infecte_1 = rd.randint(0, taille_pop-1)  # on choisit le premier individu infecté au hasard
    coord_1er_infecte = [x[:, 0][numero_infecte_1], x[:, 1][numero_infecte_1]]  # coordonnées du 1er infecté

    # 1er vague
    df_sans1erinfecte = df[(df['x'] != df['x'][numero_infecte_1]) & (df['y'] != df['y'][numero_infecte_1])]
    for k in range(taille_pop):
        if [df['x'][k], df['y'][k]] == coord_1er_infecte:
            data['coord_infectes'].append(coord_1er_infecte)
        elif distance_e(coord_1er_infecte, [df_sans1erinfecte['x'][k],df_sans1erinfecte['y'][k]]) < rayon_contamination and chance_infecte(infectiosite):
            data['coord_infectes'].append([df['x'][k], df['y'][k]])
        else:
            data['coord_sains'].append([df['x'][k], df['y'][k]])

    data['courbe_sains'].append(len(data['coord_sains']))
    data['courbe_infectes'].append(len(data['coord_infectes']))
    data['courbe_immunises'].append(0)
    data['courbe_deces'].append(0)
    data['courbe_removed'].append(0)

    # vagues 2 à n
    while len(data['coord_infectes']) > 0.08*nb_individu or len(data['courbe_sains']) < 20: #condition d'arrêt
        coord_infectes1, data['coord_immunises'] = immuniser(data['coord_infectes'], data['coord_immunises'], p)
        data['coord_infectes'], data['coord_deces'] = deces(coord_infectes1, data['coord_deces'], data['coord_immunises'], d)

        for k in range(len(data['coord_infectes'])):
            non_sains = 0
            for j in range(len(data['coord_sains'])):
                if distance_e(data['coord_infectes'][k],data['coord_sains'][j-non_sains]) < rayon_contamination and data['coord_sains'][j-non_sains] not in data['coord_infectes'] and chance_infecte(infectiosite):
                    data['coord_infectes'].append(data['coord_sains'][j-non_sains])
                    data['coord_sains'].remove(data['coord_sains'][j-non_sains])
                    non_sains+=1
        # pour les courbes finales
        data['courbe_sains'].append(len(data['coord_sains']))
        data['courbe_infectes'].append(len(data['coord_infectes']))
        data['courbe_immunises'].append(len(data['coord_immunises']))
        data['courbe_deces'].append(len(data['coord_deces']))
        data['courbe_removed'].append(len(data['coord_immunises']) + len(data['coord_deces']))


    x_courbe = list(np.arange(0, len(data['courbe_sains'])))
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_sains'], marker=dict(color='#636EFA',size=1), marker_line=dict(width=2), name="sains" ))
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_infectes'], marker=dict(color='#EF553B',size=1), marker_line=dict(width=2),name="infectés" ))
    #fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_immunises'], marker=dict(color='#00CC96',size=1), marker_line=dict(width=2),name="immunisés"))
    #fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_deces'], marker=dict(color='#AB63FA',size=1), marker_line=dict(width=2), name="décédés"))
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_removed'], marker=dict(color='#000000',size=1), marker_line=dict(width=2), name="removed"))
    fig.update_xaxes(title_text="jours")
    fig.update_yaxes(title_text="nombre d'individus")
    fig.add_annotation(text="Maximum d'infectés", x=data['courbe_infectes'].index(max(data['courbe_infectes'])),# ajouter un texte avec une flèche
                       y=max(data['courbe_infectes']) + 0.03 * nb_individu, arrowhead=1, showarrow=True)
    fig.update_traces(
        hoverinfo="name+x+y",
        mode="lines+markers",
        )
    fig.update_layout(hovermode="x")
    fig.update_layout(title_text="simulation virus")
    fig.update_layout(title_font_color='#EF553B')
    t = (time.time()-start)
    min = int(round(t,2)//60)
    sec = round(t-min*60,1)
    print('Simulation terminée en '+str(min)+' minutes \net '+str(sec)+' secondes')
    plot(fig)

def vague_seuil_px_confinement():

    nb_individu = 2500
    variance_population = 1
    rayon_contamination = 2
    rayon_contamination_confinement = rayon_contamination / 4
    infectiosite = 0.2
    infectiosite_confinement = infectiosite / 8
    p = 0.2  # immunité
    d = 0.1  # décès

    capH = 0.19 * nb_individu  # capacité hospitalière en pourcentage de population

    # NOTE : si les courbes restent constantes, augmentez le rayon de contamination
    # si le virus est trés mortel il n'y aura pas beaucoup de propagation

    # Bleu : '#636EFA'
    # Rouge : '#EF553B'
    # Vert : '#00CC96'
    # Violet : '#AB63FA'

    if nb_individu < 10 or variance_population <= 0 or rayon_contamination <= 0:
        return 'error, nb_individu and var_population and rayon_contamination must be >=10 and > 0'
    if infectiosite < 0 or infectiosite > 1:
        return 'error, infectiosité must be in [0,1]'
    if p < 0 or p > 1:
        return 'error, p must be in [0,1]'
    if d < 0 or p > 1:
        return 'error, d must be in [0,1]'

    # création des figures
    fig = go.Figure()

    # création des courbes finales
    courbes = dict(courbe_sains = [],courbe_infectes = [],courbe_deces = [],courbe_sains_confinement = [],courbe_infectes_confinement = [],courbe_deces_confinement = [])

    # dataset
    x, y = make_blobs(n_samples=nb_individu, centers=1, cluster_std=variance_population)  # création du dataset
    df = pd.DataFrame(dict(x=x[:,0],
                           y=x[:,1]))
    taille_pop = len(df['x'])

    numero_infecte_1 = rd.randint(0, taille_pop - 1)  # on choisit le premier individu infecté au hasard
    coord_1er_infecte = [df['x'][numero_infecte_1], df['y'][numero_infecte_1]]  # coordonnées du 1er infecté
    courbes['courbe_sains'].append(taille_pop - 1)
    courbes['courbe_infectes'].append(1)
    courbes['courbe_deces'].append(0)
    courbes['courbe_infectes_confinement'].append(1)
    courbes['courbe_deces_confinement'].append(0)

    # 1er vague
    coord = dict(coord_infectes = [],coord_sains = [],coord_infectes_confinement = [],coord_sains_confinement = [],coord_immunises = [],coord_deces = [],coord_immunises_confinement = [],coord_deces_confinement = [])
    for k in range(taille_pop):
        if [df['x'][k], df['y'][k]] == coord_1er_infecte:
            coord['coord_infectes'].append(coord_1er_infecte)
            coord['coord_infectes_confinement'].append(coord_1er_infecte)
        elif distance_e(coord_1er_infecte, [df['x'][k], df['y'][k]]) < rayon_contamination and chance_infecte(infectiosite):
            coord['coord_infectes'].append([df['x'][k], df['y'][k]])
            coord['coord_infectes_confinement'].append([df['x'][k], df['y'][k]])
        else:
            coord['coord_sains'].append([df['x'][k], df['y'][k]])
            coord['coord_sains_confinement'].append([df['x'][k], df['y'][k]])
    courbes['courbe_sains'].append(len(coord['coord_sains']))
    courbes['courbe_infectes'].append(len(coord['coord_infectes']))
    courbes['courbe_deces'].append(0)
    courbes['courbe_sains_confinement'].append(len(coord['coord_sains']))
    courbes['courbe_infectes_confinement'].append(len(coord['coord_infectes']))
    courbes['courbe_deces_confinement'].append(0)

    # vagues 2 à n
    i = 1
    vagues = []

    confinement = 1  # pas de confinement

    while len(coord['coord_infectes']) > 0.08 * taille_pop or len(courbes['courbe_sains']) < 25:
        if courbes['courbe_infectes'][i] > capH:
            confinement *= 0  # dès qu'on passe au dessus des capacités hospitalières on confine
        if confinement == 1:
            non_sains = []
            coord_infectes1, coord['coord_immunises'] = immuniser(coord['coord_infectes'], coord['coord_immunises'], p)
            coord['coord_infectes'], coord['coord_deces'] = deces(coord_infectes1, coord['coord_deces'], coord['coord_immunises'], d)

            for k in range(len(coord['coord_infectes'])):
                for j in range(len(coord['coord_sains'])):
                    if distance_e(coord['coord_infectes'][k],coord['coord_sains'][j]) < rayon_contamination and coord['coord_sains'][j] not in coord['coord_infectes'] and chance_infecte(infectiosite):
                        coord['coord_infectes'].append((coord['coord_sains'][j]))
                        coord['coord_infectes_confinement'].append(coord['coord_sains'][j])
                        non_sains.append(coord['coord_sains'][j])
            coord['coord_sains'] = remove_(coord['coord_sains'], non_sains)
            # pour les courbes finales
            courbes['courbe_sains'].append(len(coord['coord_sains']))
            courbes['courbe_infectes'].append(len(coord['coord_infectes']))
            courbes['courbe_deces'].append(len(coord['coord_deces']))
            courbes['courbe_sains_confinement'].append(len(coord['coord_sains']))
            courbes['courbe_infectes_confinement'].append(len(coord['coord_infectes']))
            courbes['courbe_deces_confinement'].append(len(coord['coord_deces']))
            i += 1  # vague suivante
        else:
            vagues.append(i)
            non_sains = []
            coord_infectes1, coord['coord_immunises'] = immuniser(coord['coord_infectes'], coord['coord_immunises'], p)
            coord['coord_infectes'], coord['coord_deces'] = deces(coord_infectes1, coord['coord_deces'], coord['coord_immunises'], d)

            for k in range(len(coord['coord_infectes'])):
                for j in range(len(coord['coord_sains'])):
                    if distance_e(coord['coord_infectes'][k],coord['coord_sains'][j]) < rayon_contamination and coord['coord_sains'][j] not in coord['coord_infectes'] and chance_infecte(infectiosite):
                        coord['coord_infectes'].append(coord['coord_sains'][j])
                        non_sains.append(coord['coord_sains'][j])
            coord['coord_sains'] = remove_(coord['coord_sains'], non_sains)
            # pour les courbes finales
            courbes['courbe_sains'].append(len(coord['coord_sains']))
            courbes['courbe_infectes'].append(len(coord['coord_infectes']))
            courbes['courbe_deces'].append(len(coord['coord_deces']))

            #### et avec confinement :

            non_sains = []
            coord_infectes1, coord['coord_immunises_confinement'] = immuniser(coord['coord_infectes_confinement'], coord['coord_immunises_confinement'], p)
            coord['coord_infectes_confinement'], coord['coord_deces_confinement'] = deces(coord_infectes1, coord['coord_deces_confinement'], coord['coord_immunises_confinement'], d)

            for k in range(len(coord['coord_infectes_confinement'])):
                for j in range(len(coord['coord_sains_confinement'])):
                    if distance_e(coord['coord_infectes_confinement'][k],coord['coord_sains_confinement'][j]) < rayon_contamination_confinement and coord['coord_sains_confinement'][j] not in coord['coord_infectes_confinement'] and chance_infecte(infectiosite_confinement):
                        coord['coord_infectes_confinement'].append(coord['coord_sains_confinement'][j])
                        non_sains.append(coord['coord_sains_confinement'][j])
            coord['coord_sains_confinement'] = remove_(coord['coord_sains_confinement'], non_sains)
            # pour les courbes finales
            courbes['courbe_sains_confinement'].append(len(coord['coord_sains_confinement']))
            courbes['courbe_infectes_confinement'].append(len(coord['coord_infectes_confinement']))
            courbes['courbe_deces_confinement'].append(len(coord['coord_deces_confinement']))
            i += 1  # vague suivante

    x_courbe = list(np.arange(0, len(courbes['courbe_sains'])))
    x_courbe_confinement = list(np.arange(0, len(courbes['courbe_sains_confinement'])))
    fig.add_trace(go.Scatter(x=x_courbe_confinement, y=courbes['courbe_infectes_confinement'], marker=dict(color='#EF553B'),name="infectés confinement", opacity=1, line_dash="dot"))
    fig.add_trace(go.Scatter(x=x_courbe_confinement, y=courbes['courbe_deces_confinement'], marker=dict(color='#AB63FA'),name="décédés confinement", opacity=1, line_dash="dot"))
    fig.add_trace(go.Scatter(x=x_courbe, y=courbes['courbe_infectes'], marker=dict(color='#EF553B'), name="infectés", opacity=0.6))
    fig.add_trace(go.Scatter(x=x_courbe, y=courbes['courbe_deces'], marker=dict(color='#AB63FA'), name="décédés", opacity=0.6))
    fig.add_trace(go.Scatter(x=[0, len(x_courbe) - 1], y=[capH, capH], marker=dict(color='#000000'), showlegend=False,name="capacité hospitalière", line_width=3, opacity=1, line_dash="dot", ))
    fig.update_xaxes(title_text="jours")
    fig.update_yaxes(title_text="nombre d'individus")
    fig.add_annotation(text="Capacité hospitalière", x=0,  # ajouter un texte avec une flèche
                       y=capH * 1.01, arrowhead=1, showarrow=True)
    if vagues != []:
        fig.add_annotation(text="Début du confinement", x=min(vagues),  # ajouter un texte avec une flèche
                                       y=courbes['courbe_infectes_confinement'][min(vagues)], arrowhead=1, showarrow=True)
    fig.update_layout(title_text="simulation virus")
    fig.update_layout(title_font_color='#EF553B', )
    plot(fig)



############################################
#    Github - subplot Ro et cas limites    #
############################################


def subplot_Ro():

    print('Début de la simulation ... \n')
    start = time.time()

    nb_individu = 5000 # recommandé : 1000
    variance_population = 1
    rayon_contamination = 0.5

    infectiosite_1 = 0.5
    p_1 = 0.
    d_1 = 1
    infectiosite_2 = 0.5
    p_2 = 0.
    d_2 = 0.5
    infectiosite_3 = 0.3
    p_3 = 0.
    d_3 = 0.1
    infectiosite_4 = 1.
    p_4 = 0.
    d_4 = 0.1


    # création des figures
    fig = make_subplots(rows=2, cols=2,
                        subplot_titles=["Ro=0.5, β=0.5, λ=1.0", "Ro=1, β=0.5, λ=0.5", "Ro=3, β=0.3, λ=0.1", "Ro=10, β=1.0, λ=0.1"],
                        specs=[[{'type': 'xy'}, {'type': 'xy'}], [{'type': 'xy'}, {'type': 'xy'}]])

    # création des courbes finales
    data = dict(courbe_sains = [nb_individu-1],courbe_infectes = [1],courbe_immunises = [0],courbe_deces = [0],courbe_removed = [0],coord_infectes=[],coord_sains=[],coord_immunises=[],coord_deces=[])


    # dataset
    x, y = make_blobs(n_samples=nb_individu, centers=2, cluster_std=variance_population)  # création du dataset
    df = pd.DataFrame(dict(x=x[:,0],
                           y=x[:,1]))
    taille_pop = len(x)

    numero_infecte_1 = rd.randint(0, taille_pop-1)  # on choisit le premier individu infecté au hasard
    coord_1er_infecte = [x[:, 0][numero_infecte_1], x[:, 1][numero_infecte_1]]  # coordonnées du 1er infecté

    # 1er vague
    df_sans1erinfecte = df[(df['x'] != df['x'][numero_infecte_1]) & (df['y'] != df['y'][numero_infecte_1])]
    for k in range(taille_pop):
        if [df['x'][k], df['y'][k]] == coord_1er_infecte:
            data['coord_infectes'].append(coord_1er_infecte)
        elif distance_e(coord_1er_infecte, [df_sans1erinfecte['x'][k],df_sans1erinfecte['y'][k]]) < rayon_contamination and chance_infecte(infectiosite_1):
            data['coord_infectes'].append([df['x'][k], df['y'][k]])
        else:
            data['coord_sains'].append([df['x'][k], df['y'][k]])

    data['courbe_sains'].append(len(data['coord_sains']))
    data['courbe_infectes'].append(len(data['coord_infectes']))
    data['courbe_immunises'].append(0)
    data['courbe_deces'].append(0)
    data['courbe_removed'].append(0)

    # vagues 2 à n
    while len(data['coord_infectes']) > 0.08*nb_individu or len(data['courbe_sains']) < 20: #condition d'arrêt
        coord_infectes1, data['coord_immunises'] = immuniser(data['coord_infectes'], data['coord_immunises'], p_1)
        data['coord_infectes'], data['coord_deces'] = deces(coord_infectes1, data['coord_deces'], data['coord_immunises'], d_1)

        for k in range(len(data['coord_infectes'])):
            non_sains = 0
            for j in range(len(data['coord_sains'])):
                if distance_e(data['coord_infectes'][k],data['coord_sains'][j-non_sains]) < rayon_contamination and data['coord_sains'][j-non_sains] not in data['coord_infectes'] and chance_infecte(infectiosite_1):
                    data['coord_infectes'].append(data['coord_sains'][j-non_sains])
                    data['coord_sains'].remove(data['coord_sains'][j-non_sains])
                    non_sains+=1
        # pour les courbes finales
        data['courbe_sains'].append(len(data['coord_sains']))
        data['courbe_infectes'].append(len(data['coord_infectes']))
        data['courbe_immunises'].append(len(data['coord_immunises']))
        data['courbe_deces'].append(len(data['coord_deces']))
        data['courbe_removed'].append(len(data['coord_immunises']) + len(data['coord_deces']))


    x_courbe = list(np.arange(0, len(data['courbe_sains'])))
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_sains'], marker=dict(color='#636EFA',size=1), marker_line=dict(width=2), name="S(t)" ),1,1)
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_infectes'], marker=dict(color='#EF553B',size=1), marker_line=dict(width=2),name="I(t)" ),1,1)
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_removed'], marker=dict(color='#000000',size=1), marker_line=dict(width=2), name="R(t)"),1,1)
    fig.update_xaxes(title_text="jours",row=1,col=1)
    fig.update_yaxes(title_text="nombre d'individus",row=1,col=1)
    fig.update_traces(
        hoverinfo="name+x+y",
        mode="lines+markers",row=1,col=1
        )

    ###################################

    # création des courbes finales
    data = dict(courbe_sains=[nb_individu - 1], courbe_infectes=[1], courbe_immunises=[0], courbe_deces=[0],
                courbe_removed=[0], coord_infectes=[], coord_sains=[], coord_immunises=[], coord_deces=[])
    x, y = make_blobs(n_samples=nb_individu, centers=2, cluster_std=variance_population+0.25)  # création du dataset
    df = pd.DataFrame(dict(x=x[:,0],
                           y=x[:,1]))
    numero_infecte_1 = rd.randint(0, taille_pop - 1)  # on choisit le premier individu infecté au hasard
    coord_1er_infecte = [x[:, 0][numero_infecte_1], x[:, 1][numero_infecte_1]]  # coordonnées du 1er infecté

    # 1er vague
    df_sans1erinfecte = df[(df['x'] != df['x'][numero_infecte_1]) & (df['y'] != df['y'][numero_infecte_1])]
    for k in range(taille_pop):
        if [df['x'][k], df['y'][k]] == coord_1er_infecte:
            data['coord_infectes'].append(coord_1er_infecte)
        elif distance_e(coord_1er_infecte, [df_sans1erinfecte['x'][k],
                                            df_sans1erinfecte['y'][k]]) < rayon_contamination and chance_infecte(
                infectiosite_2):
            data['coord_infectes'].append([df['x'][k], df['y'][k]])
        else:
            data['coord_sains'].append([df['x'][k], df['y'][k]])

    data['courbe_sains'].append(len(data['coord_sains']))
    data['courbe_infectes'].append(len(data['coord_infectes']))
    data['courbe_immunises'].append(0)
    data['courbe_deces'].append(0)
    data['courbe_removed'].append(0)

    # vagues 2 à n
    while len(data['coord_infectes']) > 0.08 * nb_individu or len(data['courbe_sains']) < 20:  # condition d'arrêt
        coord_infectes1, data['coord_immunises'] = immuniser(data['coord_infectes'], data['coord_immunises'], p_2)
        data['coord_infectes'], data['coord_deces'] = deces(coord_infectes1, data['coord_deces'],
                                                            data['coord_immunises'], d_2)

        for k in range(len(data['coord_infectes'])):
            non_sains = 0
            for j in range(len(data['coord_sains'])):
                if distance_e(data['coord_infectes'][k], data['coord_sains'][j - non_sains]) < rayon_contamination and \
                        data['coord_sains'][j - non_sains] not in data['coord_infectes'] and chance_infecte(
                        infectiosite_2):
                    data['coord_infectes'].append(data['coord_sains'][j - non_sains])
                    data['coord_sains'].remove(data['coord_sains'][j - non_sains])
                    non_sains += 1
        # pour les courbes finales
        data['courbe_sains'].append(len(data['coord_sains']))
        data['courbe_infectes'].append(len(data['coord_infectes']))
        data['courbe_immunises'].append(len(data['coord_immunises']))
        data['courbe_deces'].append(len(data['coord_deces']))
        data['courbe_removed'].append(len(data['coord_immunises']) + len(data['coord_deces']))

    x_courbe = list(np.arange(0, len(data['courbe_sains'])))
    fig.add_trace(
        go.Scatter(x=x_courbe, y=data['courbe_sains'], marker=dict(color='#636EFA', size=1), marker_line=dict(width=2),
                   name="S(t)"), 1, 2)
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_infectes'], marker=dict(color='#EF553B', size=1),
                             marker_line=dict(width=2), name="I(t)"), 1, 2)
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_removed'], marker=dict(color='#000000', size=1),
                             marker_line=dict(width=2), name="R(t)"), 1, 2)
    fig.update_xaxes(title_text="jours", row=1, col=2)
    fig.update_yaxes(title_text="nombre d'individus", row=1, col=2)
    fig.update_traces(
        hoverinfo="name+x+y",
        mode="lines+markers", row=1, col=2,
        showlegend=False
    )
    ##################################

    # création des courbes finales
    data = dict(courbe_sains=[nb_individu - 1], courbe_infectes=[1], courbe_immunises=[0], courbe_deces=[0],
                courbe_removed=[0], coord_infectes=[], coord_sains=[], coord_immunises=[], coord_deces=[])
    x, y = make_blobs(n_samples=nb_individu, centers=1, cluster_std=variance_population)  # création du dataset
    df = pd.DataFrame(dict(x=x[:, 0],
                           y=x[:, 1]))
    numero_infecte_1 = rd.randint(0, taille_pop - 1)  # on choisit le premier individu infecté au hasard
    coord_1er_infecte = [x[:, 0][numero_infecte_1], x[:, 1][numero_infecte_1]]  # coordonnées du 1er infecté

    # 1er vague
    df_sans1erinfecte = df[(df['x'] != df['x'][numero_infecte_1]) & (df['y'] != df['y'][numero_infecte_1])]
    for k in range(taille_pop):
        if [df['x'][k], df['y'][k]] == coord_1er_infecte:
            data['coord_infectes'].append(coord_1er_infecte)
        elif distance_e(coord_1er_infecte, [df_sans1erinfecte['x'][k],
                                            df_sans1erinfecte['y'][k]]) < rayon_contamination and chance_infecte(
            infectiosite_3):
            data['coord_infectes'].append([df['x'][k], df['y'][k]])
        else:
            data['coord_sains'].append([df['x'][k], df['y'][k]])

    data['courbe_sains'].append(len(data['coord_sains']))
    data['courbe_infectes'].append(len(data['coord_infectes']))
    data['courbe_immunises'].append(0)
    data['courbe_deces'].append(0)
    data['courbe_removed'].append(0)

    # vagues 2 à n
    while len(data['coord_infectes']) > 0.08 * nb_individu or len(data['courbe_sains']) < 20:  # condition d'arrêt
        coord_infectes1, data['coord_immunises'] = immuniser(data['coord_infectes'], data['coord_immunises'], p_3)
        data['coord_infectes'], data['coord_deces'] = deces(coord_infectes1, data['coord_deces'],
                                                            data['coord_immunises'], d_3)

        for k in range(len(data['coord_infectes'])):
            non_sains = 0
            for j in range(len(data['coord_sains'])):
                if distance_e(data['coord_infectes'][k], data['coord_sains'][j - non_sains]) < rayon_contamination and \
                        data['coord_sains'][j - non_sains] not in data['coord_infectes'] and chance_infecte(
                    infectiosite_3):
                    data['coord_infectes'].append(data['coord_sains'][j - non_sains])
                    data['coord_sains'].remove(data['coord_sains'][j - non_sains])
                    non_sains += 1
        # pour les courbes finales
        data['courbe_sains'].append(len(data['coord_sains']))
        data['courbe_infectes'].append(len(data['coord_infectes']))
        data['courbe_immunises'].append(len(data['coord_immunises']))
        data['courbe_deces'].append(len(data['coord_deces']))
        data['courbe_removed'].append(len(data['coord_immunises']) + len(data['coord_deces']))

    x_courbe = list(np.arange(0, len(data['courbe_sains'])))
    fig.add_trace(
        go.Scatter(x=x_courbe, y=data['courbe_sains'], marker=dict(color='#636EFA', size=1), marker_line=dict(width=2),
                   name="S(t)"), 2, 1)
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_infectes'], marker=dict(color='#EF553B', size=1),
                             marker_line=dict(width=2), name="I(t)"), 2,1)
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_removed'], marker=dict(color='#000000', size=1),
                             marker_line=dict(width=2), name="R(t)"), 2,1)
    fig.update_xaxes(title_text="jours", row=2, col=1)
    fig.update_yaxes(title_text="nombre d'individus", row=2, col=1)
    fig.update_traces(
        hoverinfo="name+x+y",
        mode="lines+markers", row=2, col=1,
        showlegend=False
    )
    ##################################

    # création des courbes finales
    data = dict(courbe_sains=[nb_individu - 1], courbe_infectes=[1], courbe_immunises=[0], courbe_deces=[0],
                courbe_removed=[0], coord_infectes=[], coord_sains=[], coord_immunises=[], coord_deces=[])
    x, y = make_blobs(n_samples=nb_individu, centers=1, cluster_std=variance_population -0.5)  # création du dataset
    df = pd.DataFrame(dict(x=x[:, 0],
                           y=x[:, 1]))
    numero_infecte_1 = rd.randint(0, taille_pop - 1)  # on choisit le premier individu infecté au hasard
    coord_1er_infecte = [x[:, 0][numero_infecte_1], x[:, 1][numero_infecte_1]]  # coordonnées du 1er infecté

    # 1er vague
    df_sans1erinfecte = df[(df['x'] != df['x'][numero_infecte_1]) & (df['y'] != df['y'][numero_infecte_1])]
    for k in range(taille_pop):
        if [df['x'][k], df['y'][k]] == coord_1er_infecte:
            data['coord_infectes'].append(coord_1er_infecte)
        elif distance_e(coord_1er_infecte, [df_sans1erinfecte['x'][k],
                                            df_sans1erinfecte['y'][k]]) < rayon_contamination and chance_infecte(
            infectiosite_4):
            data['coord_infectes'].append([df['x'][k], df['y'][k]])
        else:
            data['coord_sains'].append([df['x'][k], df['y'][k]])

    data['courbe_sains'].append(len(data['coord_sains']))
    data['courbe_infectes'].append(len(data['coord_infectes']))
    data['courbe_immunises'].append(0)
    data['courbe_deces'].append(0)
    data['courbe_removed'].append(0)

    # vagues 2 à n
    while len(data['coord_infectes']) > 0.08 * nb_individu or len(data['courbe_sains']) < 20:  # condition d'arrêt
        coord_infectes1, data['coord_immunises'] = immuniser(data['coord_infectes'], data['coord_immunises'], p_4)
        data['coord_infectes'], data['coord_deces'] = deces(coord_infectes1, data['coord_deces'],
                                                            data['coord_immunises'], d_4)

        for k in range(len(data['coord_infectes'])):
            non_sains = 0
            for j in range(len(data['coord_sains'])):
                if distance_e(data['coord_infectes'][k], data['coord_sains'][j - non_sains]) < rayon_contamination and \
                        data['coord_sains'][j - non_sains] not in data['coord_infectes'] and chance_infecte(
                    infectiosite_4):
                    data['coord_infectes'].append(data['coord_sains'][j - non_sains])
                    data['coord_sains'].remove(data['coord_sains'][j - non_sains])
                    non_sains += 1
        # pour les courbes finales
        data['courbe_sains'].append(len(data['coord_sains']))
        data['courbe_infectes'].append(len(data['coord_infectes']))
        data['courbe_immunises'].append(len(data['coord_immunises']))
        data['courbe_deces'].append(len(data['coord_deces']))
        data['courbe_removed'].append(len(data['coord_immunises']) + len(data['coord_deces']))

    x_courbe = list(np.arange(0, len(data['courbe_sains'])))
    fig.add_trace(
        go.Scatter(x=x_courbe, y=data['courbe_sains'], marker=dict(color='#636EFA', size=1), marker_line=dict(width=2),
                   name="S(t)"), 2, 2)
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_infectes'], marker=dict(color='#EF553B', size=1),
                             marker_line=dict(width=2), name="I(t)"), 2, 2)
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_removed'], marker=dict(color='#000000', size=1),
                             marker_line=dict(width=2), name="R(t)"), 2, 2)
    fig.update_xaxes(title_text="jours", row=2, col=2)
    fig.update_yaxes(title_text="nombre d'individus", row=2, col=2)
    fig.update_traces(
        hoverinfo="name+x+y",
        mode="lines+markers", row=2, col=2,
        showlegend=False
    )
    ##################################
    fig.update_layout(hovermode="x")
    t = (time.time()-start)
    min = int(round(t,2)//60)
    sec = round(t-min*60,1)
    print('Simulation terminée en '+str(min)+' minutes \net '+str(sec)+' secondes')
    plot(fig)


############################################
#    Github - SIR                          #
############################################


import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Population totale, N.
N = 10000
# Nombre initial de sujets infectés et sauvés (immunisés, guéris, décédés).
I0, R0 = 1, 0
# Tous les autres sont susceptibles d'être touchés.
S0 = N - I0 - R0
# beta le taux de contact et et gamma le taux de rétablissement moyen (en 1/jours).
beta, gamma = 0.6, 1.0/7.0
# la grille de temps pour le graphique (en jours)
t = np.linspace(0, 90, 90)

# Les équations différentielles du modèle SIR.
def deriv(y, t, N, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

# vecteur initial
y0 = S0, I0, R0
# Lance l'intégration des équations différentielles
ret = odeint(deriv, y0, t, args=(N, beta, gamma))

S, I, R = ret.T

# Trace les courbes
fig = go.Figure()
fig.update_layout(title_text="Modèle SIR")

fig.add_trace(
    go.Scatter(x=t, y=S, marker=dict(color='#636EFA', size=1), marker_line=dict(width=0.5),
               name="sains"))
fig.add_trace(
    go.Scatter(x=t, y=I, marker=dict(color='#EF553B',size=1), marker_line=dict(width=1),
               name="infectés" ))
fig.add_trace(
    go.Scatter(x=t, y=R, marker=dict(color='#000000', size=1), marker_line=dict(width=1),
               name="removed"))

fig.update_xaxes(title_text="jours")
plot(fig)


def subplot_comparaison_SIR():

    print('Début de la simulation ... \n')
    start = time.time()

    nb_individu = 1000 # recommandé : 1000
    variance_population = 1
    rayon_contamination = 0.5

    infectiosite_1 = 0.2
    p_1 = 0.
    d_1 = 0.6
    infectiosite_2 = 0.5
    p_2 = 0.
    d_2 = 0.5
    infectiosite_3 = 1
    p_3 = 0.
    d_3 = 0.1

    # création des figures
    fig = make_subplots(rows=3, cols=2,
                        subplot_titles=["Ro=0.3, SIR", "Ro=0.3, Python","Ro=1, SIR", "Ro=1, Python","Ro=10, SIR", "Ro=10, Python"],
                        specs=[[{'type': 'xy'}, {'type': 'xy'}], [{'type': 'xy'}, {'type': 'xy'}], [{'type': 'xy'}, {'type': 'xy'}]])

    ##############################

    N = nb_individu
    # Nombre initial de sujets infectés et sauvés (immunisés, guéris, décédés).
    I0, R0 = 1, 0
    # Tous les autres sont susceptibles d'être touchés.
    S0 = N - I0 - R0
    # beta le taux de contact et gamma le taux de rétablissement moyen (en 1/jours).
    beta, gamma = infectiosite_1, d_1
    # la grille de temps pour le graphique (en jours)
    t = np.linspace(0, 90, 90)

    # vecteur initial
    y0 = S0, I0, R0
    # Lance l'intégration des équations différentielles
    ret = odeint(deriv, y0, t, args=(N, beta, gamma))

    S, I, R = ret.T

    # on calcule le total des décès sur la base du taux de mortalité

    D = np.cumsum(I * 0.005)

    # Trace les courbes

    fig.add_trace(
        go.Scatter(x=t, y=S, marker=dict(color='#636EFA', size=1), marker_line=dict(width=0.5),
                   name="S(t)"),1,1)
    fig.add_trace(
        go.Scatter(x=t, y=I, marker=dict(color='#EF553B', size=1), marker_line=dict(width=1),
                   name="I(t)"),1,1)
    fig.add_trace(
        go.Scatter(x=t, y=R, marker=dict(color='#000000', size=1), marker_line=dict(width=1),
                   name="R(t)"),1,1)

    fig.update_yaxes(title_text="individus",row=1,col=1)

    ###############################

    # création des courbes finales
    data = dict(courbe_sains = [nb_individu-1],courbe_infectes = [1],courbe_immunises = [0],courbe_deces = [0],courbe_removed = [0],coord_infectes=[],coord_sains=[],coord_immunises=[],coord_deces=[])


    # dataset
    x, y = make_blobs(n_samples=nb_individu, centers=3, cluster_std=variance_population+2)  # création du dataset
    df = pd.DataFrame(dict(x=x[:,0],
                           y=x[:,1]))
    taille_pop = len(x)

    numero_infecte_1 = rd.randint(0, taille_pop-1)  # on choisit le premier individu infecté au hasard
    coord_1er_infecte = [x[:, 0][numero_infecte_1], x[:, 1][numero_infecte_1]]  # coordonnées du 1er infecté

    # 1er vague
    df_sans1erinfecte = df[(df['x'] != df['x'][numero_infecte_1]) & (df['y'] != df['y'][numero_infecte_1])]
    for k in range(taille_pop):
        if [df['x'][k], df['y'][k]] == coord_1er_infecte:
            data['coord_infectes'].append(coord_1er_infecte)
        elif distance_e(coord_1er_infecte, [df_sans1erinfecte['x'][k],df_sans1erinfecte['y'][k]]) < rayon_contamination and chance_infecte(infectiosite_1):
            data['coord_infectes'].append([df['x'][k], df['y'][k]])
        else:
            data['coord_sains'].append([df['x'][k], df['y'][k]])

    data['courbe_sains'].append(len(data['coord_sains']))
    data['courbe_infectes'].append(len(data['coord_infectes']))
    data['courbe_immunises'].append(0)
    data['courbe_deces'].append(0)
    data['courbe_removed'].append(0)

    # vagues 2 à n
    while len(data['coord_infectes']) > 0.08*nb_individu or len(data['courbe_sains']) < 20: #condition d'arrêt
        coord_infectes1, data['coord_immunises'] = immuniser(data['coord_infectes'], data['coord_immunises'], p_1)
        data['coord_infectes'], data['coord_deces'] = deces(coord_infectes1, data['coord_deces'], data['coord_immunises'], d_1)

        for k in range(len(data['coord_infectes'])):
            non_sains = 0
            for j in range(len(data['coord_sains'])):
                if distance_e(data['coord_infectes'][k],data['coord_sains'][j-non_sains]) < rayon_contamination and data['coord_sains'][j-non_sains] not in data['coord_infectes'] and chance_infecte(infectiosite_1):
                    data['coord_infectes'].append(data['coord_sains'][j-non_sains])
                    data['coord_sains'].remove(data['coord_sains'][j-non_sains])
                    non_sains+=1
        # pour les courbes finales
        data['courbe_sains'].append(len(data['coord_sains']))
        data['courbe_infectes'].append(len(data['coord_infectes']))
        data['courbe_immunises'].append(len(data['coord_immunises']))
        data['courbe_deces'].append(len(data['coord_deces']))
        data['courbe_removed'].append(len(data['coord_immunises']) + len(data['coord_deces']))


    x_courbe = list(np.arange(0, len(data['courbe_sains'])))
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_sains'], marker=dict(color='#636EFA',size=1), name="S(t)" ),1,2)
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_infectes'], marker=dict(color='#EF553B',size=1), name="I(t)" ),1,2)
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_removed'], marker=dict(color='#000000',size=1),  name="R(t)"),1,2)
    fig.update_traces(
        hoverinfo="name+x+y",
        mode="lines+markers",
        row=1,col=2,
        showlegend=False
        )

    ###################################

    N = nb_individu
    # Nombre initial de sujets infectés et sauvés (immunisés, guéris, décédés).
    I0, R0 = 1, 0
    # Tous les autres sont susceptibles d'être touchés.
    S0 = N - I0 - R0
    # beta le taux de contact et gamma le taux de rétablissement moyen (en 1/jours).
    beta, gamma = infectiosite_2+0.16, d_2
    # la grille de temps pour le graphique (en jours)
    t = np.linspace(0, 90, 90)

    # vecteur initial
    y0 = S0, I0, R0
    # Lance l'intégration des équations différentielles
    ret = odeint(deriv, y0, t, args=(N, beta, gamma))

    S, I, R = ret.T

    # on calcule le total des décès sur la base du taux de mortalité

    D = np.cumsum(I * 0.005)

    # Trace les courbes

    fig.add_trace(
        go.Scatter(x=t, y=S, marker=dict(color='#636EFA', size=1), marker_line=dict(width=0.5),
                   name="sains"),2,1)
    fig.add_trace(
        go.Scatter(x=t, y=I, marker=dict(color='#EF553B', size=1), marker_line=dict(width=1),
                   name="infectés"),2,1)
    fig.add_trace(
        go.Scatter(x=t, y=R, marker=dict(color='#000000', size=1), marker_line=dict(width=1),
                   name="removed"),2,1)

    fig.update_yaxes(title_text="individus",row=2,col=1)
    fig.update_traces(showlegend=False,row=2,col=1)

    ###############################

    # création des courbes finales
    data = dict(courbe_sains=[nb_individu - 1], courbe_infectes=[1], courbe_immunises=[0], courbe_deces=[0],
                courbe_removed=[0], coord_infectes=[], coord_sains=[], coord_immunises=[], coord_deces=[])
    x, y = make_blobs(n_samples=nb_individu, centers=2, cluster_std=variance_population +0.25)  # création du dataset
    df = pd.DataFrame(dict(x=x[:, 0],
                           y=x[:, 1]))
    numero_infecte_1 = rd.randint(0, taille_pop - 1)  # on choisit le premier individu infecté au hasard
    coord_1er_infecte = [x[:, 0][numero_infecte_1], x[:, 1][numero_infecte_1]]  # coordonnées du 1er infecté

    # 1er vague
    df_sans1erinfecte = df[(df['x'] != df['x'][numero_infecte_1]) & (df['y'] != df['y'][numero_infecte_1])]
    for k in range(taille_pop):
        if [df['x'][k], df['y'][k]] == coord_1er_infecte:
            data['coord_infectes'].append(coord_1er_infecte)
        elif distance_e(coord_1er_infecte, [df_sans1erinfecte['x'][k],
                                            df_sans1erinfecte['y'][k]]) < rayon_contamination and chance_infecte(
            infectiosite_2):
            data['coord_infectes'].append([df['x'][k], df['y'][k]])
        else:
            data['coord_sains'].append([df['x'][k], df['y'][k]])

    data['courbe_sains'].append(len(data['coord_sains']))
    data['courbe_infectes'].append(len(data['coord_infectes']))
    data['courbe_immunises'].append(0)
    data['courbe_deces'].append(0)
    data['courbe_removed'].append(0)

    # vagues 2 à n
    while len(data['coord_infectes']) > 0.08 * nb_individu or len(data['courbe_sains']) < 20:  # condition d'arrêt
        coord_infectes1, data['coord_immunises'] = immuniser(data['coord_infectes'], data['coord_immunises'], p_2)
        data['coord_infectes'], data['coord_deces'] = deces(coord_infectes1, data['coord_deces'],
                                                            data['coord_immunises'], d_2)

        for k in range(len(data['coord_infectes'])):
            non_sains = 0
            for j in range(len(data['coord_sains'])):
                if distance_e(data['coord_infectes'][k], data['coord_sains'][j - non_sains]) < rayon_contamination and \
                        data['coord_sains'][j - non_sains] not in data['coord_infectes'] and chance_infecte(
                    infectiosite_2):
                    data['coord_infectes'].append(data['coord_sains'][j - non_sains])
                    data['coord_sains'].remove(data['coord_sains'][j - non_sains])
                    non_sains += 1
        # pour les courbes finales
        data['courbe_sains'].append(len(data['coord_sains']))
        data['courbe_infectes'].append(len(data['coord_infectes']))
        data['courbe_immunises'].append(len(data['coord_immunises']))
        data['courbe_deces'].append(len(data['coord_deces']))
        data['courbe_removed'].append(len(data['coord_immunises']) + len(data['coord_deces']))

    x_courbe = list(np.arange(0, len(data['courbe_sains'])))
    fig.add_trace(
        go.Scatter(x=x_courbe, y=data['courbe_sains'], marker=dict(color='#636EFA', size=1),
                   name="S(t)"), 2, 2)
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_infectes'], marker=dict(color='#EF553B', size=1),
                              name="I(t)"), 2, 2)
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_removed'], marker=dict(color='#000000', size=1),
                              name="R(t)"), 2, 2)
    fig.update_traces(
        hoverinfo="name+x+y",
        mode="lines+markers", row=2, col=2,
        showlegend=False
    )

    ##################################

    N = nb_individu
    # Nombre initial de sujets infectés et sauvés (immunisés, guéris, décédés).
    I0, R0 = 1, 0
    # Tous les autres sont susceptibles d'être touchés.
    S0 = N - I0 - R0
    # beta le taux de contact et gamma le taux de rétablissement moyen (en 1/jours).
    beta, gamma = infectiosite_3, d_3
    # la grille de temps pour le graphique (en jours)
    t = np.linspace(0, 90, 90)

    # vecteur initial
    y0 = S0, I0, R0
    # Lance l'intégration des équations différentielles
    ret = odeint(deriv, y0, t, args=(N, beta, gamma))

    S, I, R = ret.T

    # on calcule le total des décès sur la base du taux de mortalité

    D = np.cumsum(I * 0.005)

    # Trace les courbes

    fig.add_trace(
        go.Scatter(x=t, y=S, marker=dict(color='#636EFA', size=1), marker_line=dict(width=0.5),
                   name="sains"), 3, 1)
    fig.add_trace(
        go.Scatter(x=t, y=I, marker=dict(color='#EF553B', size=1), marker_line=dict(width=1),
                   name="infectés"), 3, 1)
    fig.add_trace(
        go.Scatter(x=t, y=R, marker=dict(color='#000000', size=1), marker_line=dict(width=1),
                   name="removed"), 3, 1)

    fig.update_xaxes(title_text="jours", row=3, col=1)
    fig.update_yaxes(title_text="individus", row=3, col=1)
    fig.update_traces(showlegend=False, row=3, col=1)

    ###############################

    # création des courbes finales
    data = dict(courbe_sains=[nb_individu - 1], courbe_infectes=[1], courbe_immunises=[0], courbe_deces=[0],
                courbe_removed=[0], coord_infectes=[], coord_sains=[], coord_immunises=[], coord_deces=[])
    x, y = make_blobs(n_samples=nb_individu, centers=1, cluster_std=variance_population-0.2)  # création du dataset
    df = pd.DataFrame(dict(x=x[:, 0],
                           y=x[:, 1]))
    numero_infecte_1 = rd.randint(0, taille_pop - 1)  # on choisit le premier individu infecté au hasard
    coord_1er_infecte = [x[:, 0][numero_infecte_1], x[:, 1][numero_infecte_1]]  # coordonnées du 1er infecté

    # 1er vague
    df_sans1erinfecte = df[(df['x'] != df['x'][numero_infecte_1]) & (df['y'] != df['y'][numero_infecte_1])]
    for k in range(taille_pop):
        if [df['x'][k], df['y'][k]] == coord_1er_infecte:
            data['coord_infectes'].append(coord_1er_infecte)
        elif distance_e(coord_1er_infecte, [df_sans1erinfecte['x'][k],
                                            df_sans1erinfecte['y'][k]]) < rayon_contamination and chance_infecte(
            infectiosite_3):
            data['coord_infectes'].append([df['x'][k], df['y'][k]])
        else:
            data['coord_sains'].append([df['x'][k], df['y'][k]])

    data['courbe_sains'].append(len(data['coord_sains']))
    data['courbe_infectes'].append(len(data['coord_infectes']))
    data['courbe_immunises'].append(0)
    data['courbe_deces'].append(0)
    data['courbe_removed'].append(0)

    # vagues 2 à n
    while len(data['coord_infectes']) > 0.08 * nb_individu or len(data['courbe_sains']) < 20:  # condition d'arrêt
        coord_infectes1, data['coord_immunises'] = immuniser(data['coord_infectes'], data['coord_immunises'], p_3)
        data['coord_infectes'], data['coord_deces'] = deces(coord_infectes1, data['coord_deces'],
                                                            data['coord_immunises'], d_3)

        for k in range(len(data['coord_infectes'])):
            non_sains = 0
            for j in range(len(data['coord_sains'])):
                if distance_e(data['coord_infectes'][k], data['coord_sains'][j - non_sains]) < rayon_contamination and \
                        data['coord_sains'][j - non_sains] not in data['coord_infectes'] and chance_infecte(
                    infectiosite_3):
                    data['coord_infectes'].append(data['coord_sains'][j - non_sains])
                    data['coord_sains'].remove(data['coord_sains'][j - non_sains])
                    non_sains += 1
        # pour les courbes finales
        data['courbe_sains'].append(len(data['coord_sains']))
        data['courbe_infectes'].append(len(data['coord_infectes']))
        data['courbe_immunises'].append(len(data['coord_immunises']))
        data['courbe_deces'].append(len(data['coord_deces']))
        data['courbe_removed'].append(len(data['coord_immunises']) + len(data['coord_deces']))

    x_courbe = list(np.arange(0, len(data['courbe_sains'])))
    fig.add_trace(
        go.Scatter(x=x_courbe, y=data['courbe_sains'], marker=dict(color='#636EFA', size=1),
                   name="S(t)"), 3, 2)
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_infectes'], marker=dict(color='#EF553B', size=1),
                              name="I(t)"), 3, 2)
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_removed'], marker=dict(color='#000000', size=1),
                              name="R(t)"), 3, 2)
    fig.update_xaxes(title_text="jours", row=3, col=2)
    fig.update_traces(
        hoverinfo="name+x+y",
        mode="lines+markers", row=3, col=2)
    fig.update_traces(showlegend=False, row=3, col=2)

    #################################
    fig.update_layout(hovermode="x")
    t = (time.time()-start)
    min = int(round(t,2)//60)
    sec = round(t-min*60,1)
    print('Simulation terminée en '+str(min)+' minutes \net '+str(sec)+' secondes')
    plot(fig)


############################################
#    Github - SIDR    #
############################################

# Population totale, N.
N = 10000
# Nombre initial de sujets infectés et sauvés (immunisés, guéris, décédés).
I0, D0, R0 = 1, 0, 0
# Tous les autres sont susceptibles d'être touchés.
S0 = N - I0 - R0 - D0
# beta le taux de contact, mu guérison et théta mort
beta, mu, theta = 0.6, 0.28, 0.13
# la grille de temps pour le graphique (en jours)
t = np.linspace(0, 90, 90)

def deriv(y, t, N, beta, mu, theta):
    S, I, D, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - (mu+theta) * I
    dDdt = theta * I
    dRdt = mu * I
    return dSdt, dIdt, dDdt, dRdt

# vecteur initial
y0 = S0, I0, D0, R0
# Lance l'intégration des équations différentielles
ret = odeint(deriv, y0, t, args=(N, beta,mu, theta))

S, I, D, R = ret.T

# Trace les courbes
fig = go.Figure()
fig.update_layout(title_text="Modèle SIDR")

fig.add_trace(
    go.Scatter(x=t, y=S, marker=dict(color='#636EFA', size=1), marker_line=dict(width=0.5),
               name="sains"))
fig.add_trace(
    go.Scatter(x=t, y=I, marker=dict(color='#EF553B',size=1), marker_line=dict(width=1),
               name="infectés" ))
fig.add_trace(
    go.Scatter(x=t, y=D, marker=dict(color='#AB63FA', size=1), marker_line=dict(width=1),
               name="Décès"))
fig.add_trace(
    go.Scatter(x=t, y=R, marker=dict(color='#00CC96', size=1), marker_line=dict(width=1),
               name="guéris"))

fig.update_xaxes(title_text="jours")
plot(fig)


def subplot_comparaison_SIDR():

    print('Début de la simulation ... \n')
    start = time.time()

    nb_individu = 2000 # recommandé : 1000
    variance_population = 1
    rayon_contamination = 0.5

    infectiosite_1 = 0.3
    p_1 = 0.4
    d_1 = 0.1
    infectiosite_2 = 0.6
    p_2 = 0.28
    d_2 = 0.13
    infectiosite_3 = 0.85
    p_3 = 0.1
    d_3 = 0.09
    # création des figures
    fig = make_subplots(rows=3, cols=2,
                        subplot_titles=["β=0.3, θ=0.1, μ=0.4, SIDR", "β=0.3, θ=0.1, μ=0.4, Python","β=0.6, θ=0.28, μ=0.13, SIDR", "β=0.6, θ=0.28, μ=0.13, Python","β=0.85, θ=0.1, μ=0.09, SIDR", "β=0.85, θ=0.1, μ=0.09, Python"])
    # Population totale, N.
    N = nb_individu
    # Nombre initial de sujets infectés et sauvés (immunisés, guéris, décédés).
    I0, D0, R0 = 1, 0, 0
    # Tous les autres sont susceptibles d'être touchés.
    S0 = N - I0 - R0 - D0
    # beta le taux de contact, mu guérison et théta mort
    beta, mu, theta = infectiosite_1, p_1, d_1
    # la grille de temps pour le graphique (en jours)
    t = np.linspace(0, 90, 90)

    # vecteur initial
    y0 = S0, I0, D0, R0
    # Lance l'intégration des équations différentielles
    ret = odeint(deriv, y0, t, args=(N, beta, mu, theta))

    S, I, D, R = ret.T

    # Trace les courbes
    fig.update_layout(title_text="Modèle SIDR")

    fig.add_trace(
        go.Scatter(x=t, y=S, marker=dict(color='#636EFA', size=1), marker_line=dict(width=0.5),
                   name="S(t)"),1,1)
    fig.add_trace(
        go.Scatter(x=t, y=I, marker=dict(color='#EF553B', size=1), marker_line=dict(width=1),
                   name="I(t)"),1,1)
    fig.add_trace(
        go.Scatter(x=t, y=D, marker=dict(color='#AB63FA', size=1), marker_line=dict(width=1),
                   name="D(t)"),1,1)
    fig.add_trace(
        go.Scatter(x=t, y=R, marker=dict(color='#00CC96', size=1), marker_line=dict(width=1),
                   name="R(t)"),1,1)
    fig.update_yaxes(title_text="individus",row=1,col=1)

    ###############################

    # création des courbes finales
    data = dict(courbe_sains = [nb_individu-1],courbe_infectes = [1],courbe_immunises = [0],courbe_deces = [0],courbe_removed = [0],coord_infectes=[],coord_sains=[],coord_immunises=[],coord_deces=[])


    # dataset
    x, y = make_blobs(n_samples=nb_individu, centers=3, cluster_std=variance_population+2)  # création du dataset
    df = pd.DataFrame(dict(x=x[:,0],
                           y=x[:,1]))
    taille_pop = len(x)

    numero_infecte_1 = rd.randint(0, taille_pop-1)  # on choisit le premier individu infecté au hasard
    coord_1er_infecte = [x[:, 0][numero_infecte_1], x[:, 1][numero_infecte_1]]  # coordonnées du 1er infecté

    # 1er vague
    df_sans1erinfecte = df[(df['x'] != df['x'][numero_infecte_1]) & (df['y'] != df['y'][numero_infecte_1])]
    for k in range(taille_pop):
        if [df['x'][k], df['y'][k]] == coord_1er_infecte:
            data['coord_infectes'].append(coord_1er_infecte)
        elif distance_e(coord_1er_infecte, [df_sans1erinfecte['x'][k],df_sans1erinfecte['y'][k]]) < rayon_contamination and chance_infecte(infectiosite_1):
            data['coord_infectes'].append([df['x'][k], df['y'][k]])
        else:
            data['coord_sains'].append([df['x'][k], df['y'][k]])

    data['courbe_sains'].append(len(data['coord_sains']))
    data['courbe_infectes'].append(len(data['coord_infectes']))
    data['courbe_immunises'].append(0)
    data['courbe_deces'].append(0)
    data['courbe_removed'].append(0)

    # vagues 2 à n
    while len(data['coord_infectes']) > 0.08*nb_individu or len(data['courbe_sains']) < 20: #condition d'arrêt
        coord_infectes1, data['coord_immunises'] = immuniser(data['coord_infectes'], data['coord_immunises'], p_1)
        data['coord_infectes'], data['coord_deces'] = deces(coord_infectes1, data['coord_deces'], data['coord_immunises'], d_1)

        for k in range(len(data['coord_infectes'])):
            non_sains = 0
            for j in range(len(data['coord_sains'])):
                if distance_e(data['coord_infectes'][k],data['coord_sains'][j-non_sains]) < rayon_contamination and data['coord_sains'][j-non_sains] not in data['coord_infectes'] and chance_infecte(infectiosite_1):
                    data['coord_infectes'].append(data['coord_sains'][j-non_sains])
                    data['coord_sains'].remove(data['coord_sains'][j-non_sains])
                    non_sains+=1
        # pour les courbes finales
        data['courbe_sains'].append(len(data['coord_sains']))
        data['courbe_infectes'].append(len(data['coord_infectes']))
        data['courbe_immunises'].append(len(data['coord_immunises']))
        data['courbe_deces'].append(len(data['coord_deces']))
        data['courbe_removed'].append(len(data['coord_immunises']) + len(data['coord_deces']))


    x_courbe = list(np.arange(0, len(data['courbe_sains'])))
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_sains'], marker=dict(color='#636EFA',size=1), name="S(t)" ),1,2)
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_infectes'], marker=dict(color='#EF553B',size=1), name="I(t)" ),1,2)
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_immunises'], marker=dict(color='#00CC96',size=1), name="immunisés"),1,2)
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_deces'], marker=dict(color='#AB63FA',size=1), name="décédés"),1,2)
    fig.update_traces(
        hoverinfo="name+x+y",
        mode="lines+markers",
        row=1,col=2,
        showlegend=False
        )

    ###################################

    # Population totale, N.
    N = nb_individu
    # Nombre initial de sujets infectés et sauvés (immunisés, guéris, décédés).
    I0, D0, R0 = 1, 0, 0
    # Tous les autres sont susceptibles d'être touchés.
    S0 = N - I0 - R0 - D0
    # beta le taux de contact, mu guérison et théta mort
    beta, mu, theta = infectiosite_2, p_2, d_2
    # la grille de temps pour le graphique (en jours)
    t = np.linspace(0, 90, 90)

    # vecteur initial
    y0 = S0, I0, D0, R0
    # Lance l'intégration des équations différentielles
    ret = odeint(deriv, y0, t, args=(N, beta, mu, theta))

    S, I, D, R = ret.T

    # Trace les courbes
    fig.update_layout(title_text="Modèle SIDR")

    fig.add_trace(
        go.Scatter(x=t, y=S, marker=dict(color='#636EFA', size=1), marker_line=dict(width=0.5),
                   name="S(t)"), 2, 1)
    fig.add_trace(
        go.Scatter(x=t, y=I, marker=dict(color='#EF553B', size=1), marker_line=dict(width=1),
                   name="I(t)"), 2, 1)
    fig.add_trace(
        go.Scatter(x=t, y=D, marker=dict(color='#AB63FA', size=1), marker_line=dict(width=1),
                   name="D(t)"), 2, 1)
    fig.add_trace(
        go.Scatter(x=t, y=R, marker=dict(color='#00CC96', size=1), marker_line=dict(width=1),
                   name="R(t)"),2,1)
    fig.update_yaxes(title_text="individus",row=2,col=1)
    fig.update_traces(showlegend=False,row=2,col=1)

    ###############################

    # création des courbes finales
    data = dict(courbe_sains=[nb_individu - 1], courbe_infectes=[1], courbe_immunises=[0], courbe_deces=[0],
                courbe_removed=[0], coord_infectes=[], coord_sains=[], coord_immunises=[], coord_deces=[])
    x, y = make_blobs(n_samples=nb_individu, centers=2, cluster_std=variance_population +0.3)  # création du dataset
    df = pd.DataFrame(dict(x=x[:, 0],
                           y=x[:, 1]))
    numero_infecte_1 = rd.randint(0, taille_pop - 1)  # on choisit le premier individu infecté au hasard
    coord_1er_infecte = [x[:, 0][numero_infecte_1], x[:, 1][numero_infecte_1]]  # coordonnées du 1er infecté

    # 1er vague
    df_sans1erinfecte = df[(df['x'] != df['x'][numero_infecte_1]) & (df['y'] != df['y'][numero_infecte_1])]
    for k in range(taille_pop):
        if [df['x'][k], df['y'][k]] == coord_1er_infecte:
            data['coord_infectes'].append(coord_1er_infecte)
        elif distance_e(coord_1er_infecte, [df_sans1erinfecte['x'][k],
                                            df_sans1erinfecte['y'][k]]) < rayon_contamination and chance_infecte(
            infectiosite_2):
            data['coord_infectes'].append([df['x'][k], df['y'][k]])
        else:
            data['coord_sains'].append([df['x'][k], df['y'][k]])

    data['courbe_sains'].append(len(data['coord_sains']))
    data['courbe_infectes'].append(len(data['coord_infectes']))
    data['courbe_immunises'].append(0)
    data['courbe_deces'].append(0)
    data['courbe_removed'].append(0)

    # vagues 2 à n
    while len(data['coord_infectes']) > 0.08 * nb_individu or len(data['courbe_sains']) < 20:  # condition d'arrêt
        coord_infectes1, data['coord_immunises'] = immuniser(data['coord_infectes'], data['coord_immunises'], p_2)
        data['coord_infectes'], data['coord_deces'] = deces(coord_infectes1, data['coord_deces'],
                                                            data['coord_immunises'], d_2)

        for k in range(len(data['coord_infectes'])):
            non_sains = 0
            for j in range(len(data['coord_sains'])):
                if distance_e(data['coord_infectes'][k], data['coord_sains'][j - non_sains]) < rayon_contamination and \
                        data['coord_sains'][j - non_sains] not in data['coord_infectes'] and chance_infecte(
                    infectiosite_2):
                    data['coord_infectes'].append(data['coord_sains'][j - non_sains])
                    data['coord_sains'].remove(data['coord_sains'][j - non_sains])
                    non_sains += 1
        # pour les courbes finales
        data['courbe_sains'].append(len(data['coord_sains']))
        data['courbe_infectes'].append(len(data['coord_infectes']))
        data['courbe_immunises'].append(len(data['coord_immunises']))
        data['courbe_deces'].append(len(data['coord_deces']))
        data['courbe_removed'].append(len(data['coord_immunises']) + len(data['coord_deces']))

    x_courbe = list(np.arange(0, len(data['courbe_sains'])))
    fig.add_trace(
        go.Scatter(x=x_courbe, y=data['courbe_sains'], marker=dict(color='#636EFA', size=1),
                   name="S(t)"), 2, 2)
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_infectes'], marker=dict(color='#EF553B', size=1),
                              name="I(t)"), 2, 2)
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_immunises'], marker=dict(color='#00CC96',size=1), name="immunisés"),2,2)
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_deces'], marker=dict(color='#AB63FA',size=1), name="décédés"),2,2)
    fig.update_traces(
        hoverinfo="name+x+y",
        mode="lines+markers", row=2, col=2,
        showlegend=False
    )

    ##################################

    # Population totale, N.
    N = nb_individu
    # Nombre initial de sujets infectés et sauvés (immunisés, guéris, décédés).
    I0, D0, R0 = 1, 0, 0
    # Tous les autres sont susceptibles d'être touchés.
    S0 = N - I0 - R0 - D0
    # beta le taux de contact, mu guérison et théta mort
    beta, mu, theta = infectiosite_3, p_3, d_3
    # la grille de temps pour le graphique (en jours)
    t = np.linspace(0, 90, 90)

    # vecteur initial
    y0 = S0, I0, D0, R0
    # Lance l'intégration des équations différentielles
    ret = odeint(deriv, y0, t, args=(N, beta, mu, theta))

    S, I, D, R = ret.T

    # Trace les courbes
    fig.update_layout(title_text="Modèle SIDR")

    fig.add_trace(
        go.Scatter(x=t, y=S, marker=dict(color='#636EFA', size=1), marker_line=dict(width=0.5),
                   name="S(t)"), 3, 1)
    fig.add_trace(
        go.Scatter(x=t, y=I, marker=dict(color='#EF553B', size=1), marker_line=dict(width=1),
                   name="I(t)"), 3, 1)
    fig.add_trace(
        go.Scatter(x=t, y=D, marker=dict(color='#AB63FA', size=1), marker_line=dict(width=1),
                   name="D(t)"), 3, 1)
    fig.add_trace(
        go.Scatter(x=t, y=R, marker=dict(color='#00CC96', size=1), marker_line=dict(width=1),
                   name="R(t)"),3,1)

    fig.update_xaxes(title_text="jours", row=3, col=1)
    fig.update_yaxes(title_text="individus", row=3, col=1)
    fig.update_traces(showlegend=False, row=3, col=1)

    ###############################

    # création des courbes finales
    data = dict(courbe_sains=[nb_individu - 1], courbe_infectes=[1], courbe_immunises=[0], courbe_deces=[0],
                courbe_removed=[0], coord_infectes=[], coord_sains=[], coord_immunises=[], coord_deces=[])
    x, y = make_blobs(n_samples=nb_individu, centers=1, cluster_std=0.9)  # création du dataset
    df = pd.DataFrame(dict(x=x[:, 0],
                           y=x[:, 1]))
    numero_infecte_1 = rd.randint(0, taille_pop - 1)  # on choisit le premier individu infecté au hasard
    coord_1er_infecte = [x[:, 0][numero_infecte_1], x[:, 1][numero_infecte_1]]  # coordonnées du 1er infecté

    # 1er vague
    df_sans1erinfecte = df[(df['x'] != df['x'][numero_infecte_1]) & (df['y'] != df['y'][numero_infecte_1])]
    for k in range(taille_pop):
        if [df['x'][k], df['y'][k]] == coord_1er_infecte:
            data['coord_infectes'].append(coord_1er_infecte)
        elif distance_e(coord_1er_infecte, [df_sans1erinfecte['x'][k],
                                            df_sans1erinfecte['y'][k]]) < rayon_contamination and chance_infecte(
            infectiosite_3):
            data['coord_infectes'].append([df['x'][k], df['y'][k]])
        else:
            data['coord_sains'].append([df['x'][k], df['y'][k]])

    data['courbe_sains'].append(len(data['coord_sains']))
    data['courbe_infectes'].append(len(data['coord_infectes']))
    data['courbe_immunises'].append(0)
    data['courbe_deces'].append(0)
    data['courbe_removed'].append(0)

    # vagues 2 à n
    while len(data['coord_infectes']) > 0.08 * nb_individu or len(data['courbe_sains']) < 20:  # condition d'arrêt
        coord_infectes1, data['coord_immunises'] = immuniser(data['coord_infectes'], data['coord_immunises'], p_3+0.1)
        data['coord_infectes'], data['coord_deces'] = deces(coord_infectes1, data['coord_deces'],
                                                            data['coord_immunises'], d_3+0.1)

        for k in range(len(data['coord_infectes'])):
            non_sains = 0
            for j in range(len(data['coord_sains'])):
                if distance_e(data['coord_infectes'][k], data['coord_sains'][j - non_sains]) < rayon_contamination and \
                        data['coord_sains'][j - non_sains] not in data['coord_infectes'] and chance_infecte(
                    infectiosite_3):
                    data['coord_infectes'].append(data['coord_sains'][j - non_sains])
                    data['coord_sains'].remove(data['coord_sains'][j - non_sains])
                    non_sains += 1
        # pour les courbes finales
        data['courbe_sains'].append(len(data['coord_sains']))
        data['courbe_infectes'].append(len(data['coord_infectes']))
        data['courbe_immunises'].append(len(data['coord_immunises']))
        data['courbe_deces'].append(len(data['coord_deces']))
        data['courbe_removed'].append(len(data['coord_immunises']) + len(data['coord_deces']))

    x_courbe = list(np.arange(0, len(data['courbe_sains'])))
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_sains'], marker=dict(color='#636EFA', size=1),name="S(t)"), 3, 2)
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_infectes'], marker=dict(color='#EF553B', size=1),name="I(t)"), 3, 2)
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_immunises'], marker=dict(color='#00CC96',size=1), name="immunisés"),3,2)
    fig.add_trace(go.Scatter(x=x_courbe, y=data['courbe_deces'], marker=dict(color='#AB63FA',size=1),  name="décédés"),3,2)
    fig.update_xaxes(title_text="jours", row=3, col=2)
    fig.update_traces(
        hoverinfo="name+x+y",
        mode="lines+markers", row=3, col=2)
    fig.update_traces(showlegend=False, row=3, col=2)

    #################################
    fig.update_layout(hovermode="x")
    t = (time.time()-start)
    min = int(round(t,2)//60)
    sec = round(t-min*60,1)
    print('Simulation terminée en '+str(min)+' minutes \net '+str(sec)+' secondes')
    plot(fig)
