# ============================================================
# APP.PY — SERVEUR FLASK PRINCIPAL
# ============================================================

from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for
from flask_bcrypt import Bcrypt
import requests
import importlib.util
import os
import json
import math
from functools import wraps
import time
from cout import calculer_cout

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
    init_db, get_db, get_projets_utilisateur, sauvegarder_projet,
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
app.secret_key = os.environ.get('SECRET_KEY', 'hydropump_2026_secret_key_fixe')
from datetime import timedelta
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_NAME'] = 'hydropump_session'
bcrypt = Bcrypt(app)

@app.template_filter('fcfa')
def fcfa_filter(n):
    try:
        return '{:,.0f}'.format(float(n or 0)).replace(',', ' ')
    except Exception:
        return str(n)

from auth import auth as auth_blueprint
auth_blueprint.bcrypt = bcrypt
app.register_blueprint(auth_blueprint)

init_db()

@app.before_request
def verifier_session():
    if request.endpoint and request.endpoint != 'static':
        print(f"[ROUTE] {request.endpoint} — user={session.get('user_id')}")
    routes_publiques = ['auth.connexion', 'auth.inscription',
                        'auth.deconnexion', 'index', 'static',
                        'verifier_session_active', 'dimensionnement']
    if request.endpoint in routes_publiques:
        return
    if 'user_id' not in session:
        session.clear()
        return redirect(url_for('auth.connexion'))
    if not session.get('actif'):
        session.clear()
        return redirect(url_for('auth.connexion'))


@app.route('/favicon.ico')
def favicon():
    return send_file(
        os.path.join(app.root_path, 'static', 'favicon.ico'),
        mimetype='image/x-icon'
    )


@app.route('/verifier_session_active', methods=['POST'])
def verifier_session_active():
    if 'user_id' in session and session.get('actif'):
        return jsonify({'actif': True})
    return jsonify({'actif': False})

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
@app.route('/usage', methods=['GET', 'POST'])
@login_required
def usage():
    if request.method == 'POST':
        print("DEBUG /usage POST reçu :", dict(request.form))
        type_usage = request.form.get('type_usage', '')
        if type_usage == 'autre':
            type_usage = request.form.get('autre_usage', 'Autre')
        if not type_usage:
            return render_template('usage.html', user_nom=session.get('user_nom', ''), erreur="Veuillez choisir un type d'usage")
        session['usage_type'] = type_usage
        session.modified = True
        print("Session avant redirect:", dict(session))
        return redirect(url_for('choix_systeme'))
    nom_projet = request.args.get('nom_projet', '')
    session['nom_projet'] = nom_projet
    return render_template('usage.html', user_nom=session.get('user_nom', ''), nom_projet=nom_projet)

@app.route('/choix_systeme', methods=['GET', 'POST'])
@login_required
def choix_systeme():
    print(f"[ROUTE] choix_systeme {request.method} — user={session.get('user_id')}")
    if request.method == 'POST':
        session['source_energie'] = request.form.get('source_energie', 'solaire')
        session.modified = True
        print(f"[ROUTE] choix_systeme → source={session['source_energie']} → redirect dimensionnement2")
        return redirect(url_for('dimensionnement2'))
    projets = get_projets_utilisateur(session['user_id'])
    return render_template('choix_systeme.html',
                           user_nom=session.get('user_nom', ''),
                           projets=projets,
                           from_page=request.args.get('from', ''))

@app.route('/dashboard')
@login_required
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.connexion'))
    projets = get_projets_utilisateur(session['user_id'])
    return render_template(
        'dashboard.html',
        user_nom=session.get('user_nom', ''),
        user_email=session.get('user_email', ''),
        projets=projets
    )

@app.route('/dimensionnement2')
@login_required
def dimensionnement2():
    print(f"[ROUTE] dimensionnement2 — user={session.get('user_id')} "
          f"usage={session.get('usage_type')} source={session.get('source_energie')}")
    if 'usage_type' not in session:
        return redirect(url_for('usage'))
    if 'source_energie' not in session:
        return redirect(url_for('choix_systeme'))
    projets = get_projets_utilisateur(session['user_id'])
    return render_template(
        'dimensionnement2.html',
        user_nom=session.get('user_nom', ''),
        projets=projets
    )


@app.route('/lancer_calcul', methods=['POST'])
@login_required
def lancer_calcul():
    try:
        data            = request.get_json()
        print("nom_lieu reçu:", data.get('nom_lieu', 'ABSENT'))
        usage           = data.get('usage_type', session.get('usage_type', ''))
        source          = data.get('source_energie', session.get('source_energie', 'solaire'))
        heures_pompage  = float(data.get('heures_pompage') or 0)
        irradiation     = float(data.get('irradiation')    or 0)
        pr_ratio        = float(data.get('pr_ratio',  0.75))
        eta_p           = float(data.get('eta_p',     0.65))
        eta_m           = float(data.get('eta_m',     0.90))
        Rmp             = eta_p * eta_m

        if heures_pompage <= 0:
            return jsonify({'succes': False, 'erreur': 'Heures de pompage invalides.'})

        # ── 1. Besoins en eau ────────────────────────────────
        if usage == 'irrigation_agricole':
            culture    = data.get('culture', 'tomate')
            superficie = float(data.get('superficie') or 0)
            unite_sup  = data.get('unite_sup', 'ha')
            sup_ha     = superficie if unite_sup != 'm2' else superficie / 10000
            systeme    = data.get('systeme_irrigation', 'goutte_a_goutte')
            kc_manuel  = data.get('kc_manuel')
            ET0        = float(data.get('ET0') or irradiation * 0.8)
            type_sol   = data.get('type_sol', 'limoneux')
            besoins    = calculer_besoins_eau(culture, sup_ha, systeme, type_sol, ET0, kc_manuel)
            besoin_brut = besoins['besoin_brut_m3_jour']
        else:
            besoin_brut = float(data.get('besoin_journalier') or 0)
            besoins = {
                'ETc':                 round(besoin_brut, 3),
                'besoin_net_m3_jour':  round(besoin_brut, 3),
                'besoin_brut_m3_jour': round(besoin_brut, 3),
                'besoin_session_m3':   round(besoin_brut, 3),
                'kc_utilise':          None,
                'frequence_arrosage_jours': 1,
            }

        # ── 2. Hydraulique ───────────────────────────────────
        if usage == 'irrigation_agricole':
            Ha   = float(data.get('profondeur_aspiration') or 0)
            Hr   = float(data.get('hauteur_refoulement')   or 0)
            Hgeo = Ha + Hr
        else:
            Ns   = float(data.get('niveau_statique')    or 0)
            rab  = float(data.get('rabattement')        or 0)
            Nd   = Ns + rab
            Hr   = float(data.get('hauteur_refoulement') or 0)
            Hres = float(data.get('hauteur_reservoir',   0))
            Hgeo = Nd + Hr + Hres

        Pc_pertes = 0.10 * Hgeo
        HMT       = Hgeo + Pc_pertes
        Q         = besoin_brut / heures_pompage if heures_pompage > 0 else 0

        # ── 3. Puissances ────────────────────────────────────
        Ph             = 2.725 * Q * HMT / 1000
        Pp             = Ph / eta_p if eta_p > 0 else 0
        Pm             = Pp / eta_m if eta_m > 0 else 0
        Pm_commercial  = round(Pm * 1.25, 3)

        print("=== LANCER CALCUL ===")
        print("Q:", round(Q,3), "HMT:", round(HMT,2), "Pm:", round(Pm,4))
        print("Source:", source)

        # ── 4. Énergie selon source ──────────────────────────
        Eelec = Pgroupe = conso_jour = conso_mois = 0.0
        Pc_kWc = Usyst = Ps = Ia = 0
        type_reseau = ''

        if source in ('solaire', 'hybride_batteries'):
            Eelec  = 2.725 * Q * HMT * heures_pompage / (Rmp * 1000)
            Pc_kWc = Eelec / (irradiation * pr_ratio) if (irradiation > 0 and pr_ratio > 0) else 0
            Pc_W   = Pc_kWc * 1000
            if   Pc_W <= 1500: Usyst = 24
            elif Pc_W <= 5000: Usyst = 48
            else:              Usyst = 96
            print("Eelec:", round(Eelec,4), "Pc:", round(Pc_kWc,4), "kWc", "Usyst:", Usyst, "V")

        elif source in ('groupe', 'groupe_electrogene'):
            Pgroupe    = Pm * 3
            conso_jour = Pgroupe * heures_pompage * 0.3
            conso_mois = conso_jour * 30
            print("Eelec: N/A (groupe)")
            print("Pgroupe:", round(Pgroupe,3), "kW | Conso/j:", round(conso_jour,1), "L")

        elif source in ('sbee', 'reseau'):
            Ps      = Pm * 1.2
            cos_phi = 0.8
            if Pm <= 3:
                Ia          = Pm / (0.220 * cos_phi * eta_m) if eta_m > 0 else 0
                type_reseau = 'Monophase - 220V'
            else:
                Ia          = Pm / (1.732 * 0.380 * cos_phi * eta_m) if eta_m > 0 else 0
                type_reseau = 'Triphase - 380V'
            print("Eelec: N/A (reseau)")
            print("Ps:", round(Ps,3), "kW | Ia:", round(Ia,2), "A |", type_reseau)

        # ── 5. Stocker en session ────────────────────────────
        res = {
            'besoins':        besoins,
            'Q':              round(Q,    3),
            'HMT':            round(HMT,  2),
            'Hgeo':           round(Hgeo, 2),
            'Pc_pertes':      round(Pc_pertes, 2),
            'Ph':             round(Ph,   4),
            'Pp':             round(Pp,   4),
            'Pm':             round(Pm,   4),
            'Pm_commercial':  Pm_commercial,
            'eta_p':          eta_p,
            'eta_m':          eta_m,
            'Rmp':            round(Rmp,  4),
            'heures_pompage': heures_pompage,
            'source_energie': source,
            'irradiation':    irradiation,
            'pr_ratio':       pr_ratio,
            'lat':            data.get('lat'),
            'lon':            data.get('lon'),
            'usage_type':     usage,
            # solaire
            'Eelec':          round(Eelec,  4),
            'Pc_kWc':         round(Pc_kWc, 4),
            'Usyst':          Usyst,
            # groupe
            'Pgroupe':        round(Pgroupe,    3),
            'conso_jour':     round(conso_jour, 1),
            'conso_mois':     round(conso_mois, 0),
            # sbee
            'Ps':             round(Ps, 3),
            'Ia':             round(Ia, 3),
            'type_reseau':    type_reseau,
            # données brutes pour la page équipements
            'data_brut':      {k: data.get(k) for k in [
                'culture','superficie','systeme_irrigation','kc_manuel',
                'niveau_statique','rabattement','hauteur_refoulement',
                'hauteur_reservoir','profondeur_aspiration','nom_projet',
                'nom_lieu',
            ]},
        }
        session['calcul_resultats'] = res
        session['usage_type']       = usage
        session['source_energie']   = source
        session.modified = True

        return jsonify({'succes': True, 'redirect': '/equipements'})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'succes': False, 'erreur': str(e)})

