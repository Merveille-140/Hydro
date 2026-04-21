# ============================================================
# MODULE POMPE
# Dimensionnement de la pompe et du moteur
# ============================================================


# ============================================================
# CONSTANTES
# ============================================================

GRAVITE          = 9.81   # m/s²
DENSITE_EAU      = 1000   # kg/m³
RENDEMENT_POMPE  = 0.60   # rendement hydraulique de la pompe
RENDEMENT_MOTEUR = 0.90   # rendement du moteur électrique
COEFFICIENT_SECURITE = 1.15  # 15% de marge de sécurité


# ============================================================
# PUISSANCES COMMERCIALES NORMALISÉES (kW)
# ============================================================

PUISSANCES_COMMERCIALES = [
    0.25, 0.37, 0.55, 0.75,
    1.1,  1.5,  2.2,  3.0,
    3.7,  4.0,  5.5,  7.5,
    11.0, 15.0, 18.5, 22.0,
    30.0, 37.0, 45.0, 55.0,
]


# ============================================================
# FONCTION PRINCIPALE
# ============================================================

def calculer_pompe(debit_m3_h, HMT_m):
    """
    Calcule les puissances hydraulique, pompe et moteur.

    Paramètres :
        debit_m3_h : débit requis (m³/h)
        HMT_m      : hauteur manométrique totale (m)

    Retourne :
        dict avec Ph_kW, Pp_kW, Pm_kW, Pm_commercial_kW
    """

    # ─────────────────────────────────────────────────────
    # DÉBIT EN m³/s ET L/s
    # ─────────────────────────────────────────────────────

    debit_m3_s = debit_m3_h / 3600
    debit_L_s  = debit_m3_s * 1000

    # ─────────────────────────────────────────────────────
    # PUISSANCE HYDRAULIQUE Ph
    # Ph = ρ × g × Q × HMT
    # ─────────────────────────────────────────────────────

    Ph_W  = DENSITE_EAU * GRAVITE * debit_m3_s * HMT_m
    Ph_kW = Ph_W / 1000

    # ─────────────────────────────────────────────────────
    # PUISSANCE ABSORBÉE PAR LA POMPE Pp
    # Pp = Ph / η_pompe
    # ─────────────────────────────────────────────────────

    Pp_kW = Ph_kW / RENDEMENT_POMPE

    # ─────────────────────────────────────────────────────
    # PUISSANCE DU MOTEUR Pm (avec coeff. de sécurité)
    # Pm = (Pp / η_moteur) × coeff_securite
    # ─────────────────────────────────────────────────────

    Pm_kW = (Pp_kW / RENDEMENT_MOTEUR) * COEFFICIENT_SECURITE

    # ─────────────────────────────────────────────────────
    # PUISSANCE COMMERCIALE NORMALISÉE
    # On choisit la puissance commerciale immédiatement
    # supérieure à Pm calculé
    # ─────────────────────────────────────────────────────

    Pm_commercial_kW = choisir_puissance_commerciale(Pm_kW)

    return {
        "Ph_kW":             round(Ph_kW, 3),
        "Pp_kW":             round(Pp_kW, 3),
        "Pm_kW":             round(Pm_kW, 3),
        "Pm_commercial_kW":  Pm_commercial_kW,
        "debit_L_s":         round(debit_L_s, 3),
    }


# ============================================================
# CHOIX DE LA PUISSANCE COMMERCIALE
# ============================================================

def choisir_puissance_commerciale(Pm_kW):
    """
    Retourne la puissance commerciale normalisée
    immédiatement supérieure ou égale à Pm_kW.

    Paramètre :
        Pm_kW : puissance moteur calculée (kW)

    Retourne :
        puissance commerciale en kW
    """

    for puissance in PUISSANCES_COMMERCIALES:
        if puissance >= Pm_kW:
            return puissance

    # Si Pm dépasse toutes les puissances de la liste
    # on retourne la plus grande disponible
    return PUISSANCES_COMMERCIALES[-1]