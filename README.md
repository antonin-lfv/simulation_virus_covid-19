
# simulation épidémiologique 
<br/>

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/1be197d831a742f5af9d86e04a70721f)](https://app.codacy.com/manual/antoninlefevre45/simulation_virus_covid-19?utm_source=github.com&utm_medium=referral&utm_content=antonin-lfv/simulation_virus_covid-19&utm_campaign=Badge_Grade_Dashboard)

__Article lié à ce github__ : ( à venir )

Ce projet à pour objectifs de créer un __virus__, et de simuler sa propagation au sein d'une population. Les individus infectés pourront transmettre le virus avec une certaine probabilité, et peuvent aussi devenir immunisés ou bien décéder. 
En utilisant les paramètres propres du covid-19 on peut modeliser grossièrement ce dernier.

On choisira des populations de quelques dizaines à quelques milliers d'individus et on supposera qu'un individu immunisé ne peut plus être infecté.
Cette modélisation sera réalisée avec matplotlib puis avec plotly dans 2 fichiers différents.
<br/><br/>

__UPDATE :__ 
Ajout de la courbe 'removed', courbe noire, qui correspond aux personnes ne pouvant plus transmettre le virus, elle correspond à la somme des personnes immunisées et décédées. Elle est ajoutée dans le but de pouvoir comparer les résultats de la simulation à un modèle mathématiques, le modèle SIR. <br/><br/>
[Lien utile](https://interstices.info/modeliser-la-propagation-dune-epidemie/) pour comprendre le Modèle SIR. <br/>

[Thèse](https://tel.archives-ouvertes.fr/tel-00841444/file/BicharaPhDThesis.pdf) de Derdei Bichara sur l'étude de modèles épidémiologiques: Stabilité, observation et estimation de paramètres.

<br/>

## Résultat global sous plotly 
<br/>
Simulation effectuée avec des valeurs de paramètres standars. <br/>
<br/>
<img width="1407" alt="Capture d’écran 2020-10-26 à 20 42 48" src="https://user-images.githubusercontent.com/63207451/97220491-d8ead280-17cb-11eb-84b7-fa4ba0778bcf.png">
<br/>
(courbe noire : somme des personnes immunisées et décédées) <br/>


### Index
<br/>
1. Librairies
2. Principe de la simulation
3. Simulation avec différents taux d'infection
4. Simulation avec différentes létalités
5. Simulation avec différents taux d'immunité
6. Avec confinement 
7. Simuler le SARS-cov-2
8. Conclusion
<br/>

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
Lors de la simulation, plusieurs paramètres sont en jeux. Il y a tout d'abord le nombre d'invidus dans la population, ici on choisira une population entre 0 et 5000 individus pour avoir un temps d'exécution raisonnable. Ce nombre restera constant durant toute la simulation. La repartition de ces individus sera donnée par le paramètre variance_population, et qui variera entre 0 et 10 environ. Plus ce nombre est grand, plus la population sera étalée. Ensuite, le paramètre rayon_contamination donnera la portée maximale d'un individu infecté pour avoir une chance de transmettre son virus à un individu sain, avec une probabilté nommée infectiosité, qui est comprise entre 0 et 1. Chaque individu infecté reste infecté jusqu'à temps qu'il devienne immunisé ou qu'il décède. Après qu'un individu soit infecté, il a une probabilité p de devenir immunisé et donc de ne plus transmettre le virus, et une probabilité d de décéder suite à l'infection. Ces deux paramètres sont compris entre 0 et 1 également. Nous ne considérerons pas pour l'instant l'apparition d'un vaccin durant la simulation. Seule l'immunité innée des individus est prise en compte. <br/>
<br/>
Dans les 3 simulations qui suivent on ne s'intéressera qu'aux courbes et non à la représentation 2D de la population.
<br/>

## Simulation avec différents taux d'infection

<br/>
Faisons varier le taux d'infection entre 10%, 15%, 30%, 50% et 70% et observons la courbe du nombre de personnes infectés.<br/>
<br/>
<img width="1403" alt="infectés_variation_infectiosité" src="https://user-images.githubusercontent.com/63207451/97112938-6b657600-16e7-11eb-9c86-d197de969450.png">
<br/>
On remarque naturellement que plus l'infectiosité est grande, plus le nombre maximum de personnes infectés est grand. Mais également que le nombre d'infectés chute plus rapidement avec une infectiosité élevée. <br/>
Intéressons nous maintenant au nombre de décès en fonction de ces différentes valeurs d'infectiosité. <br/>
<br/>
<img width="1403" alt="morts_variation_infectiosité" src="https://user-images.githubusercontent.com/63207451/97112882-204b6300-16e7-11eb-9d9f-f3619ead67c1.png">
<br/>
Les courbes sont quasiment linéaires sur une grande partie, jusqu'à atteindre un certain seuil, qui est très proche malgrès des infectiosités très différentes. La différence se fait dans la vitesse à laquelle le seuil est atteint, plus l'infectiosité est grande plus le seuil est atteint rapidement, il est atteint en une dizaine de jours pour une infectiosité de l'ordre de 70% et en une quinzaine pour une infectiosité de l'ordre de 10%.
<br/>

## Simulation avec différentes létalités

<br/>
Faisons à présent varier la létalité entre 5%, 10%, 25%, 30% et 40%. Et observons l'évolution des courbes du nombre d'individus infectés. <br/>
<br/>
<img width="1403" alt="infectés_variation_letalité" src="https://user-images.githubusercontent.com/63207451/97112986-b1223e80-16e7-11eb-9fc4-eab052247d2a.png">
<br/>
Ici, une létalité élevée aplatit la courbe des infectés, en hauteur et largeur. En effet, si le virus ne tue pas beaucoup, il y a alors plus de personnes susceptibles de le transmettre, et sur une plus grande période. Au contraire d'une létalité élevée, qui élimine rapidement les individus infectés, avant qu'ils puissent transmettre le virus.   
<br/>
Cependant même si le nombre d'infectés est plus faible avec une grande létalité, le nombre de décès est nettement plus élevé. Comme le montre le graphique ci-dessous. <br/> 
<br/>
<img width="1403" alt="morts_variation_letalité" src="https://user-images.githubusercontent.com/63207451/97112993-bda69700-16e7-11eb-8e8a-eccd3c6e9531.png">
<br/>
Le nombre de décès avec une létalité de 40% est 7 fois plus grand qu'avec une létalité de 5%. Ce qui représente des différences énormes sur une population de plusieurs millions d'individus.
<br/>

## Simulation avec différents taux d'immunité

<br/>
Enfin, faisons varier le taux d'immunité entre 10%, 20%, 40%, 50% et 70%; et observons les courbes du nombre d'individus infectés. <br/>
<br/>
<img width="1403" alt="infectés_variation_immunité" src="https://user-images.githubusercontent.com/63207451/97113003-c9925900-16e7-11eb-8c9e-6bb57f5b8014.png">
<br/>
Sans grande surprise, si le taux d'immunité est très élevé, le maximum de personnes infectés et drastiquement réduit par rapport à un taux d'immunité plus faible, mais il est également atteint plus lentement. La propagation est freinée. 
On observe cette même tendance si l'on compare maintenant les courbes des décès. <br/>
<br/>
<img width="1403" alt="morts_variation_immunité" src="https://user-images.githubusercontent.com/63207451/97113011-d44cee00-16e7-11eb-9db0-c87facbbca32.png">
<br/>
Le nombre de décès est immensément plus grand lorsque l'immunité est quasi inexistante. Avec un taux d'immunité égale à 10%, on a 6 fois plus de décès qu'avec un taux à 70%.
<br/>

## Avec confinement 

<br/>
On peut simuler un confinement de la population, en diminuant la variance de celle-ci et en augmentant le nombre de cluster, c'est à dire le nombre de groupes distincts physiquement, d'individus dans la population.  
<br/>
Par exemple avec une variance de 2 et 7 centers (modifiable dans la fonction make_blobs), on observe que l'épidémie est très rapidement sous contrôle. On compte à la fin, moins de 4% de décès sur l'ensemble de la population. <br/>
<br/>
<img width="1440" alt="Capture d’écran 2020-10-20 à 22 00 20" src="https://user-images.githubusercontent.com/63207451/96637946-b2d2b780-131f-11eb-9695-5abf95c5b6dd.png">
<br/>

## Simuler le SARS-cov-2

<br/> 
Cette simulation est à prendre avec beaucoup de précautions, car elle ne reflète pas la réalité. Nous prendrons ici comme paramètres, un taux d'infection de 17%, un taux d'immunité de 10% et une létalité de 0.5%. <br/>
<img width="1401" alt="Capture d’écran 2020-10-26 à 19 51 58" src="https://user-images.githubusercontent.com/63207451/97215962-6ecf2f00-17c5-11eb-9f05-518d3e4872b8.png">
<br/>

Avec cette simulation on observe que le nombre d'infectés augmente très rapidement dès le début, puis diminue très lentement. Au final on compte quasiment 1/3 de décès, et plus de la moitié deviennent immunisés.
<br/>

## Conclusion

<br/>
L'étude épidémiologique reste tout de fois un domaine très théorique. Même si les résultats et observations obtenues sembles assez proches de la réalité, ces modélisations ne prennent pas en compte certains autres facteurs, tels que la vaccination, la mise en quarantaine des individus infectés, ou même le déplacement des individus dans la population. <br/>
Néanmoins, cela nous aident à comprendre comment un virus se comporte dans une population, et quel est l'influence de certains paramètres sur sa propagation.
<br/>
<br/>

---------------------------
