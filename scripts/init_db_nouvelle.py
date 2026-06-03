#!/usr/bin/env python3
"""
scripts/init_db_nouvelle.py
Lit Equipements_nouveaux.xlsx (Feuil2) -> recree 9 tables equipements
dans solarpump.db sans toucher a utilisateurs / projets.

Usage : python scripts/init_db_nouvelle.py [--debug]

Structure Excel detectee (Feuil2) :
  Row  0 : Pompes (titre)
  Row  1 : en-tetes pompes (7 cols)
  Row 55 : Variateurs AC monophase (titre VFD mono)
  Row 56 : en-tetes VFD
  Row 66 : Variateur AC triphase (titre VFD tri  - accumule dans vfd)
  Row 90 : Regulateur MPPT
  Row 148: Panneaux solaires
  Row 186: Batteries
  Row 288: Section de cables et protections  (cables+disj+para+fusi)
"""

import os, sys, re, sqlite3, unicodedata
import pandas as pd
import numpy as np

BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH   = os.path.join(BASE_DIR, "solarpump.db")
XLSX_PATH = next(
    (os.path.join(BASE_DIR, n) for n in [
        "Equipements_nouveaux.xlsx",
        "Equipements nouveaux.xlsx",
    ] if os.path.exists(os.path.join(BASE_DIR, n))),
    os.path.join(BASE_DIR, "Equipements_nouveaux.xlsx")
)
DEBUG = '--debug' in sys.argv

# ═══════════════════════════════════════════════════════════════ helpers ═════

def sf(v):
    if v is None or (isinstance(v, float) and np.isnan(v)): return None
    try: return float(str(v).strip().replace(',', '.').replace('\xa0', '').replace(' ', ''))
    except: return None

def si(v, d=0):
    f = sf(v); return int(round(f)) if f is not None else d

def ss(v):
    if v is None or (isinstance(v, float) and np.isnan(v)): return ''
    return str(v).strip()

def nrm(s):
    """Normalise : minuscules, sans accents, non-alphanum -> _"""
    s = unicodedata.normalize('NFKD', ss(s))
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+', '_', s.lower()).strip('_')

def alimentation(t_str):
    t = ss(t_str).upper().replace('\xd7', 'X').replace('x', 'X')
    dc = 'DC' in t
    if dc and ('AC' in t or '220' in t or '380' in t): return 'DC/AC'
    if dc: return 'DC'
    if '1X220' in t: return 'AC_mono'
    if '3X380' in t: return 'AC_tri'
    if '220' in t and '380' in t: return 'AC'
    return 'AC'

def dod_from_techno(techno):
    return 0.80 if 'lithium' in ss(techno).lower() else 0.50

def parse_interval(v):
    """'0.25-0.37' ou '0.25x0.37' -> (0.25, 0.37)"""
    s = ss(v).replace('–', '-').replace('—', '-').replace('−', '-')
    m = re.match(r'([\d.,]+)\s*[-]\s*([\d.,]+)', s.strip())
    if m: return sf(m.group(1)), sf(m.group(2))
    f = sf(v); return f, f

# ═══════════════════════════════════════════════════════ chargement Excel ════

def load_sheet():
    if not os.path.exists(XLSX_PATH):
        sys.exit(f"[ERREUR] Fichier introuvable : {XLSX_PATH}")
    df = pd.read_excel(XLSX_PATH, sheet_name='Feuil2', header=None, dtype=str)
    return df.fillna('')

def row_ne(row):
    """Nombre de cellules non-vides."""
    return sum(1 for v in row if ss(v) != '')

def row_nrm(row):
    return nrm(' '.join(ss(v) for v in row))

# ═══════════════════════════════════════════════════════ detection sections ══

# Mots-cles pour identifier les lignes-titres (ne <= 2)
TITLE_KW = {
    'pompes':      ['pompe'],
    'vfd':         ['variateur', 'vfd'],
    'regulateurs': ['regulateur', 'mppt', 'pwm', 'regulat'],
    'panneaux':    ['panneau', 'solaire', 'module_solaire'],
    'batteries':   ['batterie', 'battery'],
    'protection':  ['cable', 'cables_et', 'section_de'],
}

