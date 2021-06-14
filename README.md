# ENSEArrosage
Projet de première année à l'ENSEA


Projet 1ère Année à l’ENSEA


Présentation du projet :

Le but de ce projet est de créer un système permettant d’automatiser l’arrosage des 2 murs végétalisés disposés dans la K-fet de l'Ensea.

Pour cela nous disposons de 3 capteurs : un de température et d’humidité de l’air, un de luminosité et un autre mesurant l'humidité du sol. Ces 3 capteurs sont reliés à une STM32, qui elle-même communique avec une Raspberry Pi.
De plus, la Raspberry Pi récupère des données météorologiques depuis une API météo.
Pour finir, un site web, hébergé sur la RPI, permet d’observer en temps réel les données des capteurs et celles provenant de l’API météo mais aussi de contrôler le type d'arrosage des plantes. Ainsi, deux modes sont disponibles : 
- un mode manuel : L’utilisateur peut entrer sur le site une durée d’arrosage. 
- un mode automatique : L’arrosage est géré intelligemment en fonction des données des capteurs et de la météo des jours à venir.

L’acquisition des données météos et des données des capteurs s’effectuent une fois toutes les  6h.

De plus nous devons répondre au cahier des charges suivant :
- Utiliser une RPI
- Disposer de 3 types de capteurs : humidité, luminosité et température
- Travailler avec les données météorologiques en temps réel (API Météo)
- Créer un serveur WEB afin de vérifier l’état du plant et contrôler manuellement l’arrosage.
- Contrôler l’arrivée d’eau

Pour plus de détails, un diaporama de présentation est présent dans le GIT.

Liste du matériel :

- Raspberry pi 4 
- STM32-L476 nucleo
- Capteur Température + Humidité : DHT22 (AM2302)
- Capteur Luminosité : Grove Light Sensor
- Capteur Humidité : Grove Moisture Sensor
- Régulateur de tension 78L05F
- 2 Condensateurs 865060645008 WÜRTH ELEKTRONIK

Liste des logiciels utilisés :

- CUBEIDE pour le code en C
- Eagle pour le schéma électrique et  le PCB
- VS code pour programmer en python, CSS, HTML et SQL

Présentation du contenu du GIT : 

Ce GIT est composé de plusieurs fichiers : 

- Un script bash
- Un dossier comprenant le code en C que nous avons développé sous CubeIDE.
- Un dossier comprenant un site web codé en HTML et en CSS qui nous permet de contrôler l’arrosage et deux codes en python, un pour récupérer les valeurs des capteurs et les données météos et un autre pour lancer le site web.
- Le schéma et le PCB (et la librairie qui va avec) de la carte que nous avons produite.
- Le diaporama que nous avons utilisé pour faire notre présentation.

Tutoriel d’installation :

- Commencer par démarrer la raspberry et la connecter à Internet
- Là, il y a deux options : soit lancer  le script bash afin qu'il télécharge le projet et l'exécute, soit télécharger le projet en entier depuis github
- Faire le montage électrique en suivant le schéma
- Upload le code qui est sur CUBEIDE sur la STM32

NB : Comme l’UART côté RPI ne fonctionnait pas, on a préféré ne pas mettre les commandes d’installation dans le script bash car ce sont peut-être elles qui causent  ce dysfonctionnement.

NB2 : On a décidé d’anonymiser le projet ou cas où il serait rendu public.


