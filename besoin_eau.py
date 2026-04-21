# ============================================================
# MODULE BESOINS EN EAU
# Calcul ET0 (Penman-Monteith FAO-56) et besoins irrigation
# ============================================================

import math


# ============================================================
# COEFFICIENTS CULTURAUX Kc
# ============================================================

KC_CULTURES = {
    "tomate":       1.15,
    "maïs":         1.20,
    "riz":          1.20,
    "oignon":       1.05,
    "piment":       1.05,
    "haricot":      0.95,
    "manioc":       0.90,
    "chou":         1.05,
    "laitue":       1.00,
    "arachide":     1.15,
    "igname":       1.10,
    "gombo":        1.10,
    "sorgho":       1.00,
    "coton":        1.15,
    "patate_douce": 1.15,
}


# ============================================================
# EFFICACITÉ DES SYSTÈMES D'IRRIGATION
# ============================================================

EFFICACITE_IRRIGATION = {
    "goutte_a_goutte": 0.90,
    "aspersion":       0.75,
    "gravitaire":      0.55,
}


# ============================================================
# FRÉQUENCE D'ARROSAGE SELON LE SOL
# ============================================================

FREQUENCE_ARROSAGE = {
    "sableux":  1,
    "limoneux": 2,
    "argileux": 3,
}


# ============================================================
# CALCUL ET0 — PENMAN-MONTEITH FAO-56
# ============================================================

def calculer_ET0(T_max, T_min, humidite, vent, rayonnement):
    """
    Calcule l'évapotranspiration de référence ET0
    selon la méthode Penman-Monteith FAO-56.

    Paramètres :
        T_max       : température maximale (°C)
        T_min       : température minimale (°C)
        humidite    : humidité relative moyenne (%)
        vent        : vitesse du vent à 2m (m/s)
        rayonnement : rayonnement solaire (MJ/m²/jour)

    Retourne :
        ET0 en mm/jour
    """

    # Température moyenne
    T_moy = (T_max + T_min) / 2

    # Pression de vapeur saturante (kPa)
    es = (
        0.6108 * math.exp((17.27 * T_max) / (T_max + 237.3))
        + 0.6108 * math.exp((17.27 * T_min) / (T_min + 237.3))
    ) / 2

    # Pression de vapeur réelle (kPa)
    ea = es * (humidite / 100)

    # Déficit de pression de vapeur
    deficit_vpd = es - ea

    # Pente de la courbe de pression de vapeur (kPa/°C)
    delta = (
        4098
        * 0.6108
        * math.exp((17.27 * T_moy) / (T_moy + 237.3))
        / (T_moy + 237.3) ** 2
    )

    # Constante psychrométrique (kPa/°C) à altitude ~200m
    gamma = 0.0674

    # Rayonnement net estimé (MJ/m²/jour)
    # Rns = rayonnement net solaire (alpha = 0.23 pour gazon de référence)
    Rns = (1 - 0.23) * rayonnement

    # Rayonnement net thermique (simplifié)
    Rnl = 0.1 * rayonnement

    # Rayonnement net total
    Rn = Rns - Rnl

    # Flux de chaleur du sol (négligeable sur base journalière)
    G = 0

    # ET0 Penman-Monteith
    numerateur = (
        0.408 * delta * (Rn - G)
        + gamma * (900 / (T_moy + 273)) * vent * deficit_vpd
    )

    denominateur = delta + gamma * (1 + 0.34 * vent)

    ET0 = numerateur / denominateur

    return round(max(ET0, 0), 2)


# ============================================================
# CALCUL DES BESOINS EN EAU D'IRRIGATION
# ============================================================

def calculer_besoins_eau(
    culture,
    superficie_ha,
    systeme_irrigation,
    type_sol,
    ET0,
    kc_manuel=None
):
    """
    Calcule les besoins en eau journaliers d'une culture.

    Paramètres :
        culture            : nom de la culture
        superficie_ha      : superficie en hectares
        systeme_irrigation : type de système d'irrigation
        type_sol           : type de sol
        ET0                : évapotranspiration de référence (mm/jour)
        kc_manuel          : coefficient cultural manuel (si culture = 'autre')

    Retourne :
        dict avec tous les résultats de besoins
    """

    # ─────────────────────────────────────────────────────
    # VALIDATION DES ENTRÉES
    # ─────────────────────────────────────────────────────

    if superficie_ha <= 0:
        raise ValueError("La superficie doit être supérieure à zéro.")

    if ET0 <= 0:
        raise ValueError("ET0 doit être supérieur à zéro.")

    if systeme_irrigation not in EFFICACITE_IRRIGATION:
        raise ValueError(
            "Système d'irrigation non reconnu : " + systeme_irrigation
        )

    # ─────────────────────────────────────────────────────
    # COEFFICIENT CULTURAL Kc
    # ─────────────────────────────────────────────────────

    if culture == 'autre' and kc_manuel:
        kc = float(kc_manuel)

    elif culture in KC_CULTURES:
        kc = KC_CULTURES[culture]

    else:
        # Valeur par défaut si culture inconnue
        kc = 1.0

    # ─────────────────────────────────────────────────────
    # EVAPOTRANSPIRATION DE LA CULTURE ETc
    # ─────────────────────────────────────────────────────

    ETc_mm_jour = ET0 * kc

    # ─────────────────────────────────────────────────────
    # BESOIN NET EN EAU (m³/jour)
    # 1 mm/jour sur 1 ha = 10 m³/jour
    # ─────────────────────────────────────────────────────

    besoin_net_m3_jour = ETc_mm_jour * superficie_ha * 10

    # ─────────────────────────────────────────────────────
    # EFFICACITÉ D'IRRIGATION
    # ─────────────────────────────────────────────────────

    efficacite = EFFICACITE_IRRIGATION[systeme_irrigation]

    # ─────────────────────────────────────────────────────
    # BESOIN BRUT EN EAU (m³/jour)
    # Tient compte des pertes du système d'irrigation
    # ─────────────────────────────────────────────────────

    besoin_brut_m3_jour = besoin_net_m3_jour / efficacite

    # ─────────────────────────────────────────────────────
    # FRÉQUENCE D'ARROSAGE
    # ─────────────────────────────────────────────────────

    frequence = FREQUENCE_ARROSAGE.get(type_sol, 1)

    # ─────────────────────────────────────────────────────
    # BESOIN PAR SESSION D'ARROSAGE (m³)
    # ─────────────────────────────────────────────────────

    besoin_session_m3 = besoin_brut_m3_jour * frequence

    return {
        "ETc":                      round(ETc_mm_jour, 2),
        "besoin_net_m3_jour":       round(besoin_net_m3_jour, 2),
        "besoin_brut_m3_jour":      round(besoin_brut_m3_jour, 2),
        "besoin_session_m3":        round(besoin_session_m3, 2),
        "frequence_arrosage_jours": frequence,
        "kc_utilise":               round(kc, 2),
        "efficacite_irrigation":    efficacite,
    }