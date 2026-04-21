# ============================================================
# MODULE GÉNÉRATION PDF
# Rapport professionnel de dimensionnement SolarPump
# Style sobre et lisible
# ============================================================

from reportlab.lib.pagesizes   import A4
from reportlab.lib             import colors
from reportlab.lib.styles      import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units       import cm
from reportlab.platypus        import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    PageBreak
)
from reportlab.lib.enums       import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from io                        import BytesIO
from datetime                  import datetime


# ============================================================
# PALETTE DE COULEURS — SOBRE ET PROFESSIONNELLE
# ============================================================

VERT_TITRE   = colors.HexColor("#166534")
VERT_LEGER   = colors.HexColor("#f0fdf4")
GRIS_TITRE   = colors.HexColor("#1e293b")
GRIS_TEXTE   = colors.HexColor("#475569")
GRIS_LIGNE   = colors.HexColor("#e2e8f0")
GRIS_FOND    = colors.HexColor("#f8fafc")
NOIR         = colors.HexColor("#0f172a")
BLANC        = colors.white


# ============================================================
# STYLES
# ============================================================

def creer_styles():

    # Titre page de garde
    titre_garde = ParagraphStyle(
        name      = 'TitreGarde',
        fontName  = 'Helvetica-Bold',
        fontSize  = 28,
        textColor = BLANC,
        alignment = TA_CENTER,
        spaceAfter = 6,
    )

    # Sous-titre page de garde
    sous_titre_garde = ParagraphStyle(
        name      = 'SousTitreGarde',
        fontName  = 'Helvetica',
        fontSize  = 13,
        textColor = colors.HexColor("#bbf7d0"),
        alignment = TA_CENTER,
        spaceAfter = 4,
    )

    # Titre de section
    titre_section = ParagraphStyle(
        name        = 'TitreSection',
        fontName    = 'Helvetica-Bold',
        fontSize    = 11,
        textColor   = VERT_TITRE,
        spaceBefore = 14,
        spaceAfter  = 6,
        borderPad   = 4,
    )

    # Texte normal
    normal = ParagraphStyle(
        name      = 'NormalCustom',
        fontName  = 'Helvetica',
        fontSize  = 9,
        textColor = GRIS_TEXTE,
        spaceAfter = 3,
        leading   = 14,
    )

    # Texte gras
    gras = ParagraphStyle(
        name      = 'Gras',
        fontName  = 'Helvetica-Bold',
        fontSize  = 9,
        textColor = NOIR,
        spaceAfter = 3,
    )

    # Pied de page
    pied = ParagraphStyle(
        name      = 'Pied',
        fontName  = 'Helvetica',
        fontSize  = 8,
        textColor = GRIS_TEXTE,
        alignment = TA_CENTER,
    )

    # Info page de garde
    info_garde = ParagraphStyle(
        name      = 'InfoGarde',
        fontName  = 'Helvetica',
        fontSize  = 11,
        textColor = BLANC,
        alignment = TA_CENTER,
        spaceAfter = 6,
    )

    # Label page de garde
    label_garde = ParagraphStyle(
        name      = 'LabelGarde',
        fontName  = 'Helvetica',
        fontSize  = 9,
        textColor = colors.HexColor("#bbf7d0"),
        alignment = TA_CENTER,
        spaceAfter = 2,
    )

    return {
        "titre_garde":      titre_garde,
        "sous_titre_garde": sous_titre_garde,
        "titre_section":    titre_section,
        "normal":           normal,
        "gras":             gras,
        "pied":             pied,
        "info_garde":       info_garde,
        "label_garde":      label_garde,
    }


# ============================================================
# STYLE TABLEAU SIMPLE
# ============================================================

