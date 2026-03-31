from flask import Blueprint, redirect, url_for, request, render_template
from flask_login import login_required, current_user
from app.models.user import db, Commentaire, LikeCommentaire

# Blueprint commentaires : gère les commentaires et leurs likes
# sur les pages de détail des formations
commentaires_bp = Blueprint('commentaires_bp', __name__)


@commentaires_bp.route("/formation/<int:formation_id>/commentaire/ajouter",
                       methods=['POST'])
@login_required
def ajouter_commentaire(formation_id):
    """
    Ajoute un commentaire sous une formation.
    Accessible uniquement aux utilisateurs connectés.
    Récupère le texte depuis le formulaire POST et le sauvegarde en base.
    Rollback automatique en cas d'erreur.
    """
    contenu = request.form.get('contenu')

    if contenu and contenu.strip():  # Vérifie que le commentaire n'est pas vide
        try:
            commentaire = Commentaire(
                user_id=current_user.id,
                formation_id=formation_id,
                contenu=contenu.strip()
            )
            db.session.add(commentaire)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Erreur ajout commentaire : {e}")

    return redirect(url_for("formations_bp.formation_detail", id=formation_id))


@commentaires_bp.route("/commentaire/<int:commentaire_id>/supprimer",
                       methods=['POST'])
@login_required
def supprimer_commentaire(commentaire_id):
    """
    Supprime un commentaire.
    Vérifie que l'utilisateur connecté est bien l'auteur du commentaire
    avant de le supprimer. Rollback automatique en cas d'erreur.
    """
    commentaire = Commentaire.query.get_or_404(commentaire_id)
    formation_id = commentaire.formation_id

    # Sécurité : seul l'auteur peut supprimer son commentaire
    if commentaire.user_id == current_user.id:
        try:
            db.session.delete(commentaire)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Erreur suppression commentaire : {e}")

    return redirect(url_for("formations_bp.formation_detail", id=formation_id))


@commentaires_bp.route("/commentaire/<int:commentaire_id>/like",
                       methods=['POST'])
@login_required
def liker_commentaire(commentaire_id):
    """
    Like ou unlike un commentaire (toggle).
    Si l'utilisateur a déjà liké → supprime le like.
    Si l'utilisateur n'a pas liké → ajoute le like.
    Rollback automatique en cas d'erreur.
    """
    commentaire = Commentaire.query.get_or_404(commentaire_id)
    formation_id = commentaire.formation_id

    try:
        like_existant = LikeCommentaire.query.filter_by(
            user_id=current_user.id,
            commentaire_id=commentaire_id
        ).first()

        if like_existant:
            # Unlike : supprime le like existant
            db.session.delete(like_existant)
        else:
            # Like : ajoute un nouveau like
            like = LikeCommentaire(
                user_id=current_user.id,
                commentaire_id=commentaire_id
            )
            db.session.add(like)

        db.session.commit()

    except Exception as e:
        db.session.rollback()
        print(f"Erreur like commentaire : {e}")

    return redirect(url_for("formations_bp.formation_detail", id=formation_id))