def detect_title(row):
    """Retourne le nom de section si la ligne est un titre (1-2 cellules non-vides)."""
    ne = row_ne(row)
    if ne == 0 or ne > 2:
        return None
    rt = row_nrm(row)
    for sect, kws in TITLE_KW.items():
        if any(kw in rt for kw in kws):
            return sect
    return None

def is_header_row(row):
    """True si la ligne ressemble a un en-tete (>= 3 cellules, aucune numerique)."""
    ne = row_ne(row)
    if ne < 3: return False
    return all(sf(ss(v)) is None for v in row if ss(v) != '')

def extract_sections(df):
    """
    Parcourt le sheet, detecte les sections et accumule leurs lignes de donnees.
    Retourne dict: section_name -> [lignes de donnees].
    Les sous-sections VFD (mono + tri) sont accumulees dans 'vfd'.
    """
    n = len(df)
    sections = {}
    i = 0

    while i < n:
        row = list(df.iloc[i])
        sect = detect_title(row)

        if sect is not None:
            if DEBUG:
                print(f"  [titre] '{sect}' ligne {i}: {[ss(v) for v in row if ss(v)]}")

            # Trouver la ligne d'en-tetes (premiere ligne non-vide apres le titre)
            j = i + 1
            while j < n and row_ne(list(df.iloc[j])) == 0:
                j += 1
            if j >= n:
                i += 1
                continue

            # Collecter les lignes de donnees
            k = j + 1
            empty_streak = 0
            data_rows = []

            while k < n:
                dr = list(df.iloc[k])
                ne = row_ne(dr)

                if ne == 0:
                    empty_streak += 1
                    if empty_streak >= 2:
                        break
                    k += 1
                    continue

                empty_streak = 0

                # Arreter si nouvelle section detectee
                if detect_title(dr) is not None:
                    break

                # Ignorer les lignes d'en-tetes internes (ex : row 75 "VDF, Puissance...")
                if is_header_row(dr):
                    if DEBUG:
                        print(f"    [skip en-tete interne] ligne {k}: {[ss(v) for v in dr if ss(v)][:4]}")
                    k += 1
                    continue

                data_rows.append(dr)
                k += 1

            # Accumulation (VFD mono + tri vont dans 'vfd')
            if sect not in sections:
                sections[sect] = []
            sections[sect].extend(data_rows)

            if DEBUG:
                print(f"    -> {len(data_rows)} lignes ajoutees a '{sect}' (total: {len(sections[sect])})")

            i = k
        else:
            i += 1

    return sections

# ═══════════════════════════════════════════════════════ parsers positionnels ═

def parse_pompes(rows):
    # Col 0 vide (decalage Excel). Cols: 1=Marque 2=Modele 3=Type 4=Debit 5=HMT 6=Puissance 7=Tension
    out = []
    for r in rows:
        marque  = ss(r[1]) if len(r) > 1 else ''
        modele  = ss(r[2]) if len(r) > 2 else ''
        if not marque and not modele:
            continue
        type_p  = ss(r[3]) if len(r) > 3 else ''
        debit   = sf(r[4]) if len(r) > 4 else None
        hmt     = sf(r[5]) if len(r) > 5 else None
        puiss   = sf(r[6]) if len(r) > 6 else None
        tension = ss(r[7]) if len(r) > 7 else ''
        out.append((marque, modele, type_p, debit, hmt, puiss, tension, alimentation(tension)))
    return out


def parse_vfd(rows):
    # Col 0 vide. Cols: 1=Modele 2=kW 3=HP 4=I_entree 5=I_sortie 6=Intervalle 7=Prix
    out = []
    for r in rows:
        modele = ss(r[1]) if len(r) > 1 else ''
        if not modele:
            continue
        norm_m = nrm(modele)
        if norm_m in ('modele_vdf', 'vdf', 'modele', 'mod_le_vdf', 'mod_le'):
            continue
        if sf(modele) is not None:   # cellule numerique = mauvaise ligne
            continue
        p_kw   = sf(r[2]) if len(r) > 2 else None
        p_hp   = sf(r[3]) if len(r) > 3 else None
        i_in   = sf(r[4]) if len(r) > 4 else None
        i_out  = sf(r[5]) if len(r) > 5 else None
        interv = ss(r[6]) if len(r) > 6 else ''
        prix   = si(r[7]) if len(r) > 7 else 0
        mn, mx = parse_interval(interv)
        type_sortie = 'tri' if 'T2' in modele.upper() else 'mono'
        out.append((modele, p_kw, p_hp, i_in, i_out, mn, mx, type_sortie, prix))
    return out


