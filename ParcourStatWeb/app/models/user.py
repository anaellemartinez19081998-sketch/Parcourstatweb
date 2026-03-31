from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone


login = LoginManager()
db = SQLAlchemy()


class UserModel(UserMixin, db.Model):
    """
    ORM représentant la table 'users' en base de données.
    
    UserMixin fournit les méthodes requises par Flask-Login :
    is_authenticated, is_active, is_anonymous, get_id()
    
    Colonnes :
        - id : clé primaire auto-incrémentée
        - email : adresse email unique (sert d'identifiant de connexion)
        - username : nom d'utilisateur affiché
        - password_hash : mot de passe chiffré (jamais stocké en clair)
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String())

    def set_password(self, password):
        """
        Chiffre et stocke le mot de passe.
        generate_password_hash() utilise pbkdf2:sha256 —
        même mot de passe = hash différent à chaque fois (sel aléatoire).
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Vérifie si le mot de passe saisi correspond au hash stocké.
        Retourne True si correct, False sinon.
        """
        return check_password_hash(self.password_hash, password)


class Favori(db.Model):
    """
    Modèle ORM représentant la table 'favoris'.
    Un favori = lien entre un utilisateur et une formation.

    Colonnes :
        - id : clé primaire auto-incrémentée
        - user_id : clé étrangère vers la table users (obligatoire)
        - formation_id : identifiant de la formation mise en favori
        - date_ajout : date/heure automatique de création du favori (UTC)
    """
    __tablename__ = 'favoris'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    formation_id = db.Column(db.Integer, nullable=False)
    date_ajout = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class Commentaire(db.Model):
    """
    Modèle ORM représentant la table 'commentaires'.
    Un commentaire = texte laissé par un utilisateur sous une formation.

    Colonnes :
        - id : clé primaire auto-incrémentée
        - user_id : clé étrangère vers la table users
        - formation_id : identifiant de la formation commentée
        - contenu : texte du commentaire (obligatoire)
        - date_ajout : date/heure automatique de création (UTC)
    
    Relations :
        - user : accès direct à l'utilisateur auteur du commentaire
        - likes : liste des likes associés à ce commentaire
        - nb_likes : propriété calculée qui retourne le nombre de likes
    """
    __tablename__ = 'commentaires'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    formation_id = db.Column(db.Integer, nullable=False)
    contenu = db.Column(db.Text, nullable=False)
    date_ajout = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relations ORM — permettent d'accéder directement aux objets liés
    user = db.relationship('UserModel', backref='commentaires')
    likes = db.relationship('LikeCommentaire', backref='commentaire',
                           cascade='all, delete-orphan')  # Supprime les likes si le commentaire est supprimé

    @property
    def nb_likes(self):
        """Retourne le nombre de likes du commentaire."""
        return len(self.likes)


class LikeCommentaire(db.Model):
    """
    Modèle ORM représentant la table 'likes_commentaires'.
    Un like = lien entre un utilisateur et un commentaire.
    Un utilisateur ne peut liker qu'une seule fois le même commentaire.

    Colonnes :
        - id : clé primaire auto-incrémentée
        - user_id : clé étrangère vers la table users
        - commentaire_id : clé étrangère vers la table commentaires
    """
    __tablename__ = 'likes_commentaires'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    commentaire_id = db.Column(db.Integer, db.ForeignKey('commentaires.id'), nullable=False)


@login.user_loader
def load_user(id):
    """
    Fonction requise par Flask-Login.
    Appelée automatiquement à chaque requête pour recharger l'utilisateur
    depuis la base à partir de l'ID stocké dans la session.
    Retourne l'objet UserModel correspondant à l'ID, ou None si inexistant.
    """
    return UserModel.query.get(int(id))