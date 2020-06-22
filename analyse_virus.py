''' modélisation de la propagation d'un virus '''

""" importation """

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
import random as rd

def distance(x,y): #distance entre 2 points du plan cartésien
    x1 = x[0]
    x2 = x[1]
    y1 = y[0]
    y2 = y[1]
    return(abs(np.sqrt((y1-x1)**2+(y2-x2)**2)))

def remove_(a,l): #pour supprimer de la liste des sains les nouveaux infectés 
    for i in range (len(l)):
        a.remove(l[i])
    return(a)

def chance_infecte(p): #return True si il devient infecté avec une proba p
    proba = int(p*100)
    if rd.randint(0,100) <= proba :
        return(True)
    else :
        return(False)

def virus(nb_individu, variance_population, rayon_contamination, infectiosite):
    # recommandé : nb_individu = 120, var_population = 0.85, rayon_contamination = 0.9, infectiosite = 0.25
    # variance population correspond à l'espacement moyen des individus
    # infectiosite correspond à la proba d'un infecté de transmettre le virus à l'interieur de son rayon

    x, y = make_blobs(n_samples=nb_individu, centers=1, cluster_std=variance_population)  # création du dataset
    ax = plt.figure(figsize=(10,8))
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

    # Afficher 1er individu avec pourcentage infectés/sains
    numero_infecte_1 = rd.randint(0, taille_pop)  # on choisit le premier individu infecté au hasard
    coord_1er_infecte = [x[:, 0][numero_infecte_1], x[:, 1][numero_infecte_1]]  # coordonnées du 1er infecté
    ax1.scatter(x[:, 0], x[:, 1], c='dodgerblue')
    ax1.scatter(x[:, 0][numero_infecte_1], x[:, 1][numero_infecte_1], c='firebrick')
    ax1.set_title('1er individu', fontsize=8)
    ax1.axis('off')
    ax4.pie([1, taille_pop], shadow=True, autopct='%1.1f%%',
            colors=['firebrick', 'dodgerblue'],pctdistance=1.5,counterclock=False)

    # Afficher 1er vague avec pourcentage infectés/sains
    coord_infectes = []  # cette liste sera implémentée des nouveaux cas
    coord_sains = []  # liste des cas sains
    for k in range(taille_pop):
        if distance(coord_1er_infecte, [x[:, 0][k], x[:, 1][k]]) < rayon_contamination and chance_infecte(infectiosite):
            ax2.scatter(x[:, 0][k], x[:, 1][k], c='firebrick')
            coord_infectes.append([x[:, 0][k], x[:, 1][k]])
        else:
            ax2.scatter(x[:, 0][k], x[:, 1][k], c='dodgerblue')
            coord_sains.append([x[:, 0][k], x[:, 1][k]])
        ax2.scatter(x[:, 0][numero_infecte_1], x[:, 1][numero_infecte_1], c='firebrick')
        ax2.set_title('1er vague', fontsize=8)
    ax2.axis('off')
    ax5.pie([len(coord_infectes), len(coord_sains)], shadow=True, autopct='%1.1f%%',
            colors=['firebrick', 'dodgerblue'],pctdistance=1.5,counterclock=False)

    # Afficher 2e vague avec pourcentage infectés/sains
    non_sains = []
    for k in range(len(coord_infectes)):
        for j in range(len(coord_sains)):
            if distance(np.array(coord_infectes)[k, :], np.array(coord_sains)[j, :]) < 0.5 and np.array(coord_sains)[j,:] not in np.array(coord_infectes) and chance_infecte(infectiosite):
                coord_infectes.append(np.array(coord_sains)[j, :])
                non_sains.append(list(np.array(coord_sains)[j, :]))

    coord_sains = remove_(coord_sains, non_sains)
    ax3.scatter(np.array(coord_sains)[:, 0], np.array(coord_sains)[:, 1], c='dodgerblue')
    ax3.scatter(np.array(coord_infectes)[:, 0], np.array(coord_infectes)[:, 1], c='firebrick')
    ax3.set_title('2e vague', fontsize=8)
    ax3.axis('off')
    ax6.pie([len(coord_infectes), len(coord_sains)], shadow=True, autopct='%1.1f%%',colors=['firebrick', 'dodgerblue'],pctdistance=1.5,counterclock=False)

    # Afficher 3e vague avec pourcentage infectés/sains
    non_sains = []
    for k in range(len(coord_infectes)):
        for j in range(len(coord_sains)):
            if distance(np.array(coord_infectes)[k, :], np.array(coord_sains)[j, :]) < 0.5 and np.array(coord_sains)[j,:] not in np.array(coord_infectes) and chance_infecte(infectiosite):
                coord_infectes.append(np.array(coord_sains)[j, :])
                non_sains.append(list(np.array(coord_sains)[j, :]))
    coord_sains = remove_(coord_sains, non_sains)
    ax7.scatter(np.array(coord_sains)[:, 0], np.array(coord_sains)[:, 1], c='dodgerblue')
    ax7.scatter(np.array(coord_infectes)[:, 0], np.array(coord_infectes)[:, 1], c='firebrick')
    ax7.set_title('3e vague', fontsize=8)
    ax7.axis('off')
    ax8.pie([len(coord_infectes), len(coord_sains)], shadow=True, autopct='%1.1f%%',colors=['firebrick', 'dodgerblue'],pctdistance=1,counterclock=False)

    # Afficher 4e vague avec pourcentage infectés/sains
    non_sains = []
    for k in range(len(coord_infectes)):
        for j in range(len(coord_sains)):
            if distance(np.array(coord_infectes)[k, :], np.array(coord_sains)[j, :]) < 0.5 and np.array(coord_sains)[j,:] not in np.array(coord_infectes) and chance_infecte(infectiosite):
                coord_infectes.append(np.array(coord_sains)[j, :])
                non_sains.append(list(np.array(coord_sains)[j, :]))
    coord_sains = remove_(coord_sains, non_sains)
    ax9.scatter(np.array(coord_sains)[:, 0], np.array(coord_sains)[:, 1], c='dodgerblue')
    ax9.scatter(np.array(coord_infectes)[:, 0], np.array(coord_infectes)[:, 1], c='firebrick')
    ax9.set_title('4e vague', fontsize=8)
    ax9.axis('off')
    ax10.pie([len(coord_infectes), len(coord_sains)], shadow=True, autopct='%1.1f%%',colors=['firebrick', 'dodgerblue'],pctdistance=1,counterclock=False)

    ax11.axis('off')
    ax12.axis('off')
    textstr = '\n'.join((
        r'$nombre \ individu=%.2f$' % (nb_individu,),
        r'$variance \ population=%.2f$' % (variance_population,),
        r'$rayon \ de \ contamination=%.2f$' % (rayon_contamination,),
        r'$infectiosité=%.2f$' % (infectiosite,)))
    ax.text(0.12, 0.09, textstr, horizontalalignment='left',verticalalignment='bottom',fontsize=14,bbox=dict(boxstyle='round', facecolor='dodgerblue', alpha=0.6))
    plt.show()
    
