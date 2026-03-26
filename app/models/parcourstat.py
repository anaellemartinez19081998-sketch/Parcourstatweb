from app.models.user import db

class Region(db.Model):
    __tablename__ = 'region'
    __table_args__ = {"schema": "ParcourStat"}

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.Text)

class Academie(db.Model):
    __tablename__ = 'academie'
    __table_args__ = {"schema": "ParcourStat"}

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.Text)

class Departement(db.Model):
    __tablename__ = 'departement'
    __table_args__ = {"schema": "ParcourStat"}

    code = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.Text)
    region_id = db.Column(db.Integer, db.ForeignKey('ParcourStat.academie.id'))

class Commune(db.Model):
    __tablename__ = 'commune'
    __table_args__ = {"schema": "ParcourStat"}

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.Text)
    departement_id = db.Column(db.Integer, db.ForeignKey('ParcourStat.departement.code'))

class TypeFormation(db.Model):
    __tablename__ = 'types_formations'
    __table_args__ = {"schema": "ParcourStat"}

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.Text)

class Discipline(db.Model):
    __tablename__ = 'discipline'
    __table_args__ = {"schema": "ParcourStat"}

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.Text)
    type = db.Column(db.Integer, db.ForeignKey('ParcourStat.types_formations.id'))

class Etablissement(db.Model):
    __tablename__ = 'etablissement'
    __table_args__ = {"schema": "ParcourStat"}

    id = db.Column(db.Text, primary_key=True)
    nom = db.Column(db.Text)
    statut = db.Column(db.Text)
    site_web = db.Column(db.Text)
    adresse = db.Column(db.Text)
    nombre_etudiants = db.Column(db.Integer)
    url_logo = db.Column(db.Text)
    url_image = db.Column(db.Text)
    commune_id = db.Column(db.Integer, db.ForeignKey('ParcourStat.commune.id'))
    academie_id = db.Column(db.Integer, db.ForeignKey('ParcourStat.academie.id'))

class Formation(db.Model):
    __tablename__ = 'formation'
    __table_args__ = {"schema": "ParcourStat"}

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.Text, nullable=False)
    etablissement_id = db.Column(db.Text, db.ForeignKey('ParcourStat.etablissement.id'), nullable=False)
    type_formation_id = db.Column(db.Integer, db.ForeignKey('ParcourStat.types_formations.id'), nullable=False)
    discipline_id = db.Column(db.Integer, db.ForeignKey('ParcourStat.discipline.id'), nullable=False)
    selectivite = db.Column(db.Boolean)
    coordonnees_gps_formation = db.Column(db.Text)
    identifiant_parcoursup = db.Column(db.Text)

    # Relations
    etablissement = db.relationship('Etablissement', backref='formations')
    type_formation = db.relationship('TypeFormation', backref='formations')
    discipline = db.relationship('Discipline', backref='formations')


class Candidature(db.Model):
    __tablename__ = 'candidatures'
    __table_args__ = (
        db.UniqueConstraint('formation_id', 'annee', name='candidatures_unique'),
        {"schema": "ParcourStat"}
    ) #On précise la contrainte afin d'éviter des bugs lors de l'ajout de donnée via l'application Flask. Mais sans fonctionnalités d'ajouts, on pourrait s'abstenir de préciser la contrainte.

    id = db.Column(db.Integer, primary_key=True)
    formation_id = db.Column(db.Integer, db.ForeignKey('ParcourStat.formation.id'), nullable=False)
    annee = db.Column(db.Integer, nullable=False)

    # On lie la variable ET_C (majuscule) à la colonne et_c (minuscule)
    ET_C = db.Column("et_c", db.Integer)
    ET_CF = db.Column("et_cf", db.Integer)
    ET_C_PP = db.Column("et_c_pp", db.Integer)
    EC_I = db.Column("ec_i", db.Integer)
    EC_NB_G = db.Column("ec_nb_g", db.Integer)
    EC_B_NB_G = db.Column("ec_b_nb_g", db.Integer)
    EC_NB_T = db.Column("ec_nb_t", db.Integer)
    EC_B_NB_T = db.Column("ec_b_nb_t", db.Integer)
    EC_NB_P = db.Column("ec_nb_p", db.Integer)
    EC_B_NB = db.Column("ec_b_nb", db.Integer)
    EC_AC = db.Column("ec_ac", db.Integer)
    ETC_PC = db.Column("etc_pc", db.Integer)
    EC_NB_G_PC = db.Column("ec_nb_g_pc", db.Integer)
    EC_NB_T_PC = db.Column("ec_nb_t_pc", db.Integer)
    EC_NB_P_PC = db.Column("ec_nb_p_pc", db.Integer)
    EAC_PC = db.Column("eac_pc", db.Integer)
    ETC_CE = db.Column("etc_ce", db.Integer)
    EC_CE_PC = db.Column("ec_ce_pc", db.Integer)
    ETC_R_PA = db.Column("etc_r_pa", db.Integer)
    ETC_A_PE = db.Column("etc_a_pe", db.Integer)
    ETC_F_A_PE = db.Column("etc_f_a_pe", db.Integer)
    EC_TG_PA_E = db.Column("ec_tg_pa_e", db.Integer)
    EC_B_TG_PA_E = db.Column("ec_b_tg_pa_e", db.Integer)
    EC_TT_PA_E = db.Column("ec_tt_pa_e", db.Integer)
    EC_B_TT_PA_E = db.Column("ec_b_tt_pa_e", db.Integer)
    EC_TP_PA_E = db.Column("ec_tp_pa_e", db.Integer)
    EC_B_TP_PA_E = db.Column("ec_b_tp_pa_e", db.Integer)
    EAC_PA_E = db.Column("eac_pa_e", db.Integer)

    # Relation
    formation = db.relationship('Formation', backref=db.backref('candidatures', lazy='dynamic'))


