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


def evolution_virus(nb_individu,variance_population,rayon_contamination):
    # recommandé : nb_individu=150, rayon_contamination=1, variance_population=0.9
    # variance population correspond à l'espacement moyen des individus

    #note : ne pas tenir compte des erreurs "DeprecationWarning"

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
    ax1.scatter(x[:,0],x[:,1],c='dodgerblue') #sains
    ax1.scatter(x[:,0][numero_infecte_1],x[:,1][numero_infecte_1],c='firebrick') #1er individu infecté
    ax1.set_title('1er individu',fontsize=8)
    ax1.axis('off')
    ax4.pie([1,taille_pop],labels=('infectés','sains'),shadow=True,autopct='%1.1f%%',colors=['firebrick','dodgerblue'])

    #Afficher 1er vague avec pourcentage infectés/sains
    coord_infectes = [coord_1er_infecte] #cette liste sera implémentée des nouveaux cas
    coord_sains = [] #liste des cas sains après 1er vague
    for k in range (taille_pop):
        if distance(coord_1er_infecte,[x[:,0][k],x[:,1][k]]) < rayon_contamination and k != numero_infecte_1 :
            ax2.scatter(x[:,0][k],x[:,1][k],c='firebrick') #infectés
            coord_infectes.append([x[:,0][k],x[:,1][k]]) #on ajoute le nouvel individu infectés dans la liste
        else :
            ax2.scatter(x[:, 0][k], x[:, 1][k], c='dodgerblue') #sains
            coord_sains.append([x[:, 0][k], x[:, 1][k]]) #on ajoute l'individu sain
        ax2.scatter(x[:, 0][numero_infecte_1], x[:, 1][numero_infecte_1], c='firebrick') #1er individu infecté
        ax2.set_title('1er vague',fontsize=8)
    ax2.axis('off')
    ax5.pie([len(coord_infectes),len(coord_sains)],labels=('infectés','sains'),shadow=True,autopct='%1.1f%%',colors=['firebrick','dodgerblue'])

    #Afficher 2e vague avec pourcentage infectés/sains
    cas_sains_1 = [] #liste des cas sains après 2e vague
    for k in range(len(coord_infectes)):
        for j in range(len(coord_sains)):
            if distance(np.array(coord_infectes)[k, :], np.array(coord_sains)[j, :]) < rayon_contamination and np.array(coord_sains)[j, :] not in np.array(coord_infectes):
                coord_infectes.append(np.array(coord_sains)[j, :]) #on ajoute l'individu infecté
            elif np.array(coord_sains)[j, :] not in np.array(cas_sains_1):
                cas_sains_1.append(np.array(coord_sains)[j, :]) #on ajoute l'individu sain
    ax3.scatter(np.array(cas_sains_1)[:, 0], np.array(cas_sains_1)[:, 1], c='dodgerblue') #sains
    ax3.scatter(np.array(coord_infectes)[:, 0], np.array(coord_infectes)[:, 1], c='firebrick') #infectés
    ax3.set_title('2e vague',fontsize=8)
    ax3.axis('off')
    ax6.pie([len(coord_infectes),len(cas_sains_1)],labels=('infectés','sains'),shadow=True,autopct='%1.1f%%',colors=['firebrick','dodgerblue'])

    #Afficher 3e vague avec pourcentage infectés/sains
    cas_sains_2 = [] #liste des cas sains après 3e vague
    for k in range(len(coord_infectes)):
        for j in range(len(cas_sains_1)):
            if distance(np.array(coord_infectes)[k, :], np.array(cas_sains_1)[j, :]) < rayon_contamination and np.array(cas_sains_1)[j, :] not in np.array(coord_infectes):
                coord_infectes.append(np.array(cas_sains_1)[j, :]) #on ajoute les individus infectés
            elif np.array(cas_sains_1)[j, :] not in np.array(cas_sains_2):
                cas_sains_2.append(np.array(cas_sains_1)[j, :]) #on ajoute les individus sains
    ax7.scatter(np.array(cas_sains_2)[:, 0], np.array(cas_sains_2)[:, 1], c='dodgerblue') #sains
    ax7.scatter(np.array(coord_infectes)[:, 0], np.array(coord_infectes)[:, 1], c='firebrick') #infectés
    ax7.set_title('3e vague',fontsize=8)
    ax7.axis('off')
    ax8.pie([len(coord_infectes), len(cas_sains_2)], labels=('infectés', 'sains'), shadow=True, autopct='%1.1f%%',colors=['firebrick','dodgerblue'])

    plt.show()


    
