from flask import Blueprint, render_template, request, jsonify
#Blueprint permet de regroupe des routes dans un fichier separe qui font parti de lapplication flask sans etre dans app.py
#render_template charge le html depuis le dossier vers le navigateur 
#request  lit le json envoye par le js et represente la requete http entrante
#jsonify convertit les dictionnaires python en json pour que le navigateur les lisent
from sqlalchemy import text
#pour ecrire du sql brut car sinon SQLAlchemy n'accepeterai pas les requetes ecrites a la main
import matplotlib
#matplotlib permet de dessiner les graphiques de la page comparaison. Le rendu aurait peut etre ete plus propre si cette fonctionnalite avait etee realisee en JS mais comme le contexte de developpement de l'application parcourstat est celui du livrable devaluation du cours de Python, j'ai trouve plus pertinent de faire usage d'une librairie Python de datavisualisation. 
matplotlib.use('Agg')
#necessaire pour matplotlib ne cherche pas un ecran pour l'affichage du graphique (sinon il plante car il ny a pas d'interface graphique)
import matplotlib.pyplot as plt
#pyplot permet de creer et dessiner des figures
import matplotlib.ticker as mticker
#ticker permet de formater les valeurs sur les axes pour afficher en pourcentages
import io, base64
#io sert a creer un fichier en memoire pour sauvegarder limage du graphique en png
import numpy as np
#sert pour creer un tableau pour positionner les barres sur laxe du graphique

main = Blueprint('main', __name__)
#creation du blueprint main : dans app.py les il y a app.register_blueprint(main) qui fait que flask enregistre les routes d ce fichier



# Dictionnaire de configuration : il permet de ne pas avoir a changer la logique si on souhaite ajouter un autre critere pour lequel generer des graphiques de comparaison.
CRITERES = {
    "boursiers": {
        "label_critere": "Boursiers",# texte du titre du graphique
        "label_pop":     "boursiers",#mot qui s'insere dans la phrase de la synthese
        # candidats boursiers dans la table candidatures
        "sql_cand":     "SUM(ca.ec_b_nb_g + ca.ec_b_nb_t + ca.ec_b_nb)",#sql_cand exprime le numerateur du pourcentage candidats : la somme des candidats boursiers de tous les bacs
        "sql_tot_cand": "SUM(ca.ec_nb_g   + ca.ec_nb_t   + ca.ec_nb_p)",#ici le denominateur : total des candidats toutes filieres confondues
        # admis boursiers dans la table admissions
        "sql_adm":      "SUM(ad.ea_bn_b)",#numerateurs des admis boursiers
        "sql_tot_adm":  "SUM(ad.ea_nb_g + ad.ea_nb_t + ad.ea_nb_p)",#denominateur : total des admis
        # effectifs bruts pour la synthèse
        "sql_nb_cand":  "SUM(ca.ec_nb_g + ca.ec_nb_t + ca.ec_nb_p)",
        "sql_nb_adm":   "SUM(ad.ea_nb)",
    },
}



# Route des regions

@main.route('/regions')
def regions():
    from app.models.parcourstat import Region
    regions = Region.query.order_by(Region.nom).all()
    return render_template('regions.html', regions=regions)



# Route des comparaisons qui prepare les donnees pour le volet de filtres : elle construit une listes de groupes pour que les formations soient regroupees par etablissement et que lon puisse les identifier.
#  cree une structure JSON que le JS recoit dans const GROUPES = {{ groupes | tojson }} et qui est utilse pour construire les groupes par etablissement dans la liste deroulante.
@main.route('/comparaison')
def comparaison():
    from app.models.parcourstat import Formation, Etablissement

    etablissements = Etablissement.query.order_by(Etablissement.nom).all()

    groupes = []
    for etab in etablissements:
        formations = Formation.query.filter_by(
            etablissement_id=etab.id
        ).order_by(Formation.nom).all()
        if formations:
            groupes.append({
                "etablissement": etab.nom,
                "formations": [{"id": f.id, "nom": f.nom} for f in formations]
            })

    return render_template("comparaison.html", groupes=groupes)



