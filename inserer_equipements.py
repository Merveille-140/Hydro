import openpyxl
import sqlite3
import re

wb = openpyxl.load_workbook(r'D:\Pompage\Equipements nouveaux.xlsx')
ws = wb['Feuil2']
conn = sqlite3.connect(r'D:\Pompage\solarpump.db')
cur = conn.cursor()


def get_row(row_num):
    return list(ws.iter_rows(min_row=row_num, max_row=row_num, values_only=True))[0]


def safe_float(v):
    if v is None:
        return None
    try:
        return float(v)
    except (ValueError, TypeError):
        return None


def parse_intervalle(s):
    """Extract (min, max) from strings like '0.25–0.37' or '3–4'."""
    nums = re.findall(r'[\d.]+', str(s))
    if len(nums) >= 2:
        return float(nums[0]), float(nums[1])
    return None, None


HEADER_WORDS = {
    'marque', 'modèle', 'modele', 'type', 'désignation', 'designation', 'vdf'
}


def detect_type_alimentation(tension_str):
    if tension_str is None:
        return 'DC'
    t = str(tension_str).upper()
    has_dc = 'DC' in t
    has_3x = bool(re.search(r'3[X×]', t))
    has_1x = bool(re.search(r'1[X×]', t))
    has_ac = 'AC' in t or has_1x or has_3x
    if has_dc and has_ac:
        return 'DC/AC'
    if has_3x:
        return 'AC_tri'
    if has_1x or ('AC' in t and not has_dc):
        return 'AC_mono'
    return 'DC'


def prix_pompe(type_ali, puissance_kW):
    p = float(puissance_kW) if puissance_kW else 0
    if 'DC' in type_ali:
        if p <= 1:
            return 450_000
        elif p <= 4:
            return 850_000
        else:
            return 1_500_000
    else:  # AC_mono, AC_tri
        if p <= 0.5:
            return 50_000
        elif p <= 2:
            return 150_000
        else:
            return 400_000


# ── CLEAR TABLES ─────────────────────────────────────────────────────────────
tables = ['pompes', 'vfd', 'regulateurs_mppt', 'panneaux', 'batteries',
          'cables', 'disjoncteurs', 'parafoudres', 'fusibles']
for t in tables:
    cur.execute(f"DELETE FROM {t}")
    cur.execute("DELETE FROM sqlite_sequence WHERE name=?", (t,))

# ── POMPES (rows 3-54) ────────────────────────────────────────────────────────
# col: 1=marque 2=modele 3=type_pompe 4=debit_max 5=HMT_max 6=puissance_kW 7=tension_V
count_pompes = 0
for r in range(3, 55):
    row = get_row(r)
    if row[1] is None or str(row[1]).strip().lower() in HEADER_WORDS:
        continue
    marque     = str(row[1]).strip()
    modele     = str(row[2]).strip() if row[2] else None
    type_pompe = str(row[3]).strip() if row[3] else None
    debit      = safe_float(row[4])
    hmt        = safe_float(row[5])
    puiss      = safe_float(row[6])
    tension    = str(row[7]).strip() if row[7] else None
    type_ali   = detect_type_alimentation(tension)
    prix       = prix_pompe(type_ali, puiss)
    cur.execute(
        """INSERT INTO pompes
           (marque, modele, type_pompe, debit_max_m3h, HMT_max_m,
            puissance_kW, tension_V, type_alimentation, rendement, prix)
           VALUES (?,?,?,?,?,?,?,?,0.65,?)""",
        (marque, modele, type_pompe, debit, hmt, puiss, tension, type_ali, prix)
    )
    count_pompes += 1

