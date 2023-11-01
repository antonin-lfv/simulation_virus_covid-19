<p align="center">
	<img src="https://user-images.githubusercontent.com/63207451/114284722-45901b80-9a52-11eb-8a0c-e99fc8681436.gif" height="80" width="140">
	<p/>

<h1 align="center">Simulation épidémiologique</h1>

<br/>

<p align="center">
	<a href="https://www.codacy.com/gh/antonin-lfv/simulation_virus_covid-19/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=antonin-lfv/simulation_virus_covid-19&amp;utm_campaign=Badge_Grade"><img src="https://app.codacy.com/project/badge/Grade/ee1396c2e13b47b4aba29ba19881758c" height="20"/></a>
	<a href="https://www.python.org/downloads/release/python-380/"><img src="https://img.shields.io/badge/python-3.8-blue.svg" height="20"/></a>
	<p/>
<br/>

<p align="center">
Ce projet a pour objectifs de modéliser une <b>épidémie</b>, et de simuler sa propagation au sein d'une population d'individus. Le taux d'infection, de guérison et de létalité seront les paramètres de notre modèle, que nous étudierons afin de mieux comprendre leur impact sur la vitesse de propagation du virus. On choisira des populations de quelques centaines à quelques dizaines de milliers d'individus et on supposera qu'un individu immunisé le reste toute sa vie. Cette modélisation sera réalisée avec matplotlib et plotly indépendamment. <br/>
Ce modèle statistique sera ensuite comparé aux modèles mathématiques <b>SIR</b> et <b>SIDR</b>, qui appartiennent à la famille des modèles compartimenantaux en épidémiologie, qui reposent sur des équations différentielles.<br/>
<br/>
<p/>

<br/>

>__UPDATE :__  <br/>-  Ajout de la courbe 'removed', courbe noire, qui correspond aux personnes ne pouvant plus transmettre le virus, elle correspond à la somme des personnes immunisées et décédées. Elle est ajoutée dans le but de pouvoir comparer les résultats de la simulation à un modèle mathématiques, le modèle SIR. 
<br/> - Nouvelle optimisation du code, qui rend le processus quasi instantané. 
<br/> - <b>Grâce à l'optimisation, vous pouvez tester la simulation en ligne [ici](https://share.streamlit.io/antonin-lfv/simulation_virus_covid-19/Streamlit/main.py)</b>

<br/>
<br/>

# Liens utiles

- Article lié à ce github : [ici](https://machinelearnia.com/simulation-dune-epidemie-avec-python/)

- Détails sur la méthodologie [ici](https://antonin-lfv.github.io/publications/)

- Comprendre le [Modèle SIR](https://fr.wikipedia.org/wiki/Modèles_compartimentaux_en_épidémiologie). <br/>

- Thèse de Derdei Bichara sur l'[étude de modèles épidémiologiques](https://tel.archives-ouvertes.fr/tel-00841444/file/BicharaPhDThesis.pdf): Stabilité, observation et estimation de paramètres.

- Étude des [modèles épidémiologiques et du Ro](http://www.math.univ-metz.fr/~sallet/R0_EPICASA09.pdf) 

<br/>

	
# Résultat global sous Plotly
<br/>
Simulation effectuée avec des valeurs de paramètres standards. <br/>
<br/>
<p align="center">
<img src="https://user-images.githubusercontent.com/63207451/101951720-c13ea080-3bf7-11eb-9dbd-c3cb50136b29.png" width="1000">
	<p/>
	
<br/>
(courbe noire : somme des personnes immunisées et décédées) <br/>
<br/>

# Librairies

<br/>
Si vous n'avez jamais utilisé plotly pensez à le télécharger via la console :  <br/>
<br/>

	pip install plotly


Documentation [Plotly](https://plotly.com/python/) .

À chaque exécution d'une fonction sous plotly, une page html s'ouvrira avec le résultat.

Pour matplotlib une simple fenêtre python apparaîtra (ou plus).
<br/>


<p align="center">
	  <a href="https://antonin-lfv.github.io" class="fancybox" ><img src="https://user-images.githubusercontent.com/63207451/127334786-f48498e4-7aa1-4fbd-b7b4-cd78b43972b8.png" title="Web Page" width="38" height="38"></a>
  <a href="https://github.com/antonin-lfv" class="fancybox" ><img src="https://user-images.githubusercontent.com/63207451/97302854-e484da80-1859-11eb-9374-5b319ca51197.png" title="GitHub" width="40" height="40"></a>
  <a href="https://www.linkedin.com/in/antonin-lefevre-565b8b141" class="fancybox" ><img src="https://user-images.githubusercontent.com/63207451/97303444-b2c04380-185a-11eb-8cfc-864c33a64e4b.png" title="LinkedIn" width="40" height="40"></a>
  <a href="mailto:antoninlefevre45@icloud.com" class="fancybox" ><img src="https://user-images.githubusercontent.com/63207451/97303543-cec3e500-185a-11eb-8adc-c1364e2054a9.png" title="Mail" width="40" height="40"></a>
</p>


---------------------------
