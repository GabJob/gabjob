from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
import random
import string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gabjob.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'gabjob_secret_2026'
app.config['JWT_SECRET_KEY'] = 'gabjob_jwt_2026'

db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app)

# ═══════════════════════════════════════════════════
# MODÈLES
# ═══════════════════════════════════════════════════

class Utilisateur(db.Model):
    __tablename__ = 'utilisateurs'
    id        = db.Column(db.Integer, primary_key=True)
    nom       = db.Column(db.String(100), nullable=False)
    prenom    = db.Column(db.String(100))
    telephone = db.Column(db.String(20), unique=True, nullable=False)
    email     = db.Column(db.String(150), unique=True)
    type      = db.Column(db.String(20), nullable=False)
    photo_url = db.Column(db.String(255))
    quartier  = db.Column(db.String(100))
    actif     = db.Column(db.Boolean, default=True)
    cree_le   = db.Column(db.DateTime, default=datetime.utcnow)


class Prestataire(db.Model):
    __tablename__ = 'prestataires'
    id                = db.Column(db.Integer, primary_key=True)
    user_id           = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'), nullable=False)
    categorie         = db.Column(db.String(50), nullable=False)
    description       = db.Column(db.Text)
    tarif_journalier  = db.Column(db.Integer)
    zone_intervention = db.Column(db.String(255))
    disponible        = db.Column(db.Boolean, default=True)
    verifie           = db.Column(db.Boolean, default=False)
    note_moyenne      = db.Column(db.Float, default=0.0)
    nb_avis           = db.Column(db.Integer, default=0)
    utilisateur       = db.relationship('Utilisateur', backref='prestataire')

    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.utilisateur.nom,
            'prenom': self.utilisateur.prenom,
            'categorie': self.categorie,
            'description': self.description,
            'tarif_journalier': self.tarif_journalier,
            'zone_intervention': self.zone_intervention,
            'disponible': self.disponible,
            'verifie': self.verifie,
            'note_moyenne': self.note_moyenne
        }


class Mission(db.Model):
    __tablename__ = 'missions'
    id                = db.Column(db.Integer, primary_key=True)
    employeur_id      = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'), nullable=False)
    prestataire_id    = db.Column(db.Integer, db.ForeignKey('prestataires.id'))
    titre             = db.Column(db.String(200), nullable=False)
    description       = db.Column(db.Text)
    categorie         = db.Column(db.String(50), nullable=False)
    quartier          = db.Column(db.String(100))
    montant           = db.Column(db.Integer)
    statut            = db.Column(db.String(30), default='ouverte')
    commission_gabjob = db.Column(db.Integer, default=5000)
    cree_le           = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'titre': self.titre,
            'description': self.description,
            'categorie': self.categorie,
            'quartier': self.quartier,
            'montant': self.montant,
            'statut': self.statut,
            'cree_le': self.cree_le.strftime('%Y-%m-%d %H:%M')
        }


class OTPSession(db.Model):
    __tablename__ = 'otp_sessions'
    id        = db.Column(db.Integer, primary_key=True)
    telephone = db.Column(db.String(20), nullable=False)
    code      = db.Column(db.String(6), nullable=False)
    expire_le = db.Column(db.DateTime, nullable=False)
    utilise   = db.Column(db.Boolean, default=False)
    cree_le   = db.Column(db.DateTime, default=datetime.utcnow)


class Technicien(db.Model):
    __tablename__ = 'techniciens'
    id               = db.Column(db.Integer, primary_key=True)
    nom              = db.Column(db.String(100), nullable=False)
    prenom           = db.Column(db.String(100))
    telephone        = db.Column(db.String(20), unique=True, nullable=False)
    specialite       = db.Column(db.String(50), nullable=False)
    zone             = db.Column(db.String(100))
    tarif            = db.Column(db.Integer)
    experience       = db.Column(db.String(20))
    description      = db.Column(db.Text)
    photo_url        = db.Column(db.String(255))
    note             = db.Column(db.Float, default=0.0)
    nb_avis          = db.Column(db.Integer, default=0)
    disponible       = db.Column(db.Boolean, default=True)
    verifie          = db.Column(db.Boolean, default=False)
    abonnement_actif = db.Column(db.Boolean, default=False)
    abonnement_fin   = db.Column(db.DateTime)
    cree_le          = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'prenom': self.prenom or '',
            'telephone': self.telephone,
            'specialite': self.specialite,
            'zone': self.zone or '',
            'tarif': self.tarif,
            'experience': self.experience or '',
            'description': self.description or '',
            'note': self.note,
            'nb_avis': self.nb_avis,
            'disponible': self.disponible,
            'verifie': self.verifie,
            'abonnement_actif': self.abonnement_actif,
            'cree_le': self.cree_le.strftime('%Y-%m-%dT%H:%M:%S')
        }