# Route qui accepte les requetes post. Elle importe la session SQLAlchemy (db) pour executer les requetes SQL brutes
@main.route('/api/chart-data', methods=['POST'])
def chart_data():
    from app.models.user import db
    from app.models.parcourstat import Formation

    payload       = request.get_json() #lit le corps de la requete envoyee par le fetch() du JS
    formation_ids = payload.get('ids', [])
    critere       = payload.get('criteria', [None])[0] #ids (les ids des formations) et criteria (en loccurence boursiers car il n'y a qu'un seul critere) sont extraits de la liste 

    if not formation_ids or not critere or critere not in CRITERES:
        return jsonify({"error": "Paramètres invalides"}), 400 #erreur 400 renvoyee au cas ou ca planterai

    cfg     = CRITERES[critere] #raccourci vers le dictionnaire du critere choisi
    donnees = []

    for formation_id in formation_ids[:5]: #boucle sur les ids des formations avec un max de 5

        formation_obj = Formation.query.get(formation_id) #on recupere les noms de formations avec l'ORM
        nom = formation_obj.nom if formation_obj else f"Formation {formation_id}" #la condition permet de s'assurer que l'id existe

        rows = db.session.execute(text(f"""
            SELECT
                ca.annee,
                {cfg['sql_cand']}     AS num_cand,
                {cfg['sql_tot_cand']} AS den_cand,
                {cfg['sql_adm']}      AS num_adm,
                {cfg['sql_tot_adm']}  AS den_adm,
                {cfg['sql_nb_cand']}  AS nb_cand,
                {cfg['sql_nb_adm']}   AS nb_adm
            FROM "ParcourStat".candidatures ca
            JOIN "ParcourStat".admissions ad
              ON ad.formation_id = ca.formation_id
             AND ad.annee = ca.annee
            WHERE ca.formation_id = :formation_id
              AND ca.annee IN (2018, 2024)
            GROUP BY ca.annee
            ORDER BY ca.annee
        """), {"formation_id": formation_id}).mappings().all()
        #les f string sont remplacees par des expression sql du dictionnaire avant de les passer a Postgre
        #:formation_id est un parametre SQL securise il est remplace par la velaeur reelle par SQLAlchemy, pour proteger contre les injections SQL

        par_annee = {int(r["annee"]): r for r in rows}
#transforme la liste des resultats en dictionnaires indexes par annee
        def pct(num, den): #calcule un pourcentage
            num, den = float(num or 0), float(den or 0) #gere les valuers null de la base 
            return round(num / den * 100, 1) if den else 0.0 #evite de diviser par 0

        def brut(r, col): #extrait une valeur brute pour une ligne de resultat
            return int(r[col] or 0) if r else 0 #gere le cas ou une une annee est manquante

        r18 = par_annee.get(2018) # si il ny a pas de donnees pour une annee pour une formation. On le garde pour pouvoir expliauer cela dans la synthese. 
        r24 = par_annee.get(2024)

        manquantes = []
        if not r18:
            manquantes.append("2018")
        if not r24:
            manquantes.append("2024")

        donnees.append({
            "nom":           nom,
            "manquantes":    manquantes,
            "pct_cand_2018": pct(r18["num_cand"], r18["den_cand"]) if r18 else None,
            "pct_adm_2018":  pct(r18["num_adm"],  r18["den_adm"])  if r18 else None,
            "pct_cand_2024": pct(r24["num_cand"], r24["den_cand"]) if r24 else None,
            "pct_adm_2024":  pct(r24["num_adm"],  r24["den_adm"])  if r24 else None,
            "nb_cand_2018":  brut(r18, "nb_cand"),
            "nb_adm_2018":   brut(r18, "nb_adm"),
            "nb_cand_2024":  brut(r24, "nb_cand"),
            "nb_adm_2024":   brut(r24, "nb_adm"),
        })

    image_b64 = generer_graphique(donnees, cfg["label_critere"])

    label_pop = cfg["label_pop"]
    synthese  = []

    for d in donnees: #synthese avec une phrase par formation et avertissement s'il manque des donnees
        if d["manquantes"]:
            annees_manquantes = " et ".join(d["manquantes"])
            texte = (
                f" La formation \"{d['nom']}\" n'a pas de données "
                f"pour l'année {annees_manquantes}."
            )
            if "2018" not in d["manquantes"] and d["pct_cand_2018"] is not None:
                texte += (
                    f" En 2018, elle comptait {d['nb_cand_2018']:,} candidats "
                    f"dont {d['pct_cand_2018']} % étaient {label_pop}, "
                    f"et {d['nb_adm_2018']:,} admis dont "
                    f"{d['pct_adm_2018']} % étaient {label_pop}."
                ).replace(",", "\u202f") #remplace la virgule presente par defaut par un espace
            if "2024" not in d["manquantes"] and d["pct_cand_2024"] is not None:
                texte += (
                    f" En 2024, elle comptait {d['nb_cand_2024']:,} candidats "
                    f"dont {d['pct_cand_2024']} % étaient {label_pop}, "
                    f"et {d['nb_adm_2024']:,} admis dont "
                    f"{d['pct_adm_2024']} % étaient {label_pop}."
                ).replace(",", "\u202f")
        else:
            texte = (
                f"En 2018, la formation \"{d['nom']}\" comptait "
                f"{d['nb_cand_2018']:,} candidats dont {d['pct_cand_2018']} % "
                f"étaient {label_pop}, et {d['nb_adm_2018']:,} admis dont "
                f"{d['pct_adm_2018']} % étaient {label_pop}. "
                f"En 2024, elle comptait {d['nb_cand_2024']:,} candidats dont "
                f"{d['pct_cand_2024']} % étaient {label_pop}, et "
                f"{d['nb_adm_2024']:,} admis dont {d['pct_adm_2024']} % "
                f"étaient {label_pop}."
            ).replace(",", "\u202f")

        synthese.append({"nom": d["nom"], "texte": texte})

    return jsonify({
        "image":    image_b64,
        "synthese": synthese,
        "critere":  cfg["label_critere"],
    })



