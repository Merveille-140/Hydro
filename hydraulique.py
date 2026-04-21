# ============================================================
# MODULE HYDRAULIQUE
# Calcul du débit Q et de la HMT
# Supporte : irrigation, forage→réservoir, lac/rivière→réservoir
# ============================================================

import math


# ============================================================
# CONSTANTES
# ============================================================

GRAVITE               = 9.81
DENSITE_EAU           = 1000
VISCOSITE_EAU         = 1e-6
RUGOSITE_PVC          = 0.0000015
COEFFICIENT_SINGULIER = 0.20


# ============================================================
# PRESSION RÉSIDUELLE SELON SYSTÈME D'IRRIGATION
# ============================================================

PRESSION_PAR_SYSTEME = {
    'goutte_a_goutte': 10.0,
    'aspersion':       20.0,
    'gravitaire':       2.0,
}


# ============================================================
# FONCTION PRINCIPALE
# ============================================================

def calculer_hydraulique(
    besoin_brut_m3_jour,
    heures_pompage,
    systeme_irrigation       = 'gravitaire',
    source_energie           = 'solaire',
    longueur_canalisation    = 0,
    diametre_tuyau_mm        = 63,
    type_systeme_hydraulique = 'irrigation',
    type_alimentation        = 'bas',
    hauteur_reservoir        = 0,
    niveau_dynamique         = 0,
    niveau_eau_lac           = 0,
    hauteur_aspiration       = 0,
    profondeur_aspiration    = 0,
    hauteur_refoulement      = 0,
):
    """
    Calcule le débit Q et la HMT selon le type de système.

    Types supportés :
        irrigation       : système d'irrigation agricole
        forage_reservoir : forage vers réservoir
        lac_reservoir    : lac ou rivière vers réservoir
    """

    # ─────────────────────────────────────────────────────
    # DÉBIT Q
    # ─────────────────────────────────────────────────────

    debit_m3_h = besoin_brut_m3_jour / heures_pompage
    debit_m3_s = debit_m3_h / 3600
    debit_L_s  = debit_m3_s * 1000

    # ─────────────────────────────────────────────────────
    # PERTES DE CHARGE — DARCY-WEISBACH
    # ─────────────────────────────────────────────────────

    pertes_charge = 0.0
    vitesse       = 0.0

    if longueur_canalisation > 0 and debit_m3_s > 0:

        diametre_m        = diametre_tuyau_mm / 1000
        section           = math.pi * (diametre_m / 2) ** 2
        vitesse           = debit_m3_s / section
        reynolds          = (vitesse * diametre_m) / VISCOSITE_EAU
        facteur_f         = calculer_facteur_frottement(reynolds, diametre_m)
        pertes_lineaires  = (
            facteur_f
            * (longueur_canalisation / diametre_m)
            * (vitesse ** 2)
            / (2 * GRAVITE)
        )
        pertes_singulieres = pertes_lineaires * COEFFICIENT_SINGULIER
        pertes_charge      = pertes_lineaires + pertes_singulieres

    else:
        pertes_charge = 0.15 * 20

    # ─────────────────────────────────────────────────────
    # HMT SELON TYPE DE SYSTÈME
    # ─────────────────────────────────────────────────────

    if type_systeme_hydraulique == 'forage_reservoir':

        HMT = calculer_HMT_forage(
            niveau_dynamique  = niveau_dynamique,
            hauteur_reservoir = hauteur_reservoir,
            type_alimentation = type_alimentation,
            pertes_charge     = pertes_charge,
        )

        hauteur_geo = niveau_dynamique + hauteur_reservoir

    elif type_systeme_hydraulique == 'lac_reservoir':

        HMT = calculer_HMT_lac(
            niveau_eau_lac    = niveau_eau_lac,
            hauteur_aspiration = hauteur_aspiration,
            hauteur_reservoir  = hauteur_reservoir,
            type_alimentation  = type_alimentation,
            pertes_charge      = pertes_charge,
        )

        hauteur_geo = abs(niveau_eau_lac) + hauteur_aspiration + hauteur_reservoir

    else:
        # Mode irrigation
        hauteur_geo         = profondeur_aspiration + hauteur_refoulement
        pression_residuelle = PRESSION_PAR_SYSTEME.get(
            systeme_irrigation,
            2.0
        )
        HMT = hauteur_geo + pertes_charge + pression_residuelle

    return {
        "debit_m3_h":                round(debit_m3_h, 3),
        "debit_L_s":                 round(debit_L_s, 3),
        "hauteur_geo_m":             round(hauteur_geo, 2),
        "pertes_charge_m":           round(pertes_charge, 2),
        "HMT_m":                     round(HMT, 2),
        "vitesse_m_s":               round(vitesse, 2),
        "type_systeme_hydraulique":  type_systeme_hydraulique,
    }


# ============================================================
# HMT FORAGE → RÉSERVOIR
# ============================================================

def calculer_HMT_forage(
    niveau_dynamique,
    hauteur_reservoir,
    type_alimentation,
    pertes_charge,
):
    """
    Calcule la HMT pour un système forage → réservoir.

    Alimentation par le bas :
        HMT = niveau_dynamique + hauteur_reservoir + pertes_charge

    Alimentation par le haut :
        HMT = niveau_dynamique + hauteur_reservoir * 2 + pertes_charge
        (la pompe doit monter l'eau jusqu'au dessus du réservoir)
    """

    if type_alimentation == 'haut':
        HMT = niveau_dynamique + (hauteur_reservoir * 2) + pertes_charge
    else:
        HMT = niveau_dynamique + hauteur_reservoir + pertes_charge

    return round(HMT, 2)


# ============================================================
# HMT LAC / RIVIÈRE → RÉSERVOIR
# ============================================================

def calculer_HMT_lac(
    niveau_eau_lac,
    hauteur_aspiration,
    hauteur_reservoir,
    type_alimentation,
    pertes_charge,
):
    """
    Calcule la HMT pour un système lac/rivière → réservoir.

    hauteur_geo = hauteur_aspiration + hauteur_reservoir

    Alimentation par le bas :
        HMT = hauteur_aspiration + hauteur_reservoir + pertes_charge

    Alimentation par le haut :
        HMT = hauteur_aspiration + hauteur_reservoir * 2 + pertes_charge
    """

    if type_alimentation == 'haut':
        HMT = hauteur_aspiration + (hauteur_reservoir * 2) + pertes_charge
    else:
        HMT = hauteur_aspiration + hauteur_reservoir + pertes_charge

    return round(HMT, 2)


# ============================================================
# FACTEUR DE FROTTEMENT — SWAMEE-JAIN
# ============================================================

def calculer_facteur_frottement(reynolds, diametre_m):
    """
    Calcule le facteur de frottement f de Darcy-Weisbach.

    Régime laminaire  (Re < 2300) : f = 64 / Re
    Régime turbulent  (Re >= 2300) : Swamee-Jain
    """

    if reynolds < 2300:
        return 64 / reynolds

    else:
        terme_rugosite = RUGOSITE_PVC / (3.7 * diametre_m)
        terme_reynolds = 5.74 / (reynolds ** 0.9)
        f = 0.25 / (math.log10(terme_rugosite + terme_reynolds)) ** 2
        return f