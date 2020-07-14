## creation et etude d'un virus

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/1be197d831a742f5af9d86e04a70721f)](https://app.codacy.com/manual/antoninlefevre45/simulation_virus_covid-19?utm_source=github.com&utm_medium=referral&utm_content=antonin-lfv/simulation_virus_covid-19&utm_campaign=Badge_Grade_Dashboard)

Ce projet vous propose de créer une population et un virus, et de voir sa propagation au sein de cette population. Les individus infectés pourront transmettre le virus avec une certaine probabilité, et peuvent aussi devenir immunisés ou décéder. 
En utilisant les paramètres propres du covid-19 on peut le modeliser grossièrement.
On choisira des populations de quelques dizaines à quelques milliers d'individus.

Cette modélisation sera réalisée avec matplotlib et avec plotly dans 2 fichiers différents.


Si vous n'avez jamais utilisé plotly pensez à le télécharger :


	pip install plotly


Vous pouvez selectionner plusieurs paramètres :
  
	• nb_population : le nombre d'individus au départ
  
	• variance_population : pour avoir une population plus ou moins étalée
 
 	• rayon_contamination : qui détermine le rayon dans lequel un individu infecté infecte un individu sain
	
	• infectiosité : probabilité qu'un infecté transmette le virus dans son rayon de contamination

	• p : probabilité qu'une personne infectée devienne immunisée
	
	• d : probabilité qu'une personne infectée décède 

## Confinement 

On peut également simuler un confinement de la population, en diminuant la variance de celle-ci et en augmentant le nombre de centres.

Par exemple avec les paramètres :

		nb_population = 1200
	
		variance_population = 1
	
		centers = 7


Les autres paramètres peuvent être évidemment changés.

