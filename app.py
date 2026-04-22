# ============================================================
# APP.PY — SERVEUR FLASK PRINCIPAL
# ============================================================

from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for
from flask_bcrypt import Bcrypt
import requests
import importlib.util
import os
import json
from functools import wraps

# ============================================================
# CHARGEMENT MODULES
# ============================================================

def charger_module(nom, chemin):
    spec   = importlib.util.spec_from_file_location(nom, chemin)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

dossier         = os.path.dirname(os.path.abspath(__file__))
besoin_eau_mod  = charger_module("besoin_eau",  os.path.join(dossier, "besoin_eau.py"))
hydraulique_mod = charger_module("hydraulique", os.path.join(dossier, "hydraulique.py"))
pompe_mod       = charger_module("pompe",       os.path.join(dossier, "pompe.py"))
energie_mod     = charger_module("energie",     os.path.join(dossier, "energie.py"))
pompes_bd_mod   = charger_module("pompes",      os.path.join(dossier, "pompes.py"))
equipements_mod = charger_module("equipements", os.path.join(dossier, "equipements.py"))

from database import (
    init_db, get_projets_utilisateur, sauvegarder_projet,
    get_projet_par_id, supprimer_projet, mettre_a_jour_projet
)

# ============================================================
# FONCTIONS IMPORTÉES
# ============================================================

calculer_ET0               = besoin_eau_mod.calculer_ET0
calculer_besoins_eau       = besoin_eau_mod.calculer_besoins_eau
calculer_hydraulique       = hydraulique_mod.calculer_hydraulique
calculer_pompe             = pompe_mod.calculer_pompe
calculer_solaire           = energie_mod.calculer_solaire
calculer_groupe            = energie_mod.calculer_groupe
calculer_hybride_groupe    = energie_mod.calculer_hybride_groupe
calculer_hybride_batteries = energie_mod.calculer_hybride_batteries
selectionner_pompes        = pompes_bd_mod.selectionner_pompes

# ============================================================
# INITIALISATION FLASK
# ============================================================

app = Flask(__name__)
app.secret_key = 'solarpump_secret_key_2026_esmer'
from datetime import timedelta
app.config['SESSION_PERMANENT'] = False
bcrypt = Bcrypt(app)

from auth import auth as auth_blueprint
auth_blueprint.bcrypt = bcrypt
app.register_blueprint(auth_blueprint)

init_db()

# ============================================================
# DÉCORATEUR LOGIN
# ============================================================

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            if request.is_json or request.headers.get('Content-Type') == 'application/json':
                return jsonify({"succes": False, "erreur": "Non connecté"}), 401
            return redirect(url_for('auth.connexion'))
        return f(*args, **kwargs)
    return decorated

# ============================================================
# ROUTES PRINCIPALES
# ============================================================

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html',
                           user_nom=session['user_nom'],
                           user_email=session.get('user_email', ''))
# ============================================================
# DONNÉES CLIMATIQUES NASA POWER
# ============================================================

@app.route('/get_climate', methods=['POST'])
@login_required
def get_climate():
    data = request.get_json()
    lat  = data['lat']
    lon  = data['lon']
    try:
        url    = "https://power.larc.nasa.gov/api/temporal/monthly/point"
        params = {
            "latitude": lat, "longitude": lon,
            "parameters": "T2M_MAX,T2M_MIN,WS2M,RH2M,ALLSKY_SFC_SW_DWN",
            "community": "AG", "format": "JSON",
            "start": "2020", "end": "2023"
        }
        response = requests.get(url, params=params, timeout=60)
        donnees     = response.json()
        T_max       = list(donnees['properties']['parameter']['T2M_MAX'].values())
        T_min       = list(donnees['properties']['parameter']['T2M_MIN'].values())
        vent        = list(donnees['properties']['parameter']['WS2M'].values())
        humidite    = list(donnees['properties']['parameter']['RH2M'].values())
        rayonnement = list(donnees['properties']['parameter']['ALLSKY_SFC_SW_DWN'].values())

        mois = ['Jan','Fév','Mar','Avr','Mai','Jun','Jul','Aoû','Sep','Oct','Nov','Déc']
        ET0_par_mois = {}
        for i in range(12):
            ET0_par_mois[mois[i]] = calculer_ET0(T_max[i], T_min[i], humidite[i], vent[i], rayonnement[i])

        mois_critique = max(ET0_par_mois, key=ET0_par_mois.get)
        return jsonify({
            "succes": True,
            "ET0_par_mois": ET0_par_mois,
            "mois_critique": mois_critique,
            "ET0_max": ET0_par_mois[mois_critique],
            "irradiation": max(rayonnement[:12]),
            "temperature_max": max(T_max[:12]),
            "temperature_min": min(T_min[:12]),
        })
    except Exception as e:
        return jsonify({"succes": False, "erreur": str(e)})