def parse_regulateurs(rows):
    # Col 0 vide. Cols: 1=Marque 2=Modele 3=Type 4=Courant_max 5=Tension_sys 6=Plage_PV
    out = []
    for r in rows:
        marque = ss(r[1]) if len(r) > 1 else ''
        modele = ss(r[2]) if len(r) > 2 else ''
        if not marque and not modele:
            continue
        type_r = ss(r[3]) if len(r) > 3 else ''
        i_max  = sf(r[4]) if len(r) > 4 else None
        t_sys  = ss(r[5]) if len(r) > 5 else ''
        plage  = ss(r[6]) if len(r) > 6 else ''
        out.append((marque, modele, type_r, i_max, t_sys, plage))
    return out


def parse_panneaux(rows):
    # Col 0 vide. Cols: 1=Marque 2=Modele 3=Type 4=P(Wc) 5=Tension_nom
    #                   6=Voc 7=Isc 8=Vmp 9=Imp 10=Rendement(%)
    out = []
    for r in rows:
        marque = ss(r[1])  if len(r) > 1  else ''
        modele = ss(r[2])  if len(r) > 2  else ''
        if not marque and not modele:
            continue
        type_p = ss(r[3])  if len(r) > 3  else ''
        p_w    = sf(r[4])  if len(r) > 4  else None
        t_v    = sf(r[5])  if len(r) > 5  else None
        voc    = sf(r[6])  if len(r) > 6  else None
        isc    = sf(r[7])  if len(r) > 7  else None
        vmp    = sf(r[8])  if len(r) > 8  else None
        imp    = sf(r[9])  if len(r) > 9  else None
        rend_r = sf(r[10]) if len(r) > 10 else None
        prix   = si(r[11]) if len(r) > 11 else 0
        rend   = (rend_r / 100.0) if (rend_r is not None and rend_r > 1) else rend_r
        out.append((marque, modele, type_p, p_w, t_v, voc, isc, vmp, imp, rend, prix))
    return out


def parse_batteries(rows):
    # Col 0 vide. Cols: 1=Marque 2=Techno 3=Capacite(Ah) 4=Tension 5=Rendement 6=Temps 7=DoD(ignore)
    out = []
    for r in rows:
        marque  = ss(r[1]) if len(r) > 1 else ''
        techno  = ss(r[2]) if len(r) > 2 else ''
        cap     = sf(r[3]) if len(r) > 3 else None
        tension = sf(r[4]) if len(r) > 4 else None
        rend_r  = sf(r[5]) if len(r) > 5 else None
        temps   = sf(r[6]) if len(r) > 6 else None
        # col 7 = DoD fichier -> ignore, recalcule depuis technologie
        if cap is None or cap < 10:
            continue                    # ligne vide ou corrompue (ex: cap=2)
        if not marque and not techno:
            continue
        rend = (rend_r / 100.0) if (rend_r is not None and rend_r > 1) else rend_r
        dod  = dod_from_techno(techno)
        out.append((marque, techno, cap, tension, rend, temps, dod, 0))
    return out


def parse_protections(rows):
    """
    Col 0 vide. Cols: 1=Designation 2=Categorie 3=Calibre/Section 4=Unite 5=Prix
    Split par categorie -> cables / disjoncteurs / parafoudres / fusibles.
    """
    cables, disj, para, fusi = [], [], [], []
    for r in rows:
        desig   = ss(r[1]) if len(r) > 1 else ''
        cat_raw = ss(r[2]) if len(r) > 2 else ''
        calibre = ss(r[3]) if len(r) > 3 else ''
        unite   = ss(r[4]) if len(r) > 4 else ''
        prix    = si(r[5]) if len(r) > 5 else 0
        if not desig:
            continue
        cat = nrm(cat_raw)
        rec = (desig, cat_raw, calibre, unite, prix)
        if 'cable' in cat:
            cables.append(rec)
        elif 'disjoncteur' in cat or 'differentiel' in cat:
            disj.append(rec)
        elif 'parafoudre' in cat:
            para.append(rec)
        else:
            fusi.append(rec)   # fusible NH, porte-fusible, fusible gPV
    return cables, disj, para, fusi