def style_tableau():
    return TableStyle([
        # En-tête
        ('BACKGROUND',    (0, 0), (-1, 0),  VERT_TITRE),
        ('TEXTCOLOR',     (0, 0), (-1, 0),  BLANC),
        ('FONTNAME',      (0, 0), (-1, 0),  'Helvetica-Bold'),
        ('FONTSIZE',      (0, 0), (-1, 0),  9),
        ('ALIGN',         (0, 0), (-1, 0),  'LEFT'),
        ('TOPPADDING',    (0, 0), (-1, 0),  7),
        ('BOTTOMPADDING', (0, 0), (-1, 0),  7),
        ('LEFTPADDING',   (0, 0), (-1, 0),  10),

        # Données
        ('FONTNAME',      (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE',      (0, 1), (-1, -1), 9),
        ('TEXTCOLOR',     (0, 1), (0, -1),  GRIS_TEXTE),
        ('TEXTCOLOR',     (1, 1), (1, -1),  NOIR),
        ('FONTNAME',      (1, 1), (1, -1),  'Helvetica-Bold'),
        ('ALIGN',         (0, 1), (0, -1),  'LEFT'),
        ('ALIGN',         (1, 1), (1, -1),  'RIGHT'),
        ('TOPPADDING',    (0, 1), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
        ('LEFTPADDING',   (0, 0), (-1, -1), 10),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 10),

        # Alternance lignes
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [BLANC, GRIS_FOND]),

        # Bordures légères
        ('GRID',          (0, 0), (-1, -1), 0.3, GRIS_LIGNE),
        ('LINEBELOW',     (0, 0), (-1, 0),  1.0, VERT_TITRE),
    ])


def style_tableau_equipement():
    return TableStyle([
        ('BACKGROUND',    (0, 0), (-1, 0),  GRIS_FOND),
        ('TEXTCOLOR',     (0, 0), (-1, 0),  VERT_TITRE),
        ('FONTNAME',      (0, 0), (-1, 0),  'Helvetica-Bold'),
        ('FONTSIZE',      (0, 0), (-1, 0),  9),
        ('ALIGN',         (0, 0), (-1, -1), 'LEFT'),
        ('TOPPADDING',    (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING',   (0, 0), (-1, -1), 10),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 10),
        ('FONTNAME',      (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE',      (0, 1), (-1, -1), 9),
        ('TEXTCOLOR',     (0, 1), (-1, -1), NOIR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [BLANC, GRIS_FOND]),
        ('GRID',          (0, 0), (-1, -1), 0.3, GRIS_LIGNE),
    ])


# ============================================================
# LIGNE DE SÉPARATION
# ============================================================

def separateur():
    return HRFlowable(
        width      = "100%",
        thickness  = 0.5,
        color      = GRIS_LIGNE,
        spaceAfter = 6,
        spaceBefore = 2,
    )


def separateur_section():
    return HRFlowable(
        width      = "100%",
        thickness  = 1.5,
        color      = VERT_TITRE,
        spaceAfter = 8,
        spaceBefore = 2,
    )
# ============================================================
# FONCTION PRINCIPALE
# ============================================================

def generer_rapport(data):

    buffer = BytesIO()
    styles = creer_styles()

    doc = SimpleDocTemplate(
        buffer,
        pagesize     = A4,
        leftMargin   = 2.0 * cm,
        rightMargin  = 2.0 * cm,
        topMargin    = 1.5 * cm,
        bottomMargin = 2.0 * cm,
    )

    contenu = []

    # Page de garde
    contenu += page_de_garde(data, styles)
    contenu.append(PageBreak())

    # Sections
    contenu += section_identification(data, styles)
    contenu += section_localisation(data, styles)
    contenu += section_besoins(data, styles)
    contenu += section_hydraulique(data, styles)
    contenu += section_pompe(data, styles)
    contenu += section_energie(data, styles)
    contenu += section_equipements(data, styles)
    contenu += section_conclusion(data, styles)
    contenu += pied_de_page(styles)

    doc.build(contenu)
    return buffer


# ============================================================
# PAGE DE GARDE
# ============================================================

def page_de_garde(data, styles):

    elements = []
    date_str = datetime.now().strftime("%d/%m/%Y")

    # Bandeau principal vert
    bandeau_data = [[
        Paragraph("SolarPump", styles["titre_garde"]),
    ]]
    bandeau = Table(bandeau_data, colWidths=[17.0 * cm])
    bandeau.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, -1), VERT_TITRE),
        ('TOPPADDING',    (0, 0), (-1, -1), 30),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(bandeau)

    # Sous-titre
    sous_data = [[
        Paragraph(
            "Rapport de dimensionnement — Système de pompage solaire",
            styles["sous_titre_garde"]
        ),
    ]]
    sous_table = Table(sous_data, colWidths=[17.0 * cm])
    sous_table.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, -1), colors.HexColor("#15803d")),
        ('TOPPADDING',    (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 30),
    ]))
    elements.append(sous_table)
    elements.append(Spacer(1, 1.5 * cm))

    # Informations projet
    nom_projet    = data.get('nom_projet', 'Non renseigné')
    realise_par   = data.get('realise_par', 'Non renseigné')
    date_projet   = data.get('date_projet', date_str)

    infos_data = [
        [
            Paragraph("PROJET", styles["label_garde"]),
            Paragraph("RÉALISÉ PAR", styles["label_garde"]),
            Paragraph("DATE", styles["label_garde"]),
        ],
        [
            Paragraph(nom_projet, styles["info_garde"]),
            Paragraph(realise_par, styles["info_garde"]),
            Paragraph(date_projet, styles["info_garde"]),
        ],
    ]

    infos_table = Table(
        infos_data,
        colWidths=[5.67 * cm, 5.67 * cm, 5.66 * cm]
    )
    infos_table.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, -1), VERT_TITRE),
        ('TOPPADDING',    (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('ALIGN',         (0, 0), (-1, -1), 'CENTER'),
        ('LINEAFTER',     (0, 0), (1, -1),  0.5, colors.HexColor("#15803d")),
    ]))
    elements.append(infos_table)
    elements.append(Spacer(1, 1.5 * cm))

    # Résumé technique
    source_energie = data.get('source_energie', '—')
    lat            = data.get('lat', '—')
    lon            = data.get('lon', '—')

    resume_data = [
        ["Paramètre", "Valeur"],
        ["Localisation",
            "Lat : " + str(lat) + "° — Lon : " + str(lon) + "°"],
        ["Source d'énergie",
            str(source_energie).replace('_', ' ').title()],
        ["HMT calculée",
            str(data.get('hydraulique', {}).get('HMT_m', '—')) + " m"],
        ["Débit calculé",
            str(data.get('hydraulique', {}).get('debit_m3_h', '—')) + " m³/h"],
        ["Puissance moteur",
            str(data.get('pompe', {}).get('Pm_kW', '—')) + " kW"],
    ]

    resume_table = Table(
        resume_data,
        colWidths=[8.5 * cm, 8.5 * cm]
    )
    resume_table.setStyle(style_tableau())
    elements.append(resume_table)

    return elements