# ═══════════════════════════════════════════════════
# ROUTES PAGES HTML
# ═══════════════════════════════════════════════════

@app.route('/')
def accueil():
    return open('gabjob.html', encoding='utf-8').read()

@app.route('/gabjob')
def gabjob():
    return open('gabjob.html', encoding='utf-8').read()

@app.route('/dashboard')
def dashboard():
    return open('dashboard.html', encoding='utf-8').read()

@app.route('/dashboard-recruteur')
def dashboard_recruteur():
    return open('dashboard-recruteur.html', encoding='utf-8').read()

@app.route('/depannage')
def depannage():
    return open('depannage.html', encoding='utf-8').read()

@app.route('/admin')
def admin():
    return open('admin.html', encoding='utf-8').read()


# ═══════════════════════════════════════════════════
# ROUTES AUTH
# ═══════════════════════════════════════════════════


@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/api/auth/inscription', methods=['POST'])
def inscription():
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({'erreur': 'JSON invalide'}), 400
    if not data.get('telephone') or not data.get('nom') or not data.get('type'):
        return jsonify({'erreur': 'telephone, nom et type sont obligatoires'}), 400
    existant = Utilisateur.query.filter_by(telephone=data['telephone']).first()
    if existant:
        return jsonify({'erreur': 'Ce numero est deja inscrit'}), 409
    utilisateur = Utilisateur(
        nom=data['nom'],
        prenom=data.get('prenom', ''),
        telephone=data['telephone'],
        email=data.get('email'),
        type=data['type'],
        quartier=data.get('quartier')
    )
    db.session.add(utilisateur)
    db.session.commit()
    return jsonify({'message': 'Compte cree avec succes', 'id': utilisateur.id}), 201


@app.route('/api/auth/envoyer-otp', methods=['POST'])
def envoyer_otp():
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({'erreur': 'JSON invalide'}), 400
    telephone = data.get('telephone')
    if not telephone:
        return jsonify({'erreur': 'Numero requis'}), 400
    utilisateur = Utilisateur.query.filter_by(telephone=telephone).first()
    if not utilisateur:
        return jsonify({'erreur': 'Numero non trouve'}), 404
    code = ''.join(random.choices(string.digits, k=6))
    expire_le = datetime.utcnow() + timedelta(minutes=10)
    otp = OTPSession(telephone=telephone, code=code, expire_le=expire_le)
    db.session.add(otp)
    db.session.commit()
    print(f"[DEV] Code OTP : {code}")
    return jsonify({'message': 'Code OTP envoye', 'code_dev': code}), 200


@app.route('/api/auth/verifier-otp', methods=['POST'])
def verifier_otp():
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({'erreur': 'JSON invalide'}), 400
    telephone = data.get('telephone')
    code = data.get('code')
    otp = OTPSession.query.filter_by(
        telephone=telephone, code=code, utilise=False
    ).filter(OTPSession.expire_le > datetime.utcnow()).first()
    if not otp:
        return jsonify({'erreur': 'Code incorrect ou expire'}), 401
    otp.utilise = True
    db.session.commit()
    utilisateur = Utilisateur.query.filter_by(telephone=telephone).first()
    if not utilisateur:
        return jsonify({'erreur': 'Utilisateur non trouve'}), 404
    token = create_access_token(
        identity=str(utilisateur.id),
        additional_claims={'type': utilisateur.type}
    )
    return jsonify({
        'token': token,
        'utilisateur': {
            'id': utilisateur.id,
            'nom': utilisateur.nom,
            'prenom': utilisateur.prenom,
            'type': utilisateur.type
        }
    }), 200


