# ParcourStat : guide d'utilisation et description du projet

- [ParcourStat : guide d'utilisation et description du projet](#parcourstat--guide-dutilisation-et-description-du-projet)
  - [Le projet ParcourStat](#le-projet-parcourstat)
  - [Fonctionnement du repo GitHub:](#fonctionnement-du-repo-github)
  - [Installer la base de données](#installer-la-base-de-données)
    - [Séparer les deux dossiers](#séparer-les-deux-dossiers)
    - [Créer un environnement virtuel](#créer-un-environnement-virtuel)
    - [Créer un fichier `.env`](#créer-un-fichier-env)
    - [Créer la base de données](#créer-la-base-de-données)
    - [Lancer la création de la base](#lancer-la-création-de-la-base)
  - [Installer l'application ParcourStatWeb](#installer-lapplication-parcourstatweb)
    - [Créer un environnement virtuel dédié](#créer-un-environnement-virtuel-dédié)
    - [Créer un fichier `.env`](#créer-un-fichier-env-1)
    - [Lancer l'application](#lancer-lapplication)
- [ParcourStatWeb : architecture et fonctionnalités](#parcourstatweb--architecture-et-fonctionnalités)
  - [Architecture globale](#architecture-globale)
  - [La page d'accueil](#la-page-daccueil)
    - [Architecture](#architecture)
  - [Comparaison des taux de boursiers par formation](#comparaison-des-taux-de-boursiers-par-formation)
    - [Volet de filtres](#volet-de-filtres)
    - [Visualisation et synthèse](#visualisation-et-synthèse)
    - [Architecture technique](#architecture-technique)
  - [Les cartes thématiques](#les-cartes-thématiques)
    - [Architecture](#architecture-1)
  - [Graphiques par formation](#graphiques-par-formation)
    - [Fonctionnalités](#fonctionnalités)
    - [Architecture technique](#architecture-technique-1)
  - [Authentification et gestion des utilisateurs](#authentification-et-gestion-des-utilisateurs)
    - [Inscription et connexion](#inscription-et-connexion)
    - [Modification du profil](#modification-du-profil)
    - [Système de favoris](#système-de-favoris)
    - [Page de détail et export JSON](#page-de-détail-et-export-json)
  - [Commentaires et likes](#commentaires-et-likes)
    - [Fonctionnalités](#fonctionnalités-1)
    - [Architecture technique](#architecture-technique-2)
    - [Architecture des routes](#architecture-des-routes)

<br>

## Le projet ParcourStat

ParcourStat est une application web exploitant les données publiées par le gouvernement français sur les résultats Parcoursup afin d'offrir une meilleure compréhension de l'accès au système universitaire français, notamment face aux évolutions sociales et politiques de ces dernières années.

Deux jeux de données sont actuellement exploités : les résultats Parcoursup de 2018 et de 2024. 

ParcourStat poursuit plusieurs objectifs :

- Centraliser les formations et leurs taux d'accessibilité dans un outil à destination des étudiants.
- Offrir aux chercheurs un outil de visualisation et de croisement de données sur différents volets, notamment sociaux.
- Rendre accessible à tous la compréhension de l'évolution de l'accès aux études supérieures selon les catégories sociales.
- Mettre en valeur et enrichir les jeux de données gouvernementaux ouverts.

<br>

## Fonctionnement du repo GitHub: 

Ce repo GitHub permet à tout utilisateur de faire fonctionner notre application. 

Ce ReadMe sert de guide d'instruction à suivre afin de faire fonctionner l'application, et également de guide explicatif sur certaines fonctions de notre application. 

Ce repo est composé de deux dossiers : 
- **ParcourStatBase**, qui contient tout le nécessaire pour créer la base de données sur laquelle ParcourStatWeb s'appuie  
- **ParcourStatWeb**, qui contient tout le nécessaire pour faire fonctionner l'application web à partir de la base de données précédemment créer.

<br>

## Installer la base de données

<br>

### Séparer les deux dossiers

<br>

Avant de commencer, nous vous invitons à cloner ou forker le repo GitHub. 

Pour une utilisation occassionnelle, sans volonté de modifier ou quoi que ce soit d'autre, nous vous invitons à sortir **ParcourStatBase** et **ParcourStatWeb** du dossier de téléchargement pour plus de clareté dans la manipulation des dossiers. 

**Cette manipulation n'est pas obligatoire.**

<br>

### Créer un environnement virtuel

Dans un terminal, créez un environnement virtuel à l'emplacement souhaité :

```bash
python3 -m venv nom_environnement_virtuel
```

Activez-le :

```bash
source nom_environnement_virtuel/bin/activate
```

Puis installez les dépendances depuis le dossier de la base de données :

```bash
pip install -r requirements.txt
```

### Créer un fichier `.env`

À la **racine du dossier ParcourStatBase/Application**, créez un fichier `.env` contenant les informations suivantes :

> Donc il faut entrer dans le dossier ParcourStatBase, puis dans le dossier Application et créer ici son `.env`

```
pgDatabase=ParcourStat
pgUser=votre_utilisateur_postgresql
pgPassword=votre_mot_de_passe
pgPort=5432
pgHost=127.0.0.1
pgSchemaImportsCsv=ParcourStat
failOnFirstSqlError=True
failOnFirstCsvError=True
```

### Créer la base de données

Dans votre gestionnaire de base de données, créez une base de données et un schéma tous deux nommés `ParcourStat`. En SQL :

```sql
CREATE DATABASE "ParcourStat";
CREATE SCHEMA "ParcourStat";
```

Les tables relationnelles y seront créées automatiquement à l'étape suivante.

### Lancer la création de la base

Pour cela, avec votre terminal toujours placé dans le dossier **Application** de **ParcourStatBase** et avec l'**environement virtuel dédié et activé**, lancez la commence suivante :

```bash
python run.py
```

Une fois l'exécution terminée sans erreur, vérifiez dans votre gestionnaire que les tables ont bien été créées.

<br>

## Installer l'application ParcourStatWeb

<br>

### Créer un environnement virtuel dédié

ParcourStatWeb requiert des dépendances différentes de celles de ParcourStatBase. Il convient donc de créer un second environnement virtuel, de l'activer, puis d'installer les dépendances depuis le dossier de l'application :

```bash
python3 -m venv nom_environnement_virtuel
source nom_environnement_virtuel/bin/activate
pip install -r requirements.txt
```

> Vous pouvez créer cet environement virtuel dans le même dossier parents que votre précédent environement virtuel, ou directement dans le dossier **ParcourStatWeb**.

### Créer un fichier `.env`

À la racine du dossier **Application** dans **ParcourStatWeb**, créez un fichier `.env` avec les mêmes identifiants que précédemment :

```
pgUser=votre_utilisateur_postgresql
pgPassword=votre_mot_de_passe
pgHost=localhost
pgPort=5432
pgDatabase=ParcourStat
```

> Donc il faut entrer dans le dossier ParcourStatBase, puis dans le dossier Application et créer ici son `.env`

### Lancer l'application

Pour cela, avec votre terminal toujours placé dans le dossier **Application** de **ParcourStatWeb** et avec l'**environement virtuel dédié et activé**, lancez la commence suivante :

```bash
python app.py
```

Une URL s'affiche dans le terminal. Ouvrez-la dans un navigateur pour accéder à l'application.

<br>

# ParcourStatWeb : architecture et fonctionnalités

## Architecture globale

ParcourStatWeb est construite avec le framework Flask, combiné à l'ORM SQLAlchemy pour l'accès à la base de données PostgreSQL. L'application est organisée en trois modules principaux :

- **`app`** : le cœur de l'application, lui-même divisé en trois modules. `routes` (fonctionnalités et requêtes), `models` (correspondance entre la base de données et l'ORM) et `utils` (ressources partagées).
- **`static`** : les ressources statiques, incluant les fichiers JavaScript, un fichier GeoJSON pour les cartes régionales et la feuille de style CSS.
- **`templates`** : les pages HTML rendues via Jinja2, qui permet d'y intégrer des variables Python et de composer les pages par blocs réutilisables.

Cette organisation modulaire facilite la maintenance : chaque composant peut être modifié indépendamment. L'utilisation de `url_for` évite par ailleurs les chemins en dur dans les templates, ce qui limite les risques de régression lors de modifications de la structure du projet.

<br>

## La page d'accueil

La page d'accueil présente deux blocs principaux.

Le premier affiche trois compteurs globaux : le nombre de formations recensées, le nombre d'établissements et le nombre de régions couvertes.

Le second est une carte interactive construite en JavaScript sur fond OpenStreetMap, géolocalisant l'ensemble des établissements. Des filtres permettent de rechercher une formation ou un établissement précis, ou de restreindre l'affichage à une région. Un clic sur un marqueur affiche le nom de l'établissement, son statut et la liste de ses formations.

Deux limites sont à signaler : le volume de données entraîne un temps de chargement perceptible, et les positions des établissements sont des coordonnées calculées. En l'absence de géolocalisation directe, elles correspondent à la moyenne des coordonnées de leurs formations. Un message en informe l'utilisateur.

### Architecture

La page combine `base.html` (navigation et footer) et `index.html` (carte, compteurs, JavaScript). Les données sont transmises depuis plusieurs routes Flask via des variables Jinja2, sur la base de requêtes SQLAlchemy définies dans `models/parcourstat.py`.

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

Ce format permet de visualiser simultanément l'évolution temporelle (2018 → 2024) et l'écart de sélectivité entre candidats et admis au sein d'une même formation. Les pourcentages sont calculés en agrégeant les effectifs des filières baccalauréat général, technologique et professionnel.

Un résumé textuel accompagne systématiquement le graphique et détaille, pour chaque formation, les effectifs exacts de candidats et d'admis ainsi que les pourcentages de boursiers correspondants pour les deux années. Lorsqu'une formation ne dispose pas de données pour l'une des deux années, cela est signalé explicitement dans le résumé par un avertissement ⚠️ et indiqué sur le graphique par la mention **n/d**.

### Architecture technique

Côté client, un fichier JavaScript (`comparaison.js`) gère l'interface de filtrage et envoie au serveur, via une requête `fetch` en POST, un objet JSON contenant les identifiants des formations sélectionnées. Côté serveur, Flask reçoit cette requête et orchestre deux types d'accès à la base de données PostgreSQL.

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

Les résultats sont ensuite traités en Python pour calculer les pourcentages et construire les phrases de la synthèse textuelle, puis le graphique est généré avec **Matplotlib** et encodé en base64 pour être transmis au navigateur dans la réponse JSON. Le JavaScript n'a alors plus qu'à insérer l'image reçue dans un élément `<img>` et afficher les blocs de synthèse, sans aucune logique de calcul ou de visualisation côté client.

<br>

## Les cartes thématiques

Les cartes thématiques proposent des visualisations choroplèthes des données Parcoursup par région, selon trois axes d'analyse disponibles pour les deux années couvertes par le projet (2018 et 2024) :

- le nombre de formations proposées par région, filtrable par type de formation et par année ;
- le taux d'admission des femmes dans chaque région, filtrable par type de formation et par année ;
- le taux d'admission des boursiers dans chaque région, filtrable par type de formation et par année.

Ces trois niveaux de filtrage (région, type de formation, catégorie sociale) permettent de rendre compte avec une certaine granularité des disparités qui persistent dans l'accès aux études supérieures.

### Architecture

Deux routes Python alimentent cette page. La première construit un dictionnaire JSON structuré en autant de niveaux que de critères de tri (région, type de formation, indicateur), directement exploitable en JavaScript. La seconde charge le fichier GeoJSON stocké dans `static` afin de superposer un découpage régional au fond de carte OpenStreetMap.

Côté template (`carte.html`), la logique repose principalement sur JavaScript. Un seul fichier et une seule carte servent les trois analyses : à chaque action sur les filtres (année, type de formation, thématique), la carte se recharge et propose une nouvelle coloration accompagnée de sa légende. L'utilisateur accède ainsi à un grand nombre de croisements en quelques clics.

## Graphiques par formation

### Fonctionnalités
La page "Graphiques par formation" permet à l'utilisateur de visualiser les données pour une formation choisie, en filtrant par année (2018 ou 2024) et par situation (admis ou candidats). Une fois les filtres sélectionnés, elle affiche quatre graphiques interactifs ainsi qu'un résumé chiffré en bas de la page. Les fonctionnalités sont précisément les suivantes :
* Sélection de filtres : choix d'une formation avec une recherche textuelle possible, choix d'une année, et choix d'une situation
* Liste des établissements proposant la formation choisie sous forme de menu déroulant contenant : 
  * le taux d'admission de cette formation dans chacun d'entre eux, 
  * le ratio nombre de candidats/ nombre d'admis. 
  * L'adresse et le site web des établissements sont également affichés
* Quatre graphiques en camembert dynamiques, générés par la sélection des filtres, permettant de visualiser pour chaque formation : 
  * La part des étudiants boursiers 
  * La répartition par sexe 
  * La filière d'origine (technologique, professionnelle, générale)
  * La mention au bac

### Architecture technique 
La page est construite par deux routes python stockées dans 'graphique.py'

La première, /graphique, génère la structure de la page globale et retourne le template graphique.html avec des données statiques issues de la base de données : liste des établissements, informations sur les établissement, structure du formulaire de recherche des formations.

Le template 'graphique.html' construit ensuite la structure de la page avec le formulaire de recherche, l'affichage des établissements, les espaces prévus pour les graphiques, et le bloc prévu pour le résumé.

La seconde route, /graphiques/donnees, est dédiée aux données des graphqiues requêtées de manière dynamique. Elle réalise notamment des calculs de pourcentage pour calculer les taux affichés dans les graphiques. Elle retourne un dictionnaire JSON reçu et exécuté par un script javascript. 

En effet, le fichier 'graphique.js' reçoit les paramètres donnés par l'utilisateur et appelle la route /graphique/donnees via fetch(), recevant ainsi les données en JSON. Le script remplit ensuite les quatre graphiques avec les données et selon les paramètres rentrés par l'utilisateur. 


## Authentification et gestion des utilisateurs

ParcourStat propose un système complet de gestion des utilisateurs, développé avec Flask-Login et SQLAlchemy.

### Inscription et connexion

Un visiteur peut créer un compte en renseignant un nom d'utilisateur, une adresse email et un mot de passe. Le mot de passe est chiffré avec werkzeug avant d'être stocké en base — il n'est jamais conservé en clair. La connexion vérifie les identifiants et crée une session sécurisée via Flask-Login.

### Modification du profil

Un utilisateur connecté peut modifier son nom d'utilisateur et son adresse email depuis la page `/profil`. L'application vérifie que le nouvel email n'est pas déjà utilisé par un autre compte avant de sauvegarder les modifications.

### Système de favoris

Tout utilisateur connecté peut mettre des formations en favoris depuis leur page de détail. Les favoris sont consultables depuis la page `/mes-favoris`. L'ajout et la suppression utilisent des transactions SQLAlchemy avec rollback automatique en cas d'erreur.

### Page de détail et export JSON

Chaque formation dispose d'une page de détail accessible depuis la liste des formations. Elle affiche les informations de l'établissement (nom, statut, adresse, site web, image Wikidata  si disponible), le type de formation, la discipline et la sélectivité. Un bouton permet d'exporter les données de la formation au format JSON via la route `/formation/<id>/export.json`.

## Commentaires et likes

Les utilisateurs connectés peuvent laisser des commentaires sous chaque page de détail d'une formation. Chaque commentaire affiche le nom de l'auteur, la date de publication et le nombre de likes.

### Fonctionnalités

- **Publier un commentaire** : un formulaire est disponible en bas de chaque page de détail pour les utilisateurs connectés.
- **Supprimer un commentaire** : seul l'auteur du commentaire peut le supprimer via le bouton 'effacer".
- **Liker un commentaire** : chaque utilisateur connecté peut liker ou unliker un commentaire (toggle)

### Architecture technique

Trois routes gèrent les commentaires, regroupées dans `app/routes/commentaires.py` :

- `POST /formation/<id>/commentaire/ajouter` crée un commentaire en base
- `POST /commentaire/<id>/supprimer` supprime un commentaire (auteur uniquement)
- `POST /commentaire/<id>/like` like ou unlike un commentaire (toggle)

Deux modèles ORM sont utilisés, définis dans `app/models/user.py` :

- `Commentaire` stocke le contenu, l'auteur et la formation associée
- `LikeCommentaire` stocke le lien entre un utilisateur et un commentaire liké

Les opérations d'écriture en base utilisent des transactions avec rollback automatique en cas d'erreur.


### Architecture des routes

Les routes sont organisées en blueprints :
- `auth.py` — inscription, connexion, déconnexion, modification du profil
- `formations.py` — liste des formations avec recherche/filtres/pagination, page détail
- `favoris.py` — ajout, suppression, liste des favoris
- `export.py` — export JSON des données de formation