# ============================================================
# CALCUL PRINCIPAL
# ============================================================

@app.route('/calculer', methods=['POST'])
@login_required
def calculer():
    try:
        data                     = request.get_json()
        mode                     = data.get('mode', 'irrigation')
        source_energie           = data['source_energie']
        heures_pompage           = float(data['heures_pompage'])
        irradiation              = float(data['irradiation'])
        tension_pv               = data.get('tension_pv', '48V')
        longueur_canalisation    = float(data.get('longueur_canalisation', 0))
        diametre_tuyau           = float(data.get('diametre_tuyau', 63))
        profondeur_aspiration    = float(data.get('profondeur_aspiration', 0))
        hauteur_refoulement      = float(data.get('hauteur_refoulement', 0))
        type_systeme_hydraulique = data.get('type_systeme_hydraulique', 'irrigation')
        type_alimentation        = data.get('type_alimentation', 'bas')
        hauteur_reservoir        = float(data.get('hauteur_reservoir', 0))
        niveau_dynamique         = float(data.get('niveau_dynamique', 0))
        niveau_eau_lac           = float(data.get('niveau_eau_lac', 0))
        hauteur_aspiration       = float(data.get('hauteur_aspiration', 0))

        if mode == 'irrigation':
            culture           = data['culture']
            besoins           = calculer_besoins_eau(
                culture, float(data['superficie']), data['systeme_irrigation'],
                data['type_sol'], float(data['ET0']), data.get('kc_manuel')
            )
            besoin_brut       = besoins['besoin_brut_m3_jour']
            systeme_irrigation = data['systeme_irrigation']
        else:
            besoin_journalier  = float(data['besoin_journalier'])
            coeff_fuite        = float(data.get('coeff_fuite', 1.10))
            besoin_brut        = besoin_journalier * coeff_fuite
            systeme_irrigation = 'gravitaire'
            besoins = {
                "ETc": round(besoin_journalier, 2),
                "besoin_net_m3_jour": round(besoin_journalier, 2),
                "besoin_brut_m3_jour": round(besoin_brut, 2),
                "besoin_session_m3": round(besoin_brut, 2),
                "frequence_arrosage_jours": 1,
                "kc_utilise": None,
            }

        if mode == 'classique':
            hydraulique = calculer_hydraulique(
                besoin_brut_m3_jour=besoin_brut, heures_pompage=heures_pompage,
                systeme_irrigation=systeme_irrigation, source_energie=source_energie,
                longueur_canalisation=longueur_canalisation, diametre_tuyau_mm=diametre_tuyau,
                type_systeme_hydraulique=type_systeme_hydraulique, type_alimentation=type_alimentation,
                hauteur_reservoir=hauteur_reservoir, niveau_dynamique=niveau_dynamique,
                niveau_eau_lac=niveau_eau_lac, hauteur_aspiration=hauteur_aspiration,
            )
        else:
            hydraulique = calculer_hydraulique(
                besoin_brut_m3_jour=besoin_brut, heures_pompage=heures_pompage,
                profondeur_aspiration=profondeur_aspiration, hauteur_refoulement=hauteur_refoulement,
                systeme_irrigation=systeme_irrigation, source_energie=source_energie,
                longueur_canalisation=longueur_canalisation, diametre_tuyau_mm=diametre_tuyau,
                type_systeme_hydraulique='irrigation', type_alimentation='bas',
                hauteur_reservoir=0, niveau_dynamique=0, niveau_eau_lac=0, hauteur_aspiration=0,
            )

        pompe = calculer_pompe(hydraulique['debit_m3_h'], hydraulique['HMT_m'])

        if source_energie == "solaire":
            energie = calculer_solaire(pompe['Pm_kW'], heures_pompage, irradiation, tension_pv)
        elif source_energie == "groupe":
            energie = calculer_groupe(pompe['Pm_kW'], heures_pompage)
        elif source_energie == "hybride_groupe":
            energie = calculer_hybride_groupe(pompe['Pm_kW'], heures_pompage, irradiation, tension_pv)
        elif source_energie == "hybride_batteries":
            energie = calculer_hybride_batteries(
                pompe['Pm_kW'], heures_pompage, irradiation, tension_pv,
                data['tension_batterie'], data['capacite_batterie'], int(data['jours_autonomie'])
            )
        else:
            energie = {}

        pompes_recommandees = selectionner_pompes(
            hydraulique['debit_m3_h'], hydraulique['HMT_m'],
            source_energie, data.get('marque_pompe', 'toutes')
        )

        resultats = {
            "succes": True,
            "besoins": besoins,
            "hydraulique": hydraulique,
            "pompe": pompe,
            "energie": energie,
            "source_energie": source_energie,
            "pompes_recommandees": pompes_recommandees,
            "marque_pompe": data.get('marque_pompe', ''),
            "modele_pompe": data.get('modele_pompe', ''),
        }

        # SAUVEGARDE AUTOMATIQUE
        payload_json = json.dumps({**data, **resultats})
        projet_id    = data.get('projet_id')
        if projet_id:
            mettre_a_jour_projet(projet_id, session['user_id'], payload_json)
        else:
            projet_id = sauvegarder_projet(
                session['user_id'],
                data.get('nom_projet', 'Projet sans nom'),
                data.get('realise_par', ''),
                data.get('date_projet', ''),
                mode, source_energie,
                data.get('lat', ''), data.get('lon', ''),
                payload_json
            )

        resultats['projet_id'] = projet_id
        return jsonify(resultats)

    except Exception as e:
        import traceback
        print("ERREUR CALCUL :", traceback.format_exc())
        return jsonify({"succes": False, "erreur": str(e)})