# ============================================================
# SECTION 1 — IDENTIFICATION
# ============================================================

def section_identification(data, styles):

    elements = []

    elements.append(
        Paragraph("1. Identification du projet", styles["titre_section"])
    )
    elements.append(separateur_section())

    tableau_data = [
        ["Paramètre", "Valeur"],
        ["Nom du projet",
            str(data.get('nom_projet', 'Non renseigné'))],
        ["Réalisé par",
            str(data.get('realise_par', 'Non renseigné'))],
        ["Date",
            str(data.get('date_projet', datetime.now().strftime("%d/%m/%Y")))],
        ["Logiciel",
            "SolarPump v1.0 — Dimensionnement pompage solaire"],
        ["Date de génération",
            datetime.now().strftime("%d/%m/%Y à %H:%M")],
    ]

    tableau = Table(tableau_data, colWidths=[8.5 * cm, 8.5 * cm])
    tableau.setStyle(style_tableau())
    elements.append(tableau)
    elements.append(Spacer(1, 0.3 * cm))

    return elements


# ============================================================
# SECTION 2 — LOCALISATION
# ============================================================

def section_localisation(data, styles):

    elements = []

    elements.append(
        Paragraph("2. Localisation et données climatiques", styles["titre_section"])
    )
    elements.append(separateur_section())

    tableau_data = [
        ["Paramètre", "Valeur"],
        ["Latitude",
            str(data.get('lat', '—')) + "°"],
        ["Longitude",
            str(data.get('lon', '—')) + "°"],
        ["Température maximale",
            str(data.get('temperature_max', '—')) + " °C"],
        ["Température minimale",
            str(data.get('temperature_min', '—')) + " °C"],
        ["Irradiation solaire (mois critique)",
            str(data.get('irradiation', '—')) + " kWh/m²/jour"],
        ["ET0 maximale (Penman-Monteith FAO-56)",
            str(data.get('ET0_max', '—')) + " mm/jour"],
        ["Mois critique",
            str(data.get('mois_critique', '—'))],
    ]

    tableau = Table(tableau_data, colWidths=[8.5 * cm, 8.5 * cm])
    tableau.setStyle(style_tableau())
    elements.append(tableau)
    elements.append(Spacer(1, 0.3 * cm))

    return elements


