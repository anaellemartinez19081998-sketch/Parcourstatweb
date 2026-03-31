import os
import dotenv
from flask import Flask, render_template, request, redirect, url_for, jsonify, current_app
from flask_login import current_user, login_required
from sqlalchemy import func, distinct 
from sqlalchemy.orm import joinedload
from collections import defaultdict
from app.models.user import db, login, Favori
from app.models.parcourstat import Formation, Etablissement, Discipline, TypeFormation, Region, Candidature, Admission, Commune, Departement, Academie

dotenv.load_dotenv(".env")


app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'une-cle-secrete'
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'postgresql://{user}:{password}@{host}:{port}/{database}'.format(
        user=os.environ.get("pgUser"),
        password=os.environ.get("pgPassword"),
        host=os.environ.get("pgHost"),
        port=os.environ.get("pgPort"),
        database=os.environ.get("pgDatabase")
    )
)

# Initialisation
db.init_app(app)
login.init_app(app)
login.login_view = "auth.connexion"
login.login_message = "Veuillez vous connecter pour accéder à cette page."

with app.app_context():
    db.create_all()  # crée la table users si elle n'existe pas

@app.route("/")
def index():
    """
        Création d'une route acceuille qui doit permettre la génération de 3 encarts présentant le nombre de total
        de formations, établissement et régions recensé dans notre site. Ainsi qu'une carte dynamique et interactive 
        géolocalisant les formations recensées et regroupées par établissement. 

        D'abord on procède au comptage du nombre de formation, d'établissement et de régions dans des variables
        afin de stocker leurs résultats et de pouvoir les réutiliser.

        Ensuite on prépare les données pour la carte. 
            D'abord le menu déroulant du filtre régional afin de recentrer la carte sur une région française.
            Ensuite on fait notre jointure pour obtenir toutes les informations sur nos établissements et on stocke cela dans un dictionnaire
            ainsi pour chaque notre dictionnaire va présenter toute les informations pour chaque établissement. 
            Enfin on converti an JSON pour utiliser les coordonnées que l'on calcule en même temps sur notre carte 
            GéoJson. 

        Cette fonction pourrait être simplifiée si nous avions eu en notre possession les coordoonnées des établissements. 
        Comme ce n'est pas le cas et que nous n'avons pas réussi à intégrer du Géocodage pour près de 15000 établissement à notre workflow, 
        nous avons choisi cette solution fonctionnelle. 
    """
    # Calcul des totaux pour les tables formations, établissements et communes à l'aide de la fonction count().
    total_formations = Formation.query.count()
    total_etablissements = Etablissement.query.count()
    total_regions = Region.query.count()

    # Stocker les régions par ordre alphabétique dans une variable. On l'utilisera pour créer notre filtre au menu déroulant.
    regions_list = Region.query.order_by(Region.nom).all()

    """
        Notre variable all_formations permet de préparer en amont notre jointure sur 4 tables. Ainsi on évite, comme en SQL,
        les multiples allées et retours. Comme la jointure est faites en avance, toutes les données sont temporairement disponible 
        et on a pas besoin de faire de nouvelles jointures.

        Avec Formation.query.options on indique à l'ORM que l'on modifie son comportement par défaut. Ainsi il va devoir requêter les 4 tables 
        et pouvoir le faire. 

        joinedload est l'équivalent d'un "left outer join". On va chercher des correspondances d'informations avec la table depuis laquelle on part 
        et si aucune informations n'est disponible pour un enregistrement, on obtient des valeurs NULL. 
        L'avantage est de pouvoir les enchaîner afin de créer une chaîne. La table dite de droite, devient la table de gauche à son tour et ainsi de suite. 

        C'est parfait pour pouvoir remonter une chaîne de tables, une succession de tables liées, comme ici. 
    """
    all_formations = Formation.query.options(
        joinedload(Formation.etablissement)
            .joinedload(Etablissement.commune)
            .joinedload(Commune.departement)
            .joinedload(Departement.region)
    ).all() #on récupère toutes les données issus de cette jointure. Elle est sous forme de liste 

    # On initialise notre dictionnaire que l'on va remplir avec les informations obtenus sur chaque établissements.
    etab_groups = {}


    # On créer une boucle afin de récupérer les informations géographiques pour chaque établissements. 
    # Pour cela on utilise la jointure préparée en amont ! 
    for f in all_formations:
        if f.coordonnees_gps_formation and f.etablissement: 
            
            """
                Nos cordonnées sont stockées dans une seule colonne pour chaque établissement 
                au format suivant : latitude,longitude. 
                Dans cette forme actuelle, ce n'est pas exploitable. 

                Notre boucle se charge de séparer latitude et longitude en champs séparés pour chaque formations listées 
                et d'assigner ces coordonnées préparée aux établissements correspondants. 

                En somme, pour chaque établissement on créer des champs séparés, associe les bonnes données entre elles, puis stocke cela dans le dictionnaire.

                On va alors passer d'une liste récupérée dans all_formations à un dictionnaire stucturé exploitable.
            """
            
            try:
                # Séparation de notre unique champs coordonnées en deux champs latitude et longitude pour exploitation via geojson.
                parts = f.coordonnees_gps_formation.split(',')
                lat = float(parts[0].strip())
                lng = float(parts[1].strip())
                
                # Tout dictionnaire fonctionne sur une clès. Dans un dictionnaire par établissement, il est logique que cette clés soit le nom de l'établissement ou son ID. 
                # L'ID est unique, et est ainsi une ressource plus fiable. Alors on stocke l'ID dans une variable afin de manipuler plus facilement cette clés.
                etab_id = f.etablissement.id
                
                # Sécurisation de notre chargement. Avec nom_region = "Inconnue" on s'assure que pour chaque établissement il y aura des informations. 
                # Si on peut reconstituer la chaîne de traitement, on remplace "Inconnue" par le nom de la région.
                # ça limite les possibilités d'erreur.
                nom_region = "Inconnue"
                if f.etablissement.commune and \
                   f.etablissement.commune.departement and \
                   f.etablissement.commune.departement.region:
                    nom_region = f.etablissement.commune.departement.region.nom


                """
                On remplit notre dictionnaire en s'assurant que l'ID, unique, n'est pas déjà entré dans le dictionnaire. 
                Si l'ID n'existe pas dans le dictionnaire, alors on rentre pour chaque établissement un dictionnaire de valeurs.
                
                Rappelons également que notre dictionnaire fonctionne de cette manière : 1 établissement = X formations. 
                Ainsi le nom, le status de l'établissement et la région sont des données uniques car rattachée à l'établissement.
                Mais les coordoonnée GPS découpées et le nom des formations vont se multiplier car il en existe plusieurs par établissements. 

                On procède alors de la manière suivante : 
                    On créer des listes vides pour chaque champs qui vont comporter plusieurs valeurs sur chaque ID
                    Dans second temps, avant la fin de la boucle, on va ajouter aux listes via .append chaque valeur trouvées. 

                    Ainsi on va stocker un dictionnaire pour chaque établissement avec des informations propre à l'établissement 
                    et chacune des formations. 
                
                """
                if etab_id not in etab_groups:
                    etab_groups[etab_id] = {
                        'nom': f.etablissement.nom,
                        'statut': f.etablissement.statut or "Non renseigné",
                        'region': nom_region,
                        'lats': [],
                        'lngs': [],
                        'formations': []
                    }
                # Ajout des données des formations.
                etab_groups[etab_id]['lats'].append(lat)
                etab_groups[etab_id]['lngs'].append(lng)
                etab_groups[etab_id]['formations'].append(f.nom)
                
            except (ValueError, IndexError, TypeError): #On gère une erreur possible, bien que déjà fortement limitée par différents contrôle.
                continue # On ne veut pas briser la boucle. Cette boucle traite près de 15 000 établissements, nous ne souhaitons pas briser cette chaîne.

    """
        Notre dictionnaire d'informations complet n'assure pas l'employabilité de ces informations sur une carte en GeoJson. 
        Autrement dit, on a des informations, des coordonnées mais elles n'ont pas de valeur géographiques pour le moment. 

        On va alors chercher à leurs donner cette valeur pour les situer sur une carte.

        Comme nous n'avons pas de coordonnées GPS par établissements, on part du principe que les coordonnées GPS des formations 
        sont dans 90% de nos cas à peu près groupées sur leurs établissements. 

        On va donc d'abord calculer une moyenne mathématique afin de reconstituer un point central qui sera celui de notre établissement. 

        Ensuite on va préparer l'infobulle qui s'affichera lors du survolle d'un point. Pour cela on construit un dictionnaire de données 
        qui va présenter toutes les informations que l'on souhaite faire figurer. On va notamment reprendre notre liste de formations définie plus tôt. 
        La limite de 5 pour les formations permet d'éviter une troop grande liste d'informations que viendrais gâcher la carte. Dans la plus part des cas, 5 est un nombre suffisant.

        On veut tout de même indiquer qu'il existe plus de 5 formations dans les cas échéants. C'est le rôle de total_plus qui va calculer ce qui 
        ne sera présenter d'office et affichera donc le nombre de formations que cet établissement propose. 
    """
    points_carte = [] 
    for eid, data in etab_groups.items():
        avg_lat = sum(data['lats']) / len(data['lats'])
        avg_lng = sum(data['lngs']) / len(data['lngs'])
        
        points_carte.append({
            'etablissement': data['nom'],
            'statut': data['statut'],
            'region': data['region'],
            'lat': avg_lat,
            'lng': avg_lng,
            'count': len(data['formations']),
            'liste': data['formations'][:5],
            'total_plus': max(0, len(data['formations']) - 5)
        })

    # On utilise render_template pour envoyer ces informations structurée à un template HTML défini et structuré pour présentations.
    return render_template("index.html",
                           total_formations=total_formations,
                           total_etablissements=total_etablissements,
                           total_regions=total_regions,
                           regions=regions_list,
                           points_carte=points_carte)





"""
    Blueprint afin de faire le renvoie vers nos routes stockées dans des fichiers individuelles.

    Cela permet de respecter l'aspect modulaire de Flask et d'en tirer partie. 
"""

from app.routes.auth import auth
app.register_blueprint(auth)

from app.routes.main import main
app.register_blueprint(main)

from app.routes.formations import formations_bp
app.register_blueprint(formations_bp)

from app.routes.cartes import cartes
app.register_blueprint(cartes)

from app.routes.graphique import graphique
app.register_blueprint(graphique) 

from app.routes.favoris import favoris
app.register_blueprint(favoris)

from app.routes.export import export
app.register_blueprint(export)

from app.routes.commentaires import commentaires_bp
app.register_blueprint(commentaires_bp)

if __name__ == "__main__":
    app.run(debug=True)

