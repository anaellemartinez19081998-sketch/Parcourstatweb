import os
import dotenv
from flask import Flask, render_template
from sqlalchemy import create_engine, text
from app.models.user import db, login

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

with app.app_context():
    db.create_all()  # crée la table users si elle n'existe pas

# Connexion pour les requêtes manuelles
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

@app.route("/")
def index():
    with engine.connect() as conn:
        total_formations = conn.execute(text('SELECT COUNT(*) FROM "ParcourStat".formation')).scalar()
        total_etablissements = conn.execute(text('SELECT COUNT(*) FROM "ParcourStat".etablissement')).scalar()
        total_regions = conn.execute(text('SELECT COUNT(*) FROM "ParcourStat".region')).scalar()

    return render_template("index.html",
                           total_formations=total_formations,
                           total_etablissements=total_etablissements,
                           total_regions=total_regions)


from app.routes.auth import auth
app.register_blueprint(auth)

if __name__ == "__main__":
    app.run(debug=True)
