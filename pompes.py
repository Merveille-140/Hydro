# ============================================================
# MODULE POMPES
# Base de données complète + algorithme de sélection
# ============================================================


# ============================================================
# BASE DE DONNÉES DES POMPES
# ============================================================

POMPES = [

    # ─────────────────────────────────────────────────────
    # LORENTZ — Pompes solaires DC
    # ─────────────────────────────────────────────────────

    {
        "marque":            "Lorentz",
        "modele":            "PS2-600 C-SJ3-5",
        "type_pompe":        "centrifuge",
        "type_installation": "submersible",
        "debit_max_m3h":     3.0,
        "HMT_max_m":         50,
        "puissance_kW":      0.6,
        "tension_V":         "DC 24-90V",
        "source_energie":    ["solaire", "hybride_batteries"],
        "rendement":         0.60,
        "description":       "Petite pompe solaire DC pour puits peu profonds"
    },
    {
        "marque":            "Lorentz",
        "modele":            "PS2-1200 C-SJ5-5",
        "type_pompe":        "centrifuge",
        "type_installation": "submersible",
        "debit_max_m3h":     4.0,
        "HMT_max_m":         55,
        "puissance_kW":      1.2,
        "tension_V":         "DC 30-120V",
        "source_energie":    ["solaire", "hybride_batteries"],
        "rendement":         0.62,
        "description":       "Pompe solaire DC compacte et économique"
    },
    {
        "marque":            "Lorentz",
        "modele":            "PS2-1800 C-SJ5-7",
        "type_pompe":        "centrifuge",
        "type_installation": "submersible",
        "debit_max_m3h":     5.0,
        "HMT_max_m":         70,
        "puissance_kW":      1.8,
        "tension_V":         "DC 30-120V",
        "source_energie":    ["solaire", "hybride_batteries"],
        "rendement":         0.65,
        "description":       "Pompe solaire DC haute performance pour forages"
    },
    {
        "marque":            "Lorentz",
        "modele":            "PS2-1800 C-SJ8-4",
        "type_pompe":        "centrifuge",
        "type_installation": "submersible",
        "debit_max_m3h":     8.0,
        "HMT_max_m":         45,
        "puissance_kW":      1.8,
        "tension_V":         "DC 30-120V",
        "source_energie":    ["solaire", "hybride_batteries"],
        "rendement":         0.65,
        "description":       "Pompe solaire DC grand débit faible profondeur"
    },
    {
        "marque":            "Lorentz",
        "modele":            "PS2-2900 C-SJ5-11",
        "type_pompe":        "centrifuge",
        "type_installation": "submersible",
        "debit_max_m3h":     5.0,
        "HMT_max_m":         110,
        "puissance_kW":      2.9,
        "tension_V":         "DC 48-180V",
        "source_energie":    ["solaire", "hybride_batteries"],
        "rendement":         0.67,
        "description":       "Pompe solaire DC pour forages très profonds"
    },
    {
        "marque":            "Lorentz",
        "modele":            "PS2-4000 C-SJ8-8",
        "type_pompe":        "centrifuge",
        "type_installation": "submersible",
        "debit_max_m3h":     8.0,
        "HMT_max_m":         80,
        "puissance_kW":      4.0,
        "tension_V":         "DC 60-240V",
        "source_energie":    ["solaire", "hybride_batteries"],
        "rendement":         0.68,
        "description":       "Pompe solaire DC puissante pour irrigation"
    },
    {
        "marque":            "Lorentz",
        "modele":            "PS2-4000 C-SJ12-5",
        "type_pompe":        "centrifuge",
        "type_installation": "submersible",
        "debit_max_m3h":     12.0,
        "HMT_max_m":         55,
        "puissance_kW":      4.0,
        "tension_V":         "DC 60-240V",
        "source_energie":    ["solaire", "hybride_batteries"],
        "rendement":         0.67,
        "description":       "Pompe solaire DC très grand débit"
    },
    {
        "marque":            "Lorentz",
        "modele":            "PS2-7200 C-SJ8-12",
        "type_pompe":        "centrifuge",
        "type_installation": "submersible",
        "debit_max_m3h":     8.0,
        "HMT_max_m":         120,
        "puissance_kW":      7.2,
        "tension_V":         "DC 96-300V",
        "source_energie":    ["solaire", "hybride_batteries"],
        "rendement":         0.69,
        "description":       "Pompe solaire DC haute puissance forage profond"
    },
    {
        "marque":            "Lorentz",
        "modele":            "PS2-7200 C-SJ17-7",
        "type_pompe":        "centrifuge",
        "type_installation": "submersible",
        "debit_max_m3h":     17.0,
        "HMT_max_m":         75,
        "puissance_kW":      7.2,
        "tension_V":         "DC 96-300V",
        "source_energie":    ["solaire", "hybride_batteries"],
        "rendement":         0.68,
        "description":       "Pompe solaire DC très grand débit irrigation"
    },
    {
        "marque":            "Lorentz",
        "modele":            "PS2-15000 C-SJ20-10",
        "type_pompe":        "centrifuge",
        "type_installation": "submersible",
        "debit_max_m3h":     20.0,
        "HMT_max_m":         100,
        "puissance_kW":      15.0,
        "tension_V":         "DC 120-400V",
        "source_energie":    ["solaire", "hybride_batteries"],
        "rendement":         0.70,
        "description":       "Grande pompe solaire DC pour installations importantes"
    },

    # ─────────────────────────────────────────────────────
    # GRUNDFOS SQFlex — Pompes solaires AC/DC
    # ─────────────────────────────────────────────────────

    {
        "marque":            "Grundfos",
        "modele":            "SQFlex 0.6-3",
        "type_pompe":        "centrifuge",
        "type_installation": "submersible",
        "debit_max_m3h":     0.6,
        "HMT_max_m":         25,
        "puissance_kW":      0.3,
        "tension_V":         "30-300V DC / 90-240V AC",
        "source_energie":    ["solaire", "hybride_batteries", "groupe"],
        "rendement":         0.55,
        "description":       "Très petite pompe flexible DC/AC eau potable"
    },
    {
        "marque":            "Grundfos",
        "modele":            "SQFlex 1.2-8",
        "type_pompe":        "centrifuge",
        "type_installation": "submersible",
        "debit_max_m3h":     1.2,
        "HMT_max_m":         45,
        "puissance_kW":      0.5,
        "tension_V":         "30-300V DC / 90-240V AC",
        "source_energie":    ["solaire", "hybride_batteries", "groupe"],
        "rendement":         0.58,
        "description":       "Petite pompe solaire AC/DC eau potable rurale"
    },
    {
        "marque":            "Grundfos",
        "modele":            "SQFlex 3-65",
        "type_pompe":        "centrifuge",
        "type_installation": "submersible",
        "debit_max_m3h":     3.0,
        "HMT_max_m":         65,
        "puissance_kW":      1.4,
        "tension_V":         "30-300V DC / 90-240V AC",
        "source_energie":    ["solaire", "hybride_batteries", "groupe"],
        "rendement":         0.65,
        "description":       "Pompe flexible DC/AC idéale eau potable rurale"
    },
    {
        "marque":            "Grundfos",
        "modele":            "SQFlex 5-35",
        "type_pompe":        "centrifuge",
        "type_installation": "submersible",
        "debit_max_m3h":     5.0,
        "HMT_max_m":         35,
        "puissance_kW":      1.2,
        "tension_V":         "30-300V DC / 90-240V AC",
        "source_energie":    ["solaire", "hybride_batteries", "groupe"],
        "rendement":         0.63,
        "description":       "Pompe solaire AC/DC grand débit faible HMT"
    },
    {
        "marque":            "Grundfos",
        "modele":            "SQFlex 11-20",
        "type_pompe":        "centrifuge",
        "type_installation": "submersible",
        "debit_max_m3h":     11.0,
        "HMT_max_m":         20,
        "puissance_kW":      1.5,
        "tension_V":         "30-300V DC / 90-240V AC",
        "source_energie":    ["solaire", "hybride_batteries", "groupe"],
        "rendement":         0.62,
        "description":       "Pompe solaire très grand débit faible profondeur"
    },
    {
        "marque":            "Grundfos",
        "modele":            "SQFlex 2-115",
        "type_pompe":        "centrifuge",
        "type_installation": "submersible",
        "debit_max_m3h":     2.0,
        "HMT_max_m":         115,
        "puissance_kW":      1.8,
        "tension_V":         "30-300V DC / 90-240V AC",
        "source_energie":    ["solaire", "hybride_batteries", "groupe"],
        "rendement":         0.66,
        "description":       "Pompe solaire pour très grands forages"
    },
# ─────────────────────────────────────────────────────
    # SHAKTI — Pompes solaires DC (marché Afrique)
    # ─────────────────────────────────────────────────────

    {
        "marque":            "Shakti",
        "modele":            "SSH-370-4",
        "type_pompe":        "centrifuge",
        "type_installation": "submersible",
        "debit_max_m3h":     1.5,
        "HMT_max_m":         30,
        "puissance_kW":      0.37,
        "tension_V":         "DC 24-60V",
        "source_energie":    ["solaire", "hybride_batteries"],
        "rendement":         0.55,
        "description":       "Très petite pompe solaire DC économique"
    },
    {
        "marque":            "Shakti",
        "modele":            "SSH-750-4",
        "type_pompe":        "centrifuge",
        "type_installation": "submersible",
        "debit_max_m3h":     2.5,
        "HMT_max_m":         40,
        "puissance_kW":      0.75,
        "tension_V":         "DC 24-72V",
        "source_energie":    ["solaire", "hybride_batteries"],
        "rendement":         0.58,
        "description":       "Petite pompe solaire DC pour puits peu profonds"
    },
    {
        "marque":            "Shakti",
        "modele":            "SSH-1100-4",
        "type_pompe":        "centrifuge",
        "type_installation": "submersible",
        "debit_max_m3h":     3.5,
        "HMT_max_m":         50,
        "puissance_kW":      1.1,
        "tension_V":         "DC 36-96V",
        "source_energie":    ["solaire", "hybride_batteries"],
        "rendement":         0.60,
        "description":       "Pompe solaire DC fiable marché africain"
    },
    {
        "marque":            "Shakti",
        "modele":            "SSH-1500-4",
        "type_pompe":        "centrifuge",
        "type_installation": "submersible",
        "debit_max_m3h":     4.5,
        "HMT_max_m":         60,
        "puissance_kW":      1.5,
        "tension_V":         "DC 48-120V",
        "source_energie":    ["solaire", "hybride_batteries"],
        "rendement":         0.62,
        "description":       "Pompe solaire DC très répandue en Afrique"
    },
    {
        "marque":            "Shakti",
        "modele":            "SSH-2200-4",
        "type_pompe":        "centrifuge",
        "type_installation": "submersible",
        "debit_max_m3h":     6.0,
        "HMT_max_m":         75,
        "puissance_kW":      2.2,
        "tension_V":         "DC 72-150V",
        "source_energie":    ["solaire", "hybride_batteries"],
        "rendement":         0.63,
        "description":       "Pompe solaire DC robuste pour irrigation"
    },
    {
        "marque":            "Shakti",
        "modele":            "SSH-3700-6",
        "type_pompe":        "centrifuge",
        "type_installation": "submersible",
        "debit_max_m3h":     9.0,
        "HMT_max_m":         90,
        "puissance_kW":      3.7,
        "tension_V":         "DC 96-180V",
        "source_energie":    ["solaire", "hybride_batteries"],
        "rendement":         0.65,
        "description":       "Pompe solaire DC puissante grande superficie"
    },
    {
        "marque":            "Shakti",
        "modele":            "SSH-5500-6",
        "type_pompe":        "centrifuge",
        "type_installation": "submersible",
        "debit_max_m3h":     12.0,
        "HMT_max_m":         100,
        "puissance_kW":      5.5,
        "tension_V":         "DC 120-240V",
        "source_energie":    ["solaire", "hybride_batteries"],
        "rendement":         0.66,
        "description":       "Grande pompe solaire DC usage intensif"
    },
    {
        "marque":            "Shakti",
        "modele":            "SSH-7500-6",
        "type_pompe":        "centrifuge",
        "type_installation": "submersible",
        "debit_max_m3h":     16.0,
        "HMT_max_m":         110,
        "puissance_kW":      7.5,
        "tension_V":         "DC 150-300V",
        "source_energie":    ["solaire", "hybride_batteries"],
        "rendement":         0.67,
        "description":       "Très grande pompe solaire DC installations importantes"
    },


    # ─────────────────────────────────────────────────────
    # SUNPUMPS — Pompes solaires DC
    # ─────────────────────────────────────────────────────

    {
        "marque":            "Sunpumps",
        "modele":            "SCS 5-130-60",
        "type_pompe":        "centrifuge",
        "type_installation": "submersible",
        "debit_max_m3h":     0.5,
        "HMT_max_m":         20,
        "puissance_kW":      0.15,
        "tension_V":         "DC 12-48V",
        "source_energie":    ["solaire", "hybride_batteries"],
        "rendement":         0.52,
        "description":       "Très petite pompe solaire DC rurale"
    },
    {
        "marque":            "Sunpumps",
        "modele":            "SCS 10-165-160",
        "type_pompe":        "centrifuge",
        "type_installation": "submersible",
        "debit_max_m3h":     2.4,
        "HMT_max_m":         50,
        "puissance_kW":      0.5,
        "tension_V":         "DC 24-72V",
        "source_energie":    ["solaire", "hybride_batteries"],
        "rendement":         0.58,
        "description":       "Petite pompe solaire DC pour puits ruraux"
    },
    {
        "marque":            "Sunpumps",
        "modele":            "SCS 20-200-240",
        "type_pompe":        "centrifuge",
        "type_installation": "submersible",
        "debit_max_m3h":     4.8,
        "HMT_max_m":         60,
        "puissance_kW":      1.2,
        "tension_V":         "DC 48-120V",
        "source_energie":    ["solaire", "hybride_batteries"],
        "rendement":         0.60,
        "description":       "Pompe solaire DC économique et fiable"
    },
    {
        "marque":            "Sunpumps",
        "modele":            "SCS 30-250-350",
        "type_pompe":        "centrifuge",
        "type_installation": "submersible",
        "debit_max_m3h":     7.0,
        "HMT_max_m":         75,
        "puissance_kW":      2.2,
        "tension_V":         "DC 72-150V",
        "source_energie":    ["solaire", "hybride_batteries"],
        "rendement":         0.62,
        "description":       "Pompe solaire DC grand débit irrigation"
    },
    {
        "marque":            "Sunpumps",
        "modele":            "SCS 50-300-500",
        "type_pompe":        "centrifuge",
        "type_installation": "submersible",
        "debit_max_m3h":     12.0,
        "HMT_max_m":         90,
        "puissance_kW":      4.0,
        "tension_V":         "DC 96-200V",
        "source_energie":    ["solaire", "hybride_batteries"],
        "rendement":         0.64,
        "description":       "Grande pompe solaire DC irrigation intensive"
    },

]
# ============================================================
# ALGORITHME DE SÉLECTION DES POMPES
# ============================================================

