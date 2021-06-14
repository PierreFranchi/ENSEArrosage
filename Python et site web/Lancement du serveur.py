#Ce programme sert à lancer le site web permettant de contrôle de l'irrigation

#On importe les bibliothèques nécessaires
from flask import Flask, Response, render_template, request

#initialisation de l'API flask
app = Flask(__name__)

#On définit un chemin d'accès pour la racine du site
@app.route('/')
def affichage_site():
    return render_template('ENSEArrosage.html')


#On peut rentrer une durée d'arrosage. Pour cela on récupère le temps rentré par l'utilisateur. On s'en servira plus tard
#pour la partie commande de l'électrovanne. Une fois le temps entré, on affiche une page de confirmation.
@app.route('/valid', methods=['post'])
def recup():
    mode = request.form['mode']
    durée = request.form['durée']
    print('mode :',mode,'| durée =',durée,'minutes')
    return render_template('ENSEArrosage_valid.html')

app.run(host='0.0.0.0')