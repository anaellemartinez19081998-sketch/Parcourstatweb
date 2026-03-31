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



"""
    Blueprint afin de faire le renvoie vers nos routes stockées dans des fichiers individuelles.

    Cela permet de respecter l'aspect modulaire de Flask et d'en tirer partie. 
"""

from app.routes.accueil import accueil
app.register_blueprint(accueil)

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