# ═══════════════════════════════════════════════════════════════ SQL DDL ═════

DDL = {
    'pompes': """
        CREATE TABLE pompes (
            id                INTEGER PRIMARY KEY AUTOINCREMENT,
            marque            TEXT, modele TEXT, type_pompe TEXT,
            debit_max_m3h     REAL, HMT_max_m REAL, puissance_kW REAL,
            tension_V         TEXT, type_alimentation TEXT,
            rendement         REAL DEFAULT 0.65,
            prix              INTEGER DEFAULT 0,
            description       TEXT DEFAULT ''
        )""",
    'vfd': """
        CREATE TABLE vfd (
            id                      INTEGER PRIMARY KEY AUTOINCREMENT,
            modele                  TEXT, puissance_kW REAL, puissance_HP REAL,
            courant_entree_A        REAL, courant_sortie_A REAL,
            intervalle_pompe_min_kW REAL, intervalle_pompe_max_kW REAL,
            type_sortie             TEXT, prix INTEGER
        )""",
    'regulateurs_mppt': """
        CREATE TABLE regulateurs_mppt (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            marque           TEXT, modele TEXT, type TEXT,
            courant_max_A    REAL, tension_systeme TEXT, plage_tension_pv TEXT
        )""",
    'panneaux': """
        CREATE TABLE panneaux (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            marque      TEXT, modele TEXT, type TEXT,
            puissance_W REAL, tension_V REAL,
            Voc_V REAL, Isc_A REAL, Vmp_V REAL, Imp_A REAL,
            rendement   REAL, prix INTEGER DEFAULT 0
        )""",
    'batteries': """
        CREATE TABLE batteries (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            marque           TEXT, technologie TEXT,
            capacite_Ah      REAL, tension_V REAL,
            rendement        REAL, temps_decharge_h REAL,
            dod              REAL, prix INTEGER DEFAULT 0
        )""",
    'cables': """
        CREATE TABLE cables (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            designation     TEXT, categorie TEXT,
            calibre_section TEXT, unite TEXT, prix INTEGER
        )""",
    'disjoncteurs': """
        CREATE TABLE disjoncteurs (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            designation TEXT, categorie TEXT,
            calibre     TEXT, unite TEXT, prix INTEGER
        )""",
    'parafoudres': """
        CREATE TABLE parafoudres (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            designation TEXT, categorie TEXT,
            calibre     TEXT, unite TEXT, prix INTEGER
        )""",
    'fusibles': """
        CREATE TABLE fusibles (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            designation TEXT, categorie TEXT,
            calibre     TEXT, unite TEXT, prix INTEGER
        )""",
}

PROTECTED = {'utilisateurs', 'projets', 'progressions'}

# ═══════════════════════════════════════════════════════════════ main ════════

