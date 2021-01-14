''' modélisation de la propagation d'un virus '''

""" importation """

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
import random as rd
import time
from scipy.spatial import distance

def distance_e(x, y):  # distance entre 2 points du plan cartésien
    return distance.euclidean([x[0],x[1]],[y[0],y[1]])

def remove_(a,l): #pour supprimer de la liste des sains (a) les nouveaux infectés (l)
    for i in range (len(l)):
        a.remove(l[i])
    return(list(a))

def chance_infecte(p): #return True si il devient infecté avec une proba p
    proba = int(p*100)
    if rd.randint(0,100) <= proba :
        return(True)
    else :
        return(False)

def immuniser(l, l2, p): #l: infectés; l2: immunisés précédents
    coord_immu = []
    l_p = l[:]  # création d'une copie pour éviter d'erreur d'indice
    for i in range(len(l_p)):
        proba = int(p * 100)
        if rd.randint(0, 100) <= proba:
            coord_immu.append(l_p[i])
            l.remove(l_p[i])
    coord_immu += l2 #on ajoute les immunisés précédents
    return list(l), coord_immu

def deces(l, l2, l3, p): #l: infectés; l2: décès précédents; l3: immunisés
    coord_deces = []
    l_p = l[:] # création d'une copie pour éviter d'erreur d'indice
    for i in range(len(l_p)):
        proba = int(p * 100)
        if rd.randint(0, 100) <= proba and l_p[i] not in l3:
            coord_deces.append(l_p[i])
            l.remove(l_p[i])
    coord_deces += l2 #on ajoute les décès précédents
    return list(l), coord_deces
 
    
""" Afficher la vague où le virus ne circule plus, avec les graphiques  """

## version non optimisée, voir version plotly

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
    #for i in range(n - 2):
    i = 1
    while len(coord_infectes)>0.2*taille_pop or len(courbe_sains)<5 :
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
        ax1.scatter(np.array(coord_sains)[:, 0], np.array(coord_sains)[:, 1], c='dodgerblue')
    if coord_infectes != []:
        ax1.scatter(np.array(coord_infectes)[:, 0], np.array(coord_infectes)[:, 1], c='firebrick')
    if coord_immunises != []:
        ax1.scatter(np.array(coord_immunises)[:, 0], np.array(coord_immunises)[:, 1], c='g')
    if coord_deces != []:
        ax1.scatter(np.array(coord_deces)[:, 0], np.array(coord_deces)[:, 1], c='k')
    titre = str(i)+'-ième vague'
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
    print(i,'ième vague')
    plt.show()