class Admission(db.Model):
    __tablename__ = 'admissions'
    __table_args__ = (
        db.UniqueConstraint('formation_id', 'annee', name='admissions_unique'),
        {"schema": "ParcourStat"}
    )

    id = db.Column(db.Integer, primary_key=True)
    formation_id = db.Column(db.Integer, db.ForeignKey('ParcourStat.formation.id'), nullable=False)
    annee = db.Column(db.Integer, nullable=False)

    # Effectifs (EA_...)
    EA_PC = db.Column("ea_pc", db.Integer)
    EA_I = db.Column("ea_i", db.Integer)
    EA_BN_B = db.Column("ea_bn_b", db.Integer)
    EA_NB = db.Column("ea_nb", db.Integer)
    EA_NB_G = db.Column("ea_nb_g", db.Integer)
    EA_NB_T = db.Column("ea_nb_t", db.Integer)
    EA_NB_P = db.Column("ea_nb_p", db.Integer)
    EA_AC = db.Column("ea_ac", db.Integer)
    EA_NB_SI = db.Column("ea_nb_si", db.Integer)
    EA_NB_SM = db.Column("ea_nb_sm", db.Integer)
    EA_NB_AB = db.Column("ea_nb_ab", db.Integer)
    EA_NB_B = db.Column("ea_nb_b", db.Integer)
    EA_NB_TB = db.Column("ea_nb_tb", db.Integer)
    EA_NB_TBF = db.Column("ea_nb_tbf", db.Integer)
    EA_NB_G_M = db.Column("ea_nb_g_m", db.Integer)
    EA_NB_T_M = db.Column("ea_nb_t_m", db.Integer)
    EA_NB_P_M = db.Column("ea_nb_p_m", db.Integer)
    EA_NB_IME = db.Column("ea_nb_ime", db.Integer)
    EA_F_IME = db.Column("ea_f_ime", db.Integer)
    EA_IMA = db.Column("ea_ima", db.Integer)
    EA_IMA_PCV = db.Column("ea_ima_pcv", db.Integer)

    # Pourcentages (PA_...)
    PA_AB = db.Column("pa_ab", db.Integer) # Attention: vérifier si c'est Float ou Integer en base
    PA_AF_PP = db.Column("pa_af_pp", db.Integer)
    PA_F = db.Column("pa_f", db.Integer)
    PA_NB_IMA = db.Column("pa_nb_ima", db.Integer)
    PA_NB_IMA_PCV = db.Column("pa_nb_ima_pcv", db.Integer)
    PA_NB_IME = db.Column("pa_nb_ime", db.Integer)
    PA_NB_B = db.Column("pa_nb_b", db.Integer)
    PA_NB = db.Column("pa_nb", db.Integer)
    PA_NB_SI_MB = db.Column("pa_nb_si_mb", db.Integer)
    PA_NB_SM = db.Column("pa_nb_sm", db.Integer)
    PA_NB_AB = db.Column("pa_nb_ab", db.Integer)
    PA_NB_B_MB = db.Column("pa_nb_b_mb", db.Integer)
    PA_NB_TB = db.Column("pa_nb_tb", db.Integer)
    PA_NB_TB_F = db.Column("pa_nb_tb_f", db.Integer)
    PA_NB_G = db.Column("pa_nb_g", db.Integer)
    PA_M_BG = db.Column("pa_m_bg", db.Integer)
    PA_NB_T = db.Column("pa_nb_t", db.Integer)
    PA_M_BT = db.Column("pa_m_bt", db.Integer)
    PA_NB_P = db.Column("pa_nb_p", db.Integer)
    PA_M_BP = db.Column("pa_m_bp", db.Integer)

    # Relation
    formation = db.relationship('Formation', backref=db.backref('admissions', lazy='dynamic'))