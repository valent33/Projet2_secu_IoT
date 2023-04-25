# IDS pour caméra HOSAFE HX-2PT1

Ce logiciel est conçu pour détecter toute intrusion sur le réseau domestique et sur l'objet lui même. Il se base sur un modèle algorithmique de Deep-learning LSTM simple entrainé sur 3 types d'attaques différentes : 

- MDK3 (deauthentification)

- Slowloris (DOS)

- Bruteforce
  
  Le logiciel est capable de détecter en temps réel les 3 types d'attaques ainsi que leur arret et le retour en comportement normal de la caméra. Il est fourni avec une interface Web qui permet aux utilisateurs d'enregistrer leur adresse email et de s'identifier afin d'être prévenus en direct par mail lorsque le modèle prend la décision d'identifier une attaque.
  
  
  
  

## Prérequis

Pour exécuter ce programme, vous devez avoir les modules suivants installés sur votre système :

- Apache2 : Indispensable pour faire tourner la partie Web
- pyshark : un module Python qui permet de capturer et analyser des paquets réseau avec la bibliothèque libpcap.
- pandas : un module Python qui offre des structures de données et des outils d'analyse de données.
- pickle : un module Python qui permet de sérialiser et désérialiser des objets Python.
- tensorflow : un module Python qui fournit un framework de calcul numérique basé sur des graphes pour le machine learning et le deep learning.
- numpy : un module Python qui offre des fonctions mathématiques et des opérations sur des tableaux multidimensionnels.
- flask : un module Python qui permet de créer des applications web légères et modulaires.
- mysql.connector : un module Python qui permet de se connecter à une base de données MySQL et d'exécuter des requêtes SQL.
- flask_mysqldb : un module Python qui facilite l'intégration de MySQL avec Flask.
- Xampp afin de gérer les serveurs mySql et apache2 : https://www.apachefriends.org/fr/index.html

Vous pouvez installer les modules pyhton avec la commande suivante :

```bash
pip install pyshark pandas pickle tensorflow numpy flask mysql.connector flask_mysqldb

```

## Fonctionnement



### Partie Web

La partie web est composée des dossiers "static", "templates" et du fichier "app.py" 

Prérequis pour le lancement :

- L'utilisateur doit s'assurer qu'il possède bien une base de donnée sur le serveur MySql qu'il a installé via Xampp. Pour vérifier cela il pourra se rendre à l'addresse 'http://localhost/phpmyadmin/'

Suivre les étapes : New, Créer une database, Importer, charger le fichier BDD.sql

Il devra ensuite ouvrir le fichier app.py et mettre le nom de sa base de données à la fin de la ligne 13 et à la ligne 86 du fichier mailing.py

Explication du lancement :

Pour lancer la partie Web, l'utilisateur doit exécuter et laisser tourner le fichier app.py sur un terminal ainsi que Xampp:

- Lancez le programme avec la commande :
  
  ```bash
    python mailBDD/app.py
  ```

- Ouvrez votre navigateur web et accédez à l’adresse :
    http://localhost:4449

##### Fonctionalités :

- Enregistrement d'un compte utilisateur

- Login d'un utilisateur

- Affichage de la liste des utilisateurs enregistrés

- Modification des coordonnées utilisateurs

- Analyse de trames à postériori par LSTM



### Partie détection en direct :

Faire tourner le modèle de détection en direct s'avère assez complexe car l'utilisateur devra satisfaire les conditions suivantes :

- Posséder un adaptateur wifi capable de passer en mode moniteur et de capter les trames réseaux environnantes dans un format possédant un subtype (802.11)

- Posséder une machine capable de lancer tensorflow pour faire tourner un modèle LSTM

Si l'utilisateur satisfait ces conditions et que les modules de la première partie ont été installés il pourra lors lancer l'éxécution suivante :

```bash
python wireshark_tensorflow.py
```



## Auteurs :

Elard Samuel – Kadiatou Camara– Marc-Olivier Rancœur – William Arnold Tchuisseu Nanmouo – Pierre Auger - Porchet Valentin
