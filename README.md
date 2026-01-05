# Lenia – Vie artificielle émergente en temps réel

Ce projet est une implémentation web temps réel de **Lenia**, un système de vie artificielle continue. Il permet d’observer directement dans un navigateur l’apparition et l’évolution de structures dynamiques complexes, souvent qualifiées de *formes de vie informatiques*, bien qu’aucune d’entre elles ne soit explicitement programmée.

Le projet est accessible en ligne à l’adresse suivante :  
👉 https://lenia.518.fr/

---

## Lenia : un système de vie artificielle

Lenia est un système introduit par Bert Wang-Chak Chan en 2018, parfois décrit comme une généralisation continue du *Game of Life*. Contrairement aux automates cellulaires classiques, Lenia ne repose pas sur des règles discrètes du type « si telle condition est remplie, alors telle action a lieu ».  

Ici, l’espace est continu, les valeurs sont réelles, et l’évolution repose sur des équations mathématiques faisant intervenir des convolutions spatiales et des fonctions de croissance. Le système évolue de manière fluide dans le temps.

Dans ces conditions, des structures cohérentes apparaissent spontanément. Elles peuvent se stabiliser, se déplacer, osciller, se transformer ou disparaître. Leur comportement dépend uniquement de leur environnement et des interactions locales. Il n’existe ni modèle de créature, ni règle de déplacement, ni intelligence embarquée.

Les formes observées **ne sont pas programmées**. Elles émergent.

---

## Une vie qui n’est pas codée

Aucune forme visible à l’écran n’a été dessinée, décrite ou anticipée dans le code. Le programme ne contient aucune instruction définissant une “entité”, un “organisme” ou un “comportement”.

Tout ce qui est observé résulte exclusivement :
- des conditions initiales,
- des paramètres globaux du système,
- et des lois mathématiques locales appliquées uniformément.

Ce projet illustre ainsi un phénomène de **complexité émergente**, où des comportements riches et organisés apparaissent sans plan, sans objectif et sans représentation interne.

---

## Implémentation et choix techniques

Cette implémentation est **librement inspirée** du projet suivant :  
https://github.com/Wartets/Lenia-Simulation  

Le travail présenté ici s’en distingue toutefois par plusieurs choix forts.

Le moteur de calcul repose sur NumPy et l’utilisation massive de la FFT afin de rendre les convolutions suffisamment rapides pour un affichage fluide. Une attention particulière a été portée aux performances afin de permettre un fonctionnement **temps réel**, directement observable dans un navigateur.

Le rendu a été volontairement simplifié et externalisé vers le navigateur via un flux vidéo JPEG. Une méthode spécifique a été mise en place pour **réduire drastiquement la bande passante consommée**, tout en conservant une bonne lisibilité visuelle et une fréquence d’images stable.

L’interface web repose sur Flask côté serveur et sur un rendu Canvas côté client, sans dépendance lourde ni framework complexe.

---

## États initiaux et émergence

Deux modes de fonctionnement sont proposés.

Le mode principal démarre à partir d’un **état initial préconfiguré**, permettant d’observer immédiatement une structure déjà formée. Ce choix a été fait afin d’éviter un temps d’attente parfois long avant l’émergence spontanée.

Un second mode, accessible via la route `/random`, initialise le système avec du bruit aléatoire. Dans ce cas, il est possible d’observer l’émergence progressive de structures organisées à partir du chaos initial, lorsque les conditions le permettent.

Dans les deux cas, le système évolue ensuite librement, sans intervention.

---

## Ce que montre ce projet

Ce projet ne cherche pas à simuler la biologie réelle, ni à reproduire un comportement intelligent. Il montre autre chose :  
qu’un ensemble de règles mathématiques simples, appliquées localement, peut suffire à produire des dynamiques riches, surprenantes et parfois troublantes.

Il s’agit d’un terrain d’exploration entre mathématiques, physique, informatique et philosophie, où la notion même de « vie » peut être questionnée.

---

## Licence et usage

Projet expérimental et exploratoire, mis à disposition à des fins éducatives, artistiques et de recherche.  
Libre à chacun de l’étudier, le modifier et l’expérimenter.

---

## Références

- Bert Wang-Chak Chan — *Lenia: Biology of Artificial Life*
- https://chakazul.github.io/lenia.html
- https://github.com/Wartets/Lenia-Simulation
