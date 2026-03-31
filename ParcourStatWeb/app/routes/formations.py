from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.models.user import db, Favori, Commentaire, LikeCommentaire
from app.models.parcourstat import Formation

# Blueprint formations_bp : regroupe toutes les routes liées aux formations
formations_bp = Blueprint('formations_bp', __name__)


@formations_bp.route("/formations")
def formations():
    """
    Page liste des formations avec recherche, filtres et pagination.
    
    Paramètres URL (request.args) :
        - selectivite : 'true' ou 'false' pour filtrer les formations sélectives
        - recherche : texte libre pour filtrer par nom de formation (ILIKE)
        - page : numéro de page pour la pagination (défaut 1)
    """
    selectivite = request.args.get("selectivite")
    recherche = request.args.get("recherche")
    page = request.args.get("page", 1, type=int)
    par_page = 50

    # On part d'une requête ORM de base sur toutes les formations
    query = Formation.query

    # Application des filtres selon les paramètres reçus
    if selectivite == "true":
        query = query.filter(Formation.selectivite == True)
    elif selectivite == "false":
        query = query.filter(Formation.selectivite == False)
    if recherche:
        # ILIKE = recherche insensible à la casse
        # Les % permettent de chercher n'importe où dans le nom
        query = query.filter(Formation.nom.ilike(f'%{recherche}%'))

    # Calcul du nombre total de pages pour la pagination
    total = query.count()
    total_pages = (total // par_page) + 1

    # Récupération des formations pour la page courante
    # offset = combien de lignes sauter, limit = combien en prendre
    formations = query.offset((page - 1) * par_page).limit(par_page).all()

    return render_template("formations.html",
                           formations=formations,
                           page=page,
                           total_pages=total_pages,
                           selectivite=selectivite,
                           recherche=recherche)


@formations_bp.route("/formation/<int:id>")
def formation_detail(id):
    """
    Page détail d'une formation avec favoris et commentaires.
    
    Paramètres :
        - id : identifiant entier de la formation dans la base de données
    
    Vérifie si la formation est dans les favoris de l'utilisateur connecté.
    Récupère les commentaires et les likes de l'utilisateur connecté.
    Redirige vers la page d'erreur personnalisée si la formation n'existe pas.
    """
    # Récupération de la formation — redirige vers page erreur si inexistante
    formation = Formation.query.get(id)
    if not formation:
        return render_template("erreurs/erreur.html"), 404

    # Vérification si la formation est déjà dans les favoris
    est_favori = False
    if current_user.is_authenticated:
        est_favori = Favori.query.filter_by(
            user_id=current_user.id,
            formation_id=id
        ).first() is not None

    # Récupération des commentaires du plus récent au plus ancien
    commentaires = Commentaire.query.filter_by(
        formation_id=id
    ).order_by(Commentaire.date_ajout.desc()).all()

    # Liste des IDs des commentaires likés par l'utilisateur connecté
    # Utilisée dans le template pour afficher le bon bouton like/unlike
    likes_user = []
    if current_user.is_authenticated:
        likes_user = [l.commentaire_id for l in LikeCommentaire.query.filter_by(
            user_id=current_user.id
        ).all()]

    return render_template("formation_detail.html",
                           formation=formation,
                           est_favori=est_favori,
                           commentaires=commentaires,
                           likes_user=likes_user)