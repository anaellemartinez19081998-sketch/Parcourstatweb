from flask import Blueprint, jsonify
from app.models.parcourstat import Formation

export = Blueprint('export', __name__)

@export.route("/formation/<int:id>/export.json")
def formation_export_json(id):
    """Exporte les données d'une formation au format JSON."""
    formation = Formation.query.get_or_404(id)
    
    data = {
        "id": formation.id,
        "nom": formation.nom,
        "selectivite": formation.selectivite,
        "etablissement": {
            "nom": formation.etablissement.nom,
            "statut": formation.etablissement.statut,
            "adresse": formation.etablissement.adresse,
            "site_web": formation.etablissement.site_web,
        },
        "type_formation": formation.type_formation.nom,
        "discipline": formation.discipline.nom,
    }
    
    return jsonify(data)