#############################################################################################
# Obtention des données météo depuis une API (OpenWeather) et envoie sur une base de donnée #
#############################################################################################

#Ce code sert à récupérer les données de différents capteurs câblés sur une STM32 et des données météos (le temps qu'il fait, la température
#et l'humidité) des 3 prochains jours afin d'adapter l'arrosage des plantes. Comme nous n'avons pas pu activer l'UART entre la STM32 et la RPI,
#nous générons pour le moments des valeurs aléatoires.


#import des bibliothèques nécessaires
import io
import requests
import json
import datetime
import sqlite3
import random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import time
from flask import Flask, Response, render_template, request
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_svg import FigureCanvasSVG
from matplotlib.figure import Figure

#configuration de la fenêtre des courbes
plt.figure(2,figsize=(10,12))
plt.gcf().subplots_adjust(left = 0.1, bottom = 0.1, right = 0.9,
                          top = 0.9, wspace = 0, hspace = 0.5)

#génération de valeurs aléatoires qui simulent les données des capteurs
hygro = random.random()                         #génère une valeur entre 0 et 1
temperature = random.randint(-20, 50)           
ensoleillement = random.randint(0, 1800)
hygrometrie = round(hygro, 2)                   #arrondi la variable hygro à deux chiffre après la virgule. On a juste besoin d'un pourcentage, inutile d'être plus précis

value = (hygrometrie,temperature,ensoleillement)

#commande pour créer deux bdd : une pour récupérer les données météo de l'api et une pour stocker les valeurs des capteurs
tableapimeteo = '''CREATE TABLE IF NOT EXISTS APIMETEO (
            temps CHAR(32),
            temperature FLOAT,
            humidite FLOAT
        );'''
tabledonneescapteurs = '''CREATE TABLE IF NOT EXISTS DONNEESCAPTEURS (
                id INTEGER NOT NULL PRIMARY KEY,
                temperature FLOAT,
                hygrometrie FLOAT,
                ensoleillement FLOAT
        );'''
#permet d'insérer des valeurs dans une table
insererval = "INSERT INTO APIMETEO (temps, temperature, humidite) VALUES (?, ?, ?)"
addvalues = "INSERT INTO DONNEESCAPTEURS (hygrometrie, temperature,ensoleillement) VALUES (?, ?, ?)"
insererjourssuivants = '''INSERT INTO APIMETEO (temps, temperature, humidite) VALUES (?, ?, ?)'''

deletetable = "DELETE FROM APIMETEO"            #permet de supprimer toutes les lignes de la table

#En effet pour les données météos on cherche à être le plus précis possible, on remplace donc les valeurs déjà présente dans la table 
#par celles tout juste acquises.

#Déclaration de différentes variables avant de rentrer dans une boucle infinie :

j = 0  
#la variable j sert à pouvoir tracer les crourbes. Elle evolue entre 0 et 120 (on fait une mesure toutes les 6h, 120 mesures correspondent donc
#aux 30 derniers jours d'arrosage) en fonction du nombre d'acquisition faite  

cooldown = 20               #temps entre deux acquisitions de capteurs (en secondes)
#On met 20 secondes pour nos tests mais il faut remplacer cette valeur par 21600 (soit 6h)

time.sleep(5)               #mettre ici le temps restant avant d'arriver à 0h (en secondes)