# Generation du graphique

def generer_graphique(donnees, label_critere):

    n    = len(donnees) #nombre de formation soit nombre de groupes de barres car 4 barres par formation
    x    = np.arange(n) #position sur laxe X
    larg = 0.35 #largeur dun groupe de barres

    BLEU_CLAIR  = "#a0c4e0"
    BLEU_FONCE  = "#4e79a7"
    ROUGE_CLAIR = "#f4a09a"
    ROUGE_FONCE = "#e15759"

    pct_cand_18 = [d["pct_cand_2018"] if d["pct_cand_2018"] is not None else 0 for d in donnees]
    pct_adm_18  = [d["pct_adm_2018"]  if d["pct_adm_2018"]  is not None else 0 for d in donnees]
    pct_cand_24 = [d["pct_cand_2024"] if d["pct_cand_2024"] is not None else 0 for d in donnees]
    pct_adm_24  = [d["pct_adm_2024"]  if d["pct_adm_2024"]  is not None else 0 for d in donnees]
    noms        = [d["nom"] for d in donnees]

    fig, ax = plt.subplots(figsize=(max(8, n * 3), 6))
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#f8f9fa")

    offset_18_cand = x - larg * 0.75 #pour chaque formation on place 4 barres autour du centre x. calcul des $ barres pour la symetrie autour de la position de la formation
    offset_18_adm  = x - larg * 0.25
    offset_24_cand = x + larg * 0.25
    offset_24_adm  = x + larg * 0.75

    bars_cc18 = ax.bar(offset_18_cand, pct_cand_18, larg / 2,
                       label="% candidats boursiers 2018", color=BLEU_CLAIR,  zorder=3)
    bars_ca18 = ax.bar(offset_18_adm,  pct_adm_18,  larg / 2,
                       label="% admis boursiers 2018",     color=BLEU_FONCE,  zorder=3)
    bars_cc24 = ax.bar(offset_24_cand, pct_cand_24, larg / 2,
                       label="% candidats boursiers 2024", color=ROUGE_CLAIR, zorder=3)
    bars_ca24 = ax.bar(offset_24_adm,  pct_adm_24,  larg / 2,
                       label="% admis boursiers 2024",     color=ROUGE_FONCE, zorder=3)

    for bars, valeurs in [
        (bars_cc18, pct_cand_18),
        (bars_ca18, pct_adm_18),
        (bars_cc24, pct_cand_24),
        (bars_ca24, pct_adm_24),
    ]:
        for bar, val in zip(bars, valeurs):
            if val > 0:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 0.4,
                    f"{val} %",
                    ha="center", va="bottom", fontsize=7.5, color="#333"
                )

    for i, d in enumerate(donnees):
        if "2018" in d["manquantes"]:
            ax.text(i - larg * 0.5, 1, "n/d",
                    ha="center", fontsize=8, color="#999", style="italic")
        if "2024" in d["manquantes"]:
            ax.text(i + larg * 0.5, 1, "n/d",
                    ha="center", fontsize=8, color="#999", style="italic")

    for i in range(1, n):
        ax.axvline(i - 0.5, color="#cccccc", linewidth=0.8, linestyle="--", zorder=1)

    for i in range(n):
        ax.text(i - larg * 0.5, -3.5, "2018",
                ha="center", fontsize=8, color="#4e79a7", fontweight="bold")
        ax.text(i + larg * 0.5, -3.5, "2024",
                ha="center", fontsize=8, color="#e15759", fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels(
        [nom[:28] + "…" if len(nom) > 28 else nom for nom in noms],
        rotation=15, ha="right", fontsize=9
    )
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:.0f} %"))
    ax.set_ylim(0, max(
        max(pct_cand_18 + pct_adm_18 + pct_cand_24 + pct_adm_24, default=10) * 1.18,
        10
    ))
    ax.set_ylabel("Part (%)", fontsize=10)
    ax.set_title(
        f"Comparaison par formation — {label_critere}\n2018 vs 2024",
        fontsize=12, fontweight="bold", pad=14
    )
    ax.grid(axis="y", linestyle="--", alpha=0.45, zorder=0)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="upper right", fontsize=8.5, framealpha=0.85)

    buf = io.BytesIO() #cree le fichier en memoire
    plt.tight_layout()
    plt.savefig(buf, format="png", dpi=150, bbox_inches="tight") #ecrit le png dedan sau lieu dun vrai fichier
    plt.close(fig) #libere la memoire matplotlib
    buf.seek(0) #remet le curseur au debut du buffeur avnt de le lire
    return "data:image/png;base64," + base64.b64encode(buf.read()).decode("utf-8") #convertit les octets png en texte
#le prefixe data:image/png;base64 permet dafficher une image encodee sans URL externe
