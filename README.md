# Déploiement et utilisation de ParcourStat


- [Déploiement et utilisation de ParcourStat](#déploiement-et-utilisation-de-parcourstat)
  - [Installer la base de données : guide](#installer-la-base-de-données--guide)
    - [Séparation des deux dossiers.](#séparation-des-deux-dossiers)
    - [Créer un environement virtuel exploitable.](#créer-un-environement-virtuel-exploitable)
    - [Créer un fichier .env](#créer-un-fichier-env)
    - [Créer le nécessaire dans son Gestionnaire de Base de Données (DBeaver)](#créer-le-nécessaire-dans-son-gestionnaire-de-base-de-données-dbeaver)
    - [Lancer l'application](#lancer-lapplication)
  - [Installer l'application ParcourStatWeb](#installer-lapplication-parcourstatweb)
    - [Créer un environement virtuel exploitable pour ParcourStatWeb: guide](#créer-un-environement-virtuel-exploitable-pour-parcourstatweb-guide)
    - [Créer un fichier .env](#créer-un-fichier-env-1)
    - [Lancer l'application](#lancer-lapplication-1)
- [ParcourStatWeb : quelques fonctionnalités](#parcourstatweb--quelques-fonctionnalités)
  - [Comparaison des taux de boursiers par formation](#comparaison-des-taux-de-boursiers-par-formation)
    - [Volet de filtres](#volet-de-filtres)
    - [Visualisation et synthèse](#visualisation-et-synthèse)
    - [Architecture](#architecture)

## Installer la base de données : guide

<br>

### Séparation des deux dossiers.

<br>

Comme dit précédemment, ce dossier github contient en réalité deux sous-dossiers. Un sous-dossier contenant l'application web, et un second sous-dossier contenant le nécessaire afin d'installer la base de donnée sur laquelle l'application se base. 

Veuillez séparer les deux dossiers.

<br>

### Créer un environement virtuel exploitable.

<br>

Avant toute choses, il convient d'initialiser un environement virtuel. Ouvrez un terminal, aller à l'emplacement souhaité et créez un environement virtuel à l'aide de `python3 -m venv nom_environement_virtuel` ou `python -m venv nom_environement_virtuel`

> <span style=color:green> Vous pouvez tout à fait créer l'environement virtuel dans le dossier contenant le nécessaire à la création de la base de données.</span>

Dans le même terminal, veuillez activer votre environement virtuel à l'aide de `source nom_environement_virtuel/bin/activate`

Si vous êtes déjà dans le dossier de la base de données, taper : `pip install -r requirements.txt`. Cela vous installera automatiquement tout le nécessaire pour créer notre base de donnée. 

Si vous n'êtes pas dans ce dossier, veuillez vous y déplacer à l'aide de la commande `cd` puis lancer `pip install -r requirements.txt`

<br>

### Créer un fichier .env

<br>

à l'aide d'un éditeur de code comme VSCode ou VSCodium, créer un nouveau fichier intitulé **.env**. 

Dans ce fichier, entrer les lignes de codes suivantes : 

```python
pgDatabase="ParcourStat"
pgUser="Votre_utilisateur_PostGre_propriétaire_de_la_base_ParcourStat" # Rentrer son nom d'utilisateur PostGre.
pgPassword="Le_mot_de_passe_de_votre_utilisateur" # Rentrer son mot de passe.
pgPort=5432
pgHost=127.0.0.1
pgSchemaImportsCsv="ParcourStat"
failOnFirstSqlError=True
failOnFirstCsvError=True
```
<br>

### Créer le nécessaire dans son Gestionnaire de Base de Données (DBeaver)

Dans son gestionnaire de base de données comme DBeaver, créer une DataBase nommée "**ParcourStat**" et un schéma dans cette DataBase nommé également "**ParcourStat**"

C'est ici que nos tables relationnelles se créeront automatiquement.

<br>

### Lancer l'application 

Une fois ces étapes préliminaires faites, il ne reste plus qu'à construire la base de données. 

Dans votre terminal avec votre environement virtuel programmé, activé et placé dans le dossier de l'application de création de la base de donnée lancer la commande `python run.py`. Dans certains cas, cela peut aussi être `python3 run.py`

Laisser l'application faire son oeuvre. Si pas de message d'erreur, aller dans votre gestionnaire de base de donnée vérifier que les tables ont bien été créer ! 

**N'hésitez pas à nous faire part de toute problématique rencontrées !** 

<br>
<br>
<br>

## Installer l'application ParcourStatWeb

<br>

Sortons du dossier de la base de données. Nous n'en aurons plus besoins ! 

Vous pouvez désactiver votre environement virtuel à l'aide de la commande `deactivate` et sortir du dossier que nous venons de traiter.

<br>

### Créer un environement virtuel exploitable pour ParcourStatWeb: guide 

<br>

ParcourStatWeb demande d'autres instalaltion que ParcourStatBase. 

Vous devrez alors créer un autre environement virtuel 

> <span style=color:green> Sur le principe, nous pourrions simplement ajouter les librairies nécessaire à l'environement virtuel précédemment créer. Mais cela risquerais de le surcharger. Afin de ne pas le surcharger, nous proposons de faire un second environement virtuel. </span>

Dans le dossier dans lequel vous avez précédemment créer notre premier environement virtuel, vous pouvez refaire `python3 -m venv nom_environement_virtuel` ou `python -m venv nom_environement_virtuel`. 

Dans le même terminal, veuillez activer votre environement virtuel à l'aide de `source nom_environement_virtuel/bin/activate`

Si vous êtes déjà dans le dossier de la base de données, taper : `pip install -r requirements.txt`. Cela vous installera automatiquement tout le nécessaire pour utiliser notre application. 

Si vous n'êtes pas dans ce dossier, veuillez vous y déplacer à l'aide de la commande `cd` puis lancer `pip install -r requirements.txt`

<br>

### Créer un fichier .env 

à l'aide d'un éditeur de code comme VSCode ou VSCodium, créer un nouveau fichier intitulé **.env**. 

Dans ce fichier, entrer les lignes de codes suivantes : 

```python
pgUser="Votre_utilisateur_PostGre_propriétaire_de_la_base_ParcourStat" # Rentrer son nom d'utilisateur PostGre.
pgPassword="Le_mot_de_passe_de_votre_utilisateur" # Rentrer son mot de passe.
pgHost = localhost 
pgPort = 5432
pgDatabase = ParcourStat #parfois nécessaire d'écrire "ParcourStat". 
```

Bien évidémment, vous réutiliser le même utilisateur et mot de passe que précédemment sauf si vous les avez changer entre temps !

<br>

### Lancer l'application 

Une fois ces étapes préliminaires faites, il ne reste plus qu'à construire la base de données. 

Dans votre terminal avec votre environement virtuel programmé, activé et placé dans le dossier de l'application de création de la base de donnée lancer la commande `python app.py`. Dans certains cas, cela peut aussi être `python3 app.py`

L'application se lance après un petit temps de chargement. Une URL apparaîtra dans votre terminal, vous pouvez cliquer dessus afin de l'ouvrir directement dans votre navigateur par défaut ou bien la copier / coller dans le navigateur de votre choix. 

L'application web est maintenant utilisable !

**N'hésitez pas à nous faire part de toute problématique rencontrées !**

<br>
<br>
<br>

# ParcourStatWeb : quelques fonctionnalités 

<br>

## Comparaison des taux de boursiers par formation

La page de comparaison permet de mettre en regard jusqu'à cinq formations sur la question de l'accès des étudiants boursiers, en comparant les données Parcoursup de 2018 et 2024. Elle s'organise en deux zones : un volet de filtres sur la gauche et une zone de visualisation sur la droite.

### Volet de filtres

Le volet de filtres permet à l'utilisateur de constituer sa sélection de formations. Les formations y sont présentées dans une liste déroulante organisée par établissement, ce qui permet de naviguer facilement parmi les milliers de formations disponibles sans être confronté à des doublons de noms. L'utilisateur peut ajouter jusqu'à cinq formations à comparer en cliquant sur le bouton **« Ajouter une formation »**, et supprimer chaque ligne individuellement. Un résumé s'actualise en temps réel au fil des sélections, et le bouton **« Générer »** reste désactivé tant qu'aucune formation n'a été choisie. Une fois la visualisation lancée, le volet se rétracte automatiquement pour laisser la place aux graphiques, et peut être rouvert à tout moment via une flèche latérale.

### Visualisation et synthèse

Pour chaque formation sélectionnée, le graphique affiche côte à côte quatre barres :

- le **pourcentage de candidats boursiers** en 2018
- le **pourcentage d'admis boursiers** en 2018
- le **pourcentage de candidats boursiers** en 2024
- le **pourcentage d'admis boursiers** en 2024

Ce format permet de visualiser simultanément l'évolution temporelle (2018 a 2024) et l'écart de sélectivité entre candidats et admis au sein d'une même formation. Les pourcentages sont calculés en agrégeant les effectifs des filières baccalauréat général, technologique et professionnel.

Un résumé textuel accompagne systématiquement le graphique et détaille, pour chaque formation, les effectifs exacts de candidats et d'admis ainsi que les pourcentages de boursiers correspondants pour les deux années. Lorsqu'une formation ne dispose pas de données pour l'une des deux années, cela est signalé explicitement dans le résumé par un avertissement et indiqué sur le graphique par la mention **n/d**.

### Architecture

Côté utilisateur, un fichier JavaScript (`comparaison.js`) gère l'interface de filtrage et envoie au serveur, via une requête `fetch` en POST, un objet JSON contenant les identifiants des formations sélectionnées. Côté serveur, Flask reçoit cette requête et orchestre deux types d'accès à la base de données PostgreSQL.

Pour charger la liste des formations et des établissements affichés dans le volet de filtres, le code utilise l'ORM SQLAlchemy via les modèles `Formation` et `Etablissement` déjà définis dans le projet. Ces modèles permettent d'écrire des requêtes en Python pur :

```python
Formation.query.filter_by(etablissement_id=etab.id).order_by(Formation.nom).all()
```

sans écrire de SQL, SQLAlchemy se chargeant de la traduction. Pour le calcul des indicateurs statistiques en revanche, la complexité des agrégations (sommes conditionnelles sur plusieurs colonnes, jointure entre les tables `candidatures` et `admissions`, filtre sur les années) rend le SQL brut plus lisible et plus précis. Ces requêtes sont donc écrites directement en SQL et exécutées via `db.session.execute(text(...))`, la session SQLAlchemy garantissant la sécurité des paramètres contre les injections SQL grâce aux paramètres nommés (`:formation_id`) :

```sql
SELECT
    ca.annee,
    SUM(ca.ec_b_nb_g + ca.ec_b_nb_t + ca.ec_b_nb) AS num_cand,
    SUM(ca.ec_nb_g + ca.ec_nb_t + ca.ec_nb_p)      AS den_cand,
    SUM(ad.ea_bn_b)                                 AS num_adm,
    SUM(ad.ea_nb_g + ad.ea_nb_t + ad.ea_nb_p)      AS den_adm
FROM "ParcourStat".candidatures ca
JOIN "ParcourStat".admissions ad
  ON ad.formation_id = ca.formation_id
 AND ad.annee = ca.annee
WHERE ca.formation_id = :formation_id
  AND ca.annee IN (2018, 2024)
GROUP BY ca.annee
```

Les résultats sont ensuite traités en Python pour calculer les pourcentages et construire les phrases de la synthèse textuelle, puis le graphique est généré avec **Matplotlib** et encodé en base64 pour être transmis au navigateur dans la réponse JSON. Le JavaScript n'a alors plus qu'à insérer l'image reçue dans un élément `<img>` et afficher les blocs de synthèse, sans aucune logique de calcul ou de visualisation du cote de l'utilisateur.