def selectionner_pompes(debit_m3_h, HMT_m, source_energie, marque_choisie='toutes'):
    """
    Sélectionne toutes les pompes compatibles avec les paramètres,
    filtrées par marque si l'utilisateur en a choisi une.
    """

    # ─────────────────────────────────────────────────────
    # ÉTAPE 1 — FILTRAGE HYDRAULIQUE ET ÉNERGIE
    # ─────────────────────────────────────────────────────

    pompes_compatibles = []

    for pompe in POMPES:
        compatible_energie = source_energie in pompe['source_energie']
        compatible_debit   = pompe['debit_max_m3h'] >= debit_m3_h
        compatible_HMT     = pompe['HMT_max_m']     >= HMT_m

        if compatible_energie and compatible_debit and compatible_HMT:
            pompes_compatibles.append(pompe)

    # ─────────────────────────────────────────────────────
    # ÉTAPE 2 — FILTRAGE PAR MARQUE
    # ─────────────────────────────────────────────────────

    marque_introuvable = False

    if marque_choisie and marque_choisie != 'toutes':
        pompes_marque = [
            p for p in pompes_compatibles
            if p['marque'] == marque_choisie
        ]

        if len(pompes_marque) == 0:
            pompes_filtrees    = pompes_compatibles
            marque_introuvable = True
        else:
            pompes_filtrees    = pompes_marque
    else:
        pompes_filtrees = pompes_compatibles

    # ─────────────────────────────────────────────────────
    # ÉTAPE 3 — CALCUL DU SCORE ET TRI
    # ─────────────────────────────────────────────────────

    pompes_scorees = []

    for pompe in pompes_filtrees:
        score = calculer_score(pompe, debit_m3_h, HMT_m)
        pompe_avec_score = dict(pompe)
        pompe_avec_score['score'] = score
        pompes_scorees.append(pompe_avec_score)

    pompes_scorees.sort(key=lambda p: p['score'], reverse=True)

    # ─────────────────────────────────────────────────────
    # ÉTAPE 4 — FORMATAGE
    # ─────────────────────────────────────────────────────

    resultats = []

    for pompe in pompes_scorees:
        resultats.append({
            "marque":              pompe['marque'],
            "modele":              pompe['modele'],
            "type_installation":   pompe['type_installation'],
            "debit_max_m3h":       pompe['debit_max_m3h'],
            "HMT_max_m":           pompe['HMT_max_m'],
            "puissance_kW":        pompe['puissance_kW'],
            "tension_V":           pompe['tension_V'],
            "rendement":           pompe['rendement'],
            "description":         pompe['description'],
            "score":               round(pompe['score'], 2),
            "marque_introuvable":  marque_introuvable,
        })

    return resultats


