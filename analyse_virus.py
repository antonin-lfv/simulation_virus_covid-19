''' modélisation de la propagation d'un virus '''

""" importation """

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.datasets import make_blobs
import random as rd

""" I) création du dataset """

x,y = make_blobs(n_samples=100,centers=1,cluster_std=0.5)
#plt.scatter(x[:,0],x[:,1],c='dodgerblue')
#plt.show()

def distance(x,y): #distance entre 2 points du plan cartésien
    x1 = x[0]
    x2 = x[1]
    y1 = y[0]
    y2 = y[1]
    return(abs(np.sqrt((y1-x1)**2+(y2-x2)**2)))

""" II) choix de la personne infectée en premier """

taille_pop = len(x)

numero_infecte_1 = rd.randint(0,taille_pop)
coord_1er_infecte = [x[:,0][numero_infecte_1],x[:,1][numero_infecte_1]]

# afficher l'individu infecté dans la pop :

plt.scatter(x[:,0],x[:,1],c='b')
plt.scatter(x[:,0][numero_infecte_1],x[:,1][numero_infecte_1],c='r')
plt.scatter(x[:,0][numero_infecte_1],x[:,1][numero_infecte_1],c='r',s=3300,alpha=0.2)
plt.title('1er individu contaminé')
plt.show()

""" III) 1er contaminations """

coord_infectes_0 = [coord_1er_infecte]
coord_sains_0 = []

# contamination

for k in range (taille_pop):
    if distance(coord_1er_infecte,[x[:,0][k],x[:,1][k]]) < 0.5 and k != numero_infecte_1 :
        plt.scatter(x[:,0][k],x[:,1][k],c='r')
        coord_infectes_0.append([x[:,0][k],x[:,1][k]])
    else :
        plt.scatter(x[:, 0][k], x[:, 1][k], c='b')
        coord_sains_0.append([x[:, 0][k], x[:, 1][k]])
    plt.scatter(x[:, 0][numero_infecte_1], x[:, 1][numero_infecte_1], c='r')
    plt.title('1er vague de contamination')
    plt.show()

plt.clf()
plt.pie([len(coord_infectes_0),len(coord_sains_0)],labels=('infectés','sains'),shadow=True,autopct='%1.1f%%')
plt.title('1er vague de contamination')
plt.show()

""" IV) 2e contamination """

coord_sains_0 # les sains au début
cas_sains_1 = [] # les individus sains sont de moins en moins
coord_infectes_1 = coord_infectes_0 # on va rajouter les malades

for k in range (len(coord_infectes_0)):
    for j in range (len(coord_sains_0)):
        if distance(np.array(coord_infectes_0)[k,:],np.array(coord_sains_0)[j,:]) <0.5 and np.array(coord_sains_0)[j,:] not in np.array(coord_infectes_1) :
            coord_infectes_1.append(np.array(coord_sains_0)[j,:])
        elif np.array(coord_sains_0)[j,:] not in np.array(cas_sains_1) :
            cas_sains_1.append(np.array(coord_sains_0)[j,:])

plt.scatter(np.array(cas_sains_1)[:,0],np.array(cas_sains_1)[:,1],c='b')
plt.scatter(np.array(coord_infectes_1)[:,0],np.array(coord_infectes_1)[:,1],c='r')
#plt.xlim(min(x[:,0])-1,max(x[:,0])+1)
#plt.ylim(min(x[:,1])-1,max(x[:,1])+1)
plt.title('2e vague de contamination')
plt.show()

plt.clf()
plt.pie([len(coord_infectes_1),len(cas_sains_1)],labels=('infectés','sains'),shadow=True,autopct='%1.1f%%')
plt.title('2er vague de contamination')
plt.show()

""" 3e vague """

cas_sains_2 = [] # les individus sains sont de moins en moins
coord_infectes_2 = coord_infectes_1

