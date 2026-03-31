from flask import Blueprint, redirect, url_for, render_template
from flask_login import login_required, current_user
from app.models.user import db, Favori
from app.models.parcourstat import Formation

# Blueprint favoris : regroupe toutes les routes liées au système de favoris
# @login_required protège toutes les routes — un utilisateur non connecté
# est automatiquement redirigé vers la page de connexion
favoris = Blueprint('favoris', __name__)


@favoris.route("/favori/ajouter/<int:formation_id>")
@login_required
def ajouter_favori(formation_id):
    """
    Ajoute une formation aux favoris de l'utilisateur connecté.
    
    Vérifie d'abord si le favori existe déjà pour éviter les doublons.
    En cas d'erreur base de données, le rollback annule la transaction
    pour éviter de laisser la base dans un état incohérent.
    
    Paramètres :
        - formation_id : identifiant entier de la formation à ajouter
    """
    try:
        
        favori_existant = Favori.query.filter_by(
            user_id=current_user.id,
            formation_id=formation_id
        ).first()

        if not favori_existant:
            
            favori = Favori(user_id=current_user.id, formation_id=formation_id)
            db.session.add(favori)  
            db.session.commit()      

    except Exception as e:
       
        db.session.rollback()
        print(f"Erreur ajout favori : {e}")

    # Redirection vers la page détail de la formation
    return redirect(url_for("formations_bp.formation_detail", id=formation_id))


@favoris.route("/favori/supprimer/<int:formation_id>")
@login_required
def supprimer_favori(formation_id):
    """
    Supprime une formation des favoris de l'utilisateur connecté.
    
    Vérifie que le favori appartient bien à l'utilisateur connecté
    avant de le supprimer. Rollback en cas d'erreur.
    
    Paramètres :
        - formation_id : identifiant entier de la formation à retirer
    """
    try:
        
        favori = Favori.query.filter_by(
            user_id=current_user.id,
            formation_id=formation_id
        ).first()

        if favori:
            db.session.delete(favori)  
            db.session.commit()        
    except Exception as e:
        
        db.session.rollback()
        print(f"Erreur suppression favori : {e}")

    return redirect(url_for("formations_bp.formation_detail", id=formation_id))


@favoris.route("/mes-favoris")
@login_required
def mes_favoris():
    """
    Affiche la liste des formations favorites de l'utilisateur connecté.
    
    Récupère d'abord tous les favoris de l'utilisateur via l'ORM,
     pour chaque favori récupère les détails de la formation associée.
    les formations inexistantes sont ignorées (celles supprimée de la base).
    """
   
    favoris_list = Favori.query.filter_by(user_id=current_user.id).all()

    formations = []
    for favori in favoris_list:
        formation = Formation.query.get(favori.formation_id)
        if formation:  # Ignore si la formation n'existe plus en base
            formations.append(formation)

    return render_template("mes_favoris.html", formations=formations)