# ============================================================
# SECTION 3 — BESOINS EN EAU
# ============================================================

def section_besoins(data, styles):

    elements = []
    besoins  = data.get('besoins', {})

    elements.append(
        Paragraph("3. Besoins en eau", styles["titre_section"])
    )
    elements.append(separateur_section())

    tableau_data = [
        ["Paramètre", "Valeur"],
        ["ETc / Besoin journalier",
            str(besoins.get('ETc', '—')) + " mm/jour"],
        ["Besoin net en eau",
            str(besoins.get('besoin_net_m3_jour', '—')) + " m³/jour"],
        ["Besoin brut en eau",
            str(besoins.get('besoin_brut_m3_jour', '—')) + " m³/jour"],
        ["Besoin par session",
            str(besoins.get('besoin_session_m3', '—')) + " m³"],
    ]

    tableau = Table(tableau_data, colWidths=[8.5 * cm, 8.5 * cm])
    tableau.setStyle(style_tableau())
    elements.append(tableau)
    elements.append(Spacer(1, 0.3 * cm))

    return elements


# ============================================================
# SECTION 4 — HYDRAULIQUE
# ============================================================

def section_hydraulique(data, styles):

    elements    = []
    hydraulique = data.get('hydraulique', {})

    elements.append(
        Paragraph("4. Dimensionnement hydraulique", styles["titre_section"])
    )
    elements.append(separateur_section())

    tableau_data = [
        ["Paramètre", "Valeur"],
        ["Débit Q",
            str(hydraulique.get('debit_m3_h', '—')) + " m³/h"
            + "  (" + str(hydraulique.get('debit_L_s', '—')) + " L/s)"],
        ["Hauteur géométrique",
            str(hydraulique.get('hauteur_geo_m', '—')) + " m"],
        ["Pertes de charge (Darcy-Weisbach)",
            str(hydraulique.get('pertes_charge_m', '—')) + " m"],
        ["Vitesse dans la canalisation",
            str(hydraulique.get('vitesse_m_s', '—')) + " m/s"],
        ["HMT totale",
            str(hydraulique.get('HMT_m', '—')) + " m"],
    ]

    tableau = Table(tableau_data, colWidths=[8.5 * cm, 8.5 * cm])
    tableau.setStyle(style_tableau())
    elements.append(tableau)
    elements.append(Spacer(1, 0.3 * cm))

    return elements


# ============================================================
# SECTION 5 — POMPE
# ============================================================

