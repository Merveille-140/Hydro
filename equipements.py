# ============================================================
# MODULE ÉQUIPEMENTS
# Données issues de DATA_BASE_Merv.xlsx — codées en dur
# Panneaux solaires, Batteries
# (Régulateurs supprimés — fournis avec chaque pompe)
# ============================================================


# ============================================================
# PANNEAUX SOLAIRES
# ============================================================

PANNEAUX = [
    # ── Hiteck Qindao ──────────────────────────────────────
    {"marque": "Hiteck Qindao", "type": "Polycristallin", "puissance_W": 275, "tension_V": 24, "Vmp_V": 32.2,  "Imp_A": 8.54, "Voc_V": 38.8, "Isc_A": 8.92},
    {"marque": "Hiteck Qindao", "type": "Polycristallin", "puissance_W": 270, "tension_V": 24, "Vmp_V": 31.9,  "Imp_A": 8.45, "Voc_V": 38.6, "Isc_A": 8.89},
    {"marque": "Hiteck Qindao", "type": "Polycristallin", "puissance_W": 265, "tension_V": 24, "Vmp_V": 31.7,  "Imp_A": 8.36, "Voc_V": 38.4, "Isc_A": 8.85},
    {"marque": "Hiteck Qindao", "type": "Polycristallin", "puissance_W": 260, "tension_V": 24, "Vmp_V": 30.8,  "Imp_A": 8.45, "Voc_V": 38.0, "Isc_A": 8.83},
    {"marque": "Hiteck Qindao", "type": "Polycristallin", "puissance_W": 255, "tension_V": 24, "Vmp_V": 30.6,  "Imp_A": 8.33, "Voc_V": 37.8, "Isc_A": 8.74},
    {"marque": "Hiteck Qindao", "type": "Polycristallin", "puissance_W": 250, "tension_V": 24, "Vmp_V": 30.5,  "Imp_A": 8.21, "Voc_V": 37.6, "Isc_A": 8.67},
    {"marque": "Hiteck Qindao", "type": "Polycristallin", "puissance_W": 165, "tension_V": 24, "Vmp_V": 18.2,  "Imp_A": 9.06, "Voc_V": 22.3, "Isc_A": 9.74},
    {"marque": "Hiteck Qindao", "type": "Polycristallin", "puissance_W": 160, "tension_V": 24, "Vmp_V": 18.1,  "Imp_A": 8.84, "Voc_V": 22.1, "Isc_A": 9.53},
    {"marque": "Hiteck Qindao", "type": "Polycristallin", "puissance_W": 150, "tension_V": 24, "Vmp_V": 17.9,  "Imp_A": 8.38, "Voc_V": 21.9, "Isc_A": 9.01},
    {"marque": "Hiteck Qindao", "type": "Polycristallin", "puissance_W": 145, "tension_V": 24, "Vmp_V": 18.8,  "Imp_A": 8.15, "Voc_V": 21.8, "Isc_A": 8.75},
    {"marque": "Hiteck Qindao", "type": "Polycristallin", "puissance_W": 140, "tension_V": 24, "Vmp_V": 17.7,  "Imp_A": 7.92, "Voc_V": 21.7, "Isc_A": 8.49},
    {"marque": "Hiteck Qindao", "type": "Polycristallin", "puissance_W": 135, "tension_V": 24, "Vmp_V": 17.6,  "Imp_A": 7.68, "Voc_V": 21.6, "Isc_A": 8.33},
    {"marque": "Hiteck Qindao", "type": "Polycristallin", "puissance_W": 130, "tension_V": 24, "Vmp_V": 17.5,  "Imp_A": 7.43, "Voc_V": 21.5, "Isc_A": 7.96},
    # ── Mercury ────────────────────────────────────────────
    {"marque": "Mercury", "type": "Polycristallin", "puissance_W": 260, "tension_V": 24, "Vmp_V": 30.4,  "Imp_A": 8.55, "Voc_V": 37.4, "Isc_A": 9.11},
    {"marque": "Mercury", "type": "Polycristallin", "puissance_W": 265, "tension_V": 24, "Vmp_V": 30.5,  "Imp_A": 8.68, "Voc_V": 37.5, "Isc_A": 9.21},
    {"marque": "Mercury", "type": "Polycristallin", "puissance_W": 270, "tension_V": 24, "Vmp_V": 30.9,  "Imp_A": 8.74, "Voc_V": 38.2, "Isc_A": 9.30},
    {"marque": "Mercury", "type": "Polycristallin", "puissance_W": 275, "tension_V": 24, "Vmp_V": 30.9,  "Imp_A": 8.90, "Voc_V": 38.2, "Isc_A": 9.35},
    {"marque": "Mercury", "type": "Polycristallin", "puissance_W": 280, "tension_V": 24, "Vmp_V": 31.1,  "Imp_A": 9.01, "Voc_V": 38.5, "Isc_A": 9.44},
    {"marque": "Mercury", "type": "Polycristallin", "puissance_W": 285, "tension_V": 24, "Vmp_V": 31.3,  "Imp_A": 9.10, "Voc_V": 38.6, "Isc_A": 9.54},
    {"marque": "Mercury", "type": "Polycristallin", "puissance_W": 315, "tension_V": 36, "Vmp_V": 36.7,  "Imp_A": 8.58, "Voc_V": 45.5, "Isc_A": 9.17},
    {"marque": "Mercury", "type": "Polycristallin", "puissance_W": 320, "tension_V": 36, "Vmp_V": 36.7,  "Imp_A": 8.72, "Voc_V": 45.5, "Isc_A": 9.32},
    {"marque": "Mercury", "type": "Polycristallin", "puissance_W": 325, "tension_V": 36, "Vmp_V": 36.9,  "Imp_A": 8.81, "Voc_V": 45.7, "Isc_A": 9.39},
    {"marque": "Mercury", "type": "Polycristallin", "puissance_W": 330, "tension_V": 36, "Vmp_V": 37.1,  "Imp_A": 8.89, "Voc_V": 45.7, "Isc_A": 9.47},
    {"marque": "Mercury", "type": "Monocristallin", "puissance_W": 280, "tension_V": 24, "Vmp_V": 31.5,  "Imp_A": 8.89, "Voc_V": 38.5, "Isc_A": 9.37},
    {"marque": "Mercury", "type": "Monocristallin", "puissance_W": 285, "tension_V": 24, "Vmp_V": 31.7,  "Imp_A": 8.99, "Voc_V": 38.7, "Isc_A": 9.49},
    {"marque": "Mercury", "type": "Monocristallin", "puissance_W": 290, "tension_V": 24, "Vmp_V": 31.9,  "Imp_A": 9.60, "Voc_V": 38.9, "Isc_A": 9.60},
    {"marque": "Mercury", "type": "Monocristallin", "puissance_W": 295, "tension_V": 24, "Vmp_V": 32.0,  "Imp_A": 9.16, "Voc_V": 39.1, "Isc_A": 9.69},
    {"marque": "Mercury", "type": "Monocristallin", "puissance_W": 300, "tension_V": 24, "Vmp_V": 32.3,  "Imp_A": 9.29, "Voc_V": 39.2, "Isc_A": 9.82},
    {"marque": "Mercury", "type": "Monocristallin", "puissance_W": 335, "tension_V": 36, "Vmp_V": 36.3,  "Imp_A": 9.23, "Voc_V": 44.2, "Isc_A": 9.77},
    {"marque": "Mercury", "type": "Monocristallin", "puissance_W": 340, "tension_V": 36, "Vmp_V": 36.5,  "Imp_A": 9.34, "Voc_V": 44.4, "Isc_A": 9.88},
    {"marque": "Mercury", "type": "Monocristallin", "puissance_W": 345, "tension_V": 24, "Vmp_V": 36.7,  "Imp_A": 9.40, "Voc_V": 44.6, "Isc_A": 9.94},
    {"marque": "Mercury", "type": "Monocristallin", "puissance_W": 350, "tension_V": 24, "Vmp_V": 37.0,  "Imp_A": 9.46, "Voc_V": 45.0, "Isc_A": 9.99},
    # ── Victron Energy ─────────────────────────────────────
    {"marque": "Victron Energy", "type": "Polycristallin", "puissance_W": 50,  "tension_V": 12, "Vmp_V": 18.0,  "Imp_A": 2.78, "Voc_V": 22.2, "Isc_A": 3.09},
    {"marque": "Victron Energy", "type": "Polycristallin", "puissance_W": 80,  "tension_V": 12, "Vmp_V": 18.0,  "Imp_A": 4.44, "Voc_V": 21.6, "Isc_A": 5.06},
    {"marque": "Victron Energy", "type": "Polycristallin", "puissance_W": 100, "tension_V": 12, "Vmp_V": 18.0,  "Imp_A": 5.56, "Voc_V": 21.6, "Isc_A": 6.32},
    {"marque": "Victron Energy", "type": "Polycristallin", "puissance_W": 140, "tension_V": 12, "Vmp_V": 20.0,  "Imp_A": 7.78, "Voc_V": 21.6, "Isc_A": 8.85},
    {"marque": "Victron Energy", "type": "Polycristallin", "puissance_W": 250, "tension_V": 24, "Vmp_V": 30.0,  "Imp_A": 8.33, "Voc_V": 36.75,"Isc_A": 8.94},
    {"marque": "Victron Energy", "type": "Polycristallin", "puissance_W": 290, "tension_V": 24, "Vmp_V": 36.0,  "Imp_A": 8.06, "Voc_V": 44.1, "Isc_A": 8.56},
    {"marque": "Victron Energy", "type": "Polycristallin", "puissance_W": 360, "tension_V": 24, "Vmp_V": 38.4,  "Imp_A": 9.38, "Voc_V": 47.4, "Isc_A": 10.24},
    {"marque": "Victron Energy", "type": "Monocristallin", "puissance_W": 50,  "tension_V": 12, "Vmp_V": 18.0,  "Imp_A": 2.78, "Voc_V": 22.2, "Isc_A": 3.16},
    {"marque": "Victron Energy", "type": "Monocristallin", "puissance_W": 80,  "tension_V": 12, "Vmp_V": 18.0,  "Imp_A": 4.45, "Voc_V": 22.3, "Isc_A": 4.90},
    {"marque": "Victron Energy", "type": "Monocristallin", "puissance_W": 100, "tension_V": 12, "Vmp_V": 18.3,  "Imp_A": 5.47, "Voc_V": 22.4, "Isc_A": 5.99},
    {"marque": "Victron Energy", "type": "Monocristallin", "puissance_W": 160, "tension_V": 12, "Vmp_V": 18.0,  "Imp_A": 8.90, "Voc_V": 22.4, "Isc_A": 9.90},
    {"marque": "Victron Energy", "type": "Monocristallin", "puissance_W": 175, "tension_V": 12, "Vmp_V": 19.4,  "Imp_A": 9.03, "Voc_V": 23.7, "Isc_A": 9.89},
    {"marque": "Victron Energy", "type": "Monocristallin", "puissance_W": 200, "tension_V": 24, "Vmp_V": 36.0,  "Imp_A": 5.55, "Voc_V": 43.2, "Isc_A": 6.10},
    {"marque": "Victron Energy", "type": "Monocristallin", "puissance_W": 305, "tension_V": 24, "Vmp_V": 32.5,  "Imp_A": 9.38, "Voc_V": 39.7, "Isc_A": 10.27},
    {"marque": "Victron Energy", "type": "Monocristallin", "puissance_W": 340, "tension_V": 24, "Vmp_V": 36.0,  "Imp_A": 9.44, "Voc_V": 45.5, "Isc_A": 10.30},
    {"marque": "Victron Energy", "type": "Monocristallin", "puissance_W": 360, "tension_V": 24, "Vmp_V": 38.4,  "Imp_A": 9.38, "Voc_V": 47.4, "Isc_A": 10.24},
    # ── Alex Solar ─────────────────────────────────────────
    {"marque": "Alex Solar", "type": "Polycristallin", "puissance_W": 245, "tension_V": 24, "Vmp_V": 31.1,  "Imp_A": 7.88, "Voc_V": 37.4, "Isc_A": 8.40},
    {"marque": "Alex Solar", "type": "Polycristallin", "puissance_W": 250, "tension_V": 24, "Vmp_V": 31.4,  "Imp_A": 7.96, "Voc_V": 37.6, "Isc_A": 8.45},
    {"marque": "Alex Solar", "type": "Polycristallin", "puissance_W": 255, "tension_V": 24, "Vmp_V": 31.6,  "Imp_A": 8.07, "Voc_V": 37.8, "Isc_A": 8.52},
    {"marque": "Alex Solar", "type": "Polycristallin", "puissance_W": 260, "tension_V": 24, "Vmp_V": 31.9,  "Imp_A": 8.15, "Voc_V": 38.0, "Isc_A": 8.58},
    {"marque": "Alex Solar", "type": "Polycristallin", "puissance_W": 265, "tension_V": 24, "Vmp_V": 32.7,  "Imp_A": 8.23, "Voc_V": 38.1, "Isc_A": 8.61},
    # ── Centro Solar ───────────────────────────────────────
    {"marque": "Centro Solar", "type": "Monocristallin", "puissance_W": 325, "tension_V": 24, "Vmp_V": 37.22, "Imp_A": 8.74, "Voc_V": 45.65,"Isc_A": 9.24},
    {"marque": "Centro Solar", "type": "Monocristallin", "puissance_W": 330, "tension_V": 24, "Vmp_V": 37.38, "Imp_A": 8.85, "Voc_V": 45.92,"Isc_A": 9.32},
    {"marque": "Centro Solar", "type": "Monocristallin", "puissance_W": 335, "tension_V": 24, "Vmp_V": 37.47, "Imp_A": 8.96, "Voc_V": 46.04,"Isc_A": 9.41},
    # ── Innova Solarline ───────────────────────────────────
    {"marque": "Innova Solarline", "type": "Polycristallin", "puissance_W": 255, "tension_V": 24, "Vmp_V": 30.43, "Imp_A": 8.38, "Voc_V": 37.67, "Isc_A": 8.91},
    {"marque": "Innova Solarline", "type": "Polycristallin", "puissance_W": 260, "tension_V": 24, "Vmp_V": 30.59, "Imp_A": 8.50, "Voc_V": 38.16, "Isc_A": 9.07},
    {"marque": "Innova Solarline", "type": "Polycristallin", "puissance_W": 265, "tension_V": 24, "Vmp_V": 30.74, "Imp_A": 8.62, "Voc_V": 38.29, "Isc_A": 9.24},
    {"marque": "Innova Solarline", "type": "Polycristallin", "puissance_W": 270, "tension_V": 24, "Vmp_V": 30.97, "Imp_A": 8.72, "Voc_V": 38.43, "Isc_A": 9.31},
    {"marque": "Innova Solarline", "type": "Polycristallin", "puissance_W": 300, "tension_V": 24, "Vmp_V": 36.95, "Imp_A": 8.12, "Voc_V": 45.21, "Isc_A": 8.59},
    {"marque": "Innova Solarline", "type": "Polycristallin", "puissance_W": 305, "tension_V": 24, "Vmp_V": 36.97, "Imp_A": 8.25, "Voc_V": 45.23, "Isc_A": 8.60},
    {"marque": "Innova Solarline", "type": "Polycristallin", "puissance_W": 310, "tension_V": 24, "Vmp_V": 37.00, "Imp_A": 8.38, "Voc_V": 45.50, "Isc_A": 9.35},
    {"marque": "Innova Solarline", "type": "Polycristallin", "puissance_W": 315, "tension_V": 24, "Vmp_V": 37.20, "Imp_A": 8.47, "Voc_V": 45.70, "Isc_A": 9.50},
    {"marque": "Innova Solarline", "type": "Polycristallin", "puissance_W": 320, "tension_V": 24, "Vmp_V": 37.50, "Imp_A": 8.53, "Voc_V": 46.00, "Isc_A": 9.50},
    {"marque": "Innova Solarline", "type": "Monocristallin", "puissance_W": 265, "tension_V": 24, "Vmp_V": 30.10, "Imp_A": 8.81, "Voc_V": 38.02, "Isc_A": 9.13},
    {"marque": "Innova Solarline", "type": "Monocristallin", "puissance_W": 270, "tension_V": 24, "Vmp_V": 30.50, "Imp_A": 8.85, "Voc_V": 38.21, "Isc_A": 9.21},
    {"marque": "Innova Solarline", "type": "Monocristallin", "puissance_W": 275, "tension_V": 24, "Vmp_V": 30.90, "Imp_A": 8.91, "Voc_V": 38.80, "Isc_A": 9.47},
    {"marque": "Innova Solarline", "type": "Monocristallin", "puissance_W": 280, "tension_V": 24, "Vmp_V": 31.30, "Imp_A": 8.96, "Voc_V": 39.10, "Isc_A": 9.50},
    {"marque": "Innova Solarline", "type": "Monocristallin", "puissance_W": 315, "tension_V": 36, "Vmp_V": 36.35, "Imp_A": 8.67, "Voc_V": 45.86, "Isc_A": 9.42},
    {"marque": "Innova Solarline", "type": "Monocristallin", "puissance_W": 320, "tension_V": 36, "Vmp_V": 36.53, "Imp_A": 8.76, "Voc_V": 45.73, "Isc_A": 9.49},
    {"marque": "Innova Solarline", "type": "Monocristallin", "puissance_W": 325, "tension_V": 36, "Vmp_V": 36.69, "Imp_A": 8.76, "Voc_V": 45.99, "Isc_A": 9.56},
    {"marque": "Innova Solarline", "type": "Monocristallin", "puissance_W": 330, "tension_V": 36, "Vmp_V": 36.75, "Imp_A": 8.96, "Voc_V": 46.12, "Isc_A": 9.63},
    # ── Jinko Solar ────────────────────────────────────────
    {"marque": "Jinko Solar", "type": "Polycristallin", "puissance_W": 245, "tension_V": 24, "Vmp_V": 30.1,  "Imp_A": 8.14, "Voc_V": 37.5, "Isc_A": 8.76},
    {"marque": "Jinko Solar", "type": "Polycristallin", "puissance_W": 250, "tension_V": 24, "Vmp_V": 30.5,  "Imp_A": 8.20, "Voc_V": 37.7, "Isc_A": 8.85},
    {"marque": "Jinko Solar", "type": "Polycristallin", "puissance_W": 255, "tension_V": 24, "Vmp_V": 30.8,  "Imp_A": 8.28, "Voc_V": 38.0, "Isc_A": 8.92},
    {"marque": "Jinko Solar", "type": "Polycristallin", "puissance_W": 260, "tension_V": 24, "Vmp_V": 31.1,  "Imp_A": 8.37, "Voc_V": 38.1, "Isc_A": 8.98},
    {"marque": "Jinko Solar", "type": "Polycristallin", "puissance_W": 265, "tension_V": 24, "Vmp_V": 31.4,  "Imp_A": 8.44, "Voc_V": 38.6, "Isc_A": 9.03},
]


