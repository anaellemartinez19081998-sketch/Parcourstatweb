import os
import json
from flask import Blueprint, Flask, render_template, request, redirect, url_for, jsonify, current_app
from sqlalchemy import func, distinct 
from sqlalchemy.orm import joinedload
from collections import defaultdict
from app.models.user import db, login, Favori
from app.models.parcourstat import Formation, Etablissement, Discipline, TypeFormation, Region, Candidature, Admission, Commune, Departement, Academie




cartes = Blueprint('cartes', __name__)


"""
    Création d'une route /carte pour les cartes choroplèthes thématisées qui feront l'objet d'une page web. 

    Conceptuellement, nous avons une seule carte soumise à 3 filtres. Le type d'établissement, la thématique d'analyse (% boursier, % filles) et l'année d'analyse.

    Ainsi on commence par initialisé nos filtres, chaque filtre correspondant à une variable. 
    Ensuite on commence à requêter toutes les informations dont nous avons besoins : 
        D'abord tous les types de formations que l'on va ordonner par tri alphabétique afin de créer une liste déroulante pour ce filtre.
        Ensuite les données concernant nos admissions et formations : les années, la région, les pourcentages d'admissions de fille et de boursiers, etc.

        Pour les pourcentages, comme l'objectif et de créer une présentation par région on va créer des agrégations via func.avg qui calcul la moyenne des pourcentages.
        .label sert simplement à donner un nom clair au résultat de nos agrégations. C'est le même principe qu'un 'avg(admission.PA_BN_B)AS moyenne_boursiers ' en SQL 

        Et finalement on compte toutes les formations qui existent via func.count(distinct) afin de s'assurer de l'unicité de chaque informations prise en compte.

    Une fois les données requêtées on s'assure que nos données vont pouvoir être filtrée par type de formations et qu'elles sont regroupées par régions et par années.

    Puis pour finir, on structure nos données dans un dictionnaire afin de permettre un accès facile à nos données. Ainsi les filtres pourront s'appliquer et le group by s'opérer.
"""

@cartes.route('/carte')
def afficher_carte():
    try:
        type_id = request.args.get('type_id', type=int)
        active_indic = request.args.get('indic', 'filles') #par défaut, la carte montrée est celle sur la thématiques du pourcentage d'admissions des femmes par régions. C'est ce qu'indique 'filles'
        active_year = request.args.get('year', '2024') # Pareil que précédemment avec l'année 2024.
        
        liste_types = TypeFormation.query.order_by(TypeFormation.nom).all()

        query = db.session.query(
            Region.nom.label('region_nom'),
            Admission.annee.label('annee'),
            func.avg(Admission.PA_F).label('moyenne_filles'),      # % des femmes admises
            func.avg(Admission.PA_NB_B).label('moyenne_boursiers'), # % des boursiers admis
            func.count(distinct(Formation.id)).label('nb_formations')
        ).select_from(Formation)\
         .join(Etablissement)\
         .join(Commune)\
         .join(Departement)\
         .join(Region)\
         .join(Admission, Admission.formation_id == Formation.id) #On indique le chemin de la jointure à suivre afin d'obtenir toutes les données.

        if type_id:
            query = query.filter(Formation.type_formation_id == type_id) #on s'assure que notre filtre de types prend pour valeur l'identifiant de chaque types de formations.

        results = query.group_by(Region.nom, Admission.annee).all() #On fait notre regroupement par régions et par années afin de présenter des cartes annuelles et régionalisées et associant les bonnes données.

        """
            Ce dictionnaire doit permettre de présenter les différentes informations (% de femmes admises, % de boursiers admis, nombre de formations) par régions. 

            Ainsi, on va créer un dictionnaire dont la clés principale sera le nom de la région. Pour chaque région, on aura les comptes associées. 

            Afin de permettre la visualisation pour 2018 et 2024, chaque région se verra associée à deux dictionnaires :
                Un dictionnaire présentant les informations de 2018, 2018 en sera la clés. 
                Un second dictionnaire présentant les informations de 2024, et 2024 en sera la clés.

                De cette manière, on permet la bonne application du filtre année et on évite un produit cartésiens en croisant les données de temporalités différentes.
        """

        stats_temporelles = {} #initalisation du dictionnaire.
        for res in results:
            reg = res.region_nom #comme on groupe par région, on veut que chaque région sont la clés de notre dictionnaire.
            year = str(res.annee) #faire de l'année un objet de type string facilite sa manipulation. 
            
            if reg not in stats_temporelles: #Si la région, donc la clés, n'est pas dans notre dictionnaire alors ont l'ajoute.
                stats_temporelles[reg] = {"nom_reel": reg}
                
            stats_temporelles[reg][year] = {
                # On arrondit simplement la moyenne.
                "filles": round(res.moyenne_filles or 0, 2),
                "boursiers": round(res.moyenne_boursiers or 0, 2),
                "count": res.nb_formations or 0
            } #Création d'un sous dictionnaire par an afin de conditionné l'affichage.

        return render_template('carte.html', stats=stats_temporelles, types=liste_types, 
                               active_type=type_id, active_indic=active_indic, active_year=active_year) #renvoie vers le bon template et les bonnes variables pour présentation.

    except Exception as e:
        # En cas d'erreur, peu importe l'erreur
        db.session.rollback() # Annule toute transaction en cours.
        print(f"Erreur lors de la génération de la carte : {e}") 
        # On renvoie vers le template d'erreur 
        return render_template('erreurs/erreur.html'), 500

"""

    Dans le dossier app/static nous avons un fichier 'Regions_France.geojson'. 
    Il a été trouvé sur le github : 

    Ce fichier présente au format geojson une carte de France et de ces régions y compris d'outre mer. 
    Afin de traiter ces données et d'en faire une carte, on créer une route dédiée au traitement des informations pour création de la carte. 

"""

@cartes.route('/api/geojson')
def get_geojson():
    # Chargement du fichier local.
    file_path = os.path.join(current_app.static_folder, 'Regions_France.geojson')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f) #on charge les données json pour utilisation.
        return jsonify(data)
    except FileNotFoundError: #Si erreur, n'importe laquelle, on retourne se message afin d'informer l'utilisateur.
        return jsonify({"error": "Fichier GeoJSON introuvable dans static/"}), 404