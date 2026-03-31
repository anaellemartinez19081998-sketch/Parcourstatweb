from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import UserModel, db

auth = Blueprint('auth', __name__)


@auth.route('/inscription', methods=['GET', 'POST'])
def inscription():
    """
    Gère l'inscription d'un nouvel utilisateur.

    """
    if request.method == 'POST':
        # recuperation des données du formulaire
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        # verification que l'email n'est pas déjà utilisé
        user = UserModel.query.filter_by(email=email).first()
        if user:
            return render_template('inscription.html', erreur="Cet email est déjà utilisé.")

        # création du nouvel utilisateur 
        new_user = UserModel(email=email, username=username)
        new_user.set_password(password)  # Chiffre le mot de passe via werkzeug
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.connexion'))

    return render_template('inscription.html')


@auth.route('/connexion', methods=['GET', 'POST'])
def connexion():
    """
    Gère la connexion d'un utilisateur existant.

    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # recherche de l'utilisateur par email
        user = UserModel.query.filter_by(email=email).first()

        if user and user.check_password(password):
            # 'utilisateur est maintenant connecté
            login_user(user)
            return redirect(url_for('index'))

        # Affichage du message d'erreur si identifiants incorrects
        return render_template('connexion.html', erreur="Email ou mot de passe incorrect.")

    return render_template('connexion.html')


@auth.route('/deconnexion')
@login_required
def deconnexion():
    """
    Déconnecte l'utilisateur en supprimant sa session.
    logout_user() supprime les données de session Flask-Login.
    Redirige vers la page de connexion.
    """
    logout_user()
    return redirect(url_for('auth.connexion'))


@auth.route('/profil', methods=['GET', 'POST'])
@login_required
def profil():
    """
    Page de modification du profil utilisateur.
    
    """
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')

        # Vérification que l'email n'est pas déjà utilisé par un autre compte
        user_existant = UserModel.query.filter_by(email=email).first()
        if user_existant and user_existant.id != current_user.id:
            return render_template('profil.html', erreur="Cet email est déjà utilisé.")

        # Modification des données en base  UPDATE avec ORM
        current_user.username = username
        current_user.email = email
        db.session.commit()  # Sauvegarde 
        
        return render_template('profil.html', succes="Profil mis à jour !")

    return render_template('profil.html')