def section_pompe(data, styles):

    elements = []
    pompe    = data.get('pompe', {})

    elements.append(
        Paragraph("5. Dimensionnement de la pompe", styles["titre_section"])
    )
    elements.append(separateur_section())

    tableau_data = [
        ["Paramètre", "Valeur"],
        ["Puissance hydraulique Ph",
            str(pompe.get('Ph_kW', '—')) + " kW"],
        ["Puissance absorbée Pp",
            str(pompe.get('Pp_kW', '—')) + " kW"],
        ["Puissance moteur calculée Pm",
            str(pompe.get('Pm_kW', '—')) + " kW"],
        ["Puissance commerciale normalisée",
            str(pompe.get('Pm_commercial_kW', '—')) + " kW"],
    ]

    # Pompe choisie
    marque_pompe = data.get('marque_pompe', '')
    modele_pompe = data.get('modele_pompe', '')

    if marque_pompe and modele_pompe:
        tableau_data.append([
            "Pompe sélectionnée",
            str(marque_pompe) + " — " + str(modele_pompe)
        ])

    tableau = Table(tableau_data, colWidths=[8.5 * cm, 8.5 * cm])
    tableau.setStyle(style_tableau())
    elements.append(tableau)
    elements.append(Spacer(1, 0.3 * cm))

    return elements


# ============================================================
# SECTION 6 — ÉNERGIE
# ============================================================

def section_energie(data, styles):

    elements       = []
    energie        = data.get('energie', {})
    source_energie = data.get('source_energie', 'solaire')

    elements.append(
        Paragraph("6. Dimensionnement énergétique", styles["titre_section"])
    )
    elements.append(separateur_section())

    if source_energie == "solaire":
        tableau_data = [
            ["Paramètre", "Valeur"],
            ["Source d'énergie", "Solaire photovoltaïque"],
            ["Énergie journalière",
                str(energie.get('energie_jour_kWh', '—')) + " kWh/jour"],
            ["Puissance crête calculée",
                str(energie.get('puissance_crete_kWp', '—')) + " kWc"],
            ["Puissance crête réelle",
                str(energie.get('puissance_crete_reelle', '—')) + " kWc"],
            ["Nombre de panneaux 300 Wc",
                str(energie.get('nb_panneaux_300Wc', '—')) + " panneaux"],
            ["Tension système PV",
                str(energie.get('tension_pv', '—'))],
            ["Courant total champ PV",
                str(energie.get('courant_A', '—')) + " A"],
        ]

    elif source_energie == "groupe":
        tableau_data = [
            ["Paramètre", "Valeur"],
            ["Source d'énergie", "Groupe électrogène"],
            ["Énergie journalière",
                str(energie.get('energie_jour_kWh', '—')) + " kWh/jour"],
            ["Puissance groupe recommandée",
                str(energie.get('puissance_groupe_kW', '—')) + " kW"],
            ["Consommation gasoil / jour",
                str(energie.get('consommation_jour_litres', '—')) + " L"],
            ["Consommation gasoil / mois",
                str(energie.get('consommation_mois_litres', '—')) + " L"],
            ["Consommation gasoil / an",
                str(energie.get('consommation_annee_litres', '—')) + " L"],
        ]

    elif source_energie == "hybride_groupe":
        sol = energie.get('solaire', {})
        grp = energie.get('groupe',  {})
        tableau_data = [
            ["Paramètre", "Valeur"],
            ["Source d'énergie", "Hybride — Solaire 70% + Groupe 30%"],
            ["Énergie totale journalière",
                str(energie.get('energie_totale_kWh', '—')) + " kWh/jour"],
            ["— Puissance crête solaire",
                str(sol.get('puissance_crete_kWp', '—')) + " kWc"],
            ["— Nombre de panneaux",
                str(sol.get('nb_panneaux_300Wc', '—')) + " panneaux"],
            ["— Courant champ PV",
                str(sol.get('courant_A', '—')) + " A"],
            ["— Puissance groupe",
                str(grp.get('puissance_groupe_kW', '—')) + " kW"],
            ["— Consommation gasoil / jour",
                str(grp.get('consommation_jour_litres', '—')) + " L"],
            ["— Consommation gasoil / mois",
                str(grp.get('consommation_mois_litres', '—')) + " L"],
        ]

    elif source_energie == "hybride_batteries":
        sol = energie.get('solaire', {})
        tableau_data = [
            ["Paramètre", "Valeur"],
            ["Source d'énergie", "Hybride — Solaire + Batteries"],
            ["— Énergie journalière",
                str(sol.get('energie_jour_kWh', '—')) + " kWh/jour"],
            ["— Puissance crête solaire",
                str(sol.get('puissance_crete_kWp', '—')) + " kWc"],
            ["— Nombre de panneaux",
                str(sol.get('nb_panneaux_300Wc', '—')) + " panneaux"],
            ["— Courant champ PV",
                str(sol.get('courant_A', '—')) + " A"],
            ["— Énergie à stocker",
                str(energie.get('energie_stockage_kWh', '—')) + " kWh"],
            ["— Capacité totale batteries",
                str(energie.get('capacite_totale_Ah', '—')) + " Ah"],
            ["— Nombre de batteries",
                str(energie.get('nb_batteries', '—'))],
            ["— Tension batterie",
                str(energie.get('tension_batterie', '—'))],
            ["— Jours d'autonomie",
                str(energie.get('jours_autonomie', '—')) + " jour(s)"],
        ]

    else:
        tableau_data = [
            ["Paramètre", "Valeur"],
            ["Source d'énergie", str(source_energie)],
        ]

    tableau = Table(tableau_data, colWidths=[8.5 * cm, 8.5 * cm])
    tableau.setStyle(style_tableau())
    elements.append(tableau)
    elements.append(Spacer(1, 0.3 * cm))

    return elements