def main():
    print("=" * 60)
    print("init_db_nouvelle.py")
    print(f"  Excel : {XLSX_PATH}")
    print(f"  DB    : {DB_PATH}")
    print("=" * 60)

    print("\n[1/3] Lecture du fichier Excel...")
    df = load_sheet()
    print(f"  {len(df)} lignes lues (sheet='Feuil2')")

    print("\n[2/3] Detection des sections...")
    sections = extract_sections(df)
    for k, v in sections.items():
        print(f"  {k:15s} -> {len(v)} lignes de donnees brutes")

    print("\n[3/3] Mise a jour de la base de donnees...")
    conn = sqlite3.connect(DB_PATH)
    cur  = conn.cursor()

    def recreate(table, ddl, rows, sql):
        if table in PROTECTED:
            print(f"  [SKIP] {table} protegee")
            return 0
        cur.execute(f"DROP TABLE IF EXISTS {table}")
        cur.execute(ddl)
        if rows:
            cur.executemany(sql, rows)
        conn.commit()
        return cur.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]

    counts = {}

    # ── Pompes ───────────────────────────────────────────────
    rows = parse_pompes(sections.get('pompes', []))
    counts['Pompes'] = recreate('pompes', DDL['pompes'], rows,
        "INSERT INTO pompes (marque,modele,type_pompe,debit_max_m3h,HMT_max_m,"
        "puissance_kW,tension_V,type_alimentation) VALUES (?,?,?,?,?,?,?,?)")

    # ── VFD (mono S2 + tri T2) ───────────────────────────────
    rows = parse_vfd(sections.get('vfd', []))
    counts['VFD'] = recreate('vfd', DDL['vfd'], rows,
        "INSERT INTO vfd (modele,puissance_kW,puissance_HP,courant_entree_A,"
        "courant_sortie_A,intervalle_pompe_min_kW,intervalle_pompe_max_kW,"
        "type_sortie,prix) VALUES (?,?,?,?,?,?,?,?,?)")

    # ── Regulateurs MPPT ─────────────────────────────────────
    rows = parse_regulateurs(sections.get('regulateurs', []))
    counts['Regulateurs MPPT'] = recreate('regulateurs_mppt', DDL['regulateurs_mppt'], rows,
        "INSERT INTO regulateurs_mppt (marque,modele,type,courant_max_A,"
        "tension_systeme,plage_tension_pv) VALUES (?,?,?,?,?,?)")

    # ── Panneaux ─────────────────────────────────────────────
    rows = parse_panneaux(sections.get('panneaux', []))
    counts['Panneaux'] = recreate('panneaux', DDL['panneaux'], rows,
        "INSERT INTO panneaux (marque,modele,type,puissance_W,tension_V,"
        "Voc_V,Isc_A,Vmp_V,Imp_A,rendement,prix) VALUES (?,?,?,?,?,?,?,?,?,?,?)")

    # ── Batteries ────────────────────────────────────────────
    rows = parse_batteries(sections.get('batteries', []))
    counts['Batteries'] = recreate('batteries', DDL['batteries'], rows,
        "INSERT INTO batteries (marque,technologie,capacite_Ah,tension_V,"
        "rendement,temps_decharge_h,dod,prix) VALUES (?,?,?,?,?,?,?,?)")

    # ── Protections : split par categorie ────────────────────
    cables, disj, para, fusi = parse_protections(sections.get('protection', []))

    counts['Cables'] = recreate('cables', DDL['cables'], cables,
        "INSERT INTO cables (designation,categorie,calibre_section,unite,prix)"
        " VALUES (?,?,?,?,?)")
    counts['Disjoncteurs'] = recreate('disjoncteurs', DDL['disjoncteurs'], disj,
        "INSERT INTO disjoncteurs (designation,categorie,calibre,unite,prix)"
        " VALUES (?,?,?,?,?)")
    counts['Parafoudres'] = recreate('parafoudres', DDL['parafoudres'], para,
        "INSERT INTO parafoudres (designation,categorie,calibre,unite,prix)"
        " VALUES (?,?,?,?,?)")
    counts['Fusibles'] = recreate('fusibles', DDL['fusibles'], fusi,
        "INSERT INTO fusibles (designation,categorie,calibre,unite,prix)"
        " VALUES (?,?,?,?,?)")

    conn.close()

    # ── Résumé ───────────────────────────────────────────────
    print("\n" + "=" * 60)
    print(f"Pompes: {counts['Pompes']}")
    print(f"VFD: {counts['VFD']}")
    print(f"Regulateurs MPPT: {counts['Regulateurs MPPT']}")
    print(f"Panneaux: {counts['Panneaux']}")
    print(f"Batteries: {counts['Batteries']}")
    print(f"Cables: {counts['Cables']}")
    print(f"Disjoncteurs: {counts['Disjoncteurs']}")
    print(f"Parafoudres: {counts['Parafoudres']}")
    print(f"Fusibles: {counts['Fusibles']}")
    print("=" * 60)


if __name__ == '__main__':
    main()