# ============================================================
# BATTERIES
# ============================================================

BATTERIES = [
    # ── BAE ────────────────────────────────────────────────
    {"marque": "BAE", "type": "Plomb-acide GEL", "capacite_Ah": 1750, "tension_V": 2,  "rendement": 0.80, "temps_decharge_h": 100, "dod": 0.80},
    {"marque": "BAE", "type": "Plomb-acide GEL", "capacite_Ah": 2740, "tension_V": 2,  "rendement": 0.80, "temps_decharge_h": 100, "dod": 0.80},
    {"marque": "BAE", "type": "Plomb-acide GEL", "capacite_Ah": 3000, "tension_V": 2,  "rendement": 0.80, "temps_decharge_h": 100, "dod": 0.80},
    {"marque": "BAE", "type": "Plomb-acide GEL", "capacite_Ah": 3750, "tension_V": 2,  "rendement": 0.80, "temps_decharge_h": 100, "dod": 0.80},
    {"marque": "BAE", "type": "Plomb-acide GEL", "capacite_Ah": 4710, "tension_V": 2,  "rendement": 0.80, "temps_decharge_h": 100, "dod": 0.80},
    {"marque": "BAE", "type": "Plomb-acide GEL", "capacite_Ah": 121,  "tension_V": 2,  "rendement": 0.80, "temps_decharge_h": 10,  "dod": 0.80},
    {"marque": "BAE", "type": "Plomb-acide GEL", "capacite_Ah": 243,  "tension_V": 2,  "rendement": 0.80, "temps_decharge_h": 10,  "dod": 0.80},
    {"marque": "BAE", "type": "Plomb-acide GEL", "capacite_Ah": 610,  "tension_V": 2,  "rendement": 0.80, "temps_decharge_h": 10,  "dod": 0.80},
    {"marque": "BAE", "type": "Plomb-acide GEL", "capacite_Ah": 202,  "tension_V": 2,  "rendement": 0.80, "temps_decharge_h": 20,  "dod": 0.80},
    {"marque": "BAE", "type": "Plomb-acide GEL", "capacite_Ah": 404,  "tension_V": 2,  "rendement": 0.80, "temps_decharge_h": 20,  "dod": 0.80},
    # ── Fullriver ──────────────────────────────────────────
    {"marque": "Fullriver", "type": "Plomb-acide AGM", "capacite_Ah": 506,  "tension_V": 12, "rendement": 0.85, "temps_decharge_h": 20,  "dod": 0.91},
    {"marque": "Fullriver", "type": "Plomb-acide AGM", "capacite_Ah": 215,  "tension_V": 6,  "rendement": 0.85, "temps_decharge_h": 20,  "dod": 0.91},
    {"marque": "Fullriver", "type": "Plomb-acide AGM", "capacite_Ah": 415,  "tension_V": 6,  "rendement": 0.85, "temps_decharge_h": 20,  "dod": 0.91},
    {"marque": "Fullriver", "type": "Plomb-acide AGM", "capacite_Ah": 224,  "tension_V": 6,  "rendement": 0.85, "temps_decharge_h": 20,  "dod": 0.91},
    {"marque": "Fullriver", "type": "Plomb-acide AGM", "capacite_Ah": 200,  "tension_V": 12, "rendement": 0.85, "temps_decharge_h": 20,  "dod": 0.91},
    {"marque": "Fullriver", "type": "Plomb-acide AGM", "capacite_Ah": 210,  "tension_V": 12, "rendement": 0.85, "temps_decharge_h": 20,  "dod": 0.91},
    {"marque": "Fullriver", "type": "Plomb-acide AGM", "capacite_Ah": 215,  "tension_V": 12, "rendement": 0.85, "temps_decharge_h": 20,  "dod": 0.91},
    {"marque": "Fullriver", "type": "Plomb-acide AGM", "capacite_Ah": 220,  "tension_V": 12, "rendement": 0.85, "temps_decharge_h": 20,  "dod": 0.91},
    {"marque": "Fullriver", "type": "Plomb-acide AGM", "capacite_Ah": 240,  "tension_V": 12, "rendement": 0.85, "temps_decharge_h": 20,  "dod": 0.91},
    {"marque": "Fullriver", "type": "Plomb-acide AGM", "capacite_Ah": 260,  "tension_V": 12, "rendement": 0.85, "temps_decharge_h": 20,  "dod": 0.91},
    {"marque": "Fullriver", "type": "Plomb-acide AGM", "capacite_Ah": 100,  "tension_V": 12, "rendement": 0.85, "temps_decharge_h": 20,  "dod": 0.91},
    {"marque": "Fullriver", "type": "Plomb-acide AGM", "capacite_Ah": 110,  "tension_V": 12, "rendement": 0.85, "temps_decharge_h": 20,  "dod": 0.91},
    {"marque": "Fullriver", "type": "Plomb-acide AGM", "capacite_Ah": 200,  "tension_V": 2,  "rendement": 0.85, "temps_decharge_h": 100, "dod": 0.91},
    {"marque": "Fullriver", "type": "Plomb-acide AGM", "capacite_Ah": 1000, "tension_V": 2,  "rendement": 0.85, "temps_decharge_h": 100, "dod": 0.91},
    {"marque": "Fullriver", "type": "Plomb-acide GEL", "capacite_Ah": 2290, "tension_V": 12, "rendement": 0.85, "temps_decharge_h": 20,  "dod": 0.91},
    {"marque": "Fullriver", "type": "Plomb-acide GEL", "capacite_Ah": 80,   "tension_V": 12, "rendement": 0.85, "temps_decharge_h": 20,  "dod": 0.91},
    {"marque": "Fullriver", "type": "Plomb-acide GEL", "capacite_Ah": 115,  "tension_V": 12, "rendement": 0.85, "temps_decharge_h": 20,  "dod": 0.91},
    {"marque": "Fullriver", "type": "Plomb-acide GEL", "capacite_Ah": 120,  "tension_V": 12, "rendement": 0.85, "temps_decharge_h": 20,  "dod": 0.91},
    {"marque": "Fullriver", "type": "Plomb-acide GEL", "capacite_Ah": 140,  "tension_V": 12, "rendement": 0.85, "temps_decharge_h": 20,  "dod": 0.91},
    # ── Hoppecke ───────────────────────────────────────────
    {"marque": "Hoppecke", "type": "Plomb-acide GEL", "capacite_Ah": 160,  "tension_V": 12, "rendement": 0.80, "temps_decharge_h": 10,  "dod": 0.80},
    {"marque": "Hoppecke", "type": "Plomb-acide GEL", "capacite_Ah": 80,   "tension_V": 12, "rendement": 0.80, "temps_decharge_h": 100, "dod": 0.80},
    {"marque": "Hoppecke", "type": "Plomb-acide GEL", "capacite_Ah": 130,  "tension_V": 6,  "rendement": 0.80, "temps_decharge_h": 10,  "dod": 0.80},
    {"marque": "Hoppecke", "type": "Plomb-acide GEL", "capacite_Ah": 170,  "tension_V": 6,  "rendement": 0.80, "temps_decharge_h": 10,  "dod": 0.80},
    {"marque": "Hoppecke", "type": "Plomb-acide GEL", "capacite_Ah": 200,  "tension_V": 2,  "rendement": 0.80, "temps_decharge_h": 10,  "dod": 0.80},
    {"marque": "Hoppecke", "type": "Plomb-acide GEL", "capacite_Ah": 220,  "tension_V": 2,  "rendement": 0.80, "temps_decharge_h": 10,  "dod": 0.80},
    {"marque": "Hoppecke", "type": "Plomb-acide GEL", "capacite_Ah": 490,  "tension_V": 2,  "rendement": 0.80, "temps_decharge_h": 100, "dod": 0.80},
    {"marque": "Hoppecke", "type": "Plomb-acide GEL", "capacite_Ah": 520,  "tension_V": 2,  "rendement": 0.80, "temps_decharge_h": 100, "dod": 0.80},
    {"marque": "Hoppecke", "type": "Plomb-acide GEL", "capacite_Ah": 910,  "tension_V": 2,  "rendement": 0.80, "temps_decharge_h": 10,  "dod": 0.80},
    {"marque": "Hoppecke", "type": "Plomb-acide GEL", "capacite_Ah": 1200, "tension_V": 2,  "rendement": 0.80, "temps_decharge_h": 10,  "dod": 0.80},
    {"marque": "Hoppecke", "type": "Plomb-acide GEL", "capacite_Ah": 1500, "tension_V": 2,  "rendement": 0.80, "temps_decharge_h": 10,  "dod": 0.80},
    {"marque": "Hoppecke", "type": "Plomb-acide GEL", "capacite_Ah": 2000, "tension_V": 2,  "rendement": 0.80, "temps_decharge_h": 10,  "dod": 0.80},
    {"marque": "Hoppecke", "type": "Plomb-acide GEL", "capacite_Ah": 2500, "tension_V": 2,  "rendement": 0.80, "temps_decharge_h": 10,  "dod": 0.80},
    {"marque": "Hoppecke", "type": "Plomb-acide GEL", "capacite_Ah": 3000, "tension_V": 2,  "rendement": 0.80, "temps_decharge_h": 10,  "dod": 0.80},
    {"marque": "Hoppecke", "type": "Plomb-acide GEL", "capacite_Ah": 3330, "tension_V": 2,  "rendement": 0.80, "temps_decharge_h": 20,  "dod": 0.80},
    # ── Moll ───────────────────────────────────────────────
    {"marque": "Moll", "type": "Plomb-acide GEL", "capacite_Ah": 202,  "tension_V": 2, "rendement": 0.80, "temps_decharge_h": 20, "dod": 0.80},
    {"marque": "Moll", "type": "Plomb-acide GEL", "capacite_Ah": 335,  "tension_V": 2, "rendement": 0.80, "temps_decharge_h": 20, "dod": 0.80},
    {"marque": "Moll", "type": "Plomb-acide GEL", "capacite_Ah": 598,  "tension_V": 2, "rendement": 0.80, "temps_decharge_h": 20, "dod": 0.80},
    {"marque": "Moll", "type": "Plomb-acide GEL", "capacite_Ah": 2120, "tension_V": 2, "rendement": 0.80, "temps_decharge_h": 20, "dod": 0.80},
    {"marque": "Moll", "type": "Plomb-acide GEL", "capacite_Ah": 2320, "tension_V": 2, "rendement": 0.80, "temps_decharge_h": 72, "dod": 0.80},
    {"marque": "Moll", "type": "Plomb-acide GEL", "capacite_Ah": 305,  "tension_V": 2, "rendement": 0.80, "temps_decharge_h": 72, "dod": 0.80},
    {"marque": "Moll", "type": "Plomb-acide GEL", "capacite_Ah": 400,  "tension_V": 2, "rendement": 0.80, "temps_decharge_h": 10, "dod": 0.80},
    {"marque": "Moll", "type": "Plomb-acide GEL", "capacite_Ah": 610,  "tension_V": 2, "rendement": 0.80, "temps_decharge_h": 10, "dod": 0.80},
    {"marque": "Moll", "type": "Plomb-acide GEL", "capacite_Ah": 1570, "tension_V": 2, "rendement": 0.80, "temps_decharge_h": 10, "dod": 0.80},
    {"marque": "Moll", "type": "Plomb-acide GEL", "capacite_Ah": 2023, "tension_V": 2, "rendement": 0.80, "temps_decharge_h": 10, "dod": 0.80},
    # ── Rolls ──────────────────────────────────────────────
    {"marque": "Rolls", "type": "Plomb-acide AGM", "capacite_Ah": 3050, "tension_V": 6,  "rendement": 0.97, "temps_decharge_h": 10, "dod": 0.80},
    {"marque": "Rolls", "type": "Plomb-acide AGM", "capacite_Ah": 220,  "tension_V": 2,  "rendement": 0.97, "temps_decharge_h": 10, "dod": 0.80},
    {"marque": "Rolls", "type": "Plomb-acide AGM", "capacite_Ah": 500,  "tension_V": 2,  "rendement": 0.97, "temps_decharge_h": 10, "dod": 0.80},
    {"marque": "Rolls", "type": "Plomb-acide AGM", "capacite_Ah": 1000, "tension_V": 2,  "rendement": 0.97, "temps_decharge_h": 10, "dod": 0.80},
    # ── Tesvolt ────────────────────────────────────────────
    {"marque": "Tesvolt", "type": "Lithium-ion", "capacite_Ah": 3000, "tension_V": 48, "rendement": 0.90, "temps_decharge_h": 1, "dod": 1.00},
    {"marque": "Tesvolt", "type": "Lithium-ion", "capacite_Ah": 282,  "tension_V": 48, "rendement": 0.90, "temps_decharge_h": 1, "dod": 1.00},
    {"marque": "Tesvolt", "type": "Lithium-ion", "capacite_Ah": 376,  "tension_V": 48, "rendement": 0.90, "temps_decharge_h": 1, "dod": 1.00},
    {"marque": "Tesvolt", "type": "Lithium-ion", "capacite_Ah": 470,  "tension_V": 48, "rendement": 0.90, "temps_decharge_h": 1, "dod": 1.00},
    {"marque": "Tesvolt", "type": "Lithium-ion", "capacite_Ah": 564,  "tension_V": 48, "rendement": 0.90, "temps_decharge_h": 1, "dod": 1.00},
    {"marque": "Tesvolt", "type": "Lithium-ion", "capacite_Ah": 658,  "tension_V": 48, "rendement": 0.90, "temps_decharge_h": 1, "dod": 1.00},
    {"marque": "Tesvolt", "type": "Lithium-ion", "capacite_Ah": 752,  "tension_V": 48, "rendement": 0.90, "temps_decharge_h": 1, "dod": 1.00},
    {"marque": "Tesvolt", "type": "Lithium-ion", "capacite_Ah": 846,  "tension_V": 48, "rendement": 0.90, "temps_decharge_h": 1, "dod": 1.00},
    # ── Victron Energy ─────────────────────────────────────
    {"marque": "Victron Energy", "type": "Lithium-ion",      "capacite_Ah": 940,  "tension_V": 12, "rendement": 0.80, "temps_decharge_h": 1,  "dod": 0.95},
    {"marque": "Victron Energy", "type": "Lithium-ion",      "capacite_Ah": 60,   "tension_V": 12, "rendement": 0.80, "temps_decharge_h": 1,  "dod": 0.95},
    {"marque": "Victron Energy", "type": "Lithium-ion",      "capacite_Ah": 90,   "tension_V": 12, "rendement": 0.80, "temps_decharge_h": 1,  "dod": 0.95},
    {"marque": "Victron Energy", "type": "Lithium-ion",      "capacite_Ah": 180,  "tension_V": 24, "rendement": 0.80, "temps_decharge_h": 1,  "dod": 0.95},
    {"marque": "Victron Energy", "type": "Lithium-ion",      "capacite_Ah": 160,  "tension_V": 12, "rendement": 0.80, "temps_decharge_h": 1,  "dod": 0.95},
    {"marque": "Victron Energy", "type": "Plomb-acide AGM",  "capacite_Ah": 200,  "tension_V": 12, "rendement": 0.80, "temps_decharge_h": 20, "dod": 0.80},
    {"marque": "Victron Energy", "type": "Plomb-acide AGM",  "capacite_Ah": 220,  "tension_V": 12, "rendement": 0.80, "temps_decharge_h": 20, "dod": 0.80},
    {"marque": "Victron Energy", "type": "Plomb-acide AGM",  "capacite_Ah": 110,  "tension_V": 12, "rendement": 0.80, "temps_decharge_h": 20, "dod": 0.80},
    {"marque": "Victron Energy", "type": "Plomb-acide GEL",  "capacite_Ah": 130,  "tension_V": 2,  "rendement": 0.80, "temps_decharge_h": 10, "dod": 0.80},
    {"marque": "Victron Energy", "type": "Plomb-acide GEL",  "capacite_Ah": 910,  "tension_V": 2,  "rendement": 0.80, "temps_decharge_h": 10, "dod": 0.80},
    {"marque": "Victron Energy", "type": "Plomb-acide GEL",  "capacite_Ah": 1210, "tension_V": 2,  "rendement": 0.80, "temps_decharge_h": 10, "dod": 0.80},
    {"marque": "Victron Energy", "type": "Plomb-acide GEL",  "capacite_Ah": 1520, "tension_V": 2,  "rendement": 0.80, "temps_decharge_h": 10, "dod": 0.80},
    {"marque": "Victron Energy", "type": "Plomb-acide GEL",  "capacite_Ah": 1830, "tension_V": 2,  "rendement": 0.80, "temps_decharge_h": 10, "dod": 0.80},
    {"marque": "Victron Energy", "type": "Plomb-acide GEL",  "capacite_Ah": 2280, "tension_V": 2,  "rendement": 0.80, "temps_decharge_h": 10, "dod": 0.80},
    {"marque": "Victron Energy", "type": "Plomb-acide GEL",  "capacite_Ah": 3040, "tension_V": 2,  "rendement": 0.80, "temps_decharge_h": 10, "dod": 0.80},
    {"marque": "Victron Energy", "type": "Plomb-acide GEL",  "capacite_Ah": 3800, "tension_V": 2,  "rendement": 0.80, "temps_decharge_h": 10, "dod": 0.80},
    # ── Yongda power ───────────────────────────────────────
    {"marque": "Yongda power", "type": "Plomb-acide GEL", "capacite_Ah": 4560, "tension_V": 40, "rendement": 0.80, "temps_decharge_h": 10,  "dod": 0.80},
    {"marque": "Yongda power", "type": "Plomb-acide GEL", "capacite_Ah": 40,   "tension_V": 12, "rendement": 0.80, "temps_decharge_h": 10,  "dod": 0.80},
    {"marque": "Yongda power", "type": "Plomb-acide GEL", "capacite_Ah": 65,   "tension_V": 12, "rendement": 0.80, "temps_decharge_h": 10,  "dod": 0.80},
    {"marque": "Yongda power", "type": "Plomb-acide GEL", "capacite_Ah": 70,   "tension_V": 12, "rendement": 0.80, "temps_decharge_h": 10,  "dod": 0.80},
    {"marque": "Yongda power", "type": "Plomb-acide GEL", "capacite_Ah": 75,   "tension_V": 12, "rendement": 0.80, "temps_decharge_h": 10,  "dod": 0.80},
    {"marque": "Yongda power", "type": "Plomb-acide GEL", "capacite_Ah": 100,  "tension_V": 12, "rendement": 0.80, "temps_decharge_h": 10,  "dod": 0.80},
    {"marque": "Yongda power", "type": "Plomb-acide GEL", "capacite_Ah": 150,  "tension_V": 12, "rendement": 0.80, "temps_decharge_h": 10,  "dod": 0.80},
    {"marque": "Yongda power", "type": "Plomb-acide GEL", "capacite_Ah": 180,  "tension_V": 12, "rendement": 0.80, "temps_decharge_h": 20,  "dod": 0.80},
    {"marque": "Yongda power", "type": "Plomb-acide GEL", "capacite_Ah": 200,  "tension_V": 12, "rendement": 0.80, "temps_decharge_h": 20,  "dod": 0.80},
    {"marque": "Yongda power", "type": "Plomb-acide GEL", "capacite_Ah": 210,  "tension_V": 12, "rendement": 0.80, "temps_decharge_h": 20,  "dod": 0.80},
    {"marque": "Yongda power", "type": "Plomb-acide GEL", "capacite_Ah": 250,  "tension_V": 2,  "rendement": 0.80, "temps_decharge_h": 100, "dod": 0.80},
    {"marque": "Yongda power", "type": "Plomb-acide GEL", "capacite_Ah": 500,  "tension_V": 2,  "rendement": 0.80, "temps_decharge_h": 100, "dod": 0.80},
    {"marque": "Yongda power", "type": "Plomb-acide GEL", "capacite_Ah": 1000, "tension_V": 2,  "rendement": 0.80, "temps_decharge_h": 100, "dod": 0.80},
    {"marque": "Yongda power", "type": "Plomb-acide GEL", "capacite_Ah": 1500, "tension_V": 2,  "rendement": 0.80, "temps_decharge_h": 100, "dod": 0.80},
    {"marque": "Yongda power", "type": "Plomb-acide GEL", "capacite_Ah": 2930, "tension_V": 2,  "rendement": 0.80, "temps_decharge_h": 100, "dod": 0.80},
    {"marque": "Yongda power", "type": "Plomb-acide GEL", "capacite_Ah": 2320, "tension_V": 2,  "rendement": 0.80, "temps_decharge_h": 100, "dod": 0.80},
]


# ============================================================
# FONCTIONS DE RECHERCHE — PANNEAUX
# ============================================================

def get_marques_panneaux():
    marques = []
    for p in PANNEAUX:
        if p["marque"] not in marques:
            marques.append(p["marque"])
    return sorted(marques)


def get_modeles_panneaux(marque):
    return [p for p in PANNEAUX if p["marque"] == marque]


# ============================================================
# FONCTIONS DE RECHERCHE — BATTERIES
# ============================================================

def get_marques_batteries():
    marques = []
    for b in BATTERIES:
        if b["marque"] not in marques:
            marques.append(b["marque"])
    return sorted(marques)


def get_modeles_batteries(marque):
    return [b for b in BATTERIES if b["marque"] == marque]