# ═══════════════════════════════════════════════════
# ROUTES PRESTATAIRES
# ═══════════════════════════════════════════════════

@app.route('/api/prestataires/', methods=['GET'])
def liste_prestataires():
    categorie = request.args.get('categorie')
    quartier = request.args.get('quartier')
    query = Prestataire.query.filter_by(disponible=True)
    if categorie:
        query = query.filter_by(categorie=categorie)
    if quartier:
        query = query.filter(Prestataire.zone_intervention.ilike(f'%{quartier}%'))
    prestataires = query.order_by(Prestataire.note_moyenne.desc()).all()
    return jsonify([p.to_dict() for p in prestataires]), 200


@app.route('/api/prestataires/<int:id>', methods=['GET'])
def profil_prestataire(id):
    prestataire = Prestataire.query.get_or_404(id)
    return jsonify(prestataire.to_dict()), 200


@app.route('/api/prestataires/mon-profil', methods=['POST'])
@jwt_required()
def creer_profil():
    user_id = get_jwt_identity()
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({'erreur': 'JSON invalide'}), 400
    existant = Prestataire.query.filter_by(user_id=user_id).first()
    if existant:
        return jsonify({'erreur': 'Profil deja existant'}), 409
    prestataire = Prestataire(
        user_id=user_id,
        categorie=data.get('categorie'),
        description=data.get('description'),
        tarif_journalier=data.get('tarif_journalier'),
        zone_intervention=data.get('zone_intervention')
    )
    db.session.add(prestataire)
    db.session.commit()
    return jsonify({'message': 'Profil cree', 'id': prestataire.id}), 201


# ═══════════════════════════════════════════════════
# ROUTES MISSIONS
# ═══════════════════════════════════════════════════

@app.route('/api/missions/', methods=['POST'])
@jwt_required()
def creer_mission():
    employeur_id = get_jwt_identity()
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({'erreur': 'JSON invalide'}), 400
    if not data.get('titre') or not data.get('categorie'):
        return jsonify({'erreur': 'titre et categorie obligatoires'}), 400
    mission = Mission(
        employeur_id=employeur_id,
        titre=data['titre'],
        description=data.get('description'),
        categorie=data['categorie'],
        quartier=data.get('quartier'),
        montant=data.get('montant'),
        commission_gabjob=5000
    )
    db.session.add(mission)
    db.session.commit()
    return jsonify({'message': 'Mission creee', 'id': mission.id}), 201


@app.route('/api/missions/', methods=['GET'])
@jwt_required()
def mes_missions():
    user_id = get_jwt_identity()
    missions = Mission.query.filter_by(employeur_id=user_id).all()
    return jsonify([m.to_dict() for m in missions]), 200


@app.route('/api/missions/<int:id>/accepter', methods=['PUT'])
@jwt_required()
def accepter_mission(id):
    user_id = get_jwt_identity()
    prestataire = Prestataire.query.filter_by(user_id=user_id).first_or_404()
    mission = Mission.query.get_or_404(id)
    if mission.statut != 'ouverte':
        return jsonify({'erreur': 'Mission non disponible'}), 400
    mission.prestataire_id = prestataire.id
    mission.statut = 'en_cours'
    db.session.commit()
    return jsonify({'message': 'Mission acceptee'}), 200


# ═══════════════════════════════════════════════════
# ROUTES TECHNICIENS (DÉPANNAGE)
# ═══════════════════════════════════════════════════

