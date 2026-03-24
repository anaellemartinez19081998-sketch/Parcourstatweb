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
    region_id = db.Column(db.Integer, db.ForeignKey('ParcourStat.region.id'))

class Departement(db.Model):
    __tablename__ = 'departement'
    __table_args__ = {"schema": "ParcourStat"}

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.Text)
    academie_id = db.Column(db.Integer, db.ForeignKey('ParcourStat.academie.id'))

class Commune(db.Model):
    __tablename__ = 'commune'
    __table_args__ = {"schema": "ParcourStat"}

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.Text)
    departement_id = db.Column(db.Integer, db.ForeignKey('ParcourStat.departement.id'))

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