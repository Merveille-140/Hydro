# ============================================================
# MODULE COÛT ESTIMATIF
# Sources : Senegrid 2025, SOS Énergie 2024, Senemarket 2025,
#           HélioBénin 2025 (All-in-One),
#           senegrid.sn/onduleur-solaire/prix (Classique/Hybride 2023)
# Marge k=1.15 selon AACE International Class 5
# ============================================================

PRIX_PANNEAU_PAR_WC       = 183       # FCFA/Wc — Senegrid 2025
PRIX_BATTERIE_GEL_AGM_AH  = 1250      # FCFA/Ah — Senegrid 2023
PRIX_BATTERIE_LITHIUM_AH  = 3750      # FCFA/Ah — Senegrid 2025
TAUX_INSTALLATION         = 0.15      # 15% du matériel
TAUX_DIVERS               = 0.10      # 10% du total
K_MARGE                   = 1.15      # Marge AACE Class 5

def prix_pompe(puissance_kW, alimentation):
    """Retourne le prix estimatif de la pompe selon puissance et type."""
    if alimentation == 'DC':
        if puissance_kW <= 1:
            return 450000
        elif puissance_kW <= 4:
            return 850000
        else:
            return 1500000
    else:  # AC
        if puissance_kW <= 0.5:
            return 50000
        elif puissance_kW <= 2:
            return 150000
        else:
            return 400000

def prix_groupe(puissance_kW):
    """Retourne le prix estimatif du groupe électrogène selon puissance."""
    if puissance_kW <= 3:
        return 250000
    elif puissance_kW <= 7:
        return 700000
    else:
        return 2600000

def prix_onduleur(puissance_kW, type_onduleur='Classique'):
    """
    Prix onduleur selon puissance et type.
    Sources :
    - Classique/Hybride : senegrid.sn/onduleur-solaire/prix (2023)
    - All-in-One : HélioBénin 2025
    """
    t = type_onduleur.lower()

    if 'classique' in t or 'offgrid' in t:
        if puissance_kW <= 1.0:   return 150000
        elif puissance_kW <= 2.0: return 240000
        elif puissance_kW <= 3.0: return 450000
        else:                     return 590000

    elif 'hybride' in t:
        if puissance_kW <= 3.0: return 450000
        else:                   return 590000

    elif 'all' in t or 'aio' in t:
        if puissance_kW <= 1.0:   return 189000
        elif puissance_kW <= 2.0: return 294000
        elif puissance_kW <= 3.0: return 472500
        elif puissance_kW <= 5.0: return 619500
        else:                     return 892500

    else:
        if puissance_kW <= 1.0:   return 150000
        elif puissance_kW <= 2.0: return 240000
        elif puissance_kW <= 3.0: return 450000
        else:                     return 590000


def calculer_cout(data):
    """
    Calcule le coût estimatif total de l'installation.
    data : dict contenant les résultats du dimensionnement
    """
    source   = data.get('source_energie', 'solaire')
    Pm_kW    = float(data.get('Pm_commercial_kW', 0))
    alimentation = 'DC' if source in ['solaire', 'hybride_batteries', 'hybride_groupe'] else 'AC'

    # Coût pompe
    C_pompe = prix_pompe(Pm_kW, alimentation)

    # Coût énergie (détaillé par poste)
    C_panneaux  = 0
    C_onduleur  = 0
    C_batteries = 0
    C_groupe    = 0

    if source in ['solaire', 'hybride_groupe', 'hybride_batteries']:
        nb_panneaux  = int(data.get('nb_panneaux', 0))
        puissance_wc = float(data.get('puissance_panneau_Wc', 300))
        C_panneaux   = nb_panneaux * puissance_wc * PRIX_PANNEAU_PAR_WC

    if source in ['solaire', 'hybride_batteries', 'hybride_groupe']:
        puissance_ond = float(data.get('puissance_onduleur_kW', 0))
        type_ond      = data.get('type_onduleur', 'Classique')
        if puissance_ond > 0:
            C_onduleur = prix_onduleur(puissance_ond, type_ond)

    if source == 'hybride_batteries':
        nb_batteries  = int(data.get('nb_batteries', 0))
        capacite_Ah   = float(data.get('capacite_batterie_Ah', 200))
        type_batterie = data.get('type_batterie', 'GEL')
        prix_ah       = PRIX_BATTERIE_LITHIUM_AH if 'lithium' in type_batterie.lower() else PRIX_BATTERIE_GEL_AGM_AH
        C_batteries   = nb_batteries * capacite_Ah * prix_ah

    if source in ['groupe', 'hybride_groupe']:
        puissance_groupe = float(data.get('puissance_groupe_kW', Pm_kW * 3))
        C_groupe         = prix_groupe(puissance_groupe)

    C_energie = C_panneaux + C_onduleur + C_batteries + C_groupe

    # Coût installation
    C_installation = TAUX_INSTALLATION * (C_pompe + C_energie)

    # Coût divers
    C_divers = TAUX_DIVERS * (C_pompe + C_energie + C_installation)

    # Coût total avec marge
    C_total = (C_pompe + C_energie + C_installation + C_divers) * K_MARGE

    return {
        'C_pompe':        round(C_pompe),
        'C_panneaux':     round(C_panneaux),
        'C_batteries':    round(C_batteries),
        'C_onduleur':     round(C_onduleur),
        'C_groupe':       round(C_groupe),
        'C_energie':      round(C_energie),
        'C_installation': round(C_installation),
        'C_divers':       round(C_divers),
        'C_total':        round(C_total),
        'k':              K_MARGE,
    }
