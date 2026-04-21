# ============================================================
# MODULE ÉNERGIE
# Dimensionnement solaire, groupe électrogène et hybride
# ============================================================

import math


# ============================================================
# CONSTANTES
# ============================================================

RENDEMENT_SYSTEME_PV  = 0.75   # pertes câblage, onduleur, poussière
PUISSANCE_PANNEAU_WC  = 300    # puissance unitaire panneau (Wc)
PROFONDEUR_DECHARGE   = 0.80   # DoD batterie AGM (80%)
RENDEMENT_BATTERIE    = 0.85   # rendement charge/décharge batterie
CONSO_CARBURANT       = 0.25   # litres de gasoil par kWh produit
COEFF_GROUPE          = 1.25   # surdimensionnement groupe électrogène


# ============================================================
# TENSIONS SYSTÈME PV — VALEURS NUMÉRIQUES
# ============================================================

TENSIONS_PV = {
    "12V":  12,
    "24V":  24,
    "48V":  48,
    "96V":  96,
}


# ============================================================
# TENSIONS BATTERIES — VALEURS NUMÉRIQUES
# CORRECTION : dictionnaire séparé de TENSIONS_PV
# Les batteries n'ont pas de tension 96V
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
# ÉNERGIE JOURNALIÈRE
# ============================================================

def calculer_energie_journaliere(puissance_moteur_kW, heures_pompage):
    """
    Calcule l'énergie consommée par jour.

    Paramètres :
        puissance_moteur_kW : puissance du moteur (kW)
        heures_pompage      : heures de fonctionnement par jour

    Retourne :
        énergie en kWh/jour
    """

    return round(puissance_moteur_kW * heures_pompage, 3)


# ============================================================
# DIMENSIONNEMENT SOLAIRE PUR
# ============================================================

def calculer_solaire(
    puissance_moteur_kW,
    heures_pompage,
    irradiation,
    tension_pv
):
    """
    Dimensionne l'installation solaire photovoltaïque.

    Paramètres :
        puissance_moteur_kW : puissance moteur (kW)
        heures_pompage      : heures de pompage par jour
        irradiation         : irradiation solaire (kWh/m²/jour)
        tension_pv          : tension système PV ('12V', '24V', '48V', '96V')

    Retourne :
        dict avec tous les paramètres de l'installation PV
    """

    energie_jour_kWh = calculer_energie_journaliere(
        puissance_moteur_kW,
        heures_pompage
    )

    puissance_crete_kWp = energie_jour_kWh / (
        irradiation * RENDEMENT_SYSTEME_PV
    )

    nb_panneaux = math.ceil(
        (puissance_crete_kWp * 1000) / PUISSANCE_PANNEAU_WC
    )

    puissance_crete_reelle_kWp = round(
        (nb_panneaux * PUISSANCE_PANNEAU_WC) / 1000,
        2
    )

    tension_num = TENSIONS_PV.get(tension_pv, 48)

    courant_A = round(
        (puissance_crete_reelle_kWp * 1000) / tension_num,
        2
    )

    return {
        "energie_jour_kWh":       round(energie_jour_kWh, 2),
        "puissance_crete_kWp":    round(puissance_crete_kWp, 2),
        "puissance_crete_reelle": puissance_crete_reelle_kWp,
        "nb_panneaux_300Wc":      nb_panneaux,
        "tension_pv":             tension_pv,
        "courant_A":              courant_A,
    }


# ============================================================
# DIMENSIONNEMENT GROUPE ÉLECTROGÈNE
# ============================================================

def calculer_groupe(puissance_moteur_kW, heures_pompage):
    """
    Dimensionne le groupe électrogène.
    """

    puissance_groupe_kW = round(
        puissance_moteur_kW * COEFF_GROUPE,
        2
    )

    energie_jour_kWh = calculer_energie_journaliere(
        puissance_moteur_kW,
        heures_pompage
    )

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
# ============================================================

