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

def virus(nb_individu,variance_population,rayon_contamination):
    # recommandé : nb_individu=150, rayon_contamination=1, variance_population=0.9
    # variance population correspond à l'espacement moyen des individus

    x, y = make_blobs(n_samples=nb_individu, centers=1, cluster_std=variance_population) # création du dataset
    ax = plt.figure()
    taille_pop = len(x)

    # création des figures
    ax1 = ax.add_subplot(4,2,1)
    ax2 = ax.add_subplot(4,2,3)
    ax3 = ax.add_subplot(4,2,5)
    ax4 = ax.add_subplot(4,2,2)
    ax5 = ax.add_subplot(4,2,4)
    ax6 = ax.add_subplot(4,2,6)
    ax7 = ax.add_subplot(4,2,7)
    ax8 = ax.add_subplot(4,2,8)

    #Afficher 1er individu avec pourcentage infectés/sains
    numero_infecte_1 = rd.randint(0, taille_pop) # on choisit le premier individu infecté au hasard
    coord_1er_infecte = [x[:, 0][numero_infecte_1], x[:, 1][numero_infecte_1]] # coordonnées du 1er infecté
    ax1.scatter(x[:,0],x[:,1],c='dodgerblue')
    ax1.scatter(x[:,0][numero_infecte_1],x[:,1][numero_infecte_1],c='firebrick')
    ax1.set_title('1er individu',fontsize=8)
    ax1.axis('off')
    ax4.pie([1,taille_pop],labels=('infectés','sains'),shadow=True,autopct='%1.1f%%',colors=['firebrick','dodgerblue'])

    #Afficher 1er vague avec pourcentage infectés/sains
    coord_infectes = [] #cette liste sera implémentée des nouveaux cas
    coord_sains = [] #liste des cas sains
    for k in range (taille_pop):
        if distance(coord_1er_infecte,[x[:,0][k],x[:,1][k]]) < rayon_contamination:
            ax2.scatter(x[:,0][k],x[:,1][k],c='firebrick')
            coord_infectes.append([x[:,0][k],x[:,1][k]])
        else :
            ax2.scatter(x[:, 0][k], x[:, 1][k], c='dodgerblue')
            coord_sains.append([x[:, 0][k], x[:, 1][k]])
        ax2.scatter(x[:, 0][numero_infecte_1], x[:, 1][numero_infecte_1], c='firebrick')
        ax2.set_title('1er vague',fontsize=8)
    ax2.axis('off')
    ax5.pie([len(coord_infectes),len(coord_sains)],labels=('infectés','sains'),shadow=True,autopct='%1.1f%%',colors=['firebrick','dodgerblue'])

    #Afficher 2e vague avec pourcentage infectés/sains
    non_sains = [] #liste des personnes devenus infectés 
    for k in range(len(coord_infectes)):
        for j in range(len(coord_sains)):
            if distance(np.array(coord_infectes)[k, :], np.array(coord_sains)[j, :]) < 0.5 and np.array(coord_sains)[j,:] not in np.array(coord_infectes):
                coord_infectes.append(np.array(coord_sains)[j, :])
                non_sains.append(list(np.array(coord_sains)[j, :]))

    coord_sains = remove_(coord_sains, non_sains)
    ax3.scatter(np.array(coord_sains)[:, 0], np.array(coord_sains)[:, 1], c='dodgerblue')
    ax3.scatter(np.array(coord_infectes)[:, 0], np.array(coord_infectes)[:, 1], c='firebrick')
    ax3.set_title('2e vague',fontsize=8)
    ax3.axis('off')
    ax6.pie([len(coord_infectes),len(coord_sains)],labels=('infectés','sains'),shadow=True,autopct='%1.1f%%',colors=['firebrick','dodgerblue'])

    #Afficher 3e vague avec pourcentage infectés/sains
    non_sains = []
    for k in range(len(coord_infectes)):
        for j in range(len(coord_sains)):
            if distance(np.array(coord_infectes)[k, :], np.array(coord_sains)[j, :]) < 0.5 and np.array(coord_sains)[j,:] not in np.array(coord_infectes):
                coord_infectes.append(np.array(coord_sains)[j, :])
                non_sains.append(list(np.array(coord_sains)[j, :]))
    coord_sains = remove_(coord_sains, non_sains)
    ax7.scatter(np.array(coord_sains)[:, 0], np.array(coord_sains)[:, 1], c='dodgerblue')
    ax7.scatter(np.array(coord_infectes)[:, 0], np.array(coord_infectes)[:, 1], c='firebrick')
    ax7.set_title('3e vague',fontsize=8)
    ax7.axis('off')
    ax8.pie([len(coord_infectes), len(coord_sains)], labels=('infectés', 'sains'), shadow=True, autopct='%1.1f%%',colors=['firebrick','dodgerblue'])
    plt.show()

    
