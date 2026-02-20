from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, login_required
from app.models.user import UserModel, db

auth = Blueprint('auth', __name__)

@auth.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        user = UserModel.query.filter_by(email=email).first()
        if user:
            return redirect(url_for('auth.inscription'))

        new_user = UserModel(email=email, username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.connexion'))

    return render_template('inscription.html')

@auth.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = UserModel.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))

    return render_template('connexion.html')

@auth.route('/deconnexion')
@login_required
def deconnexion():
    logout_user()
    return redirect(url_for('auth.connexion'))