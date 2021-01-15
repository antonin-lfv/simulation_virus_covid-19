''' modélisation de la propagation d'un virus '''

""" importation """

from typing import List, Any
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.datasets import make_blobs
import random as rd
import dash

""" I) création du dataset """

x, y = make_blobs(n_samples=1000, centers=2, cluster_std=5, shuffle = True)
plt.scatter(x[:, 0], x[:, 1], c='dodgerblue')
plt.title('dataset')
plt.show()


def distance(x, y):  # distance entre 2 points du plan cartésien
    x1 = x[0]
    x2 = x[1]
    y1 = y[0]
    y2 = y[1]
    return (abs(np.sqrt((y1 - x1) ** 2 + (y2 - x2) ** 2)))


def remove_(a, l):
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
    if distance(coord_1er_infecte, [x[:, 0][k], x[:, 1][k]]) < 0.5:
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
        if distance(np.array(coord_infectes)[k, :], np.array(coord_sains)[j, :]) < 0.5 and list(
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
        if distance(np.array(coord_infectes)[k, :], np.array(coord_sains)[j, :]) < 0.5 and np.array(coord_sains)[j,
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
        elif distance(coord_1er_infecte, [x[:, 0][k], x[:, 1][k]]) < rayon_contamination and chance_infecte(
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
            if distance(np.array(coord_infectes)[k, :], np.array(coord_sains)[j, :]) < rayon_contamination and \
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
            if distance(np.array(coord_infectes)[k, :], np.array(coord_sains)[j, :]) < rayon_contamination and list(
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
            if distance(np.array(coord_infectes)[k, :], np.array(coord_sains)[j, :]) < rayon_contamination and list(
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
        elif distance(coord_1er_infecte, [x[:, 0][k], x[:, 1][k]]) < rayon_contamination and chance_infecte(
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
                if distance(np.array(coord_infectes)[k, :],
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
        if distance(coord_1er_infecte, [x[:, 0][k], x[:, 1][k]]) < rayon_contamination and chance_infecte(infectiosite):
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
                if distance(np.array(coord_infectes)[k, :],
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
        elif distance(coord_1er_infecte, [x[:, 0][k], x[:, 1][k]]) < rayon_contamination and chance_infecte(
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
                if distance(np.array(coord_infectes)[k, :],
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



















"""AVEC PLOTLY"""

from plotly.offline import download_plotlyjs, init_notebook_mode, plot,iplot # pour travailler en offline!
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

x, y = make_blobs(n_samples=1000, centers=2, cluster_std=5, shuffle = True)
fig = go.Figure()
fig.add_trace(go.Scatter(x=x[:, 0],y=x[:, 1],mode="markers",marker=dict(color="Blue")))
plot(fig)

nb_individu = 1000
variance_population=5
rayon_contamination=1.2
infectiosite=0.7
p=0.4
d=0.3
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
fig.add_trace(go.Scatter(x=x[:, 0],y=x[:, 1],mode="markers",marker=dict(color="Blue")))
fig.add_trace(go.Scatter(x=[x[:, 0][numero_infecte_1]],y=[x[:, 1][numero_infecte_1]],mode="markers",marker=dict(color="DarkOrange")))
fig.update_layout(title_text="1er infecté",showlegend=False,)
plot(fig)

fig = go.Figure()
labels = ["sains","infectés","immunisés","décédés"]
fig.add_trace(go.Pie(values=[taille_pop-1,1], labels=labels,))
fig.update_layout(title_text="Proportions population")
plot(fig)

courbe_sains.append(taille_pop - 1)
courbe_infectes.append(1)
courbe_immunises.append(0)
courbe_deces.append(0)

#subplots
fig = go.Figure()
fig = make_subplots(rows=2, cols=1,subplot_titles=("population",""),specs=[[{'type':'xy'}], [{'type':'domain'}]])
fig.add_trace(go.Scatter(x=x[:, 0],y=x[:, 1],mode="markers",marker=dict(color="Blue"),showlegend=False),1,1)
fig.add_trace(go.Scatter(x=[x[:, 0][numero_infecte_1]],y=[x[:, 1][numero_infecte_1]],mode="markers",marker=dict(color="DarkOrange"),showlegend=False),1,1)
fig.update_layout(template="simple_white")
labels = ["sains","infectés","immunisés","décédés"]
fig.add_trace(go.Pie(labels=labels, values=[taille_pop-1,1,0,0],sort=False),2,1)
fig.update_xaxes(showgrid=False, visible= False, row=1, col=1)
fig.update_xaxes(showgrid=False, visible= False, row=2, col=1)
fig.update_yaxes(showgrid=False, visible= False,row=1, col=1)
fig.update_yaxes(showgrid=False, visible= False, row=2, col=1)
plot(fig)

""" III) 1er vague """

# Afficher 1er vague avec pourcentage infectés/sains
coord_infectes = []  # cette liste sera implémentée des nouveaux cas
coord_sains = []  # liste des cas sains
fig = go.Figure()
for k in range(taille_pop):
    if [x[:, 0][k], x[:, 1][k]] == coord_1er_infecte:
        coord_infectes.append(coord_1er_infecte)
    elif distance(coord_1er_infecte, [x[:, 0][k], x[:, 1][k]]) < rayon_contamination and chance_infecte(infectiosite):
        fig.add_trace(go.Scatter(x=[x[:, 0][k]], y=[x[:, 1][k]], mode="markers", marker=dict(color="DarkOrange"), showlegend=False))
        coord_infectes.append([x[:, 0][k], x[:, 1][k]])
    else:
        fig.add_trace(go.Scatter(x=[x[:, 0][k]], y=[x[:, 1][k]], mode="markers", marker=dict(color="Blue"), showlegend=False))
        coord_sains.append([x[:, 0][k], x[:, 1][k]])
        fig.add_trace(go.Scatter(x=[x[:, 0][numero_infecte_1]], y=[x[:, 1][numero_infecte_1]], mode="markers",marker=dict(color="DarkOrange"), showlegend=False))
plot(fig)

fig = go.Figure()
labels = ["sains","infectés","immunisés","décédés"]
fig.add_trace(go.Pie(values=[ len(coord_sains),len(coord_infectes),0,0], labels=labels,sort=False))
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
        if distance(np.array(coord_infectes)[k, :], np.array(coord_sains)[j, :]) < rayon_contamination and list(np.array(coord_sains)[j, :]) not in coord_infectes:
            coord_infectes.append(list(np.array(coord_sains)[j, :]))
            non_sains.append(list(np.array(coord_sains)[j, :]))

coord_sains = remove_(coord_sains, non_sains)
fig = go.Figure()
if coord_sains != []:
    fig.add_trace(go.Scatter(x=np.array(coord_sains)[:, 0], y=np.array(coord_sains)[:, 1], mode="markers", marker=dict(color="Blue"), showlegend=False))
if coord_infectes != []:
    fig.add_trace(go.Scatter(x=np.array(coord_infectes)[:, 0], y=np.array(coord_infectes)[:, 1], mode="markers",marker=dict(color="Red"), showlegend=False))
if coord_immunises != []:
    fig.add_trace(go.Scatter(x=np.array(coord_immunises)[:, 0], y=np.array(coord_immunises)[:, 1], mode="markers",marker=dict(color="Green"), showlegend=False))
if coord_deces != []:
    fig.add_trace(go.Scatter(x=np.array(coord_deces)[:, 0], y=np.array(coord_deces)[:, 1], mode="markers",marker=dict(color="Purple"), showlegend=False))
plot(fig)

fig = go.Figure()
labels = ["sains","infectés","immunisés","décédés"]
fig.add_trace(go.Pie(values=[len(coord_sains),len(coord_infectes) ,len(coord_immunises), len(coord_deces)], labels=labels,sort=False))
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
        if distance(np.array(coord_infectes)[k, :], np.array(coord_sains)[j, :]) < rayon_contamination and list(
                np.array(coord_sains)[j, :]) \
                not in coord_infectes and chance_infecte(infectiosite):
            coord_infectes.append(list(np.array(coord_sains)[j, :]))
            non_sains.append(list(np.array(coord_sains)[j, :]))
coord_sains = remove_(coord_sains, non_sains)
fig = go.Figure()
if coord_sains != []:
    fig.add_trace(go.Scatter(x=np.array(coord_sains)[:, 0], y=np.array(coord_sains)[:, 1], mode="markers", marker=dict(color="Blue"), showlegend=False))
if coord_infectes != []:
    fig.add_trace(go.Scatter(x=np.array(coord_infectes)[:, 0], y=np.array(coord_infectes)[:, 1], mode="markers",marker=dict(color="Red"), showlegend=False))
if coord_immunises != []:
    fig.add_trace(go.Scatter(x=np.array(coord_immunises)[:, 0], y=np.array(coord_immunises)[:, 1], mode="markers",marker=dict(color="Green"), showlegend=False))
if coord_deces != []:
    fig.add_trace(go.Scatter(x=np.array(coord_deces)[:, 0], y=np.array(coord_deces)[:, 1], mode="markers",marker=dict(color="Purple"), showlegend=False))
plot(fig)

fig = go.Figure()
labels = ["sains","infectés","immunisés","décédés"]
fig.add_trace(go.Pie(values=[len(coord_sains),len(coord_infectes) ,len(coord_immunises), len(coord_deces)], labels=labels,sort=False))
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
        if distance(np.array(coord_infectes)[k, :], np.array(coord_sains)[j, :]) < rayon_contamination and list(
                np.array(coord_sains)[j, :]) not in \
                coord_infectes and chance_infecte(infectiosite):
            coord_infectes.append(list(np.array(coord_sains)[j, :]))
            non_sains.append(list(np.array(coord_sains)[j, :]))
coord_sains = remove_(coord_sains, non_sains)
fig = go.Figure()
if coord_sains != []:
    fig.add_trace(go.Scatter(x=np.array(coord_sains)[:, 0], y=np.array(coord_sains)[:, 1], mode="markers", marker=dict(color="Blue"), showlegend=False))
if coord_infectes != []:
    fig.add_trace(go.Scatter(x=np.array(coord_infectes)[:, 0], y=np.array(coord_infectes)[:, 1], mode="markers",marker=dict(color="Red"), showlegend=False))
if coord_immunises != []:
    fig.add_trace(go.Scatter(x=np.array(coord_immunises)[:, 0], y=np.array(coord_immunises)[:, 1], mode="markers",marker=dict(color="Green"), showlegend=False))
if coord_deces != []:
    fig.add_trace(go.Scatter(x=np.array(coord_deces)[:, 0], y=np.array(coord_deces)[:, 1], mode="markers",marker=dict(color="Purple"), showlegend=False))
plot(fig)

fig = go.Figure()
labels = ["sains","infectés","immunisés","décédés"]
fig.add_trace(go.Pie(values=[len(coord_sains),len(coord_infectes) ,len(coord_immunises), len(coord_deces)], labels=labels,sort=False))
fig.update_layout(title_text="Proportions population")
plot(fig)

courbe_sains.append(len(coord_sains))
courbe_infectes.append(len(coord_infectes))
courbe_immunises.append(len(coord_immunises))
courbe_deces.append(len(coord_deces))

fig = go.Figure()
x_courbe = list(np.arange(0, len(courbe_sains)))
fig.add_trace(go.Scatter(x=x_courbe,y=courbe_sains,marker=dict(color="Blue")))
fig.add_trace(go.Scatter(x=x_courbe,y=courbe_infectes,marker=dict(color="Red")))
fig.add_trace(go.Scatter(x=x_courbe,y=courbe_immunises,marker=dict(color="Green")))
fig.add_trace(go.Scatter(x=x_courbe,y=courbe_deces,marker=dict(color="Black")))
plot(fig)


def virus_px():

    nb_individu = 1000
    variance_population = 5
    rayon_contamination = 2
    infectiosite = 0.7
    p = 0.4
    d = 0.2

    fig = go.Figure()
    x, y = make_blobs(n_samples=nb_individu, centers=2, cluster_std=variance_population, shuffle=True)
    fig.add_trace(go.Scatter(x=x[:, 0], y=x[:, 1], mode="markers", marker=dict(color="Blue")))
    taille_pop = len(x)

    fig = make_subplots(rows=6, cols=2,column_widths=[0.8, 0.2],specs=[[{'type':'xy'},{'type':'domain'}],[{'type':'xy'},{'type':'domain'}],[{'type':'xy'},{'type':'domain'}],[{'type':'xy'},{'type':'domain'}],[{'type':'xy'},{'type':'domain'}],[{'type':'xy', "colspan": 2},None]])
    courbe_sains = []
    courbe_infectes = []
    courbe_immunises = []
    courbe_deces = []
    "1er infecté"
    numero_infecte_1 = rd.randint(0, taille_pop)
    coord_1er_infecte = [x[:, 0][numero_infecte_1], x[:, 1][numero_infecte_1]]
    fig.add_trace(go.Scatter(x=x[:, 0],y=x[:, 1],mode="markers",marker=dict(color="Blue"),showlegend=False),1,1)
    fig.add_trace(go.Scatter(x=[x[:, 0][numero_infecte_1]],y=[x[:, 1][numero_infecte_1]],mode="markers",marker=dict(color="Red"),showlegend=False),1,1)
    "pie"
    labels = ["sains","infectés","immunisés","décédés"]
    fig.add_trace(go.Pie(labels=labels, values=[taille_pop-1,1,0,0],sort=False),1,2)
    fig.update_xaxes(showgrid=False, visible= False, row=1, col=1)
    fig.update_yaxes(showgrid=False, visible= False, row=1, col=1)
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
            fig.add_trace(go.Scatter(x=[x[:, 0][k]], y=[x[:, 1][k]], mode="markers", marker=dict(color="Red"), showlegend=False),2,1)
            coord_infectes.append([x[:, 0][k], x[:, 1][k]])
        else:
            fig.add_trace(go.Scatter(x=[x[:, 0][k]], y=[x[:, 1][k]], mode="markers", marker=dict(color="Blue"), showlegend=False),2,1)
            coord_sains.append([x[:, 0][k], x[:, 1][k]])
            fig.add_trace(go.Scatter(x=[x[:, 0][numero_infecte_1]], y=[x[:, 1][numero_infecte_1]], mode="markers",marker=dict(color="DarkOrange"), showlegend=False),2,1)
    fig.update_xaxes(showgrid=False, visible=False, row=1, col=1)
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
        fig.add_trace(go.Scatter(x=np.array(coord_sains)[:, 0], y=np.array(coord_sains)[:, 1], mode="markers", marker=dict(color="Blue"), showlegend=False),3,1)
    if coord_infectes != []:
        fig.add_trace(go.Scatter(x=np.array(coord_infectes)[:, 0], y=np.array(coord_infectes)[:, 1], mode="markers",marker=dict(color="Red"), showlegend=False),3,1)
    if coord_immunises != []:
        fig.add_trace(go.Scatter(x=np.array(coord_immunises)[:, 0], y=np.array(coord_immunises)[:, 1], mode="markers",marker=dict(color="Green"), showlegend=False),3,1)
    if coord_deces != []:
        fig.add_trace(go.Scatter(x=np.array(coord_deces)[:, 0], y=np.array(coord_deces)[:, 1], mode="markers",marker=dict(color="Purple"), showlegend=False),3,1)
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
    coord_sains = remove_(coord_sains, non_sains)
    if coord_sains != []:
        fig.add_trace(go.Scatter(x=np.array(coord_sains)[:, 0], y=np.array(coord_sains)[:, 1], mode="markers", marker=dict(color="Blue"), showlegend=False),4,1)
    if coord_infectes != []:
        fig.add_trace(go.Scatter(x=np.array(coord_infectes)[:, 0], y=np.array(coord_infectes)[:, 1], mode="markers",marker=dict(color="Red"), showlegend=False),4,1)
    if coord_immunises != []:
        fig.add_trace(go.Scatter(x=np.array(coord_immunises)[:, 0], y=np.array(coord_immunises)[:, 1], mode="markers",marker=dict(color="Green"), showlegend=False),4,1)
    if coord_deces != []:
        fig.add_trace(go.Scatter(x=np.array(coord_deces)[:, 0], y=np.array(coord_deces)[:, 1], mode="markers",marker=dict(color="Purple"), showlegend=False),4,1)
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
        fig.add_trace(go.Scatter(x=np.array(coord_sains)[:, 0], y=np.array(coord_sains)[:, 1], mode="markers", marker=dict(color="Blue"), showlegend=False),5,1)
    if coord_infectes != []:
        fig.add_trace(go.Scatter(x=np.array(coord_infectes)[:, 0], y=np.array(coord_infectes)[:, 1], mode="markers",marker=dict(color="Red"), showlegend=False),5,1)
    if coord_immunises != []:
        fig.add_trace(go.Scatter(x=np.array(coord_immunises)[:, 0], y=np.array(coord_immunises)[:, 1], mode="markers",marker=dict(color="Green"), showlegend=False),5,1)
    if coord_deces != []:
        fig.add_trace(go.Scatter(x=np.array(coord_deces)[:, 0], y=np.array(coord_deces)[:, 1], mode="markers",marker=dict(color="Purple"), showlegend=False),5,1)
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
    fig.add_trace(go.Scatter(x=x_courbe,y=courbe_sains,marker=dict(color="Blue"), name="sain",showlegend=False),6,1)
    fig.add_trace(go.Scatter(x=x_courbe,y=courbe_infectes,marker=dict(color="Red"), name="infecté",showlegend=False),6,1)
    fig.add_trace(go.Scatter(x=x_courbe,y=courbe_immunises,marker=dict(color="Green"), name="immunisé", showlegend=False),6,1)
    fig.add_trace(go.Scatter(x=x_courbe,y=courbe_deces,marker=dict(color="Black"),name="décédé",showlegend=False),6,1)
    fig.update_traces(
        hoverinfo="name+x+y",
        line={"width": 1.2},
        marker={"size": 6},
        mode="lines+markers",
        showlegend=False, row=2, col=1)
    fig.update_layout(hovermode="x")
    plot(fig)



def vague_seuil_px():

    nb_individu = 500 # recommandé : 1000
    variance_population = 5
    rayon_contamination = 4
    infectiosite = 0.7
    p = 0.5
    d = 0.3

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
    fig = make_subplots(rows=2, cols=2,column_widths=[0.8, 0.2],row_heights=[0.5,0.5],subplot_titles=["population","",""],specs=[[{'type': 'xy'},{'type': 'domain'}],[{'type': 'xy', 'colspan' : 2},None]],horizontal_spacing = 0.05,vertical_spacing=0.05)

    # création des courbes finales
    courbe_sains = []
    courbe_infectes = []
    courbe_immunises = []
    courbe_deces = []

    # dataset
    x, y = make_blobs(n_samples=nb_individu, centers=2, cluster_std=variance_population)  # création du dataset
    taille_pop = len(x)

    numero_infecte_1 = rd.randint(0, taille_pop-1)  # on choisit le premier individu infecté au hasard
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
        elif distance(coord_1er_infecte, [x[:, 0][k], x[:, 1][k]]) < rayon_contamination and chance_infecte(
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
    #for i in range(n - 2):
    i = 1
    while len(courbe_infectes)!=0 and courbe_sains[i-1] > courbe_sains[i] :
        non_sains = []
        coord_infectes1, coord_immunises = immuniser(coord_infectes, coord_immunises, p)
        coord_infectes, coord_deces = deces(coord_infectes1, coord_deces, coord_immunises, d)

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
        i += 1 # vague suivante
    if coord_sains != []:
        fig.add_trace(go.Scatter(x=np.array(coord_sains)[:, 0], y=np.array(coord_sains)[:, 1],name="sain", mode="markers", marker=dict(color='#636EFA'), showlegend=False),1,1)
    if coord_infectes != []:
        fig.add_trace(go.Scatter(x=np.array(coord_infectes)[:, 0], y=np.array(coord_infectes)[:, 1],name="infecté", mode="markers",marker=dict(color='#EF553B'), showlegend=False),1,1)
    if coord_immunises != []:
        fig.add_trace(go.Scatter(x=np.array(coord_immunises)[:, 0], y=np.array(coord_immunises)[:, 1],name='immunisé', mode="markers",marker=dict(color='#00CC96'), showlegend=False),1,1)
    if coord_deces != []:
        fig.add_trace(go.Scatter(x=np.array(coord_deces)[:, 0], y=np.array(coord_deces)[:, 1],name="décédé", mode="markers", marker=dict(color='#AB63FA'), showlegend=False),1,1)
    fig.update_traces(hoverinfo="name")
    fig.update_xaxes(showgrid=False, visible=False, row=1, col=1)
    fig.update_yaxes(showgrid=False, visible=False, row=1, col=1)
    titre = str(i)+'-ième vague'

    labels = ["sains","infectés","immunisés","décédés"]
    fig.add_trace(go.Pie(values=[len(coord_sains),len(coord_infectes) ,len(coord_immunises), len(coord_deces)], labels=labels, sort=False),1,2)

    x_courbe = list(np.arange(0, len(courbe_sains)))
    fig.add_trace(go.Scatter(x=x_courbe, y=courbe_sains, marker=dict(color='#636EFA'), showlegend=False, name="sains", yaxis="y",),2,1)
    fig.add_trace(go.Scatter(x=x_courbe, y=courbe_infectes,  marker=dict(color='#EF553B'), showlegend=False, name="infectés", yaxis="y2",),2,1)
    fig.add_trace(go.Scatter(x=x_courbe, y=courbe_immunises, marker=dict(color='#00CC96'), showlegend=False, name="immunisés", yaxis="y3",),2,1)
    fig.add_trace(go.Scatter(x=x_courbe, y=courbe_deces, marker=dict(color='#AB63FA'), showlegend=False, name="décédés", yaxis="y4",),2,1)
    fig.update_xaxes(title_text="vague", row=2, col=1)
    fig.update_yaxes(title_text="nombre d'individus", row=2, col=1)
    fig.add_annotation(text="Maximum d'infectés", x=courbe_infectes.index(max(courbe_infectes)), # ajouter un texte avec une flèche
                   y=max(courbe_infectes)+0.05*taille_pop, arrowhead=1, showarrow=True,row=2,col=1)
    fig.update_traces(
        hoverinfo="name+x+y",
        line={"width": 1.2},
        marker={"size": 6},
        mode="lines+markers",
        showlegend=False, row=2, col=1)
    fig.update_layout(hovermode="x")
    fig.update_layout(title_text="simulation virus")
    fig.update_layout(title_font_color='#EF553B',)
    plot(fig)