while 1:
    if j<120:                #sert à afficher les 30 dernières valeurs acquises
        j=j+1
    seltemp = 0
    selhygro = 0
    selensol = 0

    #On va chercher les données météo
    url_weather = "http://api.openweathermap.org/data/2.5/weather?q="+"cergy"+"&APPID=beb97c1ce62559bba4e81e28de8be095"
    r_weather = requests.get(url_weather)
    data = r_weather.json()
    t = data['main']['temp']  
    humid = data['main']['humidity']
    temps = data['weather'][0]['description']
    url_forecast = "http://api.openweathermap.org/data/2.5/forecast?q="+"cergy"+"&APPID=beb97c1ce62559bba4e81e28de8be095"
    r_forecast = requests.get(url_forecast)
    data = r_forecast.json()

    #Mise en forme des valeurs acquises
    passdegC = t-273.15
    temperature = round(passdegC, 1)
    humidite = humid/100
    mesures = (temps, temperature, humidite)

    #Communication avec les bases de données
    try:
        conn = sqlite3.connect('testbddmeteo2.db')
        cur = conn.cursor()
        cur.execute(tableapimeteo)                          #on crée la bdd pour récupérer les données météo
        cur.execute(tabledonneescapteurs)                   #on crée la bdd pour récupérer les données des capteurs
        cur.execute(deletetable)                            #on commence par effacer tout ce que contenait la table
        cur.execute(addvalues, value)
        print("Connexion réussie à SQLite")
        cur.execute(insererval, mesures)
        moyennetempj3 = 0
        moyennetempj2 = 0
        moyennetempj1 = 0
        #récupération des données des 3 jours à venir (a raison d'une mesure toutes les 3h)
        for i in range (24):
            t = data['list'][i]['main']['temp']
            temps = data['list'][i]['weather'][0]['description']
            date = data['list'][i]['dt_txt']
            print("Previsions pour le {}".format(date))
            print("La temperature moyenne est de {: .1f} degres Celsius".format(t-273.15))
            print("Conditions climatiques : {}".format(temps))

            #moyenne de la température des jours à venir et insertion dans la table
            #cette moyenne doit être modifiée en fonction du temps restant avant le démarage du programme
            #ici on part du pricipe que le programme démarre à minuit.
            if i == 5:
                tempsj1 = temps
            if i == 12:
                tempsj2 = temps
            if i == 20:
                tempsj3 = temps
            if i<25 and i>15:
                moyennetempj3 = moyennetempj3 + t
            if i<16 and i>7:
                moyennetempj2 = moyennetempj2 + t
            if i<8 and i>-1:
                moyennetempj1 = moyennetempj1 + t
        moyennetempj3 = moyennetempj3/8
        moyennetempj3 = moyennetempj3-273.15
        moyennetempj2 = moyennetempj2/8
        moyennetempj2 = moyennetempj2-273.15
        moyennetempj1 = moyennetempj1/8
        moyennetempj1 = moyennetempj1-273.15
        moyennetemperaturej1 = round(moyennetempj1, 2)
        moyennetemperaturej2 = round(moyennetempj2, 2)
        moyennetemperaturej3 = round(moyennetempj3, 2)
        print(moyennetemperaturej3)
        print(moyennetemperaturej2)
        print(moyennetemperaturej1)
        mesuresjour1 = (tempsj1, moyennetemperaturej1, 0)
        mesuresjour2 = (tempsj2, moyennetemperaturej2, 0)
        mesuresjour3 = (tempsj3, moyennetemperaturej3, 0)
        cur.execute(insererjourssuivants, mesuresjour1)
        cur.execute(insererjourssuivants, mesuresjour2)
        cur.execute(insererjourssuivants, mesuresjour3)

        conn.commit()    
        print("Enregistrement inséré avec succès dans la table METEO")

        cur.execute('''SELECT temperature FROM DONNEESCAPTEURS ORDER BY id DESC LIMIT 120''') #sélectionne les 30 dernières valeurs de la table
        seltemp = cur.fetchall() #affiche toutes les valeurs selectionnées
        seltemp[j:]=[]           #supprime toutes les valeurs de la liste après la j eme (sert à tracer les courbes un plus loin dans le programme)
        cur.execute('''SELECT hygrometrie FROM DONNEESCAPTEURS ORDER BY id DESC LIMIT 120''')
        selhygro = cur.fetchall()
        selhygro[j:]=[]
        cur.execute('''SELECT ensoleillement FROM DONNEESCAPTEURS ORDER BY id DESC LIMIT 120''')
        selensol = cur.fetchall()
        selensol[j:]=[]
        cur.close()    
        conn.close()
        print("Connexion SQLite est fermée")
    except sqlite3.Error as error:
        print("Erreur lors de l'insertion dans la table APIMETEO", error)



    #tracé des courbes
    #L'abscisse de chacune des ces courbes et le numéro de l'arrosage allant de 
    x = range(j)
    plt.subplot(3,1,1)                                 #3 lignes 1 colonne 1ere figure
    plt.plot(x,seltemp,color='r', marker = 'o')        #on choisit l'abscisse et l'ordonnée, la couleur, et les les marqueurs (ici couleur rouge et marqueurs en forme de point)
    plt.title('température')                           #on affiche un titre
    plt.grid()                                         #on affiche une grille
    plt.xlabel('arrosage numéro')                      #légende des abscisses
    plt.ylabel('température (en deg)')                 #et des ordonnées
    plt.ylim(-20, 50)                                  #on limite la plage de valeurs à (-20, 50)
    plt.xlim(1, j)

    plt.subplot(3,1,2)
    plt.plot(x,selhygro,color='b', marker = 'o')
    plt.title ('hygrométrie')
    plt.grid()
    plt.xlabel('arrosage numéro')
    plt.ylabel('hygrométrie')
    plt.ylim(0, 1)
    plt.xlim(1, j)

    plt.subplot(3,1,3)
    plt.plot(x, selensol,color='orange', marker = 'o')
    plt.title('ensoleillement')
    plt.grid()
    plt.xlabel('arrosage numéro')
    plt.ylabel('ensoleillement(en Wh par mètre carré)')
    plt.ylim(0, 5000)
    plt.xlim(1, j)
    plt.savefig('static/images/historiquecapteurs.png')
    print("Remplacement des tracés des capteurs")
    #plt.show()
    time.sleep(cooldown)


