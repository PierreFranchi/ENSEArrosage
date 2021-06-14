#Scriptbash pour le projet ENSEArrosage 


sudo apt update

#Installation des bibliothèques nécessaires
sudo apt install python3-pip
pip3 install flask
pip3 install matplotlib

#Création d'un dossier pour le projet
mkdir Projet_1B
cd Projet_1B

#On clone le projet dans le dossier précédemment créé
git clone https://github.com/PierreFranchi/ENSEArrosage
cd ENSEArrosage
cd Python\ et\ site\ web

#On lance les programmes pour récupérer les données et on lance le serveur
echo "Début de la récupération des données"
python3 Recuperation\ des\ donnees.py &
echo "Lancement du serveur"
python3 Lancement\ du\ serveur.py 