# ── VFD MONO (rows 58-64) ────────────────────────────────────────────────────
# After filtering None: modele, kW, HP, I_in, I_out, intervalle, prix  (7 values)
count_vfd = 0
for r in range(58, 65):
    row = get_row(r)
    if row[1] is None:
        continue
    vals = [v for v in row[1:] if v is not None]
    if len(vals) < 7:
        continue
    modele = str(vals[0]).strip()
    kw     = safe_float(vals[1])
    hp     = safe_float(vals[2])
    i_in   = safe_float(vals[3])
    i_out  = safe_float(vals[4])
    mn, mx = parse_intervalle(vals[5])
    prix   = int(vals[6])
    cur.execute(
        """INSERT INTO vfd
           (modele, puissance_kW, puissance_HP, courant_entree_A, courant_sortie_A,
            intervalle_pompe_min_kW, intervalle_pompe_max_kW, type_sortie, prix)
           VALUES (?,?,?,?,?,?,?,'mono',?)""",
        (modele, kw, hp, i_in, i_out, mn, mx, prix)
    )
    count_vfd += 1

# ── VFD TRI (rows 70-88) ─────────────────────────────────────────────────────
# All column patterns produce exactly 7 non-None values; row 75 empty, row 76 sub-header
# (6 non-None) → both skipped automatically.
for r in range(70, 89):
    row = get_row(r)
    if row[1] is None:
        continue
    if str(row[1]).strip().lower() in HEADER_WORDS:
        continue
    vals = [v for v in row[1:] if v is not None]
    if len(vals) < 7:
        continue
    modele = str(vals[0]).strip()
    kw     = safe_float(vals[1])
    hp     = safe_float(vals[2])
    i_in   = safe_float(vals[3])
    i_out  = safe_float(vals[4])
    mn, mx = parse_intervalle(vals[5])
    prix   = int(vals[6])
    cur.execute(
        """INSERT INTO vfd
           (modele, puissance_kW, puissance_HP, courant_entree_A, courant_sortie_A,
            intervalle_pompe_min_kW, intervalle_pompe_max_kW, type_sortie, prix)
           VALUES (?,?,?,?,?,?,?,'tri',?)""",
        (modele, kw, hp, i_in, i_out, mn, mx, prix)
    )
    count_vfd += 1

# ── REGULATEURS MPPT (rows 94-147, MPPT uniquement) ──────────────────────────
# col: 1=marque 2=modele 3=type 4=courant_max_A 5=tension_systeme 6=plage_tension_pv
count_reg = 0
for r in range(94, 148):
    row = get_row(r)
    if row[1] is None or str(row[1]).strip().lower() in HEADER_WORDS:
        continue
    type_reg = str(row[3]).strip() if row[3] else ''
    if type_reg.upper() != 'MPPT':
        continue
    cur.execute(
        """INSERT INTO regulateurs_mppt
           (marque, modele, type, courant_max_A, tension_systeme, plage_tension_pv)
           VALUES (?,?,?,?,?,?)""",
        (str(row[1]).strip(),
         str(row[2]).strip() if row[2] else None,
         type_reg,
         safe_float(row[4]),
         str(row[5]).strip() if row[5] else None,
         str(row[6]).strip() if row[6] else None)
    )
    count_reg += 1

