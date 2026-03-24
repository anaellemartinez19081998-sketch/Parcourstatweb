import os
import dotenv
from flask import Flask, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from app.models.user import db, login, Favori
from app.models.parcourstat import Formation, Etablissement, Discipline, TypeFormation, Region

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
    total_formations = Formation.query.count()
    total_etablissements = Etablissement.query.count()
    total_regions = Region.query.count()

    return render_template("index.html",
                           total_formations=total_formations,
                           total_etablissements=total_etablissements,
                           total_regions=total_regions)

@app.route("/formations")
def formations():
    selectivite = request.args.get("selectivite")
    recherche = request.args.get("recherche")
    page = request.args.get("page", 1, type=int)
    par_page = 50

    query = Formation.query

    if selectivite == "true":
        query = query.filter(Formation.selectivite == True)
    elif selectivite == "false":
        query = query.filter(Formation.selectivite == False)
    if recherche:
        query = query.filter(Formation.nom.ilike(f'%{recherche}%'))

    total = query.count()
    total_pages = (total // par_page) + 1

    formations = query.offset((page - 1) * par_page).limit(par_page).all()

    return render_template("formations.html",
                           formations=formations,
                           page=page,
                           total_pages=total_pages,
                           selectivite=selectivite,
                           recherche=recherche)

@app.route("/formation/<int:id>")
def formation_detail(id):
    formation = Formation.query.get_or_404(id)

    est_favori = False
    if current_user.is_authenticated:
        est_favori = Favori.query.filter_by(
            user_id=current_user.id,
            formation_id=id
        ).first() is not None

    return render_template("formation_detail.html",
                           formation=formation,
                           est_favori=est_favori)

@app.route("/favori/ajouter/<int:formation_id>")
@login_required
def ajouter_favori(formation_id):
    favori_existant = Favori.query.filter_by(
        user_id=current_user.id,
        formation_id=formation_id
    ).first()
    
    if not favori_existant:
        favori = Favori(user_id=current_user.id, formation_id=formation_id)
        db.session.add(favori)
        db.session.commit()
    
    return redirect(url_for("formation_detail", id=formation_id))


@app.route("/favori/supprimer/<int:formation_id>")
@login_required
def supprimer_favori(formation_id):
    favori = Favori.query.filter_by(
        user_id=current_user.id,
        formation_id=formation_id
    ).first()
    
    if favori:
        db.session.delete(favori)
        db.session.commit()
    
    return redirect(url_for("formation_detail", id=formation_id))

@app.route("/mes-favoris")
@login_required
def mes_favoris():
    favoris = Favori.query.filter_by(user_id=current_user.id).all()
    
    formations = []
    for favori in favoris:
        formation = Formation.query.get(favori.formation_id)
        if formation:
            formations.append(formation)
    
    return render_template("mes_favoris.html", formations=formations)

from app.routes.auth import auth
app.register_blueprint(auth)

from app.routes.main import main
app.register_blueprint(main)

if __name__ == "__main__":
    app.run(debug=True)