# ============================================================
# SECTION 7 — ÉQUIPEMENTS CHOISIS
# ============================================================

def section_equipements(data, styles):

    elements       = []
    source_energie = data.get('source_energie', '')
    equipements    = data.get('equipements', {})

    hasPV = source_energie in ['solaire', 'hybride_groupe', 'hybride_batteries']

    if not hasPV and not data.get('marque_pompe'):
        return elements

    elements.append(
        Paragraph("7. Équipements sélectionnés", styles["titre_section"])
    )
    elements.append(separateur_section())

    # Pompe
    marque_pompe = data.get('marque_pompe', '')
    modele_pompe = data.get('modele_pompe', '')

    if marque_pompe and modele_pompe:
        elements.append(
            Paragraph("Pompe", styles["gras"])
        )
        pompe_data = [
            ["Marque", "Modèle"],
            [str(marque_pompe), str(modele_pompe)],
        ]
        pompe_table = Table(pompe_data, colWidths=[8.5 * cm, 8.5 * cm])
        pompe_table.setStyle(style_tableau_equipement())
        elements.append(pompe_table)
        elements.append(Spacer(1, 0.2 * cm))

    if hasPV:

        # Panneau
        marque_pan  = equipements.get('marque_panneau', '')
        modele_pan  = equipements.get('modele_panneau', '')
        nb_panneaux = data.get('nb_panneaux_calcul', '')

        if marque_pan:
            elements.append(
                Paragraph("Panneau solaire", styles["gras"])
            )
            pan_data = [
                ["Marque", "Modèle", "Nombre calculé"],
                [
                    str(marque_pan),
                    str(modele_pan),
                    str(nb_panneaux) + " panneaux"
                ],
            ]
            pan_table = Table(
                pan_data,
                colWidths=[5.0 * cm, 8.0 * cm, 4.0 * cm]
            )
            pan_table.setStyle(style_tableau_equipement())
            elements.append(pan_table)
            elements.append(Spacer(1, 0.2 * cm))

        # Régulateur
        marque_reg  = equipements.get('marque_regulateur', '')
        modele_reg  = equipements.get('modele_regulateur', '')

        if marque_reg:
            elements.append(
                Paragraph("Régulateur de charge", styles["gras"])
            )
            reg_data = [
                ["Marque", "Modèle"],
                [str(marque_reg), str(modele_reg)],
            ]
            reg_table = Table(reg_data, colWidths=[8.5 * cm, 8.5 * cm])
            reg_table.setStyle(style_tableau_equipement())
            elements.append(reg_table)
            elements.append(Spacer(1, 0.2 * cm))

        # Batterie
        if source_energie == 'hybride_batteries':
            marque_bat  = equipements.get('marque_batterie', '')
            modele_bat  = equipements.get('modele_batterie', '')
            nb_bat      = data.get('energie', {}).get('nb_batteries', '')

            if marque_bat:
                elements.append(
                    Paragraph("Batterie", styles["gras"])
                )
                bat_data = [
                    ["Marque", "Modèle", "Nombre calculé"],
                    [
                        str(marque_bat),
                        str(modele_bat),
                        str(nb_bat) + " batteries"
                    ],
                ]
                bat_table = Table(
                    bat_data,
                    colWidths=[5.0 * cm, 8.0 * cm, 4.0 * cm]
                )
                bat_table.setStyle(style_tableau_equipement())
                elements.append(bat_table)
                elements.append(Spacer(1, 0.2 * cm))

    elements.append(Spacer(1, 0.3 * cm))
    return elements