# ============================================================
# SUPPRESSION PROJET
# ============================================================

@app.route('/supprimer_projet/<int:projet_id>', methods=['POST'])
@login_required
def supprimer_projet_route(projet_id):
    supprimer_projet(projet_id, session['user_id'])
    return jsonify({"succes": True})

# ============================================================
# PDF
# ============================================================

@app.route('/generer_pdf', methods=['POST'])
@login_required
def generer_pdf():
    try:
        data = request.get_json()
        generateur_pdf = charger_module('generateur_pdf', os.path.join(dossier, 'generateur_pdf.py'))
        data['equipements'] = {
            'marque_panneau':    data.get('marque_panneau', ''),
            'modele_panneau':    data.get('modele_panneau', ''),
            'marque_regulateur': data.get('marque_regulateur', ''),
            'modele_regulateur': data.get('modele_regulateur', ''),
            'marque_batterie':   data.get('marque_batterie', ''),
            'modele_batterie':   data.get('modele_batterie', ''),
        }
        buffer = generateur_pdf.generer_rapport(data)
        buffer.seek(0)
        return send_file(buffer, as_attachment=True,
                         download_name='rapport_hydro.pdf',
                         mimetype='application/pdf')
    except Exception as e:
        return jsonify({'succes': False, 'erreur': str(e)}), 500

# ============================================================
# POMPES & ÉQUIPEMENTS
# ============================================================

@app.route('/get_marques', methods=['GET'])
@login_required
def get_marques():
    return jsonify({"succes": True, "marques": pompes_bd_mod.get_marques()})

@app.route('/get_modeles', methods=['POST'])
@login_required
def get_modeles():
    data = request.get_json()
    return jsonify({"succes": True, "modeles": pompes_bd_mod.get_modeles_par_marque(data.get('marque', ''))})

@app.route('/get_pompe', methods=['POST'])
@login_required
def get_pompe():
    data  = request.get_json()
    pompe = pompes_bd_mod.get_caracteristiques_pompe(data.get('marque', ''), data.get('modele', ''))
    if pompe:
        return jsonify({"succes": True, "pompe": pompe})
    return jsonify({"succes": False, "erreur": "Pompe non trouvée"})

@app.route('/get_marques_panneaux', methods=['GET'])
@login_required
def get_marques_panneaux():
    return jsonify({"succes": True, "marques": equipements_mod.get_marques_panneaux()})

@app.route('/get_modeles_panneaux', methods=['POST'])
@login_required
def get_modeles_panneaux():
    data = request.get_json()
    return jsonify({"succes": True, "modeles": equipements_mod.get_modeles_panneaux(data.get('marque', ''))})

@app.route('/get_marques_batteries', methods=['GET'])
@login_required
def get_marques_batteries():
    return jsonify({"succes": True, "marques": equipements_mod.get_marques_batteries()})

@app.route('/get_modeles_batteries', methods=['POST'])
@login_required
def get_modeles_batteries():
    data = request.get_json()
    return jsonify({"succes": True, "modeles": equipements_mod.get_modeles_batteries(data.get('marque', ''))})

@app.route('/get_regulateurs', methods=['POST'])
@login_required
def get_regulateurs():
    data = request.get_json()
    return jsonify({"succes": True, "regulateurs": equipements_mod.get_regulateurs(
        data.get('marque', ''), data.get('type_reg', None)
    )})

@app.route('/get_marques_regulateurs', methods=['GET'])
@login_required
def get_marques_regulateurs():
    return jsonify({"succes": True, "marques": equipements_mod.get_marques_regulateurs()})

# ============================================================
# LANCEMENT
# ============================================================

if __name__ == '__main__':
    app.run(debug=True)