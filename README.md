# Projet PacourStat : guide d'utilisation et description du projet.


- [Projet PacourStat : guide d'utilisation et description du projet.](#projet-pacourstat--guide-dutilisation-et-description-du-projet)
  - [Le projet ParcourStat en quelques mots :](#le-projet-parcourstat-en-quelques-mots-)
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
- [ParcourStatWeb : architecture globale et quelques fonctionnalités](#parcourstatweb--architecture-globale-et-quelques-fonctionnalités)
  - [Architecture globale :](#architecture-globale-)
  - [La page d'accueil :](#la-page-daccueil-)
    - [Architecture](#architecture)
  - [Comparaison des taux de boursiers par formation](#comparaison-des-taux-de-boursiers-par-formation)
    - [Volet de filtres](#volet-de-filtres)
    - [Visualisation et synthèse](#visualisation-et-synthèse)
    - [Architecture](#architecture-1)
  - [Les cartes thématiques](#les-cartes-thématiques)
    - [Architecture](#architecture-2)

<br>
<br>

## Le projet ParcourStat en quelques mots : 

ParcourStat est un projet ambitieux de création d'une application permettant l'exploitabilité des données publiées par le Gouvernement français sur les résultats ParcourSup à l'issue de chaque campagne. 

Ce projet part d'un constat : ces données publiques et librement accessibles sont peu exploitées. Leur exploitation pourrait, au regard de leur exhaustivité, permettre une meilleure compréhension et vision globale du système universitaire français. De plus, les jeux de données sont nombreux : il y en a un par année. Leurs croisements au sein d'un même outil peut permettre d'obtenir une vision globale permettant de comprendre l'évolution du système universitaire français face aux évolutions sociales et politiques. 

Pour cela, nous avons choisi d'exploiter, pour le moment, deux jeux de données : les résultats de ParcourSup de 2018 et de 2024. Cela nous permet de créer un outil de visualisation et de compréhension de l'impact de la crise de la Covid-19 (2019-2022).

Ainsi, ParcourStat vise à traiter ces données afin de créer une base de données relationnelle propre et enrichie servant de base à une application web python basée sur le _framework_ Flask. Et c'est ce que nous vous proposons de découvrir aujourd'hui. 

L'objectif de ParcourStat est mutliple : 
- Permettre aux étudiants de disposer d'un outil complet centralisant les formations et leurs taux d'accessibilités. 
- Permettre aux chercheur de disposer d'un outil de visualisation et de croisement de données sur différents volets, notamment sociaux, afin d'offrir une base solide pour la recherche. 
- Permettre à n'importe qui de mieux comprendre l'évolution de l'accessibilité aux études supérieures et cela pour différentes catégories sociales _(aujourd'hui au coeur de véritables enjeux sociaux)_
- Mettre en valeur et enrichir les jeux de données gouvernementaux et publics.

<br>
<br>

## Installer la base de données : guide

<br>

### Séparation des deux dossiers.

<br>

Comme dit précédemment, ce dossier GitHub contient en réalité deux sous-dossiers. Un sous-dossier contenant l'application web, et un second sous-dossier contenant le nécessaire afin d'installer la base de données sur laquelle l'application se base. 

Veuillez séparer les deux dossiers.

<br>

### Créer un environement virtuel exploitable.

<br>

Avant toutes choses, il convient d'initialiser un environenment virtuel. Ouvrez un terminal, allez à l'emplacement souhaité et créez un environement virtuel à l'aide de `python3 -m venv nom_environement_virtuel` ou `python -m venv nom_environement_virtuel`

> <span style=color:green> Vous pouvez tout à fait créer l'environement virtuel dans le dossier contenant le nécessaire à la création de la base de données.</span>

Dans le même terminal, veuillez activer votre environement virtuel à l'aide de `source nom_environement_virtuel/bin/activate`

Si vous êtes déjà dans le dossier de la base de données, tapez : `pip install -r requirements.txt`. Cela vous installera automatiquement tout le nécessaire pour créer notre base de données. 

Si vous n'êtes pas dans ce dossier, veuillez vous y déplacer à l'aide de la commande `cd` puis lancer `pip install -r requirements.txt`

<br>

### Créer un fichier .env

<br>

À l'aide d'un éditeur de code comme VSCode ou VSCodium, créez un nouveau fichier intitulé **.env**. 

Dans ce fichier, entrez les lignes de code suivantes : 

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

Dans votre gestionnaire de base de données comme DBeaver, créez une base de données nommée "**ParcourStat**" et un schéma dans cette base de données nommé également "**ParcourStat**"

Vous pouvez le faire graphiquement avec votre souris : 
- Clique droit sur "base de données" ou "database" dans l'onglet à gauche, puis "créer une nouvelle base" ou "create database" 
- Puis clique droit sur "schéma" dans l'onglet à gauche, puis "créer un nouveau schéma" ou "create schema" 

ou en SQL : 

```SQL

CREATE DATABASE "ParcourStat"

```

<br>

Puis :

```SQL
CREATE SCHEMA "ParcourStat"
```

C'est ici que nos tables relationnelles se créeront automatiquement.

<br>

### Lancer l'application 

Une fois ces étapes préliminaires faites, il ne reste plus qu'à construire la base de données. 

Dans votre terminal avec votre environnement virtuel programmé, activé et placé dans le dossier de l'application de création de la base de données, lancez la commande `python run.py`. Dans certains cas, cela peut aussi être `python3 run.py`

Laissez l'application faire son oeuvre. Si pas de message d'erreur, allez dans votre gestionnaire de base de donnée vérifier que les tables ont bien été créées ! 

**N'hésitez pas à nous faire part de toute problématique rencontrées !** 

<br>
<br>
<br>

## Installer l'application ParcourStatWeb

<br>

Sortons du dossier de la base de données. Nous n'en aurons plus besoin ! 

Vous pouvez désactiver votre environnement virtuel à l'aide de la commande `deactivate` et sortir du dossier que nous venons de traiter.

<br>

### Créer un environement virtuel exploitable pour ParcourStatWeb: guide 

<br>

ParcourStatWeb demande d'autres instalation que ParcourStatBase. 

Vous devrez alors **créer un autre environnement virtuel.** 

> <span style=color:green> Sur le principe, nous pourrions simplement ajouter les librairies nécessaires à l'environement virtuel précédemment créé. Mais cela risquerait de le surcharger. Afin de ne pas le surcharger, nous proposons de faire un second environement virtuel. </span>

Dans le dossier dans lequel vous avez précédemment créé notre premier environement virtuel, vous pouvez refaire `python3 -m venv nom_environement_virtuel` ou `python -m venv nom_environement_virtuel`. 

Dans le même terminal, veuillez activer votre environement virtuel à l'aide de `source nom_environement_virtuel/bin/activate`

Si vous êtes déjà dans le dossier de la base de données, tapez : `pip install -r requirements.txt`. Cela vous installera automatiquement tout le nécessaire pour utiliser notre application. 

Si vous n'êtes pas dans ce dossier, veuillez vous y déplacer à l'aide de la commande `cd` puis lancer `pip install -r requirements.txt`

<br>

### Créer un fichier .env 

à l'aide d'un éditeur de code comme VSCode ou VSCodium, créez un nouveau fichier intitulé **.env**. 

Dans ce fichier, entrez les lignes de code suivantes : 

```python
pgUser="Votre_utilisateur_PostGre_propriétaire_de_la_base_ParcourStat" # Rentrer son nom d'utilisateur PostGre.
pgPassword="Le_mot_de_passe_de_votre_utilisateur" # Rentrer son mot de passe.
pgHost = localhost 
pgPort = 5432
pgDatabase = ParcourStat #parfois nécessaire d'écrire "ParcourStat". 
```

Bien évidémment, vous réutilisez le même utilisateur et mot de passe que précédemment sauf si vous les avez changés entre temps !

<br>

### Lancer l'application 

<br>

Une fois ces étapes préliminaires faites, il ne reste plus qu'à construire la base de données. 

Dans votre terminal avec votre environnement virtuel programmé, activé et placé dans le dossier de l'application ParcourStatWeb lancez la commande `python app.py`. Dans certains cas, cela peut aussi être `python3 app.py`

L'application se lance après un petit temps de chargement. Une URL apparaîtra dans votre terminal, vous pouvez cliquer dessus afin de l'ouvrir directement dans votre navigateur par défaut ou bien la copier / coller dans le navigateur de votre choix. 

L'application web est maintenant utilisable !

**N'hésitez pas à nous faire part de toute problématiques rencontrées !**

<br>
<br>
<br>

# ParcourStatWeb : architecture globale et quelques fonctionnalités 

<br>

## Architecture globale : 

Notre application est basée sur l'utilisation du _Framework_ Flask qui permet la création de sites web en python, les rendant simples et très souples grâce à son principe de modularité. Nous combinons l'utilisation de Flask avec celle de l'ORM SQLAlchemy pour manipuler avec facilité notre base de données à travers notre application. Cet ORM présente l'avantage d'être encore maintenu, largement utilisé et surtout simple d'utilisation créant ainsi une interface agréable à utiliser entre notre base de données et notre application.

Ainsi notre application est composée de différentes sections, appelées modules, qui toutes jouent un rôle précis. 

Un premier module nommé `app`. C'est le module qui contient l'essentiel de notre application, notamment le traitement de notre base de données. Ce module se divise en 3 modules : `routes` pour la création de nos fonctionnalités et nos calculs SQL avec l'ORM. `models` qui fait le lien entre notre base de données et notre application pour permettre à l'ORM de déployer toute sa puissance. et enfin le module `utils` qui contient quelques ressources sur lesquelles s'appuyer. 

Un second module nommé `static` qui contient toutes nos ressources exploitables et non dynamiques, disons qui n'est pas soumis à variations. Dans notre cas, nous y avons mis du javascript peu sensible au changement, un fichier geojson essentiel à la génération de cartes et notamment pour les régions de France, et du CSS en un fichier .css afin de donner un aspect visuel agréable. 

Un troisième et dernier module nommé `templates` qui contient différentes pages HTML. Pour ce module nous utilisons Jinja2 pour nous permettre de combiner la puissance d'HTML et de python _(emploi de variable python dans le html)_ et de jouer sur la modularité de Flask en créant plutôt des morceaux de pages HTML plutôt que des pages entières afin de briser le côté statique du langage HTML. 

Cette modularité est intéressante car elle renforce la facilité de manipulation de notre site. Grâce à Jinja2, SQLAlchemy et Flask, presque tout se fait à l'aide de variables ce qui permet de modifier un seul morceau de code à un endroit précis afin de changer totalement notre site ou résoudre un problème. Cela nous permet également d'utiliser la fonction `url-for` évitant de créer des liens avec des chemins de fichier en dur. Cela limite les possibles bugs et renforce l'aspect modulaire.

L'utilisateur profite également de cette modularité qui rend les calculs plus légers et donc plus rapides. 

<br>
<br>

## La page d'accueil : 

La page d'accueil a été conçue pour donner à tout utilisateur un aperçu global de la masse de données traitées. Nous avons pensé son espace en deux blocs _(outre la barre de navigation et le footer de notre site)_

Un premier bloc qui présente à l'utilisateur différents chiffres clés. Il s'agit de 3 totaux : 

- Un sur le nombre de formations recensées et accessible sdans notre site 
- Un second sur le nombre total d'établissements recensés 
- Un troisième et dernier total sur le nombre de région françaises traitées. 

Un second bloc qui présente à l'utilisateur une carte dynamique et interactive, conçue en JavaScript et basée sur le fond de carte proposé par OpenStreetMap. Cette carte géolocalise les établissements recensés sur une carte et permet d'un simple coup d'oeil de voir l'ampleur des données traitées. 

Cette carte a aussi été conçue comme une expérience interactive. L'utilisateur peut, à l'aide de différents filtres, chercher une formation ou un établissement précis ou alors se concentrer sur une région française afin de se faire une idée sur l'offre de formation de la région. 

D'un simple clic sur un des nombreux points présents sur la carte, l'utilisateur fait apparaître une info-bulle qui lui donnera accès aux informations essentielles : 

- Nom de l'établissement 
- Statut de l'établissement 
- Formations proposées par l'établissement. 

Cette carte pose cependant quelques problématiques : 

- D'abord, son traitement est un peu lourd et crée donc un temps de chargement légèrement lent.
- Finalement, les points de géolocalisation sont des points calculés. Nous ne disposions pas des localisations des établissements, nous avons créé un point d'établissement à partir d'une moyenne calculée sur l'ensemble des coordonnées des formations proposées par l'établissement. Un message d'avertissement a été ajouté pour prévenir l'utilisateur. 

Nous travaillons sur des mises à jour potentielles afin de régler ces quelques soucis. 

<br>

### Architecture 

<br>

L'utilisateur voit la combinaison de deux templates HTML : base.html, pour la barre de navigation et le footer, et index.html qui contient la carte, les éléments dynamiques JavaScript ainsi que les compteurs créés uniquement en HTML. 

Cette page reçoit les données de plusieurs routes Python présentant différentes requêtes plus ou moins conséquentes. Les données sont envoyées sous forme de variables à notre page HTML et correctement traitées grâce au module Jinja2 qui permet cette interopérabilité. 

Tout cela se base sur l'utilisation de l'ORM SQLAlchemy qui nous permet de traiter simplement et efficacement les données stockées dans notre base de données. Après lui avoir donné l'architecture de notre base de données dans notre module `models/parcourstat.py`, l'ORM permet de traduire très facilement nos requêtes SQL en Python. Cela offre une grande simplicité.

<br>
<br>

## Comparaison des taux de boursiers par formation

<br>

La page de comparaison permet de mettre en regard jusqu'à cinq formations sur la question de l'accès des étudiants boursiers, en comparant les données Parcoursup de 2018 et 2024. Elle s'organise en deux zones : un volet de filtres sur la gauche et une zone de visualisation sur la droite.

<br>

### Volet de filtres

<br>

Le volet de filtres permet à l'utilisateur de constituer sa sélection de formations. Les formations y sont présentées dans une liste déroulante organisée par établissement, ce qui permet de naviguer facilement parmi les milliers de formations disponibles sans être confronté à des doublons de noms. L'utilisateur peut ajouter jusqu'à cinq formations à comparer en cliquant sur le bouton **« Ajouter une formation »**, et supprimer chaque ligne individuellement. Un résumé s'actualise en temps réel au fil des sélections, et le bouton **« Générer »** reste désactivé tant qu'aucune formation n'a été choisie. Une fois la visualisation lancée, le volet se rétracte automatiquement pour laisser la place aux graphiques, et peut être rouvert à tout moment via une flèche latérale.

<br>

### Visualisation et synthèse

<br>

Pour chaque formation sélectionnée, le graphique affiche côte à côte quatre barres :

- le **pourcentage de candidats boursiers** en 2018
- le **pourcentage d'admis boursiers** en 2018
- le **pourcentage de candidats boursiers** en 2024
- le **pourcentage d'admis boursiers** en 2024

Ce format permet de visualiser simultanément l'évolution temporelle (2018 a 2024) et l'écart de sélectivité entre candidats et admis au sein d'une même formation. Les pourcentages sont calculés en agrégeant les effectifs des filières baccalauréat général, technologique et professionnel.

Un résumé textuel accompagne systématiquement le graphique et détaille, pour chaque formation, les effectifs exacts de candidats et d'admis ainsi que les pourcentages de boursiers correspondants pour les deux années. Lorsqu'une formation ne dispose pas de données pour l'une des deux années, cela est signalé explicitement dans le résumé par un avertissement et indiqué sur le graphique par la mention **n/d**.

<br>

### Architecture

<br>

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

<br>
<br>

## Les cartes thématiques

<br>

Les cartes thématiques proposent à l'utilisateur l'accès à des visualisations de données par des cartes choroplèthes selon des thématiques et années précises. 

Nous proposons 3 axes d'analyses, ou thématiques, disponibles pour les deux années concernées par notre projet _(2018 et 2024)_ : 

- Le nombre de formations proposées par région, filtrable par type de formation et années. 
- Le taux d'admission des femmes sur Parcoursup dans chaque région, filtrable par type de formation et années
- Le taux d'admission des boursiers dans chaque région, filtrable par type de formation et années. 

Ainsi, l'utilisateur peut très vite se renseigner sur les disparités existant encore aujourd'hui entre les régions, entres les types de formations et différentes catégories sociales. 

Il nous a semblé important de permettre à l'utilisateur de pouvoir filtrer sur ces 3 niveaux : régions, types de formations, catégories sociales. Cela permet de mieux rendre compte, avec une plus grande granularité, des différentes disparités existant encore aujourd'hui dans le monde des études supérieures. 

<br>

### Architecture 

Deux routes Python alimentent cette page de notre site web. Une première route permettant de rendre exploitable toutes les données cibles. Cette dernière commence par une requête SQL qui d'abord requête toutes les données, puis les agrége par régions notamment, puis se prolonge dans la construction d'un dictionnaire JSON, très facilement exploitable en JavaScript, décomposé en différents niveaux : autant de niveaux que de critères de tri _(donc région, type de formation, % de boursiers/% de femmes)_

Notre seconde routes récupère les données GeoJSON de notre <a href="https://github.com/gregoiredavid/france-geojson/blob/master/departements-avec-outre-mer.geojson"> fichier GeoJSON </a> stocké dans le module `static` et les traite afin de les rendre exploitables. L'idée est de pouvoir superposer ces données à notre fonds de carte OpenStreetMap afin de proposer un découpage régional pertinent.

Du côté de notre templates `carte.html`, nous avons essentiellement du JavaScript afin de créer une carte dynamique. 

La difficultés était de pouvoir proposé une seule page web, une seule carte, mais différentes analyses. C'est là où JavaScript se montre puissant car il permet, en résumé, de compartimenter les données, de les rattacher à des filtres et donc de permettre d'un clic de changer totalement de visualisation. 

Le JavaScript est alors assez conséquent. Nous proposons 3 filtres : un filtre par année, un filtre par type de formations et un filtre par thématiques (nombre de formations, % de boursiers, % de femmes). Cela explique l'importance du code JavaScript. 

Du côté utilisateur, c'est assez simple. Il dispose d'une seule carte et de 3 filtres. A l'action de chacun de ces filtres, la carte se recharge immédiatement et propose une nouvelle visualisation avec une nouvelle coloration qui est légendé. 

L'avantage est que l'utilisateur à accès à un très grand nombre de croisement en simplement quelques clics. 