@app.route('/api/techniciens/inscription', methods=['POST'])
def inscription_technicien():
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({'erreur': 'JSON invalide'}), 400
    if not data.get('nom') or not data.get('telephone') or not data.get('specialite'):
        return jsonify({'erreur': 'nom, telephone et specialite obligatoires'}), 400
    existant = Technicien.query.filter_by(telephone=data['telephone']).first()
    if existant:
        return jsonify({'erreur': 'Numero deja inscrit', 'id': existant.id}), 409
    tech = Technicien(
        nom=data['nom'],
        prenom=data.get('prenom', ''),
        telephone=data['telephone'],
        specialite=data['specialite'],
        zone=data.get('zone', ''),
        tarif=data.get('tarif'),
        experience=data.get('experience', ''),
        description=data.get('description', ''),
        abonnement_actif=False
    )
    db.session.add(tech)
    db.session.commit()
    return jsonify({'message': 'Inscription reussie', 'id': tech.id}), 201


@app.route('/api/techniciens/', methods=['GET'])
def liste_techniciens():
    specialite = request.args.get('specialite')
    zone = request.args.get('zone')
    query = Technicien.query.filter_by(abonnement_actif=True, disponible=True)
    if specialite:
        query = query.filter_by(specialite=specialite)
    if zone:
        query = query.filter(Technicien.zone.ilike(f'%{zone}%'))
    techs = query.order_by(Technicien.note.desc()).all()
    return jsonify([t.to_dict() for t in techs]), 200


@app.route('/api/techniciens/<int:id>', methods=['GET'])
def profil_technicien(id):
    tech = Technicien.query.get_or_404(id)
    return jsonify(tech.to_dict()), 200


@app.route('/api/techniciens/<int:id>/activer', methods=['POST'])
def activer_technicien(id):
    tech = Technicien.query.get_or_404(id)
    tech.abonnement_actif = True
    tech.abonnement_fin = datetime.utcnow() + timedelta(days=30)
    db.session.commit()
    return jsonify({'message': 'Abonnement active', 'fin': tech.abonnement_fin.strftime('%Y-%m-%d')}), 200


@app.route('/api/techniciens/<int:id>/desactiver', methods=['POST'])
def desactiver_technicien(id):
    tech = Technicien.query.get_or_404(id)
    tech.abonnement_actif = False
    db.session.commit()
    return jsonify({'message': 'Abonnement desactive'}), 200


# ═══════════════════════════════════════════════════
# ROUTES ADMIN
# ═══════════════════════════════════════════════════

@app.route('/api/admin/stats', methods=['GET'])
def admin_stats():
    candidats = Utilisateur.query.filter_by(type='candidat').count()
    recruteurs = Utilisateur.query.filter_by(type='recruteur').count()
    offres = Mission.query.count()
    techniciens = Technicien.query.count()
    return jsonify({
        'candidats': candidats,
        'recruteurs': recruteurs,
        'offres': offres,
        'techniciens': techniciens
    }), 200


@app.route('/api/admin/utilisateurs', methods=['GET'])
def admin_utilisateurs():
    type_filtre = request.args.get('type')
    if type_filtre:
        users = Utilisateur.query.filter_by(type=type_filtre).order_by(Utilisateur.cree_le.desc()).all()
    else:
        users = Utilisateur.query.order_by(Utilisateur.cree_le.desc()).all()
    return jsonify([{
        'id': u.id,
        'nom': u.nom,
        'prenom': u.prenom or '',
        'telephone': u.telephone,
        'email': u.email or '',
        'type': u.type,
        'quartier': u.quartier or '',
        'actif': u.actif,
        'cree_le': u.cree_le.strftime('%Y-%m-%dT%H:%M:%S')
    } for u in users]), 200


@app.route('/api/admin/utilisateurs/<int:id>', methods=['DELETE'])
def admin_supprimer_utilisateur(id):
    user = Utilisateur.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'Utilisateur supprime'}), 200


@app.route('/api/admin/techniciens', methods=['GET'])
def admin_techniciens():
    techs = Technicien.query.order_by(Technicien.cree_le.desc()).all()
    return jsonify([t.to_dict() for t in techs]), 200


@app.route('/api/admin/techniciens/<int:id>', methods=['DELETE'])
def admin_supprimer_technicien(id):
    tech = Technicien.query.get_or_404(id)
    db.session.delete(tech)
    db.session.commit()
    return jsonify({'message': 'Technicien supprime'}), 200


# ═══════════════════════════════════════════════════
# DÉMARRAGE
# ═══════════════════════════════════════════════════

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)