# ============================================================
# SECTION 8 — CONCLUSION
# ============================================================

def section_conclusion(data, styles):

    elements = []

    elements.append(
        Paragraph("8. Conclusion", styles["titre_section"])
    )
    elements.append(separateur_section())

    hydraulique    = data.get('hydraulique', {})
    pompe          = data.get('pompe', {})
    source_energie = data.get('source_energie', '—')
    marque_pompe   = data.get('marque_pompe', '—')
    modele_pompe   = data.get('modele_pompe', '—')

    texte = (
        "Le présent rapport présente les résultats du dimensionnement "
        "du système de pompage. "
        "Le débit calculé est de <b>" +
        str(hydraulique.get('debit_m3_h', '—')) +
        " m³/h</b> pour une hauteur manométrique totale (HMT) de <b>" +
        str(hydraulique.get('HMT_m', '—')) +
        " m</b>. "
        "La puissance moteur nécessaire est de <b>" +
        str(pompe.get('Pm_kW', '—')) +
        " kW</b> (puissance commerciale normalisée : <b>" +
        str(pompe.get('Pm_commercial_kW', '—')) +
        " kW</b>). "
        "La source d'énergie retenue est : <b>" +
        str(source_energie).replace('_', ' ').title() +
        "</b>. "
        "La pompe sélectionnée est la <b>" +
        str(marque_pompe) + " " + str(modele_pompe) +
        "</b>."
    )

    style_conclusion = ParagraphStyle(
        name      = 'Conclusion',
        fontName  = 'Helvetica',
        fontSize  = 9,
        textColor = GRIS_TEXTE,
        leading   = 16,
        alignment = TA_JUSTIFY,
        spaceAfter = 10,
    )

    elements.append(Paragraph(texte, style_conclusion))
    elements.append(Spacer(1, 0.3 * cm))

    return elements


# ============================================================
# PIED DE PAGE
# ============================================================

def pied_de_page(styles):

    elements = []

    elements.append(Spacer(1, 0.8 * cm))
    elements.append(separateur())

    elements.append(
        Paragraph(
            "Rapport généré par SolarPump v1.0 · "
            "Les résultats sont donnés à titre indicatif "
            "et doivent être validés par un ingénieur qualifié.",
            styles["pied"]
        )
    )

    return elements