# ============================================================
# CALCUL DU SCORE
# ============================================================

def calculer_score(pompe, debit_requis, HMT_requis):
    """
    Calcule un score de pertinence pour une pompe donnée.
    Critères : proximité débit (40%), proximité HMT (40%), rendement (20%)
    """

    # Score débit
    ratio_debit = pompe['debit_max_m3h'] / debit_requis

    if ratio_debit < 1.0:
        score_debit = 0.0
    elif ratio_debit <= 1.5:
        score_debit = 1.0
    elif ratio_debit <= 2.0:
        score_debit = 1.0 - ((ratio_debit - 1.5) / 0.5) * 0.4
    elif ratio_debit <= 3.0:
        score_debit = 0.6 - ((ratio_debit - 2.0) / 1.0) * 0.4
    else:
        score_debit = 0.2

    # Score HMT
    ratio_HMT = pompe['HMT_max_m'] / HMT_requis

    if ratio_HMT < 1.0:
        score_HMT = 0.0
    elif ratio_HMT <= 1.5:
        score_HMT = 1.0
    elif ratio_HMT <= 2.0:
        score_HMT = 1.0 - ((ratio_HMT - 1.5) / 0.5) * 0.4
    elif ratio_HMT <= 3.0:
        score_HMT = 0.6 - ((ratio_HMT - 2.0) / 1.0) * 0.4
    else:
        score_HMT = 0.2

    # Score rendement
    rendement_min   = 0.52
    rendement_max   = 0.70
    score_rendement = (
        (pompe['rendement'] - rendement_min)
        / (rendement_max - rendement_min)
    )
    score_rendement = max(0.0, min(1.0, score_rendement))

    # Score final
    score_final = (
        score_debit       * 0.40
        + score_HMT       * 0.40
        + score_rendement * 0.20
    )

    return score_final


