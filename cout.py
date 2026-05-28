# ============================================================
# MODULE COÛT ESTIMATIF
# Sources : Senegrid 2025, SOS Énergie 2024, Senemarket 2025
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

    # Coût énergie
    C_energie = 0

    if source in ['solaire', 'hybride_groupe', 'hybride_batteries']:
        nb_panneaux   = int(data.get('nb_panneaux', 0))
        puissance_wc  = float(data.get('puissance_panneau_Wc', 300))
        C_energie    += nb_panneaux * puissance_wc * PRIX_PANNEAU_PAR_WC

    if source == 'hybride_batteries':
        nb_batteries  = int(data.get('nb_batteries', 0))
        capacite_Ah   = float(data.get('capacite_batterie_Ah', 200))
        type_batterie = data.get('type_batterie', 'GEL')
        prix_ah = PRIX_BATTERIE_LITHIUM_AH if 'lithium' in type_batterie.lower() else PRIX_BATTERIE_GEL_AGM_AH
        C_energie    += nb_batteries * capacite_Ah * prix_ah

    if source in ['groupe', 'hybride_groupe']:
        puissance_groupe = float(data.get('puissance_groupe_kW', Pm_kW * 3))
        C_energie       += prix_groupe(puissance_groupe)

    # Coût installation
    C_installation = TAUX_INSTALLATION * (C_pompe + C_energie)

    # Coût divers
    C_divers = TAUX_DIVERS * (C_pompe + C_energie + C_installation)

    # Coût total avec marge
    C_total = (C_pompe + C_energie + C_installation + C_divers) * K_MARGE

    return {
        'C_pompe':        round(C_pompe),
        'C_energie':      round(C_energie),
        'C_installation': round(C_installation),
        'C_divers':       round(C_divers),
        'C_total':        round(C_total),
        'k':              K_MARGE
    }