# ── PANNEAUX (rows 151-186) ───────────────────────────────────────────────────
# col: 1=marque 2=modele 3=type 4=puissance_W 5=tension_V 6=Voc 7=Isc 8=Vmp 9=Imp 10=rendement
# prix = 183 × puissance_W
count_pan = 0
for r in range(151, 187):
    row = get_row(r)
    if row[1] is None or str(row[1]).strip().lower() in HEADER_WORDS:
        continue
    puiss = safe_float(row[4])
    if puiss is None:
        continue
    cur.execute(
        """INSERT INTO panneaux
           (marque, modele, type, puissance_W, tension_V,
            Voc_V, Isc_A, Vmp_V, Imp_A, rendement, prix)
           VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
        (str(row[1]).strip(),
         str(row[2]).strip() if row[2] else None,
         str(row[3]).strip() if row[3] else None,
         puiss,
         safe_float(row[5]),
         safe_float(row[6]),
         safe_float(row[7]),
         safe_float(row[8]),
         safe_float(row[9]),
         safe_float(row[10]),
         int(183 * puiss))
    )
    count_pan += 1

# ── BATTERIES (rows 189-287) ─────────────────────────────────────────────────
# col: 1=marque 2=technologie 3=capacite_Ah 4=tension_V 5=rendement 6=temps_decharge 7=dod
# prix = 1250 × capacite_Ah × tension_V / 1000
count_bat = 0
for r in range(189, 288):
    row = get_row(r)
    if row[1] is None or str(row[1]).strip().lower() in HEADER_WORDS:
        continue
    cap = safe_float(row[3])
    ten = safe_float(row[4])
    if cap is None or ten is None:
        continue
    cur.execute(
        """INSERT INTO batteries
           (marque, technologie, capacite_Ah, tension_V,
            rendement, temps_decharge_h, dod, prix)
           VALUES (?,?,?,?,?,?,?,?)""",
        (str(row[1]).strip(),
         str(row[2]).strip() if row[2] else None,
         cap, ten,
         safe_float(row[5]),
         safe_float(row[6]),
         safe_float(row[7]),
         int(1250 * cap * ten / 1000))
    )
    count_bat += 1

# ── CABLES (rows 291-314) ─────────────────────────────────────────────────────
# col: 1=designation 2=categorie 3=calibre_section 4=unite 5=prix
count_cab = 0
for r in range(291, 315):
    row = get_row(r)
    if row[1] is None:
        continue
    cur.execute(
        "INSERT INTO cables (designation, categorie, calibre_section, unite, prix) VALUES (?,?,?,?,?)",
        (str(row[1]).strip(),
         str(row[2]).strip() if row[2] else None,
         str(row[3]).strip() if row[3] else None,
         str(row[4]).strip() if row[4] else None,
         int(row[5]) if row[5] is not None else 0)
    )
    count_cab += 1

# ── DISJONCTEURS (rows 315-346) ───────────────────────────────────────────────
count_disj = 0
for r in range(315, 347):
    row = get_row(r)
    if row[1] is None:
        continue
    cur.execute(
        "INSERT INTO disjoncteurs (designation, categorie, calibre, unite, prix) VALUES (?,?,?,?,?)",
        (str(row[1]).strip(),
         str(row[2]).strip() if row[2] else None,
         str(row[3]).strip() if row[3] else None,
         str(row[4]).strip() if row[4] else None,
         int(row[5]) if row[5] is not None else 0)
    )
    count_disj += 1

# ── PARAFOUDRES (rows 347-353) ────────────────────────────────────────────────
count_para = 0
for r in range(347, 354):
    row = get_row(r)
    if row[1] is None:
        continue
    cur.execute(
        "INSERT INTO parafoudres (designation, categorie, calibre, unite, prix) VALUES (?,?,?,?,?)",
        (str(row[1]).strip(),
         str(row[2]).strip() if row[2] else None,
         str(row[3]).strip() if row[3] else None,
         str(row[4]).strip() if row[4] else None,
         int(row[5]) if row[5] is not None else 0)
    )
    count_para += 1

# ── FUSIBLES (rows 354-376) ───────────────────────────────────────────────────
count_fus = 0
for r in range(354, 377):
    row = get_row(r)
    if row[1] is None:
        continue
    cur.execute(
        "INSERT INTO fusibles (designation, categorie, calibre, unite, prix) VALUES (?,?,?,?,?)",
        (str(row[1]).strip(),
         str(row[2]).strip() if row[2] else None,
         str(row[3]).strip() if row[3] else None,
         str(row[4]).strip() if row[4] else None,
         int(row[5]) if row[5] is not None else 0)
    )
    count_fus += 1

conn.commit()
conn.close()

print(f"pompes           : {count_pompes} lignes")
print(f"vfd              : {count_vfd} lignes")
print(f"regulateurs_mppt : {count_reg} lignes")
print(f"panneaux         : {count_pan} lignes")
print(f"batteries        : {count_bat} lignes")
print(f"cables           : {count_cab} lignes")
print(f"disjoncteurs     : {count_disj} lignes")
print(f"parafoudres      : {count_para} lignes")
print(f"fusibles         : {count_fus} lignes")
