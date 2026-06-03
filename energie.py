# ============================================================
# MODULE ÉNERGIE
# Dimensionnement solaire, groupe électrogène et hybride
# ============================================================

import math


# ============================================================
# CONSTANTES
# ============================================================

PUISSANCE_PANNEAU_WC  = 300    # puissance unitaire panneau par défaut (Wc)
CONSO_CARBURANT       = 0.25   # litres de gasoil par kWh produit
COEFF_GROUPE          = 1.25   # surdimensionnement groupe électrogène


# ============================================================
# TENSIONS SYSTÈME PV — VALEURS NUMÉRIQUES (legacy)
# ============================================================

TENSIONS_PV = {
    "12V":  12,
    "24V":  24,
    "48V":  48,
    "96V":  96,
}


# ============================================================
# TENSIONS BATTERIES — VALEURS NUMÉRIQUES
# ============================================================

TENSIONS_BATTERIES = {
    "12V": 12,
    "24V": 24,
    "48V": 48,
}


# ============================================================
# CAPACITÉS BATTERIES — VALEURS NUMÉRIQUES (Ah)
# ============================================================

CAPACITES_BATTERIES = {
    "100Ah": 100,
    "150Ah": 150,
    "200Ah": 200,
    "250Ah": 250,
}


# ============================================================
# TENSION SYSTÈME AUTO
# Pc en W → tension système en V
# ============================================================

def _auto_tension(Pc_W):
    if Pc_W <= 500:
        return 12
    elif Pc_W <= 1500:
        return 24
    elif Pc_W <= 5000:
        return 48
    else:
        return 96


# ============================================================
# ÉNERGIE JOURNALIÈRE (legacy — conservé pour compatibilité)
# ============================================================

def calculer_energie_journaliere(puissance_moteur_kW, heures_pompage):
    return round(puissance_moteur_kW * heures_pompage, 3)


# ============================================================
# DIMENSIONNEMENT SOLAIRE PUR
# Eelec (kWh/j) = 2.725e-3 × Q (m³/j) × HMT (m) / Rmp
# Pc (kWc)      = Eelec / (Ir × Pr)
# U_syst        = calculé automatiquement selon Pc
# ============================================================

def calculer_solaire(Q_m3_jour, HMT_m, Rmp, irradiation, Pr=0.75, puissance_panneau_W=300):
    Eelec      = (2.725e-3 * Q_m3_jour * HMT_m) / Rmp
    Pc_kWp     = Eelec / (irradiation * Pr)
    U_syst     = _auto_tension(Pc_kWp * 1000)
    nb_panneaux = math.ceil((Pc_kWp * 1000) / puissance_panneau_W)
    courant_A  = round((Pc_kWp * 1000) / U_syst, 2)

    return {
        "energie_jour_kWh":    round(Eelec, 2),
        "puissance_crete_kWp": round(Pc_kWp, 2),
        "nb_panneaux_300Wc":   nb_panneaux,
        "tension_pv":          f"{U_syst}V",
        "U_syst":              U_syst,
        "courant_A":           courant_A,
    }


# ============================================================
# DIMENSIONNEMENT GROUPE ÉLECTROGÈNE (inchangé)
# ============================================================

def calculer_groupe(puissance_moteur_kW, heures_pompage):
    puissance_groupe_kW       = round(puissance_moteur_kW * COEFF_GROUPE, 2)
    energie_jour_kWh          = calculer_energie_journaliere(puissance_moteur_kW, heures_pompage)
    consommation_jour_litres  = round(energie_jour_kWh * CONSO_CARBURANT, 2)
    consommation_mois_litres  = round(consommation_jour_litres * 30, 1)
    consommation_annee_litres = round(consommation_jour_litres * 365, 1)

    return {
        "puissance_groupe_kW":       puissance_groupe_kW,
        "energie_jour_kWh":          round(energie_jour_kWh, 2),
        "consommation_jour_litres":  consommation_jour_litres,
        "consommation_mois_litres":  consommation_mois_litres,
        "consommation_annee_litres": consommation_annee_litres,
    }


# ============================================================
# DIMENSIONNEMENT HYBRIDE SOLAIRE + GROUPE
# Partie solaire : nouvelle formule Eelec
# Partie groupe  : basée sur puissance moteur (inchangée)
# ============================================================