@app.route('/dimensionnement')
def dimensionnement():
    nouveau = request.args.get('nouveau', '0')
    projets = get_projets_utilisateur(session.get('user_id', 0))
    return render_template(
        'dimensionnement.html',
        nouveau_projet=nouveau,
        user_nom=session.get('user_nom', ''),
        user_email=session.get('user_email', ''),
        projets=projets
    )


@app.route('/equipements')
@login_required
def equipements():
    print(f"[ROUTE] equipements — user={session.get('user_id')} calcul={'OK' if session.get('calcul_resultats') else 'ABSENT'}")
    calcul = session.get('calcul_resultats')
    if not calcul:
        return redirect(url_for('dimensionnement2'))
    projets = get_projets_utilisateur(session['user_id'])
    return render_template(
        'equipements.html',
        calcul=calcul,
        user_nom=session.get('user_nom', ''),
        projets=projets
    )


@app.route('/sauvegarder_equipements', methods=['POST'])
@login_required
def sauvegarder_equipements():
    try:
        data   = request.get_json()
        calcul = session.get('calcul_resultats')
        if not calcul:
            return jsonify({'succes': False, 'erreur': 'Session expirée. Relancez le calcul.'})

        print(f"[sauvegarder_equipements] pompe={data.get('id_pompe')} "
              f"ctrl={data.get('id_controleur')} pan={data.get('id_panneau')} "
              f"bat={data.get('id_batterie')}")

        # ── Récupérer les équipements depuis la DB ───────────
        conn         = get_db()
        pompe        = None
        ctrl         = None
        type_ctrl    = data.get('type_ctrl', '')
        panneau      = None
        batterie     = None

        id_pompe = data.get('id_pompe')
        if id_pompe:
            r = conn.execute('SELECT * FROM pompes WHERE id=?', (int(id_pompe),)).fetchone()
            if r: pompe = dict(r)

        id_controleur = data.get('id_controleur')
        if id_controleur:
            # Essayer VFD en premier, puis MPPT
            r = conn.execute('SELECT * FROM vfd WHERE id=?', (int(id_controleur),)).fetchone()
            if r:
                ctrl = dict(r); ctrl['_type'] = 'VFD'; type_ctrl = 'VFD'
            else:
                r = conn.execute(
                    'SELECT * FROM regulateurs_mppt WHERE id=?', (int(id_controleur),)
                ).fetchone()
                if r:
                    ctrl = dict(r); ctrl['_type'] = 'MPPT'; type_ctrl = 'MPPT'

        id_panneau = data.get('id_panneau')
        if id_panneau:
            r = conn.execute('SELECT * FROM panneaux WHERE id=?', (int(id_panneau),)).fetchone()
            if r: panneau = dict(r)

        id_batterie = data.get('id_batterie')
        if id_batterie:
            r = conn.execute('SELECT * FROM batteries WHERE id=?', (int(id_batterie),)).fetchone()
            if r: batterie = dict(r)

        conn.close()

        # ── Calcul du coût ───────────────────────────────────
        nbr_panneaux = int(data.get('nbr_panneaux') or 0)
        nbat_tot     = int(data.get('nbat_tot')     or 0)
        cables_list  = data.get('cables_resultats', [])
        parafoudres  = data.get('parafoudres', {})

        # Filtrer les tronçons DC si source AC
        source_e = session.get('calcul_resultats', {}).get('source_energie', '')
        isAC = source_e in ['groupe', 'groupe_electrogene', 'sbee', 'reseau']
        if isAC:
            cables_list = [t for t in cables_list if t.get('type') != 'DC']

        C_pompe = 0
        if id_pompe:
            conn2 = get_db()
            row2  = conn2.execute('SELECT prix FROM pompes WHERE id=?', (int(id_pompe),)).fetchone()
            C_pompe = int(row2['prix'] or 0) if row2 and row2['prix'] else 0
            conn2.close()
        print(f"[prix pompe] id={id_pompe} prix={C_pompe}")
        C_controleur = int(ctrl.get('prix', 0) or 0)       if ctrl     else 0
        C_panneaux   = int(panneau.get('prix', 0) or 0) * nbr_panneaux if panneau  else 0
        C_batteries  = int(batterie.get('prix', 0) or 0) * nbat_tot    if batterie else 0

        C_cables = sum(
            (t.get('cable') or {}).get('prix', 0) * t.get('L_m', 0)
            for t in cables_list if t.get('cable')
        )
        C_disj = sum(
            (t.get('disjoncteur') or {}).get('prix', 0)
            for t in cables_list if t.get('disjoncteur')
        )
        C_para = sum(
            (p or {}).get('prix', 0)
            for p in parafoudres.values() if p
        )

        C_equipements  = int(C_pompe + C_controleur + C_panneaux + C_batteries + C_cables + C_disj + C_para)
        C_installation = round(C_equipements * 0.15)
        C_divers       = round(C_equipements * 0.10)
        C_total        = C_equipements + C_installation + C_divers

        print(f"[sauvegarder_equipements] cout: pompe={C_pompe} ctrl={C_controleur} "
              f"pan={C_panneaux} bat={C_batteries} cables={int(C_cables)} total={C_total}")

        # ── Stocker en session ───────────────────────────────
        equip_res = {
            'pompe':      pompe    or {},
            'controleur': ctrl     or {},
            'type_ctrl':  type_ctrl,
            'mode_alim':  data.get('mode_alim', ''),
            'panneau':    panneau  or {},
            'batterie':   batterie or {},
            'nbr_panneaux':     nbr_panneaux,
            'nbr_pv_serie':     int(data.get('nbr_pv_serie')     or 0),
            'nbr_pv_parallele': int(data.get('nbr_pv_parallele') or 0),
            'ctot':             float(data.get('ctot')           or 0),
            'nbat_serie':       int(data.get('nbat_serie')       or 0),
            'nbat_par':         int(data.get('nbat_par')         or 0),
            'nbat_tot':         nbat_tot,
            'jours_autonomie':  int(data.get('jours_autonomie')  or 2),
            'cables_resultats': cables_list,
            'parafoudres':      parafoudres,
            'cout': {
                'C_pompe':       C_pompe,
                'C_controleur':  C_controleur,
                'C_panneaux':    C_panneaux,
                'C_batteries':   C_batteries,
                'C_cables':      int(C_cables),
                'C_disjoncteurs':int(C_disj),
                'C_parafoudres': int(C_para),
                'C_equipements': C_equipements,
                'C_installation':C_installation,
                'C_divers':      C_divers,
                'C_total':       C_total,
            },
        }
        session['equipements_resultats'] = equip_res
        session.modified = True

        # ── Sauvegarder le projet en DB ──────────────────────
        payload_json = json.dumps({**calcul, **equip_res})
        nom_projet   = session.get('nom_projet', 'Projet sans nom')
        projet_id    = sauvegarder_projet(
            session['user_id'], nom_projet, '', '',
            calcul.get('usage_type', ''),
            calcul.get('source_energie', ''),
            str(calcul.get('lat', '')),
            str(calcul.get('lon', '')),
            payload_json
        )
        session['projet_id'] = projet_id
        session.modified     = True

        print(f"[sauvegarder_equipements] projet sauvegardé id={projet_id} total={C_total} FCFA")
        return jsonify({'succes': True, 'redirect': '/resultats2', 'projet_id': projet_id})

    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({'succes': False, 'erreur': str(e)})


