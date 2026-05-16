# ============================================================
# DATABASE.PY — GESTION BASE DE DONNÉES SQLITE
# ============================================================

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'solarpump.db')
EXCEL_PATH = r"D:\Pompage\DATA_BASE_Merv.xlsx"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # TABLE UTILISATEURS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS utilisateurs (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            nom           TEXT NOT NULL,
            email         TEXT NOT NULL UNIQUE,
            mot_de_passe  TEXT NOT NULL,
            organisation  TEXT,
            date_creation TEXT DEFAULT (datetime('now'))
        )
    ''')

    # TABLE PROJETS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projets (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id      INTEGER NOT NULL,
            nom_projet   TEXT NOT NULL,
            realise_par  TEXT,
            date_projet  TEXT,
            mode         TEXT,
            source_energie TEXT,
            lat          TEXT,
            lon          TEXT,
            resultats    TEXT,
            date_creation TEXT DEFAULT (datetime('now')),
            date_modif    TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES utilisateurs(id)
        )
    ''')

    # TABLES ÉQUIPEMENTS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pompes (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            marque          TEXT,
            modele          TEXT,
            type_pompe      TEXT,
            type_installation TEXT,
            debit_max_m3h   REAL,
            HMT_max_m       REAL,
            puissance_kW    REAL,
            tension_V       TEXT,
            rendement       REAL,
            alimentation    TEXT,
            source_energie  TEXT,
            description     TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS panneaux_solaires (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            marque          TEXT,
            type            TEXT,
            puissance_W     REAL,
            tension_V       REAL,
            Vmp_V           REAL,
            Imp_A           REAL,
            Voc_V           REAL,
            Isc_A           REAL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS batteries (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            marque          TEXT,
            technologie     TEXT,
            capacite_Ah     REAL,
            tension_V       REAL,
            rendement       REAL,
            temps_decharge_h REAL,
            dod             REAL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS disjoncteurs (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            marque          TEXT,
            modele          TEXT,
            type            TEXT,
            calibre_A       REAL,
            tension_V       REAL,
            pouvoir_coupure REAL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fusibles_dc (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            marque          TEXT,
            type            TEXT,
            modele          TEXT,
            calibre_A       REAL,
            tension_V       REAL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parafoudres (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            marque          TEXT,
            modele          TEXT,
            type_protection TEXT,
            tension_V       REAL,
            courant_kA      REAL,
            niveau_up_kV    REAL
        )
    ''')

    conn.commit()
    conn.close()
    print("[OK] Base de donnees initialisee.")
    _importer_equipements_si_vide()


# ============================================================
# IMPORT ÉQUIPEMENTS DEPUIS EXCEL
# ============================================================

def _source_energie_from_alimentation(alimentation):
    if alimentation is None:
        return '["solaire","hybride_batteries","groupe","reseau"]'
    al = str(alimentation).strip().upper()
    if al == 'DC':
        return '["solaire","hybride_batteries"]'
    if al == 'AC':
        return '["groupe","reseau"]'
    return '["solaire","hybride_batteries","groupe","reseau"]'


def _type_installation_from_pompe(type_pompe, alimentation):
    if type_pompe is None:
        return 'submersible'
    tp = str(type_pompe).lower()
    if 'surface' in tp or 'aspiration' in tp:
        return 'surface'
    return 'submersible'


def importer_equipements_excel(excel_path=None):
    if excel_path is None:
        excel_path = EXCEL_PATH
    try:
        import openpyxl
    except ImportError:
        print("[WARN] openpyxl non installe - equipements non importes.")
        return

    if not os.path.exists(excel_path):
        print(f"[WARN] Fichier Excel introuvable : {excel_path}")
        return

    wb = openpyxl.load_workbook(excel_path)
    conn = get_db()
    c = conn.cursor()

    def first_data_row(ws):
        rows = list(ws.iter_rows(values_only=True))
        for i, row in enumerate(rows):
            if any(v is not None for v in row):
                return i + 1, rows
        return 1, rows

    # ─── POMPES ───
    c.execute('DELETE FROM pompes')
    ws = wb['Pompes']
    start, rows = first_data_row(ws)
    for row in rows[start:]:
        vals = [v for v in row if v is not None or True]
        # cols offset 2 (two leading None cols)
        r = [v for v in row]
        if len(r) < 11 or all(v is None for v in r):
            continue
        marque = r[2]; modele = r[3]; type_pompe = r[4]
        debit = r[5]; hmt = r[6]; puiss = r[7]
        tension = r[8]; rend = r[9]; alim = r[10]
        if marque is None:
            continue
        rend_float = float(rend) / 100 if rend else 0.65
        c.execute('''INSERT INTO pompes
            (marque,modele,type_pompe,type_installation,debit_max_m3h,HMT_max_m,
             puissance_kW,tension_V,rendement,alimentation,source_energie,description)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''', (
            str(marque), str(modele) if modele else '',
            str(type_pompe) if type_pompe else '',
            _type_installation_from_pompe(type_pompe, alim),
            float(debit) if debit else 0,
            float(hmt) if hmt else 0,
            float(puiss) if puiss else 0,
            str(tension) if tension else '',
            rend_float,
            str(alim) if alim else '',
            _source_energie_from_alimentation(alim),
            ''
        ))

    # ─── PANNEAUX SOLAIRES ───
    c.execute('DELETE FROM panneaux_solaires')
    ws = wb['Panneaux solaires']
    start, rows = first_data_row(ws)
    for row in rows[start:]:
        r = list(row)
        if len(r) < 10 or all(v is None for v in r):
            continue
        marque = r[2]; typ = r[3]; puiss = r[4]; tension = r[5]
        vmp = r[6]; imp = r[7]; voc = r[8]; isc = r[9]
        if marque is None:
            continue
        c.execute('''INSERT INTO panneaux_solaires
            (marque,type,puissance_W,tension_V,Vmp_V,Imp_A,Voc_V,Isc_A)
            VALUES (?,?,?,?,?,?,?,?)''', (
            str(marque), str(typ) if typ else '',
            float(puiss) if puiss else 0, float(tension) if tension else 0,
            float(vmp) if vmp else 0, float(imp) if imp else 0,
            float(voc) if voc else 0, float(isc) if isc else 0
        ))

    # ─── BATTERIES ───
    c.execute('DELETE FROM batteries')
    try:
        ws = wb['Battéries']
    except KeyError:
        ws = wb.get('Batt\xe9ries') or wb.get('Battéries')
    if ws:
        start, rows = first_data_row(ws)
        for row in rows[start:]:
            r = list(row)
            if len(r) < 10 or all(v is None for v in r):
                continue
            marque = r[2]; techno = r[3]; capa = r[4]
            tension = r[5]; rend = r[6]; tdec = r[7]; dod = r[8]
            if marque is None:
                continue
            rend_f = float(rend) / 100 if rend and float(rend) > 1 else float(rend) if rend else 0.8
            dod_f = float(dod) / 100 if dod and float(dod) > 1 else float(dod) if dod else 0.8
            c.execute('''INSERT INTO batteries
                (marque,technologie,capacite_Ah,tension_V,rendement,temps_decharge_h,dod)
                VALUES (?,?,?,?,?,?,?)''', (
                str(marque), str(techno) if techno else '',
                float(capa) if capa else 0, float(tension) if tension else 0,
                rend_f, float(tdec) if tdec else 0, dod_f
            ))

    # ─── DISJONCTEURS ───
    c.execute('DELETE FROM disjoncteurs')
    try:
        ws = wb['Disjoncteurs ']
    except KeyError:
        ws = None
    if ws:
        start, rows = first_data_row(ws)
        for row in rows[start:]:
            r = list(row)
            # cols start at index 20
            offset = next((i for i, v in enumerate(r) if v is not None and str(v).strip() not in ('', 'None')), None)
            if offset is None:
                continue
            vals = [v for v in r if v is not None]
            if len(vals) < 6:
                continue
            marque, modele, typ, calibre, tension, pouvoir = vals[0], vals[1], vals[2], vals[3], vals[4], vals[5]
            if marque is None:
                continue
            c.execute('''INSERT INTO disjoncteurs
                (marque,modele,type,calibre_A,tension_V,pouvoir_coupure)
                VALUES (?,?,?,?,?,?)''', (
                str(marque), str(modele) if modele else '',
                str(typ) if typ else '',
                float(calibre) if calibre else 0,
                float(tension) if tension else 0,
                float(pouvoir) if pouvoir else 0
            ))

    # ─── FUSIBLES DC ───
    c.execute('DELETE FROM fusibles_dc')
    try:
        ws = wb['Fusibles DC']
    except KeyError:
        ws = None
    if ws:
        start, rows = first_data_row(ws)
        for row in rows[start:]:
            r = list(row)
            if len(r) < 7 or all(v is None for v in r):
                continue
            marque = r[2]; typ = r[3]; modele = r[4]; calibre = r[5]; tension = r[6]
            if marque is None:
                continue
            c.execute('''INSERT INTO fusibles_dc
                (marque,type,modele,calibre_A,tension_V)
                VALUES (?,?,?,?,?)''', (
                str(marque), str(typ) if typ else '',
                str(modele) if modele else '',
                float(calibre) if calibre else 0,
                float(tension) if tension else 0
            ))

    # ─── PARAFOUDRES ───
    c.execute('DELETE FROM parafoudres')
    try:
        ws = wb['Parafoudre']
    except KeyError:
        ws = None
    if ws:
        start, rows = first_data_row(ws)
        for row in rows[start:]:
            r = list(row)
            if len(r) < 7 or all(v is None for v in r):
                continue
            marque = r[1]; modele = r[2]; typ = r[3]; tension = r[4]; courant = r[5]; up = r[6]
            if marque is None:
                continue
            c.execute('''INSERT INTO parafoudres
                (marque,modele,type_protection,tension_V,courant_kA,niveau_up_kV)
                VALUES (?,?,?,?,?,?)''', (
                str(marque), str(modele) if modele else '',
                str(typ) if typ else '',
                float(tension) if tension else 0,
                float(courant) if courant else 0,
                float(up) if up else 0
            ))

    conn.commit()
    conn.close()
    print("[OK] Equipements importes depuis Excel.")


def _importer_equipements_si_vide():
    conn = get_db()
    count = conn.execute('SELECT COUNT(*) FROM pompes').fetchone()[0]
    conn.close()
    if count == 0:
        importer_equipements_excel()


# ============================================================
# REQUÊTES ÉQUIPEMENTS — POMPES
# ============================================================

def db_get_marques_pompes():
    conn = get_db()
    rows = conn.execute('SELECT DISTINCT marque FROM pompes ORDER BY marque').fetchall()
    conn.close()
    return [r[0] for r in rows]


def db_get_modeles_pompes(marque):
    conn = get_db()
    rows = conn.execute(
        '''SELECT modele,debit_max_m3h,HMT_max_m,puissance_kW,tension_V,
                  type_installation,source_energie
           FROM pompes WHERE marque=? ORDER BY debit_max_m3h''',
        (marque,)
    ).fetchall()
    conn.close()
    import json
    result = []
    for r in rows:
        try:
            src = json.loads(r[6]) if r[6] else []
        except Exception:
            src = []
        result.append({
            'modele': r[0], 'debit_max_m3h': r[1], 'HMT_max_m': r[2],
            'puissance_kW': r[3], 'tension_V': r[4],
            'type_installation': r[5], 'source_energie': src,
        })
    return result


def db_get_caracteristiques_pompe(marque, modele):
    conn = get_db()
    r = conn.execute(
        'SELECT * FROM pompes WHERE marque=? AND modele=?', (marque, modele)
    ).fetchone()
    conn.close()
    if not r:
        return None
    import json
    try:
        src = json.loads(r['source_energie']) if r['source_energie'] else []
    except Exception:
        src = []
    return {
        'marque': r['marque'], 'modele': r['modele'],
        'type_pompe': r['type_pompe'], 'type_installation': r['type_installation'],
        'debit_max_m3h': r['debit_max_m3h'], 'HMT_max_m': r['HMT_max_m'],
        'puissance_kW': r['puissance_kW'], 'tension_V': r['tension_V'],
        'rendement': r['rendement'], 'source_energie': src,
        'description': r['description'] or '',
    }


def db_selectionner_pompes(debit_m3_h, HMT_m, source_energie, marque_choisie='toutes'):
    conn = get_db()
    rows = conn.execute(
        'SELECT * FROM pompes WHERE debit_max_m3h>=? AND HMT_max_m>=? ORDER BY puissance_kW',
        (debit_m3_h * 0.9, HMT_m * 0.9)
    ).fetchall()
    conn.close()
    import json
    result = []
    for r in rows:
        try:
            src = json.loads(r['source_energie']) if r['source_energie'] else []
        except Exception:
            src = []
        if source_energie and source_energie not in src:
            continue
        if marque_choisie and marque_choisie != 'toutes' and r['marque'] != marque_choisie:
            continue
        result.append({
            'marque': r['marque'], 'modele': r['modele'],
            'type_pompe': r['type_pompe'], 'type_installation': r['type_installation'],
            'debit_max_m3h': r['debit_max_m3h'], 'HMT_max_m': r['HMT_max_m'],
            'puissance_kW': r['puissance_kW'], 'tension_V': r['tension_V'],
            'rendement': r['rendement'], 'source_energie': src,
            'description': r['description'] or '',
        })
    return result[:5]


# ============================================================
# UTILISATEURS
# ============================================================

def creer_utilisateur(nom, email, mot_de_passe_hash, organisation=''):
    conn = get_db()
    try:
        conn.execute(
            'INSERT INTO utilisateurs (nom, email, mot_de_passe, organisation) VALUES (?, ?, ?, ?)',
            (nom, email, mot_de_passe_hash, organisation)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def get_utilisateur_par_email(email):
    conn = get_db()
    user = conn.execute(
        'SELECT * FROM utilisateurs WHERE email = ?', (email,)
    ).fetchone()
    conn.close()
    return user


def get_utilisateur_par_id(user_id):
    conn = get_db()
    user = conn.execute(
        'SELECT * FROM utilisateurs WHERE id = ?', (user_id,)
    ).fetchone()
    conn.close()
    return user


# ============================================================
# PROJETS
# ============================================================

def sauvegarder_projet(user_id, nom_projet, realise_par, date_projet,
                        mode, source_energie, lat, lon, resultats_json):
    conn = get_db()
    cursor = conn.execute(
        '''INSERT INTO projets
           (user_id, nom_projet, realise_par, date_projet, mode, source_energie, lat, lon, resultats)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (user_id, nom_projet, realise_par, date_projet,
         mode, source_energie, lat, lon, resultats_json)
    )
    projet_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return projet_id


def mettre_a_jour_projet(projet_id, user_id, resultats_json):
    conn = get_db()
    conn.execute(
        '''UPDATE projets SET resultats = ?, date_modif = datetime('now')
           WHERE id = ? AND user_id = ?''',
        (resultats_json, projet_id, user_id)
    )
    conn.commit()
    conn.close()


def get_projets_utilisateur(user_id):
    conn = get_db()
    projets = conn.execute(
        '''SELECT id, nom_projet, realise_par, date_projet, mode,
                  source_energie, lat, lon, date_creation, date_modif
           FROM projets WHERE user_id = ?
           ORDER BY date_modif DESC''',
        (user_id,)
    ).fetchall()
    conn.close()
    return projets

def get_projet_par_id(projet_id, user_id):
    conn = get_db()
    projet = conn.execute(
        'SELECT * FROM projets WHERE id = ? AND user_id = ?',
        (projet_id, user_id)
    ).fetchone()
    conn.close()
    return projet


def supprimer_projet(projet_id, user_id):
    conn = get_db()
    conn.execute(
        'DELETE FROM projets WHERE id = ? AND user_id = ?',
        (projet_id, user_id)
    )
    conn.commit()
    conn.close()


# Initialisation automatique au démarrage
init_db()