def calculer_hybride_groupe(
    puissance_moteur_kW,
    heures_pompage,
    irradiation,
    tension_pv
):
    """
    Dimensionne un système hybride solaire + groupe électrogène.
    Répartition : 70% solaire / 30% groupe.
    """

    PART_SOLAIRE = 0.70
    PART_GROUPE  = 0.30

    energie_totale_kWh  = calculer_energie_journaliere(puissance_moteur_kW, heures_pompage)
    energie_solaire_kWh = energie_totale_kWh * PART_SOLAIRE
    energie_groupe_kWh  = energie_totale_kWh * PART_GROUPE
    puissance_grp_kW    = puissance_moteur_kW * PART_GROUPE

    puissance_crete_kWp = energie_solaire_kWh / (irradiation * RENDEMENT_SYSTEME_PV)

    nb_panneaux = math.ceil((puissance_crete_kWp * 1000) / PUISSANCE_PANNEAU_WC)

    tension_num = TENSIONS_PV.get(tension_pv, 48)

    courant_A = round((nb_panneaux * PUISSANCE_PANNEAU_WC) / tension_num, 2)

    puissance_groupe_kW      = round(puissance_grp_kW * COEFF_GROUPE, 2)
    consommation_jour_litres = round(energie_groupe_kWh * CONSO_CARBURANT, 2)
    consommation_mois_litres = round(consommation_jour_litres * 30, 1)

    return {
        "energie_totale_kWh":  round(energie_totale_kWh, 2),
        "part_solaire_pct":    int(PART_SOLAIRE * 100),
        "part_groupe_pct":     int(PART_GROUPE * 100),
        "solaire": {
            "energie_jour_kWh":    round(energie_solaire_kWh, 2),
            "puissance_crete_kWp": round(puissance_crete_kWp, 2),
            "nb_panneaux_300Wc":   nb_panneaux,
            "courant_A":           courant_A,
        },
        "groupe": {
            "puissance_groupe_kW":      puissance_groupe_kW,
            "energie_jour_kWh":         round(energie_groupe_kWh, 2),
            "consommation_jour_litres": consommation_jour_litres,
            "consommation_mois_litres": consommation_mois_litres,
        },
    }


# ============================================================
# DIMENSIONNEMENT HYBRIDE SOLAIRE + BATTERIES
# ============================================================

def calculer_hybride_batteries(
    puissance_moteur_kW,
    heures_pompage,
    irradiation,
    tension_pv,
    tension_batterie,
    capacite_batterie,
    jours_autonomie
):
    """
    Dimensionne un système hybride solaire + banc de batteries.
    """

    solaire = calculer_solaire(
        puissance_moteur_kW,
        heures_pompage,
        irradiation,
        tension_pv
    )

    energie_stockage_kWh = round(
        solaire['energie_jour_kWh'] * jours_autonomie,
        2
    )

    # CORRECTION : TENSIONS_BATTERIES au lieu de TENSIONS_PV
    tension_bat_num = TENSIONS_BATTERIES.get(tension_batterie, 24)

    capacite_totale_Ah = round(
        (energie_stockage_kWh * 1000)
        / (tension_bat_num * PROFONDEUR_DECHARGE * RENDEMENT_BATTERIE),
        1
    )

    capacite_unitaire_Ah = CAPACITES_BATTERIES.get(capacite_batterie, 200)

    nb_batteries = math.ceil(capacite_totale_Ah / capacite_unitaire_Ah)

    if nb_batteries % 2 != 0:
        nb_batteries += 1

    return {
        "solaire":              solaire,
        "energie_stockage_kWh": energie_stockage_kWh,
        "capacite_totale_Ah":   capacite_totale_Ah,
        "nb_batteries":         nb_batteries,
        "tension_batterie":     tension_batterie,
        "capacite_unitaire_Ah": capacite_unitaire_Ah,
        "jours_autonomie":      jours_autonomie,
    }