for k in range (len(coord_infectes_1)):
    for j in range (len(cas_sains_1)):
        if distance(np.array(coord_infectes_2)[k,:],np.array(cas_sains_1)[j,:]) <0.5 and np.array(cas_sains_1)[j,:] not in np.array(coord_infectes_2) :
            coord_infectes_2.append(np.array(cas_sains_1)[j,:])
        elif np.array(cas_sains_1)[j,:] not in np.array(cas_sains_2) :
            cas_sains_2.append(np.array(cas_sains_1)[j,:])

plt.scatter(np.array(cas_sains_2)[:,0],np.array(cas_sains_2)[:,1],c='b')
plt.scatter(np.array(coord_infectes_2)[:,0],np.array(coord_infectes_2)[:,1],c='r')
plt.title('3e vague de contamination')
plt.show()

plt.clf()
plt.pie([len(coord_infectes_2),len(cas_sains_2)],labels=('infectés','sains'),shadow=True,autopct='%1.1f%%')
plt.title('3e vague de contamination')
plt.show()

""" résumé des 3 premières vagues """

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
    ax1.scatter(x[:,0],x[:,1],c='dodgerblue')
    ax1.scatter(x[:,0][numero_infecte_1],x[:,1][numero_infecte_1],c='firebrick')
    ax1.set_title('1er individu',fontsize=8)
    ax1.axis('off')
    ax4.pie([1,taille_pop],labels=('infectés','sains'),shadow=True,autopct='%1.1f%%',colors=['firebrick','dodgerblue'])

    #Afficher 1er vague avec pourcentage infectés/sains
    coord_infectes = [coord_1er_infecte] #cette liste sera implémentée des nouveaux cas
    coord_sains = [] #liste des cas sains après 1er vague
    for k in range (taille_pop):
        if distance(coord_1er_infecte,[x[:,0][k],x[:,1][k]]) < rayon_contamination and k != numero_infecte_1 :
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
    cas_sains_1 = [] #liste des cas sains après 2e vague
    for k in range(len(coord_infectes)):
        for j in range(len(coord_sains)):
            if distance(np.array(coord_infectes)[k, :], np.array(coord_sains)[j, :]) < rayon_contamination and np.array(coord_sains)[j, :] not in np.array(coord_infectes):
                coord_infectes.append(np.array(coord_sains)[j, :])
            elif np.array(coord_sains)[j, :] not in np.array(cas_sains_1):
                cas_sains_1.append(np.array(coord_sains)[j, :])
    ax3.scatter(np.array(cas_sains_1)[:, 0], np.array(cas_sains_1)[:, 1], c='dodgerblue')
    ax3.scatter(np.array(coord_infectes)[:, 0], np.array(coord_infectes)[:, 1], c='firebrick')
    ax3.set_title('2e vague',fontsize=8)
    ax3.axis('off')
    ax6.pie([len(coord_infectes),len(cas_sains_1)],labels=('infectés','sains'),shadow=True,autopct='%1.1f%%',colors=['firebrick','dodgerblue'])

    #Afficher 3e vague avec pourcentage infectés/sains
    cas_sains_2 = [] #liste des cas sains après 3e vague
    for k in range(len(coord_infectes)):
        for j in range(len(cas_sains_1)):
            if distance(np.array(coord_infectes)[k, :], np.array(cas_sains_1)[j, :]) < rayon_contamination and np.array(cas_sains_1)[j, :] not in np.array(coord_infectes):
                coord_infectes.append(np.array(cas_sains_1)[j, :])
            elif np.array(cas_sains_1)[j, :] not in np.array(cas_sains_2):
                cas_sains_2.append(np.array(cas_sains_1)[j, :])
    ax7.scatter(np.array(cas_sains_2)[:, 0], np.array(cas_sains_2)[:, 1], c='dodgerblue')
    ax7.scatter(np.array(coord_infectes)[:, 0], np.array(coord_infectes)[:, 1], c='firebrick')
    ax7.set_title('3e vague',fontsize=8)
    ax7.axis('off')
    ax8.pie([len(coord_infectes), len(cas_sains_2)], labels=('infectés', 'sains'), shadow=True, autopct='%1.1f%%',colors=['firebrick','dodgerblue'])

    plt.show()

""" V) Avec n vagues """

def n_vagues():

    