def calculer_hybride_groupe(puissance_moteur_kW, heures_pompage, irradiation,
                             Q_m3_jour, HMT_m, Rmp, Pr=0.75, puissance_panneau_W=300):
    PART_SOLAIRE = 0.70
    PART_GROUPE  = 0.30

    Eelec_total = (2.725e-3 * Q_m3_jour * HMT_m) / Rmp
    Eelec_sol   = Eelec_total * PART_SOLAIRE
    Eelec_grp   = Eelec_total * PART_GROUPE

    Pc_kWp      = Eelec_sol / (irradiation * Pr)
    U_syst      = _auto_tension(Pc_kWp * 1000)
    nb_panneaux = math.ceil((Pc_kWp * 1000) / puissance_panneau_W)
    courant_A   = round((Pc_kWp * 1000) / U_syst, 2)

    puissance_groupe_kW      = round(puissance_moteur_kW * PART_GROUPE * COEFF_GROUPE, 2)
    consommation_jour_litres = round(Eelec_grp * CONSO_CARBURANT, 2)
    consommation_mois_litres = round(consommation_jour_litres * 30, 1)

    return {
        "energie_totale_kWh": round(Eelec_total, 2),
        "part_solaire_pct":   int(PART_SOLAIRE * 100),
        "part_groupe_pct":    int(PART_GROUPE * 100),
        "solaire": {
            "energie_jour_kWh":    round(Eelec_sol, 2),
            "puissance_crete_kWp": round(Pc_kWp, 2),
            "nb_panneaux_300Wc":   nb_panneaux,
            "courant_A":           courant_A,
            "U_syst":              U_syst,
        },
        "groupe": {
            "puissance_groupe_kW":      puissance_groupe_kW,
            "energie_jour_kWh":         round(Eelec_grp, 2),
            "consommation_jour_litres": consommation_jour_litres,
            "consommation_mois_litres": consommation_mois_litres,
        },
    }


# ============================================================
# DIMENSIONNEMENT HYBRIDE SOLAIRE + BATTERIES
# Cap_Ah  = Eelec × 1000 × J / (U_syst × DoD)
# N_serie = ceil(U_syst / U_bat)
# N_para  = ceil(Cap_Ah / Cap_unitaire)
# N_total = N_serie × N_para
# ============================================================

def calculer_hybride_batteries(Q_m3_jour, HMT_m, Rmp, irradiation, Pr,
                                puissance_panneau_W, tension_batterie,
                                capacite_batterie, jours_autonomie, type_bat='GEL'):
    dod = 0.5 if str(type_bat).upper() == 'GEL' else 0.8
    solaire = calculer_solaire(Q_m3_jour, HMT_m, Rmp, irradiation, Pr, puissance_panneau_W)
    Eelec   = solaire["energie_jour_kWh"]
    U_syst  = solaire["U_syst"]

    tension_bat_num = (tension_batterie if isinstance(tension_batterie, (int, float))
                       else TENSIONS_BATTERIES.get(str(tension_batterie), 24))
    cap_unitaire_Ah = (capacite_batterie if isinstance(capacite_batterie, (int, float))
                       else CAPACITES_BATTERIES.get(str(capacite_batterie), 200))

    capacite_totale_Ah = round((Eelec * 1000 * jours_autonomie) / (U_syst * dod), 1)
    N_serie            = math.ceil(U_syst / tension_bat_num)
    N_parallele        = math.ceil(capacite_totale_Ah / cap_unitaire_Ah)
    N_total            = N_serie * N_parallele

    print("=== BATTERIES ===")
    print("DoD utilisé:", dod, "| Type batterie:", type_bat)
    print("Eelec:", round(Eelec, 3), "kWh/j | Jours autonomie:", jours_autonomie)
    print("Usyst:", U_syst, "V | Ubat:", tension_bat_num, "V | Cbat:", cap_unitaire_Ah, "Ah")
    print("Ctot:", capacite_totale_Ah, "Ah")
    print("Nbat_série:", N_serie, "| Nbat_parallèles:", N_parallele, "| Total:", N_total)

    return {
        "solaire":              solaire,
        "energie_stockage_kWh": round(Eelec * jours_autonomie, 2),
        "capacite_totale_Ah":   capacite_totale_Ah,
        "nb_batteries":         N_total,
        "nb_serie":             N_serie,
        "nb_parallele":         N_parallele,
        "tension_batterie":     tension_batterie,
        "capacite_unitaire_Ah": cap_unitaire_Ah,
        "jours_autonomie":      jours_autonomie,
        "dod":                  dod,
    }