# ============================================================
# RÉCUPÉRATION DES MARQUES
# ============================================================

def get_marques():
    """
    Retourne la liste des marques disponibles.
    """
    marques = []
    for pompe in POMPES:
        if pompe['marque'] not in marques:
            marques.append(pompe['marque'])
    return sorted(marques)


# ============================================================
# RÉCUPÉRATION DES MODÈLES PAR MARQUE
# ============================================================

def get_modeles_par_marque(marque):
    """
    Retourne tous les modèles disponibles pour une marque donnée.
    """
    modeles = []
    for pompe in POMPES:
        if pompe['marque'] == marque:
            modeles.append({
                "modele":            pompe['modele'],
                "debit_max_m3h":     pompe['debit_max_m3h'],
                "HMT_max_m":         pompe['HMT_max_m'],
                "puissance_kW":      pompe['puissance_kW'],
                "tension_V":         pompe['tension_V'],
                "type_installation": pompe['type_installation'],
                "source_energie":    pompe['source_energie'],
            })
    return modeles


# ============================================================
# RÉCUPÉRATION DES CARACTÉRISTIQUES D'UNE POMPE
# ============================================================

def get_caracteristiques_pompe(marque, modele):
    """
    Retourne toutes les caractéristiques d'une pompe.
    """
    for pompe in POMPES:
        if pompe['marque'] == marque and pompe['modele'] == modele:
            return {
                "marque":            pompe['marque'],
                "modele":            pompe['modele'],
                "type_pompe":        pompe['type_pompe'],
                "type_installation": pompe['type_installation'],
                "debit_max_m3h":     pompe['debit_max_m3h'],
                "HMT_max_m":         pompe['HMT_max_m'],
                "puissance_kW":      pompe['puissance_kW'],
                "tension_V":         pompe['tension_V'],
                "source_energie":    pompe['source_energie'],
                "rendement":         pompe['rendement'],
                "description":       pompe['description'],
            }
    return None
