# simulation épidémiologique
<br/>

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/ee1396c2e13b47b4aba29ba19881758c)](https://www.codacy.com/gh/antonin-lfv/simulation_virus_covid-19/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=antonin-lfv/simulation_virus_covid-19&amp;utm_campaign=Badge_Grade)
<a href="https://www.python.org" class="fancybox" ><img align="right" width="110" height="110" src="https://user-images.githubusercontent.com/63207451/97306728-26fce600-185f-11eb-9784-14151a6b2c43.png"><a/>
	


__Article lié à ce github__ : ( à venir )

Ce projet à pour objectifs de créer un __virus__, et de simuler sa propagation au sein d'une population. Les individus infectés pourront transmettre le virus avec une certaine probabilité, et peuvent aussi devenir immunisés ou bien décéder. En utilisant les paramètres propres du covid-19 on peut modeliser grossièrement ce dernier. <br/>
Ce modèle statistique sera comparé au modèle __SIR__, reposant sur des équations différentielles.

On choisira des populations de quelques dizaines à quelques milliers d'individus et on supposera qu'un individu immunisé ne peut plus être infecté.
Cette modélisation sera réalisée avec matplotlib et plotly indépendamment.
<br/><br/>

>__UPDATE :__  <br/>-  Ajout de la courbe 'removed', courbe noire, qui correspond aux personnes ne pouvant plus transmettre le virus, elle correspond à la somme des personnes immunisées et décédées. Elle est ajoutée dans le but de pouvoir comparer les résultats de la simulation à un modèle mathématiques, le modèle SIR. 
<br/> - Optimisation du code, temps d'exécution réduit de façon considérable.  

<br/>
<br/>

## Liens utiles

- Comprendre le [Modèle SIR](https://fr.wikipedia.org/wiki/Modèles_compartimentaux_en_épidémiologie). <br/>

- Thèse de Derdei Bichara sur l'[étude de modèles épidémiologiques](https://tel.archives-ouvertes.fr/tel-00841444/file/BicharaPhDThesis.pdf): Stabilité, observation et estimation de paramètres.

<br/>

## Résultat global sous plotly 
<br/>
Simulation effectuée avec des valeurs de paramètres standars. <br/>
<br/>
<p align="center">
<img src="https://user-images.githubusercontent.com/63207451/101951720-c13ea080-3bf7-11eb-9dbd-c3cb50136b29.png">
	<p/>
	
<br/>
(courbe noire : somme des personnes immunisées et décédées) <br/>
<br/>

## Index
- [Librairies](#librairies)
- [Principe de la simulation](#principe-de-la-simulation)
	- [Simulation avec différents taux d'infection](#Simulation-avec-différents-taux-dinfection)
	- [Simulation avec différentes létalités](#simulation-avec-différentes-létalités)
	- [Simulation avec différents taux d'immunité](#simulation-avec-différents-taux-dimmunité)
- [Simulation avec différents Ro et cas limites](#Simulation-avec-différents-Ro-et-cas-limites)
- [Avec confinement](#avec-confinement)
	- [Confinement immédiat](#confinement-dès-le-premier-cas-detecté)
	- [Confinement après dépassement du seuil hospitalier](#confinement-après-dépassement-de-la-capacité-hospitalière) 
- [Simuler le SARS-cov-2](#simuler-le-SARS-cov-2)
- [Le modèle SIR](#le-modèle-SIR)
	- [Modèle mathématique](#Modèle-mathématique)
	- [Validation du modèle statistique par le modèle SIR](#Validation-du-modèle-statistique-par-le-modèle-SIR)
- [Conclusion](#conclusion)


## Librairies 

<br/>
Si vous n'avez jamais utilisé plotly pensez à le télécharger via la console :  <br/>
<br/>

	pip install plotly


Documentation [Plotly](https://plotly.com/python/) .

A chaque exécution d'une fonction sous plotly, une page html s'ouvrira avec le résultat.

Pour matplotlib une simple fenêtre python apparaîtra (ou plus).
<br/><br/> 

## Principe de la simulation

<br/>
Lors de la simulation, plusieurs paramètres sont en jeux. Il y a tout d'abord le nombre d'invidus dans la population, ici on choisira une population entre 0 et 15000 individus pour avoir un temps d'exécution raisonnable. Ce nombre restera constant durant toute la simulation. La repartition de ces individus sera donnée par le paramètre __variance_population__, et qui variera entre 0 et 10 environ. Plus ce nombre est grand, plus la population sera étalée.  
<br/>
Ensuite, le paramètre rayon_contamination donnera la portée maximale d'un individu infecté pour avoir une chance de transmettre son virus à un individu sain, avec une probabilté nommée infectiosité, qui est comprise entre 0 et 1. Chaque individu infecté reste infecté jusqu'à temps qu'il devienne immunisé ou qu'il décède. Après qu'un individu soit infecté, il a une probabilité p de devenir immunisé et donc de ne plus transmettre le virus, et une probabilité d de décéder suite à l'infection. Ces deux paramètres sont compris entre 0 et 1 également. Nous ne considérerons pas pour l'instant l'apparition d'un vaccin durant la simulation. Seule l'immunité innée des individus est prise en compte. 
On notera __Ro__ le taux de reproduction du virus, qui est le nombre moyen d'individus qu'une personne infectieuse infecte tant qu'elle est contagieuse, et qui est égale au rapport de l'infectiosité sur le taux de retirement ( somme de la létalité et du taux d'immunité ).
<br/>
<br/>
Dans les 3 simulations qui suivent on ne s'intéressera qu'aux courbes évolutives et non à la représentation 2D de la population.
<br/>

### Simulation avec différents taux d'infection

<br/>
Faisons varier le taux d'infection entre 10%, 15%, 30%, 50% et 70% et observons la courbe du nombre de personnes infectés.<br/>
<br/>
<p align="center">
<img width="1403" alt="infectés_variation_infectiosité" src="https://user-images.githubusercontent.com/63207451/97112938-6b657600-16e7-11eb-9c86-d197de969450.png">
	<p/>
<br/>
On remarque naturellement que plus l'infectiosité est grande, plus le nombre maximum de personnes infectés est grand. Mais également que le nombre d'infectés chute plus rapidement avec une infectiosité élevée. <br/>
Intéressons nous maintenant au nombre de décès en fonction de ces différentes valeurs d'infectiosité. <br/>
<br/>
<p align="center">
<img width="1403" alt="morts_variation_infectiosité" src="https://user-images.githubusercontent.com/63207451/97112882-204b6300-16e7-11eb-9d9f-f3619ead67c1.png">
	<p/>
<br/>
Les courbes sont quasiment linéaires sur une grande partie, jusqu'à atteindre un certain seuil, qui est très proche malgrès des infectiosités très différentes. La différence se fait dans la vitesse à laquelle le seuil est atteint, plus l'infectiosité est grande plus le seuil est atteint rapidement, il est atteint en une dizaine de jours pour une infectiosité de l'ordre de 70% et en une quinzaine pour une infectiosité de l'ordre de 10%.
<br/>
						     
### Simulation avec différentes létalités

<br/>
Faisons à présent varier la létalité entre 5%, 10%, 25%, 30% et 40%. Et observons l'évolution des courbes du nombre d'individus infectés. <br/>
<br/>
<p align="center">
<img width="1403" alt="infectés_variation_letalité" src="https://user-images.githubusercontent.com/63207451/97112986-b1223e80-16e7-11eb-9fc4-eab052247d2a.png">
	<p/>
<br/>
Ici, une létalité élevée aplatit la courbe des infectés, en hauteur et largeur. En effet, si le virus ne tue pas beaucoup, il y a alors plus de personnes susceptibles de le transmettre, et sur une plus grande période. Au contraire d'une létalité élevée, qui élimine rapidement les individus infectés, avant qu'ils puissent transmettre le virus.   
<br/>
Cependant même si le nombre d'infectés est plus faible avec une grande létalité, le nombre de décès est nettement plus élevé. Comme le montre le graphique ci-dessous. <br/> 
<br/>
<p align="center">
<img width="1403" alt="morts_variation_letalité" src="https://user-images.githubusercontent.com/63207451/97112993-bda69700-16e7-11eb-8e8a-eccd3c6e9531.png">
	<p/>
<br/>
Le nombre de décès avec une létalité de 40% est 7 fois plus grand qu'avec une létalité de 5%. Ce qui représente des différences énormes sur une population de plusieurs millions d'individus.
<br/>

### Simulation avec différents taux d'immunité

<br/>
Enfin, faisons varier le taux d'immunité entre 10%, 20%, 40%, 50% et 70%; et observons les courbes du nombre d'individus infectés. <br/>
<br/>
<p align="center">
<img width="1403" alt="infectés_variation_immunité" src="https://user-images.githubusercontent.com/63207451/97113003-c9925900-16e7-11eb-8c9e-6bb57f5b8014.png">
	<p/>
<br/>
Sans grande surprise, si le taux d'immunité est très élevé, le maximum de personnes infectés et drastiquement réduit par rapport à un taux d'immunité plus faible, mais il est également atteint plus lentement. La propagation est freinée. 
On observe cette même tendance si l'on compare maintenant les courbes des décès. <br/>
<br/>
<p align="center">
<img width="1403" alt="morts_variation_immunité" src="https://user-images.githubusercontent.com/63207451/97113011-d44cee00-16e7-11eb-9db0-c87facbbca32.png">
	<p/>
<br/>
Le nombre de décès est immensément plus grand lorsque l'immunité est quasi inexistante. Avec un taux d'immunité égale à 10%, on a 6 fois plus de décès qu'avec un taux à 70%.

<br/>

## Simulation avec différents Ro et cas limites

On fait varier ici le taux de reproduction de base _Ro_ du virus, dont l'epression est Ro=β/λ, ou ici __β est l'infectiosité du virus__, et __λ la probabilité pour qu'un individu ne puisse plus transmettre le virus__, c'est à dire p+d. On remarque que la situation est très différente pour un Ro inférieur et supérieur à 1. Pour un Ro < 1, peu d'individus sont infectés, et le virus ne propage pas. À la frontière Ro=1, le nombre de personnes retirées atteint quasiment le nombre de personnes saines, mais sans l'atteindre, il faut attendre un Ro>1 pour que la courbe des individus retirées passe au dessus de celle des individus sains, et provoque ainsi la propagation du virus, qui est d'autant plus importante et rapide que la valeur du Ro est grande.

<br/>

<p align="center">
<img src="https://user-images.githubusercontent.com/63207451/104498981-b2735100-55dc-11eb-8c99-83720fae9a45.png">
	<p/>
<br/>

Étudions maintenant les cas extrêmes. En faisant varier les valeurs _infectiosité_ qui est le __taux d'infection__, _p_ le __taux de guérison__ et _d_ la __létalité__.

## Avec confinement 

<br>

### Confinement dès le premier cas detecté

<br/>
On peut simuler un confinement de la population, en diminuant la variance de celle-ci et en augmentant le nombre de cluster, c'est à dire le nombre de groupes distincts physiquement, d'individus dans la population.  
<br/>
Par exemple avec une variance de 0.6 et 10 centers (modifiable dans la fonction make_blobs), on observe que l'épidémie est globalement sous contrôle, le pic d'infectés est très bas. On compte à la fin, 12% de décès sur l'ensemble de la population. <br/>
<br/>
<p align="center">
<img width="1376" alt="Capture d’écran 2020-12-12 à 15 07 57" src="https://user-images.githubusercontent.com/63207451/101986058-e11fa400-3c8b-11eb-8053-16c26d8def16.png">
	<p/>
<br/>

### Confinement après dépassement de la capacité hospitalière

<br/>
Une fois le seuil dépassé, l'infectiosité est divisé par 8 et le rayon de contamination est divisé par 4.
<br/>
Ici, la courbe pleine représente l'épidémie sans l'application du confinement, et la courbe en pointillé avec application du confinement à partir du jour ou le nombre de personnes infectés est superieur à la capacité hospitalière. On remarque que le nombre de personnes infectés diminue quelques jours après le début du confinement, et que le nombre de décès journaliers atteint un seuil inférieur au cas ou il n'y a pas de confinement.  <br/>
<br/>
<p align="center">
<img src="https://user-images.githubusercontent.com/63207451/101983272-4cf91100-3c7a-11eb-8282-cb5eb8df8240.png">
	<p/>
<br/>

## Simuler le SARS-cov-2

<br/> 
Cette simulation est à prendre avec beaucoup de précautions, car elle ne reflète pas la réalité. Nous prendrons ici comme paramètres, un taux d'infection de 17%, un taux d'immunité de 10% et une létalité de 0.5%.
<br/>

<p align="center">
<img width="1356" alt="Capture d’écran 2020-12-11 à 15 51 16" src="https://user-images.githubusercontent.com/63207451/101917618-bddff080-3bc8-11eb-83eb-46a68c3b803f.png">
	<p/>
<br/>

Avec cette simulation on observe que le nombre d'infectés augmente rapidement dès le début pour arriver à son maximum au bout de 8 jours, puis diminue très lentement pendant 16 jours. Au final on compte quasiment 30% de décès, et plus de la moitié deviennent immunisés.
<br/>
<br/>

## Le modèle __SIR__



### Modèle mathématique

<br/>
Le modèle SIR est un modèle mathématique déterministe à compartiments permettant de simuler de façon simplifiée l'évolution d'une population face à une épidémie. Ce modèle fait partie d'une famille de modèles compartimentaux en épidémiologie, qui ont commencé à être mis en pratique avec le SIDA dans les années 1980, ils sont à l'heure actuelle de plus en plus présents lors des décisions politiques concernant la gestion de problèmes sanitaires. <br/>
Dans ce modèle en particulier, la population est divisée en 3 catégories : sains (S), infectés (I) et removed (R) (removed, c'est à dire dans l'incapacité de transmettre le virus). Ce modèle étudie la taille de ces 3 catégories au cours du temps, tel que S(t), I(t) et R(t) soient le nombre d'individus dans chaque catégorie à l'instant t, et ou le nombre d'individu par compartiment est gouverné par un ensemble d'équations différentielles. <br/> 
On peut donc remarquer que, soit N le nombre d'individus dans la population, on a : 
<br/>

<p align="center"> 
	<br/>
	∀t	  N = S(t) + I(t) + R(t) <p/>

On introduit maintenant nos paramètres : <br/>

- β : le taux d'infection du virus, qui correspond à la probabilité d'être infecté après avoir été en contact avec un individu infecté 
- λ : le taux de retirement, qui correspond à la probabilité de ne plus pouvoir transmettre le virus, soit après être immunisé soit après le décès

On peut alors définir Ro le taux de reproduction de base du virus, qui vaut β/λ et qui représente le nombre moyen de personnes infectées par un seul individu. 

Le modèle SIR peut donc être representé par le diagramme suivant :

<p align="center">
<img width="692" alt="Capture d’écran 2021-01-12 à 15 44 43" src="https://user-images.githubusercontent.com/63207451/104329401-246c6d00-54ed-11eb-95f2-55974f363be7.png">
	<p/>

Puis on introduit nos équations différentielles qui régissent le modèle :  

<p align="center">
<img width="1112" alt="Capture d’écran 2021-01-12 à 16 44 25" src="https://user-images.githubusercontent.com/63207451/104337207-8335e480-54f5-11eb-92c3-e221b2c94644.png">
	<p/>
On remarque que :
<p align="center"> 
	dS/dt + dI/dt + dR/dt = 0  <p/>
	
<br/>
	
Ce qui confirme le fait que ∀t S(t) + I(t) + R(t) = constante = N car la dérivée de la somme est nulle.

<br/>

La première équation différentielle correspond au nombre de personnes saines, dont le signe est négatif, en effet la fonction S est décroissante pour tout t, car le nombre de personnes saines ne peut que diminuer (conformément au modèle dans lequel on se place, où les personnes infectés ne peuvent redevenir saines). <br/>
Ensuite, la deuxième équation a le signe de la différence entre le nombre de personne saines βS(t)I(t)/N et retirés λI(t), donc le nombre de personnes infectés diminue sur une période dt quand le nombre de personne saines est plus grande que le nombre de personnes retirées. <br/>
La dernière équation, elle, correspond au nombre de personnes retirées qui est simplement le produit du nombre d'individus infectés à l'instant t par le taux de retirement.

Le vecteur unitaire [S0, I0, R0] correspond aux nombres d'individus sains, infectés et retirés à t=0. Dans ce projet, aucun individu n'est immunisé à t=0 et la valeur de I0 est 1. 

<br/>

### Validation du modèle statistique par le modèle SIR

<br/>

Comparons maintenant le modèle mathématique SIR et le modèle statistique crée avec python. Les paramètres β et λ du modèle SIR correspondent respectivement aux paramètres infectiosité et à la somme p+d du modèle python.


Modèle mathématique :

<p align="center">
<img width="1301" alt="modèle SIR" src="https://user-images.githubusercontent.com/63207451/104339610-140dbf80-54f8-11eb-9e49-ab1a4b170137.png">
	<p/>

Modèle statistique :

<p align="center">
<img alt="modèle SIR" src="https://user-images.githubusercontent.com/63207451/104345853-132c5c00-54ff-11eb-9ed8-a56aa960c267.png">
	<p/>

<br/>

Les courbes sont assez similaires, la différence au niveau des abscisses est du au faite que les deux modèles n'ont pas la même représentation temporelle.
Le modèle crée en python est donc conforme au modèle mathématique.

## Conclusion

<br/>
L'étude épidémiologique reste au final un domaine très théorique. Même si les résultats et observations obtenues sembles assez proches de la réalité et du modèle mathématique SIR, ces modélisations ne prennent pas en compte certains autres facteurs, tels que la vaccination, la mise en quarantaine des individus dès qu'ils sont infectés, ou même le déplacement des individus dans la population. <br/>
Néanmoins, cela nous aident à comprendre comment un virus se comporte dans une population, et quel est l'influence de certains paramètres sur sa propagation.
<br/>
<br/>

<p align="center">
<a href="#simulation-épidémiologique"> haut de la page 
	</a>
<p/>

<br/>

<p align="center">
  <a href="https://github.com/antonin-lfv" class="fancybox" ><img src="https://user-images.githubusercontent.com/63207451/97302854-e484da80-1859-11eb-9374-5b319ca51197.png" title="GitHub" width="40" height="40"></a>
  <a href="https://www.linkedin.com/in/antonin-lefevre-565b8b141" class="fancybox" ><img src="https://user-images.githubusercontent.com/63207451/97303444-b2c04380-185a-11eb-8cfc-864c33a64e4b.png" title="LinkedIn" width="40" height="40"></a>
  <a href="mailto:antoninlefevre45@icloud.com" class="fancybox" ><img src="https://user-images.githubusercontent.com/63207451/97303543-cec3e500-185a-11eb-8adc-c1364e2054a9.png" title="Mail" width="40" height="40"></a>
</p>

---------------------------