@app.route('/resultats2')
@login_required
def resultats2():
    print(f"[ROUTE] resultats2 — user={session.get('user_id')} "
          f"calcul={'OK' if session.get('calcul_resultats') else 'ABSENT'} "
          f"equip={'OK' if session.get('equipements_resultats') else 'ABSENT'}")
    calcul = session.get('calcul_resultats')
    equip  = session.get('equipements_resultats')
    if not calcul or not equip:
        return redirect(url_for('dimensionnement2'))
    projets = get_projets_utilisateur(session['user_id'])
    return render_template(
        'resultats2.html',
        calcul=calcul,
        equip=equip,
        user_nom=session.get('user_nom', ''),
        projets=projets
    )

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
        print("DEBUG NASA URL:", response.request.url)
        print("DEBUG NASA status:", response.status_code)
        donnees     = response.json()
        T_max_raw    = list(donnees['properties']['parameter']['T2M_MAX'].values())
        T_min_raw    = list(donnees['properties']['parameter']['T2M_MIN'].values())
        vent_raw     = list(donnees['properties']['parameter']['WS2M'].values())
        humidite_raw = list(donnees['properties']['parameter']['RH2M'].values())
        ray_raw      = list(donnees['properties']['parameter']['ALLSKY_SFC_SW_DWN'].values())
        print("DEBUG ray_raw (MJ/m²/j, 48 valeurs brutes):", ray_raw)

        nb_valeurs = len(T_max_raw)
        nb_annees  = nb_valeurs // 12

        T_max_moy = []
        T_min_moy = []
        vent_moy  = []
        hum_moy   = []
        ray_moy   = []

        for m in range(12):
            vals_tmax = [T_max_raw[a*12+m]    for a in range(nb_annees) if T_max_raw[a*12+m]    not in (-999, -99, None)]
            vals_tmin = [T_min_raw[a*12+m]    for a in range(nb_annees) if T_min_raw[a*12+m]    not in (-999, -99, None)]
            vals_vent = [vent_raw[a*12+m]      for a in range(nb_annees) if vent_raw[a*12+m]     not in (-999, -99, None)]
            vals_hum  = [humidite_raw[a*12+m]  for a in range(nb_annees) if humidite_raw[a*12+m] not in (-999, -99, None)]
            vals_ray  = [ray_raw[a*12+m]       for a in range(nb_annees) if ray_raw[a*12+m]      not in (-999, -99, None)]

            T_max_moy.append(sum(vals_tmax)/len(vals_tmax) if vals_tmax else 0)
            T_min_moy.append(sum(vals_tmin)/len(vals_tmin) if vals_tmin else 0)
            vent_moy.append( sum(vals_vent)/len(vals_vent)  if vals_vent  else 0)
            hum_moy.append(  sum(vals_hum) /len(vals_hum)  if vals_hum   else 0)
            ray_moy.append(  sum(vals_ray) /len(vals_ray)  if vals_ray   else 0)

        print("DEBUG ray_moy avant conversion (MJ/m²/j moyenne par mois):", [round(r,3) for r in ray_moy])
        # Conversion MJ/m²/jour -> kWh/m²/jour
        ray_moy = [round(r / 3.6, 2) for r in ray_moy]
        print("DEBUG ray_moy après conversion (kWh/m²/j):", ray_moy)

        mois = ['Jan','Fév','Mar','Avr','Mai','Jun',
                'Jul','Aoû','Sep','Oct','Nov','Déc']
        ET0_par_mois = {}
        for i in range(12):
            ET0_par_mois[mois[i]] = calculer_ET0(
                T_max_moy[i], T_min_moy[i],
                hum_moy[i], vent_moy[i], ray_moy[i]
            )

        # Mois critique = irradiation minimale (pire cas solaire pour dimensionnement)
        idx_critique  = ray_moy.index(min(ray_moy))
        mois_critique = mois[idx_critique]
        valeur_brute = ray_moy[idx_critique] * 3.6  # reconstitution avant ÷3.6
        print("Valeur brute NASA (MJ/m²/j):", round(valeur_brute, 3))
        print("Après ÷3.6 (kWh/m²/j):", round(valeur_brute / 3.6, 3))
        print("DEBUG mois_critique:", mois_critique, "| irradiation finale:", round(ray_moy[idx_critique],2), "kWh/m²/j")
        print("DEBUG ray_moy par mois (kWh/m²/j):", dict(zip(mois, ray_moy)))

        return jsonify({
            "succes":          True,
            "ET0_par_mois":    ET0_par_mois,
            "mois_critique":   mois_critique,
            "ET0_max":         round(ET0_par_mois[mois_critique], 2),
            "irradiation":     round(ray_moy[idx_critique], 2),
            "temperature_max": round(max(T_max_moy), 2),
            "temperature_min": round(min(T_min_moy), 2),
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
        heures_pompage           = float(data.get('heures_pompage') or 0)
        if heures_pompage <= 0:
            return jsonify({'succes': False, 'erreur': 'Heures de pompage invalides'})
        irradiation              = float(data['irradiation'])
        pr_ratio                 = float(data.get('pr_ratio', 0.75))
        puissance_panneau_W      = float(data.get('puissance_panneau_Wc', 300))
        longueur_canalisation    = float(data.get('longueur_canalisation', 0))
        diametre_tuyau           = float(data.get('diametre_tuyau', 63))
        coeff_pertes_charge      = float(data.get('coeff_pertes_charge', 0.10))
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
            print("=== BESOINS EAU (irrigation) ===")
            print("culture:", culture, "| superficie:", data['superficie'], "ha")
            print("ET0:", data.get('ET0'), "mm/j | Kc:", besoins.get('kc_utilise'))
            print("ETc:", besoins.get('ETc'), "mm/j")
            print("η efficience:", besoins.get('efficacite_irrigation'))
            print("Besoin net:", besoins.get('besoin_net_m3_jour'), "m³/j")
            print("Besoin brut:", besoins.get('besoin_brut_m3_jour'), "m³/j")
        else:
            besoin_journalier  = float(data['besoin_journalier'])
            besoin_brut        = besoin_journalier
            systeme_irrigation = 'gravitaire'
            besoins = {
                "ETc": round(besoin_journalier, 2),
                "besoin_net_m3_jour": round(besoin_journalier, 2),
                "besoin_brut_m3_jour": round(besoin_journalier, 2),
                "besoin_session_m3": round(besoin_journalier, 2),
                "frequence_arrosage_jours": 1,
                "kc_utilise": None,
            }
            print("=== BESOINS EAU (classique) ===")
            print("Besoin journalier:", besoin_journalier, "m³/j")

        if mode == 'classique':
            hydraulique = calculer_hydraulique(
                besoin_brut_m3_jour=besoin_brut, heures_pompage=heures_pompage,
                systeme_irrigation=systeme_irrigation, source_energie=source_energie,
                longueur_canalisation=longueur_canalisation, diametre_tuyau_mm=diametre_tuyau,
                type_systeme_hydraulique=type_systeme_hydraulique, type_alimentation=type_alimentation,
                hauteur_reservoir=hauteur_reservoir, niveau_dynamique=niveau_dynamique,
                niveau_eau_lac=niveau_eau_lac, hauteur_aspiration=hauteur_aspiration,
                coeff_pertes_charge=coeff_pertes_charge,
            )
        else:
            hydraulique = calculer_hydraulique(
                besoin_brut_m3_jour=besoin_brut, heures_pompage=heures_pompage,
                profondeur_aspiration=profondeur_aspiration, hauteur_refoulement=hauteur_refoulement,
                systeme_irrigation=systeme_irrigation, source_energie=source_energie,
                longueur_canalisation=longueur_canalisation, diametre_tuyau_mm=diametre_tuyau,
                type_systeme_hydraulique='irrigation', type_alimentation='bas',
                hauteur_reservoir=0, niveau_dynamique=0, niveau_eau_lac=0, hauteur_aspiration=0,
                coeff_pertes_charge=coeff_pertes_charge,
            )

        print("=== HYDRAULIQUE ===")
        print("Hgeo:", hydraulique.get('hauteur_geo_m'), "m")
        print("Pertes charge (Pc):", hydraulique.get('pertes_charge_m'), "m")
        print("HMT:", hydraulique.get('HMT_m'), "m")
        print("Q:", hydraulique.get('debit_m3_h'), "m³/h")

        pompe = calculer_pompe(hydraulique['debit_m3_h'], hydraulique['HMT_m'])

        print("=== VALEURS REÇUES ===")
        print("besoin_journalier:", data.get('besoin_journalier'))
        print("heures_pompage:",    data.get('heures_pompage'))
        print("niveau_dynamique:",  data.get('niveau_dynamique'))
        print("hauteur_refoulement:", data.get('hauteur_refoulement'))
        print("hauteur_reservoir:", data.get('hauteur_reservoir'))
        print("Q calculé:",  hydraulique['debit_m3_h'])
        print("HMT calculée:", hydraulique['HMT_m'])
        print("Ph:", pompe.get('Ph_kW'), "Pp:", pompe.get('Pp_kW'), "Pm:", pompe.get('Pm_kW'))

        eta_p = float(data.get('eta_p', 0.65))
        eta_m = float(data.get('eta_m', 0.90))
        Rmp   = eta_p * eta_m
        Q_m3_jour = besoin_brut
        HMT_m = hydraulique['HMT_m']
        print("=== PUISSANCE POMPE ===")
        print("Rmp (ηp × ηm):", round(Rmp, 3))
        print("Ph:", pompe.get('Ph_kW'), "kW | Pp:", pompe.get('Pp_kW'), "kW | Pm:", pompe.get('Pm_kW'), "kW")
        print("Pm commercial:", pompe.get('Pm_commercial_kW'), "kW")

        # Valeurs par défaut — écrasées si hybride_batteries
        type_bat = 'GEL'
        dod      = 0.0

        if source_energie == "solaire":
            energie = calculer_solaire(Q_m3_jour, HMT_m, Rmp, irradiation, pr_ratio, puissance_panneau_W)
            print("=== SOLAIRE ===")
            print("Eelec:", energie.get('energie_jour_kWh'), "kWh/j")
            print("Pc:", energie.get('puissance_crete_kWp'), "kWc")
            print("Usyst:", energie.get('U_syst'), "V")
            print("Ir:", irradiation, "kWh/m²/j | Pr:", pr_ratio)
        elif source_energie in ("groupe", "groupe_electrogene"):
            Pm_grp               = pompe['Pm_kW']
            puissance_groupe_kW  = round(Pm_grp * 3, 3)
            e_jour_kWh           = round(Pm_grp * heures_pompage, 3)
            consommation_jour    = round(puissance_groupe_kW * heures_pompage * 0.3, 1)
            consommation_mois    = round(consommation_jour * 30, 1)
            print("=== GROUPE ===")
            print("Pm:", Pm_grp, "kW")
            print("Puissance groupe:", puissance_groupe_kW, "kW")
            print("Conso/jour:", consommation_jour, "L")
            print("Conso/mois:", consommation_mois, "L")
            energie = {
                "puissance_groupe_kW":       puissance_groupe_kW,
                "energie_jour_kWh":          e_jour_kWh,
                "consommation_jour_litres":  consommation_jour,
                "consommation_mois_litres":  consommation_mois,
                "consommation_annee_litres": round(consommation_jour * 365, 1),
            }
        elif source_energie == "hybride_groupe":
            energie = calculer_hybride_groupe(
                pompe['Pm_kW'], heures_pompage, irradiation,
                Q_m3_jour, HMT_m, Rmp, pr_ratio, puissance_panneau_W
            )
            grp = energie.get('groupe', {})
            print("=== HYBRIDE GROUPE ===")
            print("Pm:", pompe['Pm_kW'], "kW")
            print("Puissance groupe:", grp.get('puissance_groupe_kW'), "kW")
            print("Conso/jour:", grp.get('consommation_jour_litres'), "L")
            print("Conso/mois:", grp.get('consommation_mois_litres'), "L")
        elif source_energie == "hybride_batteries":
            marque_bat = data.get('marque_batterie', '')
            bats = equipements_mod.get_modeles_batteries(marque_bat) if marque_bat else []
            batterie_choisie = bats[0] if bats else {}
            type_bat = batterie_choisie.get('technologie', data.get('type_batterie', 'GEL'))
            dod = 0.5 if 'GEL' in str(type_bat).upper() else 0.8
            capacite_bat_Ah = int(batterie_choisie.get('capacite_Ah', data.get('capacite_bat_Ah', 200)))
            tension_bat_V   = batterie_choisie.get('tension_V', data.get('tension_bat_V', 24))
            energie = calculer_hybride_batteries(
                Q_m3_jour, HMT_m, Rmp, irradiation, pr_ratio, puissance_panneau_W,
                tension_bat_V, capacite_bat_Ah, int(data.get('jours_autonomie') or 2), type_bat
            )
        else:
            energie = {}

        pompes_recommandees = selectionner_pompes(
            hydraulique['debit_m3_h'], hydraulique['HMT_m'],
            source_energie, data.get('marque_pompe', 'toutes')
        )

        # ── Panneaux PV : série / parallèle ──────────────────────────────
        pu_panneau = float(data.get('puissance_panneau_Wc', puissance_panneau_W))
        u_pv = float(data.get('vmp_panneau', 0) or data.get('tension_panneau', 0) or 36)
        Nbr_panneaux = Nbr_pvsérie = Nbr_paralleles_pv = 0
        Pc = 0
        if source_energie in ('solaire', 'hybride_groupe', 'hybride_batteries') and pu_panneau > 0 and u_pv > 0:
            sol = energie if source_energie == 'solaire' else energie.get('solaire', {})
            Pc = sol.get('puissance_crete_kWp', 0)
            U_syst = sol.get('U_syst', 48)
            if Pc > 0:
                Nbr_panneaux       = math.ceil(Pc * 1000 / pu_panneau)
                Nbr_pvsérie        = max(round(U_syst / u_pv), 1)
                Nbr_paralleles_pv  = math.ceil(Nbr_panneaux / Nbr_pvsérie)
        print("Pc transmise aux résultats:", Pc)
        print("Nbr_panneaux:", Nbr_panneaux)
        print("Nbr_pv_serie:", Nbr_pvsérie)

        Eelec = energie.get('energie_jour_kWh', 0) if source_energie == 'solaire' else \
                energie.get('solaire', {}).get('energie_jour_kWh', 0)
        print("=== COMPARAISON PREVIEW vs CALCUL FINAL ===")
        print("Q utilisé:", Q_m3_jour)
        print("HMT utilisée:", HMT_m)
        print("Ir utilisé:", irradiation)
        print("Pr utilisé:", pr_ratio)
        print("Rmp:", round(Rmp, 3))
        print("Eelec calculé:", Eelec)
        print("Pc calculé:", Pc)
        print("Payload reçu - Q depuis besoin/heures:", data.get('besoin_journalier'), "/", data.get('heures_pompage'))
        print("Payload reçu - HMT:", data.get('HMT'))
        print("Payload reçu - Ir:", data.get('irradiation'))
        print("Payload reçu - Pr:", data.get('pr_ratio'))

        # ── Batteries : série / parallèle (hybride_batteries uniquement) ──
        Ctot = Nbat_serie = Nbr_bat_paralleles = Nbat_tot = 0
        if source_energie == 'hybride_batteries':
            Ctot               = energie.get('capacite_totale_Ah', 0)
            Nbat_serie         = energie.get('nb_serie', 0)
            Nbr_bat_paralleles = energie.get('nb_parallele', 0)
            Nbat_tot           = energie.get('nb_batteries', 0)

        print("DoD:", dod, "type bat:", type_bat)
        print("Nbr panneaux:", Nbr_panneaux, "série:", Nbr_pvsérie, "parallèle:", Nbr_paralleles_pv)
        print("Ctot:", Ctot, "Nbat tot:", Nbat_tot)
        if source_energie == 'hybride_batteries':
            _sol_bat = energie.get('solaire', {})
            print("=== BATTERIES (app.py) ===")
            print("Eelec:", _sol_bat.get('energie_jour_kWh', 0), "kWh/j")
            print("Jours_autonomie:", data.get('jours_autonomie'))
            print("Usyst:", _sol_bat.get('U_syst', '—'), "V")
            print("DoD:", dod)
            print("Ctot:", Ctot, "Ah")

        # ── Courant d'alimentation Ia (groupe / réseau uniquement) ────────
        cos_phi  = 0.8
        Pm       = pompe.get('Pm_kW', 0)
        eta_m    = pompe_mod.RENDEMENT_MOTEUR
        Ia       = 0
        type_alim = ''
        if source_energie in ('groupe', 'groupe_electrogene', 'sbee', 'reseau'):
            if Pm <= 3:
                Ia        = round(Pm / (0.220 * cos_phi * eta_m), 2)
                type_alim = 'Monophasé — 220V'
            else:
                Ia        = round(Pm / (1.732 * 0.380 * cos_phi * eta_m), 2)
                type_alim = 'Triphasé — 380V'
        print("=== COURANT Ia ===")
        print("Ia:", Ia, "A | type:", type_alim)
        pompe['Ia_A']            = Ia
        pompe['type_alimentation'] = type_alim

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
            "nbr_panneaux":     Nbr_panneaux,
            "nbr_pv_serie":     Nbr_pvsérie,
            "nbr_pv_parallele": Nbr_paralleles_pv,
            "ctot":             round(float(Ctot), 2),
            "nbat_serie":       Nbat_serie,
            "nbr_bat_parallele": Nbr_bat_paralleles,
            "nbat_tot":         Nbat_tot,
        }

        # SAUVEGARDE AUTOMATIQUE
        payload_json = json.dumps({**data, **resultats})
        projet_id    = data.get('projet_id')
        if projet_id:
            mettre_a_jour_projet(projet_id, session['user_id'], payload_json)
        else:
            nom_final = session.pop('nom_projet', None) or data.get('nom_projet', '') or 'Projet sans nom'
            projet_id = sauvegarder_projet(
                session['user_id'],
                nom_final,
                data.get('realise_par', ''),
                data.get('date_projet', ''),
                mode, source_energie,
                data.get('lat', ''), data.get('lon', ''),
                payload_json
            )

        resultats['projet_id'] = projet_id

        # ── Équipements sélectionnés via IDs (frontend) ──────
        id_pompe      = data.get('id_pompe')
        id_controleur = data.get('id_controleur')
        id_panneau    = data.get('id_panneau')
        id_batterie   = data.get('id_batterie')
        equipements_choisis = {}

        if any([id_pompe, id_controleur, id_panneau, id_batterie]):
            conn_eq = get_db()

            if id_pompe:
                row = conn_eq.execute('SELECT * FROM pompes WHERE id=?', (int(id_pompe),)).fetchone()
                if row:
                    equipements_choisis['pompe'] = dict(row)
                    print(f"[calculer] pompe choisie: {row['marque']} {row['modele']} {row['puissance_kW']}kW")

            if id_controleur:
                # Cherche d'abord dans vfd, puis dans regulateurs_mppt
                vfd_row = conn_eq.execute('SELECT * FROM vfd WHERE id=?', (int(id_controleur),)).fetchone()
                if vfd_row:
                    c = dict(vfd_row); c['_type_ctrl'] = 'VFD'
                    equipements_choisis['controleur'] = c
                    print(f"[calculer] contrôleur VFD choisi: {c.get('modele')} {c.get('puissance_kW')}kW")
                else:
                    reg_row = conn_eq.execute(
                        'SELECT * FROM regulateurs_mppt WHERE id=?', (int(id_controleur),)
                    ).fetchone()
                    if reg_row:
                        c = dict(reg_row); c['_type_ctrl'] = 'MPPT'
                        equipements_choisis['controleur'] = c
                        print(f"[calculer] contrôleur MPPT choisi: {c.get('marque')} {c.get('modele')}")

            if id_panneau:
                row = conn_eq.execute('SELECT * FROM panneaux WHERE id=?', (int(id_panneau),)).fetchone()
                if row:
                    equipements_choisis['panneau'] = dict(row)
                    p_choisi = equipements_choisis['panneau']
                    print(f"[calculer] panneau choisi: {p_choisi['marque']} {p_choisi['modele']} {p_choisi['puissance_W']}Wc")
                    # Recalculer série/parallèle avec la vraie puissance du panneau
                    pu_reel = p_choisi['puissance_W']
                    u_reel  = p_choisi.get('Vmp_V') or 36
                    sol_ref = energie if source_energie == 'solaire' else energie.get('solaire', {})
                    Pc_reel = sol_ref.get('puissance_crete_kWp', 0)
                    U_syst_reel = sol_ref.get('U_syst', 48)
                    if Pc_reel > 0 and pu_reel > 0 and u_reel > 0:
                        Nbr_panneaux       = math.ceil(Pc_reel * 1000 / pu_reel)
                        Nbr_pvsérie        = max(round(U_syst_reel / u_reel), 1)
                        Nbr_paralleles_pv  = math.ceil(Nbr_panneaux / Nbr_pvsérie)
                        resultats['nbr_panneaux']     = Nbr_panneaux
                        resultats['nbr_pv_serie']     = Nbr_pvsérie
                        resultats['nbr_pv_parallele'] = Nbr_paralleles_pv
                        print(f"[calculer] panneaux recalculés: {Nbr_panneaux} ({Nbr_pvsérie}S×{Nbr_paralleles_pv}P)")

            if id_batterie:
                row = conn_eq.execute('SELECT * FROM batteries WHERE id=?', (int(id_batterie),)).fetchone()
                if row:
                    equipements_choisis['batterie'] = dict(row)
                    b = equipements_choisis['batterie']
                    print(f"[calculer] batterie choisie: {b['marque']} {b['capacite_Ah']}Ah {b['tension_V']}V")

            conn_eq.close()

            # Prix détaillés pour le coût total côté frontend
            nb_pan = resultats.get('nbr_panneaux', 0)
            nb_bat = resultats.get('nbat_tot', 0)
            resultats['prix_equipements'] = {
                'pompe':           (equipements_choisis.get('pompe')      or {}).get('prix', 0) or 0,
                'panneau_unitaire':(equipements_choisis.get('panneau')    or {}).get('prix', 0) or 0,
                'batterie_unitaire':(equipements_choisis.get('batterie')  or {}).get('prix', 0) or 0,
                'controleur':      (equipements_choisis.get('controleur') or {}).get('prix', 0) or 0,
                'total_panneaux':  ((equipements_choisis.get('panneau') or {}).get('prix', 0) or 0) * nb_pan,
                'total_batteries': ((equipements_choisis.get('batterie') or {}).get('prix', 0) or 0) * nb_bat,
            }
            print(f"[calculer] prix_equipements: {resultats['prix_equipements']}")

        resultats['equipements_choisis'] = equipements_choisis

        try:
            cout_data = {
                'source_energie':       source_energie,
                'Pm_commercial_kW':     resultats['pompe']['Pm_commercial_kW'],
                'nb_panneaux':          resultats.get('energie', {}).get('nb_panneaux_300Wc', 0),
                'puissance_panneau_Wc': data.get('puissance_panneau_Wc', 300),
                'nb_batteries':         resultats.get('energie', {}).get('nb_batteries', 0),
                'capacite_batterie_Ah': data.get('capacite_batterie_Ah', 200),
                'type_batterie':        data.get('type_batterie', 'GEL'),
                'puissance_groupe_kW':  resultats.get('energie', {}).get('puissance_groupe_kW', 0),
                'puissance_onduleur_kW': float(data.get('puissance_onduleur_kW', 0) or 0),
                'type_onduleur':         data.get('type_onduleur', ''),
            }
            resultats['cout'] = calculer_cout(cout_data)
        except Exception as e:
            print("ERREUR COUT:", str(e))
            import traceback
            traceback.print_exc()
            resultats['cout'] = None
        print("DEBUG COUT:", cout_data if 'cout_data' in locals() else "cout_data non défini")
        print("DEBUG RESULTAT COUT:", resultats.get('cout'))
        return jsonify(resultats)

    except Exception as e:
        import traceback
        print("ERREUR CALCUL :", traceback.format_exc())
        return jsonify({"succes": False, "erreur": str(e)})

# ============================================================
# SAUVEGARDE PROGRESSION (autosave toutes les 30s)
# ============================================================

@app.route('/sauvegarder_progression', methods=['POST'])
@login_required
def sauvegarder_progression():
    data       = request.get_json()
    projet_id  = data.get('projet_id')
    user_id    = session['user_id']
    if not projet_id:
        return jsonify({'success': False, 'raison': 'pas de projet_id'})
    conn = get_db()
    row  = conn.execute(
        'SELECT resultats FROM projets WHERE id=? AND user_id=?',
        (projet_id, user_id)
    ).fetchone()
    if not row:
        conn.close()
        return jsonify({'success': False, 'raison': 'projet introuvable'})
    try:
        existant = json.loads(row['resultats']) if row['resultats'] else {}
    except Exception:
        existant = {}
    champs = ['nb_beneficiaires', 'besoin_journalier', 'niveau_dynamique',
              'hauteur_refoulement', 'hmt', 'eta_p', 'eta_m',
              'heures_pompage', 'jours_autonomie']
    for c in champs:
        if data.get(c) is not None:
            existant[c] = data[c]
    conn.execute(
        "UPDATE projets SET resultats=?, date_modif=datetime('now') WHERE id=? AND user_id=?",
        (json.dumps(existant), projet_id, user_id)
    )
    conn.commit()
    conn.close()
    return jsonify({'success': True})

# ============================================================
# SUPPRESSION PROJET
# ============================================================

@app.route('/supprimer_projet/<int:projet_id>', methods=['POST'])
def supprimer_projet_route(projet_id):
    if 'user_id' not in session:
        return '', 401
    supprimer_projet(projet_id, session['user_id'])
    return '', 200

# ============================================================
# PDF
# ============================================================

@app.route('/generer_pdf', methods=['POST'])
@login_required
def generer_pdf():
    try:
        data = request.get_json()
        generateur_pdf = charger_module('generateur_pdf', os.path.join(dossier, 'generateur_pdf.py'))
        tension_systeme       = data.get('tension_systeme', '—')
        type_onduleur         = data.get('type_onduleur', '')
        puissance_onduleur_kW = float(data.get('puissance_onduleur_kW', 0) or 0)
        marque_onduleur       = data.get('marque_onduleur', '')
        modele_onduleur       = data.get('modele_onduleur', '')
        data['equipements'] = {
            'marque_panneau':    data.get('marque_panneau', ''),
            'modele_panneau':    data.get('modele_panneau', ''),
            'marque_regulateur': data.get('marque_regulateur', ''),
            'modele_regulateur': data.get('modele_regulateur', ''),
            'marque_batterie':   data.get('marque_batterie', ''),
            'modele_batterie':   data.get('modele_batterie', ''),
            'marque_onduleur':   marque_onduleur,
            'modele_onduleur':   modele_onduleur,
        }
        data['tension_systeme']       = tension_systeme
        data['type_onduleur']         = type_onduleur
        data['puissance_onduleur_kW'] = puissance_onduleur_kW
        data.setdefault('nom_client',      '')
        data.setdefault('jours_autonomie', None)
        data.setdefault('dod',             0.70)
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
    data                = request.get_json()
    marque              = data.get('marque', '')
    q_min               = float(data.get('q_min', 0))
    hmt_min             = float(data.get('hmt_min', 0))
    alimentation_filtre = data.get('alimentation_filtre', None)
    modeles = pompes_bd_mod.get_modeles_par_marque(marque)
    for p in modeles:
        src = str(p.get('source_energie', '')).lower()
        p['alimentation'] = 'DC' if 'solaire' in src or 'dc' in src else 'AC'
    if q_min > 0 and hmt_min > 0:
        modeles = [p for p in modeles
                   if p.get('debit_max_m3h', 0) >= q_min
                   and p.get('HMT_max_m', 0) >= hmt_min]
    if alimentation_filtre == 'AC':
        def _est_ac(p):
            alim    = str(p.get('alimentation', '')).upper()
            tension = str(p.get('tension_V', '')).upper()
            return (alim == 'AC'
                    or 'AC'  in tension
                    or '220' in tension
                    or '230' in tension
                    or '380' in tension)
        modeles = [p for p in modeles if _est_ac(p)]
    print("Filtre alimentation:", alimentation_filtre, "| Résultats:", len(modeles))
    return jsonify({"succes": True, "modeles": modeles})

@app.route('/get_pompes')
@login_required
def get_pompes():
    Q      = float(request.args.get('Q',   0))
    HMT    = float(request.args.get('HMT', 0))
    Pm     = float(request.args.get('Pm',  0))
    source = session.get('source_energie', 'solaire')
    sources_ac = ['groupe_electrogene', 'sbee']

    conn = get_db()
    if source in sources_ac:
        rows = conn.execute('''
            SELECT * FROM pompes
            WHERE (tension_V LIKE '%AC%'
                OR tension_V LIKE '%220%'
                OR tension_V LIKE '%380%')
            AND tension_V NOT LIKE 'DC %'
            AND debit_max_m3h >= ?
            AND HMT_max_m >= ?
            AND puissance_kW >= ?
            ORDER BY puissance_kW''',
            (Q * 0.85, HMT * 0.85, Pm * 0.85 if Pm > 0 else 0)
        ).fetchall()
    else:
        rows = conn.execute('''
            SELECT * FROM pompes
            WHERE (tension_V LIKE 'DC%'
                OR alimentation = 'DC'
                OR alimentation = 'DC/AC')
            AND tension_V NOT LIKE '%AC 50Hz%'
            AND debit_max_m3h >= ?
            AND HMT_max_m >= ?
            AND puissance_kW >= ?
            ORDER BY puissance_kW''',
            (Q * 0.85, HMT * 0.85, Pm * 0.85 if Pm > 0 else 0)
        ).fetchall()
    conn.close()

    pompes = [dict(r) for r in rows]

    print("Source:", source)
    print("Nb pompes:", len(pompes))
    print("Marques:", list(set([p['marque'] for p in pompes])))

    return jsonify({"succes": True, "pompes": pompes[:8]})

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
    data   = request.get_json()
    marque = data.get('marque', '')
    pc_min = float(data.get('pc_min', 0))
    modeles = equipements_mod.get_modeles_panneaux(marque)
    if pc_min > 0:
        modeles = [p for p in modeles
                   if p.get('puissance_W', 0) >= (pc_min * 1000 / 4)]
    return jsonify({"succes": True, "modeles": modeles})

@app.route('/get_marques_batteries', methods=['GET'])
@login_required
def get_marques_batteries():
    return jsonify({"succes": True, "marques": equipements_mod.get_marques_batteries()})

@app.route('/get_modeles_batteries', methods=['POST'])
@login_required
def get_modeles_batteries():
    data = request.get_json()
    return jsonify({"succes": True, "modeles": equipements_mod.get_modeles_batteries(data.get('marque', ''))})

@app.route('/get_batteries')
@login_required
def get_batteries():
    marque = request.args.get('marque', '')
    conn = get_db()
    rows = conn.execute(
        'SELECT * FROM batteries WHERE marque = ? ORDER BY capacite_Ah',
        (marque,)
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route('/get_batterie_detail')
@login_required
def get_batterie_detail():
    bat_id = request.args.get('id', 0, type=int)
    conn = get_db()
    row = conn.execute('SELECT * FROM batteries WHERE id = ?', (bat_id,)).fetchone()
    conn.close()
    return jsonify(dict(row) if row else {})

@app.route('/get_types_onduleurs')
@login_required
def get_types_onduleurs():
    from equipements import get_types_onduleurs
    return jsonify({'succes': True, 'types': get_types_onduleurs()})

@app.route('/get_marques_onduleurs', methods=['POST'])
@login_required
def get_marques_onduleurs():
    from equipements import get_marques_onduleurs
    data = request.get_json()
    return jsonify({'succes': True, 'marques': get_marques_onduleurs(data.get('type_onduleur'))})

@app.route('/get_modeles_onduleurs', methods=['POST'])
@login_required
def get_modeles_onduleurs():
    from equipements import get_modeles_onduleurs
    data = request.get_json()
    return jsonify({'succes': True, 'modeles': get_modeles_onduleurs(data.get('marque'), data.get('type_onduleur'))})


# ============================================================
# NOUVELLES ROUTES — ÉQUIPEMENTS DB (solarpump.db)
# ============================================================

import re as _re

# ── helpers parsing câbles / disjoncteurs ─────────────────────

def _section_mm2(calibre_str):
    """Extrait la section numérique depuis '1×2.5mm²' -> 2.5"""
    m = _re.search(r'[×xX*]([\d.]+)\s*mm', str(calibre_str))
    if m: return float(m.group(1))
    m = _re.search(r'^([\d.]+)\s*mm', str(calibre_str))
    if m: return float(m.group(1))
    return 9999.0

def _ampere_calibre(calibre_str):
    """Extrait l'ampérage depuis '1000V/10A' ou '16A' ou '25' -> float"""
    t = str(calibre_str)
    m = _re.search(r'/(\d+)\s*A', t)
    if m: return float(m.group(1))
    m = _re.search(r'^(\d+)\s*A', t, _re.I)
    if m: return float(m.group(1))
    try: return float(t.split('A')[0].split('/')[-1].strip())
    except: return 9999.0

_SECTIONS_STD = [1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240]
_CALIBRES_STD = [6, 10, 16, 20, 25, 32, 40, 63, 80, 100, 125, 160, 200, 250, 315, 400, 630]

def _section_std(s_calc):
    for v in _SECTIONS_STD:
        if v >= s_calc: return v
    return _SECTIONS_STD[-1]

def _calibre_std(c_calc):
    for v in _CALIBRES_STD:
        if v >= c_calc: return v
    return _CALIBRES_STD[-1]

def _calc_section_dc(I, L, U, rho=0.0225):
    """Section DC (aller-retour) : S = 2 × ρ × L × I / (0.025 × U)"""
    if U <= 0 or I <= 0 or L <= 0: return 0
    return 2 * rho * L * I / (0.025 * U)

def _calc_section_reg_pompe(I, L, U, rho=0.0225):
    """Section Régulateur → Pompe DC : ΔU = 2.5% × U"""
    if U <= 0 or I <= 0 or L <= 0: return 0
    return 2 * rho * L * I / (0.025 * U)

def _calc_section_ac_mono(I, L, U, rho=0.0225):
    """Section AC mono : même formule que DC"""
    return _calc_section_dc(I, L, U, rho)

def _calc_section_ac_tri(I, L, U, rho=0.0225):
    """Section AC tri : S = √3 × ρ × L × I / (0.03 × U)"""
    if U <= 0 or I <= 0 or L <= 0: return 0
    return 1.732 * rho * L * I / (0.03 * U)

def _find_cable(conn, categorie, S_min):
    rows = conn.execute(
        "SELECT * FROM cables WHERE categorie=? ORDER BY prix ASC", (categorie,)
    ).fetchall()
    cands = [dict(r) for r in rows if _section_mm2(r['calibre_section']) >= S_min]
    if not cands: return None
    return min(cands, key=lambda r: _section_mm2(r['calibre_section']))

def _find_cable_by_desig(conn, desig_like, S_min):
    rows = conn.execute(
        "SELECT * FROM cables WHERE designation LIKE ? ORDER BY prix ASC",
        (f'%{desig_like}%',)
    ).fetchall()
    cands = [dict(r) for r in rows if _section_mm2(r['calibre_section']) >= S_min]
    if not cands: return None
    return min(cands, key=lambda r: _section_mm2(r['calibre_section']))

def _find_disj(conn, cat_like, In_min):
    rows = conn.execute(
        "SELECT * FROM disjoncteurs WHERE categorie LIKE ? ORDER BY prix ASC",
        (f'%{cat_like}%',)
    ).fetchall()
    cands = [dict(r) for r in rows if _ampere_calibre(r['calibre']) >= In_min]
    if not cands: return None
    return min(cands, key=lambda r: _ampere_calibre(r['calibre']))

def _find_para(conn, cat_like):
    # Cherche d'abord dans la désignation, puis dans la catégorie
    row = conn.execute(
        """SELECT * FROM parafoudres
           WHERE designation LIKE ? OR categorie LIKE ?
           ORDER BY prix ASC LIMIT 1""",
        (f'%{cat_like}%', f'%{cat_like}%')
    ).fetchone()
    return dict(row) if row else None

# ── 1. /get_pompes_compatibles ────────────────────────────────

@app.route('/get_pompes_compatibles', methods=['POST'])
@login_required
def get_pompes_compatibles():
    try:
        data   = request.get_json()
        Q      = float(data.get('Q',  0))
        HMT    = float(data.get('HMT', 0))
        Pm     = float(data.get('Pm',  0))
        Pc_kWc = float(data.get('Pc_kWc', 0))
        source = data.get('source_energie', 'solaire')
        Usyst  = int(float(data.get('Usyst', 24)))
        print(f"[get_pompes_compatibles] Q={Q} HMT={HMT} Pm={Pm} source={source} Usyst={Usyst}")

        # Filtre alimentation selon source
        if source in ('solaire', 'hybride_batteries'):
            alim_cond = "1=1"           # toutes alimentations acceptées
            alim_params = []
        else:
            alim_cond = "type_alimentation IN ('AC_mono','AC_tri','AC','DC/AC')"
            alim_params = []

        conn = get_db()
        rows = conn.execute(
            f"""SELECT p.*,
                p.ctrl_modele, p.ctrl_plage_tension_pv,
                CAST(p.ctrl_vmin_V AS REAL) as ctrl_vmin_V,
                CAST(p.ctrl_vmax_V AS REAL) as ctrl_vmax_V,
                CAST(p.ctrl_imax_A AS REAL) as ctrl_imax_A
                FROM pompes p
                WHERE p.debit_max_m3h >= ?
                AND p.HMT_max_m >= ?
                AND p.puissance_kW >= ?
                AND ({alim_cond})
                ORDER BY p.puissance_kW ASC""",
            [Q, HMT, Pm] + alim_params
        ).fetchall()
        pompes = [dict(r) for r in rows]
        print(f"[get_pompes_compatibles] {len(pompes)} pompe(s) trouvée(s)")
        result = []
        for p in pompes:
            alim = p.get('type_alimentation', '')
            controleur = None

            if alim in ('DC', 'DC/AC'):
                try:
                    ctrl_vmin = float(p.get('ctrl_vmin_V') or 0)
                    ctrl_vmax = float(p.get('ctrl_vmax_V') or 9999)
                except:
                    ctrl_vmin = 0
                    ctrl_vmax = 9999

                if ctrl_vmin > 0 and not (ctrl_vmin <= Usyst <= ctrl_vmax):
                    continue

                Ireg_p = round((Pc_kWc * 1.25 * 1000) / Usyst, 1) if Usyst > 0 else 0.0
                controleur = {
                    'id': None,
                    'type': 'MPPT',
                    'modele': p.get('ctrl_modele') or 'MPPT intégré',
                    'plage_tension_pv': p.get('ctrl_plage_tension_pv') or '—',
                    'Ireg_A': Ireg_p,
                    'prix': 0
                }

            elif alim == 'AC_mono':
                vfd = conn.execute("""
                    SELECT * FROM vfd WHERE type_sortie='mono'
                    AND intervalle_pompe_min_kW <= ?
                    AND intervalle_pompe_max_kW >= ?
                    ORDER BY puissance_kW ASC LIMIT 1
                """, (p['puissance_kW'], p['puissance_kW'])).fetchone()
                if vfd:
                    vd = dict(vfd)
                    controleur = {'id': vd.get('id'), 'type': 'VFD_mono',
                        'modele': vd.get('modele',''), 'puissance_kW': vd.get('puissance_kW'),
                        'prix': vd.get('prix', 0)}

            elif alim == 'AC_tri':
                vfd = conn.execute("""
                    SELECT * FROM vfd WHERE type_sortie='tri'
                    AND intervalle_pompe_min_kW <= ?
                    AND intervalle_pompe_max_kW >= ?
                    ORDER BY puissance_kW ASC LIMIT 1
                """, (p['puissance_kW'], p['puissance_kW'])).fetchone()
                if vfd:
                    vd = dict(vfd)
                    controleur = {'id': vd.get('id'), 'type': 'VFD_tri',
                        'modele': vd.get('modele',''), 'puissance_kW': vd.get('puissance_kW'),
                        'prix': vd.get('prix', 0)}

            p['controleur'] = controleur
            result.append(p)

        pompes = result

        conn.close()
        return jsonify({"succes": True, "pompes": pompes})

    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({"succes": False, "erreur": str(e)})


# ── 2. /get_panneaux_compatibles ──────────────────────────────

@app.route('/get_panneaux_compatibles', methods=['POST'])
@login_required
def get_panneaux_compatibles():
    try:
        data    = request.get_json()
        Pc_kWc  = float(data.get('Pc_kWc', 0))
        Usyst   = int(float(data.get('Usyst', 24)))
        # Puissance min par panneau : couvrir Pc avec ≤ 10 panneaux
        P_min_W = (Pc_kWc * 1000 / 10) if Pc_kWc > 0 else 0
        print(f"[get_panneaux_compatibles] Pc_kWc={Pc_kWc} Usyst={Usyst} P_min={P_min_W}W")

        if Usyst == 12:
            voc_cond = "AND Voc_V < 24"
        elif Usyst == 24:
            voc_cond = "AND Voc_V >= 24 AND Voc_V < 48"
        elif Usyst == 48:
            voc_cond = "AND Voc_V >= 48"
        else:
            voc_cond = ""

        conn = get_db()
        rows = conn.execute(
            f"""SELECT * FROM panneaux
               WHERE puissance_W >= ?
               {voc_cond}
               ORDER BY puissance_W ASC""",
            (P_min_W,)
        ).fetchall()
        panneaux = [dict(r) for r in rows]
        conn.close()
        print(f"[panneaux] Usyst={Usyst} voc_cond={voc_cond} nb={len(panneaux)}")
        return jsonify({"succes": True, "panneaux": panneaux})

    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({"succes": False, "erreur": str(e)})


# ── 3. /get_batteries_compatibles ─────────────────────────────

@app.route('/get_batteries_compatibles', methods=['POST'])
@login_required
def get_batteries_compatibles():
    try:
        data     = request.get_json()
        Ctot_Ah  = float(data.get('Ctot_Ah', 0))
        Usyst    = int(float(data.get('Usyst', 24)))
        print(f"[get_batteries_compatibles] Ctot_Ah={Ctot_Ah} Usyst={Usyst}")

        conn = get_db()
        rows = conn.execute(
            """SELECT * FROM batteries
               WHERE tension_V <= ?
               ORDER BY capacite_Ah ASC""",
            (Usyst,)
        ).fetchall()
        batteries = [dict(r) for r in rows]
        conn.close()
        print(f"[get_batteries_compatibles] {len(batteries)} batterie(s) trouvée(s)")
        return jsonify({"succes": True, "batteries": batteries})

    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({"succes": False, "erreur": str(e)})


# ── 4. /get_vfd ───────────────────────────────────────────────

@app.route('/get_vfd', methods=['POST'])
@login_required
def get_vfd():
    try:
        data        = request.get_json()
        Pm          = float(data.get('Pm', 0))
        type_sortie = data.get('type_sortie', 'mono')
        print(f"[get_vfd] Pm={Pm} type_sortie={type_sortie}")

        conn = get_db()
        rows = conn.execute(
            """SELECT id, modele, puissance_kW, courant_sortie_A,
                      type_sortie, prix
               FROM vfd
               WHERE type_sortie = ?
               AND intervalle_pompe_min_kW <= ?
               AND intervalle_pompe_max_kW >= ?
               ORDER BY puissance_kW ASC""",
            (type_sortie, Pm, Pm)
        ).fetchall()
        vfds = [dict(r) for r in rows]
        conn.close()
        print(f"[get_vfd] {len(vfds)} VFD trouvé(s)")
        return jsonify({"succes": True, "vfd": vfds})

    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({"succes": False, "erreur": str(e)})


# ── 5. /get_regulateurs ───────────────────────────────────────

@app.route('/get_regulateurs', methods=['POST'])
@login_required
def get_regulateurs():
    try:
        data  = request.get_json()
        Ireg  = float(data.get('Ireg', 0))
        Usyst = int(float(data.get('Usyst', 24)))
        print(f"[get_regulateurs] Ireg={Ireg} Usyst={Usyst}")

        conn = get_db()
        rows = conn.execute(
            """SELECT id, marque, modele, type,
                      courant_max_A, tension_systeme, plage_tension_pv
               FROM regulateurs_mppt
               WHERE courant_max_A >= ?
               AND tension_systeme LIKE ?
               ORDER BY courant_max_A ASC""",
            (Ireg, f'%{Usyst}%')
        ).fetchall()
        regulateurs = [dict(r) for r in rows]
        conn.close()
        print(f"[get_regulateurs] {len(regulateurs)} régulateur(s) trouvé(s)")
        return jsonify({"succes": True, "regulateurs": regulateurs})

    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({"succes": False, "erreur": str(e)})


# ── 6. /get_cables_protections ────────────────────────────────

@app.route('/get_cables_protections', methods=['POST'])
@login_required
def get_cables_protections():
    try:
        d = request.get_json()
        source      = d.get('source', 'solaire')
        type_pompe  = d.get('type_pompe', 'DC')      # DC | AC_mono | AC_tri | DC/AC
        Pm          = float(d.get('Pm', 0))
        Usyst       = float(d.get('Usyst', 24))
        Isc         = float(d.get('Isc', 0))
        Voc         = float(d.get('Voc', 0))
        Nbr_par     = int(float(d.get('Nbr_par', 1)))
        Nbr_ser     = int(float(d.get('Nbr_ser', 1)))
        Ireg        = float(d.get('Ireg', 0))
        Ivar        = float(d.get('Ivar', 0))
        Ia          = float(d.get('Ia', 0))
        L_pv_reg    = float(d.get('L_pv_reg', 0))
        L_reg_pompe = float(d.get('L_reg_pompe', 0))
        L_reg_bat   = float(d.get('L_reg_bat', 0))
        L_ac_pompe  = float(d.get('L_ac_pompe', 0))
        materiau    = d.get('materiau', 'cu')
        rho         = 0.0225 if materiau == 'cu' else 0.036

        print(f"[get_cables_protections] source={source} type_pompe={type_pompe} "
              f"Pm={Pm}kW Usyst={Usyst}V Ireg={Ireg}A Ivar={Ivar}A Ia={Ia}A")

        conn  = get_db()
        result = {'troncons': [], 'parafoudres': {}}
        has_pv = source in ('solaire', 'hybride_batteries', 'hybride_groupe')
        U_pv   = Voc * Nbr_ser if Nbr_ser > 0 else Voc
        I_pv   = Isc * Nbr_par if Nbr_par > 0 else Isc

        # ── Tronçon 1 : PV -> Régulateur (câble DC H1Z2Z2K) ──
        if has_pv and L_pv_reg > 0 and I_pv > 0 and U_pv > 0:
            S_calc  = _calc_section_dc(I_pv, L_pv_reg, U_pv, rho)
            S_norm  = _section_std(S_calc)
            In_calc = round(1.25 * I_pv, 1)
            In_norm = _calibre_std(In_calc)
            cable   = _find_cable_by_desig(conn, 'H1Z2Z2K', S_norm)
            disj    = _find_disj(conn, 'Disjoncteur DC', In_norm)
            result['troncons'].append({
                'troncon':      'PV -> Régulateur',
                'type':         'DC',
                'I_A':          round(I_pv, 2),
                'L_m':          L_pv_reg,
                'U_V':          round(U_pv, 1),
                'S_calculee':   round(S_calc, 2),
                'S_normalisee': S_norm,
                'In_calcule':   In_calc,
                'In_normalisee':In_norm,
                'cable':        cable,
                'disjoncteur':  disj,
            })
            print(f"  Tronçon PV->Reg : S={S_calc:.2f}->{S_norm}mm² In={In_calc}->{In_norm}A")

        # ── Tronçon 2 : Régulateur -> Batterie (câble DC souple) ─
        if source == 'hybride_batteries' and L_reg_bat > 0 and Ireg > 0:
            S_calc  = _calc_section_dc(Ireg, L_reg_bat, Usyst, rho)
            S_norm  = _section_std(S_calc)
            In_calc = round(1.25 * Ireg, 1)
            In_norm = _calibre_std(In_calc)
            cable   = _find_cable_by_desig(conn, 'souple rouge', S_norm)
            disj    = _find_disj(conn, 'Disjoncteur DC', In_norm)
            result['troncons'].append({
                'troncon':      'Régulateur -> Batterie',
                'type':         'DC',
                'I_A':          round(Ireg, 2),
                'L_m':          L_reg_bat,
                'U_V':          Usyst,
                'S_calculee':   round(S_calc, 2),
                'S_normalisee': S_norm,
                'In_calcule':   In_calc,
                'In_normalisee':In_norm,
                'cable':        cable,
                'disjoncteur':  disj,
            })
            print(f"  Tronçon Reg->Bat : S={S_calc:.2f}->{S_norm}mm² In={In_calc}->{In_norm}A")

        # ── Tronçon 3 : Régulateur -> Pompe DC ────────────────
        if type_pompe in ('DC', 'DC/AC') and L_reg_pompe > 0 and Ireg > 0 \
                and source not in ('groupe', 'groupe_electrogene', 'sbee', 'reseau'):
            S_calc  = _calc_section_reg_pompe(Ireg, L_reg_pompe, Usyst, rho)
            S_norm  = _section_std(S_calc)
            In_calc = round(1.25 * Ireg, 1)
            In_norm = _calibre_std(In_calc)
            cable   = _find_cable_by_desig(conn, 'souple rouge', S_norm)
            disj    = _find_disj(conn, 'Disjoncteur DC', In_norm)
            result['troncons'].append({
                'troncon':      'Régulateur -> Pompe DC',
                'type':         'DC',
                'I_A':          round(Ireg, 2),
                'L_m':          L_reg_pompe,
                'U_V':          Usyst,
                'S_calculee':   round(S_calc, 2),
                'S_normalisee': S_norm,
                'In_calcule':   In_calc,
                'In_normalisee':In_norm,
                'cable':        cable,
                'disjoncteur':  disj,
            })
            print(f"  Tronçon Reg->Pompe DC : S={S_calc:.2f}->{S_norm}mm² In={In_calc}->{In_norm}A")

        # ── Tronçon 4 : VFD / Source -> Pompe AC ──────────────
        I_ac = Ivar if Ivar > 0 else Ia
        if type_pompe in ('AC_mono', 'AC_tri', 'DC/AC') and L_ac_pompe > 0 and I_ac > 0 \
                and source not in ('groupe', 'groupe_electrogene', 'sbee', 'reseau'):
            is_tri  = type_pompe == 'AC_tri'
            U_ac    = 380.0 if is_tri else 220.0
            S_calc  = (_calc_section_ac_tri if is_tri else _calc_section_ac_mono)(I_ac, L_ac_pompe, U_ac, rho)
            S_norm  = _section_std(S_calc)
            In_calc = round(1.25 * I_ac, 1)
            In_norm = _calibre_std(In_calc)
            cat_ac  = 'Câble AC'
            cable   = _find_cable(conn, cat_ac, S_norm)
            disj    = _find_disj(conn, 'Disjoncteur AC', In_norm)
            result['troncons'].append({
                'troncon':      'VFD/Source -> Pompe AC',
                'type':         'AC_tri' if is_tri else 'AC_mono',
                'I_A':          round(I_ac, 2),
                'L_m':          L_ac_pompe,
                'U_V':          U_ac,
                'S_calculee':   round(S_calc, 2),
                'S_normalisee': S_norm,
                'In_calcule':   In_calc,
                'In_normalisee':In_norm,
                'cable':        cable,
                'disjoncteur':  disj,
            })
            print(f"  Tronçon VFD->Pompe AC : S={S_calc:.2f}->{S_norm}mm² In={In_calc}->{In_norm}A")

        # ── Tronçon 5 : Source AC -> Pompe (groupe/sbee/reseau) ─
        if source in ('groupe', 'groupe_electrogene', 'sbee', 'reseau') and L_ac_pompe > 0 and Ia > 0:
            is_tri  = Ia > 15          # heuristique : > 15A -> triphasé
            U_ac    = 380.0 if is_tri else 220.0
            S_calc  = (_calc_section_ac_tri if is_tri else _calc_section_ac_mono)(Ia, L_ac_pompe, U_ac, rho)
            S_norm  = _section_std(S_calc)
            In_calc = round(1.25 * Ia, 1)
            In_norm = _calibre_std(In_calc)
            cable   = _find_cable(conn, 'Câble AC', S_norm)
            disj    = _find_disj(conn, 'Disjoncteur AC', In_norm)
            result['troncons'].append({
                'troncon':      'Source AC -> Pompe',
                'type':         'AC_tri' if is_tri else 'AC_mono',
                'I_A':          round(Ia, 2),
                'L_m':          L_ac_pompe,
                'U_V':          U_ac,
                'S_calculee':   round(S_calc, 2),
                'S_normalisee': S_norm,
                'In_calcule':   In_calc,
                'In_normalisee':In_norm,
                'cable':        cable,
                'disjoncteur':  disj,
            })
            print(f"  Tronçon Source AC->Pompe : S={S_calc:.2f}->{S_norm}mm² In={In_calc}->{In_norm}A")

        # ── Parafoudres recommandés ───────────────────────────
        if has_pv:
            result['parafoudres']['DC'] = _find_para(conn, 'DC')
        if type_pompe in ('AC_mono', 'AC_tri') or source in ('groupe', 'sbee', 'reseau'):
            result['parafoudres']['AC'] = _find_para(conn, 'AC')

        conn.close()
        result['succes'] = True
        print(f"[get_cables_protections] {len(result['troncons'])} tronçon(s) calculé(s)")
        return jsonify(result)

    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({"succes": False, "erreur": str(e)})


# ============================================================
# GÉNÉRATION PDF v2 (nouveau flux dimensionnement2)
# ============================================================

@app.route('/generer_pdf2', methods=['POST'])
@login_required
def generer_pdf2():
    try:
        calcul = session.get('calcul_resultats', {})
        equip  = session.get('equipements_resultats', {})
        data   = request.get_json() or {}

        data_brut = calcul.get('data_brut', {}) or {}

        pdf_data = {
            # Infos rapport
            'nom_projet':  data.get('nom_projet',  session.get('nom_projet', 'Non renseigné')),
            'nom_client':  data.get('nom_client',  'Non renseigné'),
            'realise_par': data.get('realise_par', 'Non renseigné'),
            'date_projet': data.get('date_projet', ''),
            # Localisation
            'lat': calcul.get('lat', ''),
            'lon': calcul.get('lon', ''),
            # Climatique
            'irradiation':     calcul.get('irradiation', 0),
            'ET0':             data_brut.get('ET0', 0),
            'ET0_max':         data_brut.get('ET0', 0),
            'mois_critique':   data_brut.get('mois_critique', ''),
            'temperature_max': data_brut.get('temperature_max', ''),
            'temperature_min': data_brut.get('temperature_min', ''),
            # Besoins
            'besoins': calcul.get('besoins', {}),
            # Hydraulique
            'hydraulique': {
                'debit_m3_h':      calcul.get('Q', 0),
                'hauteur_geo_m':   calcul.get('Hgeo', 0),
                'pertes_charge_m': calcul.get('Pc_pertes', 0),
                'HMT_m':           calcul.get('HMT', 0),
            },
            # Pompe
            'pompe': {
                'Ph_kW':             calcul.get('Ph', 0),
                'Pp_kW':             calcul.get('Pp', 0),
                'Pm_kW':             calcul.get('Pm', 0),
                'Pm_commercial_kW':  calcul.get('Pm_commercial', 0),
                'Ia_A':              calcul.get('Ia', 0),
                'type_alimentation': calcul.get('type_reseau', ''),
            },
            # Source
            'source_energie': calcul.get('source_energie', ''),
            'heures_pompage': calcul.get('heures_pompage', 0),
            # Énergie
            'energie': {
                'energie_jour_kWh':         calcul.get('Eelec', 0),
                'puissance_crete_kWp':      calcul.get('Pc_kWc', 0),
                'U_syst':                   calcul.get('Usyst', 0),
                'puissance_groupe_kW':      calcul.get('Pgroupe', 0),
                'consommation_jour_litres': calcul.get('conso_jour', 0),
                'consommation_mois_litres': calcul.get('conso_mois', 0),
                'puissance_souscrite_kW':   calcul.get('Ps', 0),
                'type_reseau':              calcul.get('type_reseau', ''),
            },
            # Configuration PV
            'nbr_panneaux':     equip.get('nbr_panneaux', 0),
            'nbr_pv_serie':     equip.get('nbr_pv_serie', 0),
            'nbr_pv_parallele': equip.get('nbr_pv_parallele', 0),
            # Configuration batteries
            'jours_autonomie': equip.get('jours_autonomie', 0),
            'ctot':            equip.get('ctot', 0),
            'nbat_serie':      equip.get('nbat_serie', 0),
            'nbat_par':        equip.get('nbat_par', 0),
            'nbat_tot':        equip.get('nbat_tot', 0),
            # Équipements (nouveau format)
            'equipements': {
                'pompe':      equip.get('pompe', {}),
                'controleur': equip.get('controleur', {}),
                'type_ctrl':  equip.get('type_ctrl', ''),
                'mode_alim':  equip.get('mode_alim', ''),
                'panneau':    equip.get('panneau', {}),
                'batterie':   equip.get('batterie', {}),
            },
            # Câbles et protections
            'cables_resultats': equip.get('cables_resultats', []),
            'parafoudres':      equip.get('parafoudres', {}),
            # Coûts
            'cout': equip.get('cout', {}),
        }

        print(f"[generer_pdf2] source={pdf_data['source_energie']} "
              f"Q={pdf_data['hydraulique']['debit_m3_h']} "
              f"cout={pdf_data.get('cout', {}).get('C_total', 0)} FCFA")

        gen = charger_module('generateur_pdf', os.path.join(dossier, 'generateur_pdf.py'))
        buffer = gen.generer_rapport(pdf_data)
        buffer.seek(0)
        nom = pdf_data['nom_projet'].replace(' ', '_') or 'rapport'
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f'rapport_hydropump_{nom}.pdf',
            mimetype='application/pdf'
        )
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({'succes': False, 'erreur': str(e)}), 500


# ============================================================
# LANCEMENT
# ============================================================

if __name__ == '__main__':
    app.run(debug=True)