# ============================================================
# MODULE GÉNÉRATION PDF
# Rapport professionnel de dimensionnement HydroPump
# ============================================================

from reportlab.lib.pagesizes   import A4
from reportlab.lib             import colors
from reportlab.lib.styles      import ParagraphStyle
from reportlab.lib.units       import cm
from reportlab.platypus        import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, HRFlowable, PageBreak
)
from reportlab.lib.enums       import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from io                        import BytesIO
from datetime                  import datetime


# ============================================================
# PALETTE
# ============================================================

VERT_TITRE   = colors.HexColor("#166534")
VERT_LEGER   = colors.HexColor("#f0fdf4")
VERT_MOYEN   = colors.HexColor("#15803d")
VERT_ACCENT  = colors.HexColor("#22c55e")
GRIS_TEXTE   = colors.HexColor("#475569")
GRIS_LIGNE   = colors.HexColor("#e2e8f0")
GRIS_FOND    = colors.HexColor("#f8fafc")
GRIS_SOUS    = colors.HexColor("#94a3b8")
NOIR         = colors.HexColor("#0f172a")
BLANC        = colors.white


# ============================================================
# HELPERS
# ============================================================

def formater_date(date_str):
    if not date_str:
        return datetime.now().strftime("%d/%m/%Y")
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%d/%m/%Y")
    except Exception:
        return str(date_str)


def val_ou_nc(v):
    return str(v) if v and str(v) != '—' else 'Non calculé'


def unite_nb(valeur, singulier, pluriel_form):
    try:
        nb = int(float(str(valeur)))
    except Exception:
        return str(valeur)
    return str(nb) + " " + (singulier if nb <= 1 else pluriel_form)


# ============================================================
# STYLES
# ============================================================

def creer_styles():

    titre_garde = ParagraphStyle(
        name='TitreGarde', fontName='Helvetica-Bold',
        fontSize=28, textColor=BLANC, alignment=TA_CENTER, spaceAfter=4,
    )
    sous_titre_garde = ParagraphStyle(
        name='SousTitreGarde', fontName='Helvetica',
        fontSize=13, textColor=colors.HexColor("#bbf7d0"),
        alignment=TA_CENTER, spaceAfter=4,
    )
    titre_section = ParagraphStyle(
        name='TitreSection', fontName='Helvetica-Bold',
        fontSize=11, textColor=VERT_TITRE,
        spaceBefore=14, spaceAfter=6,
    )
    normal = ParagraphStyle(
        name='NormalCustom', fontName='Helvetica',
        fontSize=9, textColor=GRIS_TEXTE, spaceAfter=3, leading=14,
    )
    gras = ParagraphStyle(
        name='Gras', fontName='Helvetica-Bold',
        fontSize=9, textColor=NOIR, spaceAfter=3,
    )
    pied = ParagraphStyle(
        name='Pied', fontName='Helvetica',
        fontSize=8, textColor=GRIS_SOUS, alignment=TA_CENTER,
    )
    label_garde = ParagraphStyle(
        name='LabelGarde', fontName='Helvetica',
        fontSize=8, textColor=colors.HexColor("#bbf7d0"),
        alignment=TA_CENTER, spaceAfter=2,
    )
    info_garde = ParagraphStyle(
        name='InfoGarde', fontName='Helvetica-Bold',
        fontSize=10, textColor=BLANC,
        alignment=TA_CENTER, spaceAfter=4,
    )
    return {
        "titre_garde":      titre_garde,
        "sous_titre_garde": sous_titre_garde,
        "titre_section":    titre_section,
        "normal":           normal,
        "gras":             gras,
        "pied":             pied,
        "label_garde":      label_garde,
        "info_garde":       info_garde,
    }


# ============================================================
# STYLES TABLEAUX
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
        ('TOPPADDING',    (0, 1), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 7),
        ('LEFTPADDING',   (0, 0), (-1, -1), 10),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 10),
        # Alternance
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [BLANC, GRIS_FOND]),
        # Bordures
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
        ('TOPPADDING',    (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING',   (0, 0), (-1, -1), 10),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 10),
        ('FONTNAME',      (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE',      (0, 1), (-1, -1), 9),
        ('TEXTCOLOR',     (0, 1), (0, -1),  GRIS_TEXTE),
        ('TEXTCOLOR',     (1, 1), (1, -1),  NOIR),
        ('FONTNAME',      (1, 1), (1, -1),  'Helvetica-Bold'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [BLANC, GRIS_FOND]),
        ('GRID',          (0, 0), (-1, -1), 0.3, GRIS_LIGNE),
    ])


# ============================================================
# SÉPARATEURS
# ============================================================

def separateur():
    return HRFlowable(width="100%", thickness=0.5, color=GRIS_LIGNE,
                      spaceAfter=6, spaceBefore=2)


def separateur_section():
    return HRFlowable(width="100%", thickness=1.5, color=VERT_TITRE,
                      spaceAfter=8, spaceBefore=2)


# ============================================================
# FONCTION PRINCIPALE
# ============================================================

def generer_rapport(data):
    buffer = BytesIO()
    styles = creer_styles()

    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        leftMargin=2.0 * cm, rightMargin=2.0 * cm,
        topMargin=1.5 * cm, bottomMargin=2.0 * cm,
    )

    contenu = []
    contenu += page_de_garde(data, styles)
    contenu.append(PageBreak())
    contenu += section_identification(data, styles)
    contenu += section_localisation(data, styles)
    contenu += section_besoins(data, styles)
    contenu += section_hydraulique(data, styles)
    contenu += section_pompe(data, styles)
    contenu += section_energie(data, styles)
    contenu += section_equipements(data, styles)
    contenu += section_cout(data, styles)
    contenu += section_conclusion(data, styles)
    contenu += pied_de_page(styles)

    doc.build(contenu)
    return buffer


# ============================================================
# PAGE DE GARDE
# ============================================================

def page_de_garde(data, styles):
    elements = []

    # A) Bandeau logo
    logo_data = [[
        Paragraph(
            '<font color="#22c55e" size="22">●</font>'
            '  <font color="white" size="28"><b>HydroPump</b></font>',
            styles["titre_garde"]
        ),
    ]]
    logo_table = Table(logo_data, colWidths=[17.0 * cm])
    logo_table.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, -1), VERT_TITRE),
        ('TOPPADDING',    (0, 0), (-1, -1), 30),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('ALIGN',         (0, 0), (-1, -1), 'CENTER'),
    ]))
    elements.append(logo_table)

    # Sous-titre
    sous_data = [[
        Paragraph(
            "Rapport de dimensionnement — Système de pompage solaire",
            styles["sous_titre_garde"]
        ),
    ]]
    sous_table = Table(sous_data, colWidths=[17.0 * cm])
    sous_table.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, -1), VERT_MOYEN),
        ('TOPPADDING',    (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 30),
    ]))
    elements.append(sous_table)

    # B) Bandeau projet — 4 colonnes
    nom_projet  = str(data.get('nom_projet',  'Non renseigné'))
    nom_client  = str(data.get('nom_client',  'Non renseigné'))
    realise_par = str(data.get('realise_par', 'Non renseigné'))
    date_projet = formater_date(data.get('date_projet', ''))

    sep_color = colors.HexColor("#ffffff")
    infos_data = [
        [
            Paragraph("PROJET",      styles["label_garde"]),
            Paragraph("CLIENT",      styles["label_garde"]),
            Paragraph("RÉALISÉ PAR", styles["label_garde"]),
            Paragraph("DATE",        styles["label_garde"]),
        ],
        [
            Paragraph(nom_projet,  styles["info_garde"]),
            Paragraph(nom_client,  styles["info_garde"]),
            Paragraph(realise_par, styles["info_garde"]),
            Paragraph(date_projet, styles["info_garde"]),
        ],
    ]
    infos_table = Table(infos_data,
                        colWidths=[4.25 * cm, 4.25 * cm, 4.25 * cm, 4.25 * cm])
    infos_table.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, -1), VERT_TITRE),
        ('TOPPADDING',    (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('ALIGN',         (0, 0), (-1, -1), 'CENTER'),
        ('LINEAFTER',     (0, 0), (2, -1),  0.5, colors.HexColor("#ffffff33")),
    ]))
    elements.append(infos_table)
    elements.append(Spacer(1, 1.5 * cm))

    # D) Résumé technique
    cout = data.get('cout') or {}
    source_energie = data.get('source_energie', '—')
    lat = data.get('lat', '—')
    lon = data.get('lon', '—')
    hmt = str(data.get('hydraulique', {}).get('HMT_m', '—')) + " m"
    debit = str(data.get('hydraulique', {}).get('debit_m3_h', '—')) + " m³/h"
    pm = str(data.get('pompe', {}).get('Pm_kW', '—')) + " kW"

    resume_data = [
        ["Paramètre", "Valeur"],
        ["Localisation",     "Lat : " + str(lat) + "° — Lon : " + str(lon) + "°"],
        ["Source d'énergie", str(source_energie).replace('_', ' ').title()],
        ["Débit calculé",    debit],
        ["HMT calculée",     hmt],
        ["Puissance moteur", pm],
    ]

    if cout and cout.get('C_total'):
        resume_data.append([
            "Coût total estimatif",
            "{:,.0f}".format(cout.get('C_total', 0)).replace(',', ' ') + " FCFA"
        ])

    resume_table = Table(resume_data, colWidths=[8.5 * cm, 8.5 * cm])
    base = style_tableau()
    if cout and cout.get('C_total'):
        resume_table.setStyle(TableStyle([
            *base._cmds,
            ('FONTNAME',   (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('TEXTCOLOR',  (0, -1), (-1, -1), VERT_TITRE),
            ('BACKGROUND', (0, -1), (-1, -1), VERT_LEGER),
        ]))
    else:
        resume_table.setStyle(base)
    elements.append(resume_table)

    return elements


# ============================================================
# SECTION 1 — IDENTIFICATION
# ============================================================

def section_identification(data, styles):
    elements = []
    elements.append(Paragraph("1. Identification du projet", styles["titre_section"]))
    elements.append(separateur_section())

    tableau_data = [
        ["Paramètre", "Valeur"],
        ["Nom du projet",   str(data.get('nom_projet',  'Non renseigné'))],
        ["Nom du client",   str(data.get('nom_client',  'Non renseigné'))],
        ["Réalisé par",     str(data.get('realise_par', 'Non renseigné'))],
        ["Date",            formater_date(data.get('date_projet', ''))],
        ["Logiciel",        "HydroPump v1.0 — Dimensionnement pompage solaire"],
        ["Date de génération", datetime.now().strftime("%d/%m/%Y à %H:%M")],
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
    elements.append(Paragraph("2. Localisation et données climatiques", styles["titre_section"]))
    elements.append(separateur_section())

    tableau_data = [
        ["Paramètre", "Valeur"],
        ["Latitude",            str(data.get('lat', '—')) + "°"],
        ["Longitude",           str(data.get('lon', '—')) + "°"],
        ["Température maximale", str(data.get('temperature_max', '—')) + " °C"],
        ["Température minimale", str(data.get('temperature_min', '—')) + " °C"],
        ["Irradiation solaire (mois critique)",
            str(data.get('irradiation', '—')) + " kWh/m²/jour"],
        ["ET0 maximale (Penman-Monteith FAO-56)",
            str(data.get('ET0_max', '—')) + " mm/jour"],
        ["Mois critique", str(data.get('mois_critique', '—'))],
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
    besoins = data.get('besoins', {})
    elements.append(Paragraph("3. Besoins en eau", styles["titre_section"]))
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
    elements = []
    h = data.get('hydraulique', {})
    elements.append(Paragraph("4. Dimensionnement hydraulique", styles["titre_section"]))
    elements.append(separateur_section())

    debit_ls = val_ou_nc(h.get('debit_L_s'))
    vitesse  = val_ou_nc(h.get('vitesse_m_s'))

    tableau_data = [
        ["Paramètre", "Valeur"],
        ["Débit Q",
            str(h.get('debit_m3_h', '—')) + " m³/h  (" + debit_ls + " L/s)"],
        ["Hauteur géométrique",
            str(h.get('hauteur_geo_m', '—')) + " m"],
        ["Pertes de charge (Darcy-Weisbach)",
            str(h.get('pertes_charge_m', '—')) + " m"],
        ["Vitesse dans la canalisation", vitesse + (" m/s" if vitesse != 'Non calculé' else "")],
        ["HMT totale", str(h.get('HMT_m', '—')) + " m"],
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
    pompe = data.get('pompe', {})
    elements.append(Paragraph("5. Dimensionnement de la pompe", styles["titre_section"]))
    elements.append(separateur_section())

    tableau_data = [
        ["Paramètre", "Valeur"],
        ["Puissance hydraulique Ph",     str(pompe.get('Ph_kW', '—')) + " kW"],
        ["Puissance absorbée Pp",        str(pompe.get('Pp_kW', '—')) + " kW"],
        ["Puissance moteur calculée Pm", str(pompe.get('Pm_kW', '—')) + " kW"],
        ["Puissance commerciale normalisée",
            str(pompe.get('Pm_commercial_kW', '—')) + " kW"],
    ]

    marque_pompe = data.get('marque_pompe', '')
    modele_pompe = data.get('modele_pompe', '')
    if marque_pompe and modele_pompe:
        tableau_data.append(["Pompe sélectionnée",
                              str(marque_pompe) + " — " + str(modele_pompe)])

    tableau = Table(tableau_data, colWidths=[8.5 * cm, 8.5 * cm])
    tableau.setStyle(style_tableau())
    elements.append(tableau)
    elements.append(Spacer(1, 0.3 * cm))
    return elements


# ============================================================
# SECTION 6 — ÉNERGIE
# ============================================================

def section_energie(data, styles):
    elements = []
    energie = data.get('energie', {})
    source  = data.get('source_energie', 'solaire')
    elements.append(Paragraph("6. Dimensionnement énergétique", styles["titre_section"]))
    elements.append(separateur_section())

    # Tension système : U_syst (entier) ou tension_pv (string "48V")
    def tension_str(e):
        u = e.get('U_syst')
        if u:
            return str(u) + " V"
        tv = str(e.get('tension_pv', '—'))
        return tv if tv == '—' else tv

    if source == "solaire":
        tableau_data = [
            ["Paramètre", "Valeur"],
            ["Source d'énergie",       "Solaire photovoltaïque"],
            ["Énergie journalière",
                str(energie.get('energie_jour_kWh', '—')) + " kWh/jour"],
            ["Puissance crête calculée",
                str(energie.get('puissance_crete_kWp', '—')) + " kWc"],
            ["Nombre de panneaux",
                unite_nb(energie.get('nb_panneaux_300Wc', '—'), 'panneau', 'panneaux')],
            ["Tension système PV",     tension_str(energie)],
            ["Courant total champ PV",
                str(energie.get('courant_A', '—')) + " A"],
        ]

    elif source == "groupe":
        tableau_data = [
            ["Paramètre", "Valeur"],
            ["Source d'énergie",           "Groupe électrogène"],
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

    elif source == "hybride_groupe":
        sol = energie.get('solaire', {})
        grp = energie.get('groupe',  {})
        tableau_data = [
            ["Paramètre", "Valeur"],
            ["Source d'énergie",           "Hybride — Solaire 70% + Groupe 30%"],
            ["Énergie totale journalière",
                str(energie.get('energie_totale_kWh', '—')) + " kWh/jour"],
            ["— Puissance crête solaire",
                str(sol.get('puissance_crete_kWp', '—')) + " kWc"],
            ["— Nombre de panneaux",
                unite_nb(sol.get('nb_panneaux_300Wc', '—'), 'panneau', 'panneaux')],
            ["— Tension système",          tension_str(sol)],
            ["— Courant champ PV",         str(sol.get('courant_A', '—')) + " A"],
            ["— Puissance groupe",         str(grp.get('puissance_groupe_kW', '—')) + " kW"],
            ["— Consommation gasoil / jour",
                str(grp.get('consommation_jour_litres', '—')) + " L"],
            ["— Consommation gasoil / mois",
                str(grp.get('consommation_mois_litres', '—')) + " L"],
        ]

    elif source == "hybride_batteries":
        sol = energie.get('solaire', {})
        tableau_data = [
            ["Paramètre", "Valeur"],
            ["Source d'énergie",          "Hybride — Solaire + Batteries"],
            ["— Énergie journalière",
                str(energie.get('energie_jour_kWh',
                    sol.get('energie_jour_kWh', '—'))) + " kWh/jour"],
            ["— Puissance crête solaire",
                str(sol.get('puissance_crete_kWp', '—')) + " kWc"],
            ["— Nombre de panneaux",
                unite_nb(sol.get('nb_panneaux_300Wc', '—'), 'panneau', 'panneaux')],
            ["— Tension système",         tension_str(sol)],
            ["— Courant champ PV",        str(sol.get('courant_A', '—')) + " A"],
            ["— Énergie à stocker",
                str(energie.get('energie_stockage_kWh', '—')) + " kWh"],
            ["— Capacité totale batteries",
                str(energie.get('capacite_totale_Ah', '—')) + " Ah"],
            ["— Nombre de batteries",
                unite_nb(energie.get('nb_batteries', '—'), 'batterie', 'batteries')],
            ["— Jours d'autonomie",
                str(data.get('jours_autonomie',
                    energie.get('jours_autonomie', '—'))) + " jour(s)"],
            ["— DoD",
                str(round(float(data.get('dod', energie.get('dod', 0.70))) * 100)) + " %"],
        ]

    else:
        tableau_data = [
            ["Paramètre", "Valeur"],
            ["Source d'énergie", str(source)],
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
    elements = []
    source      = data.get('source_energie', '')
    equipements = data.get('equipements', {})
    hasPV = source in ['solaire', 'hybride_groupe', 'hybride_batteries']

    if not hasPV and not data.get('marque_pompe'):
        return elements

    elements.append(Paragraph("7. Équipements sélectionnés", styles["titre_section"]))
    elements.append(separateur_section())

    marque_pompe = data.get('marque_pompe', '')
    modele_pompe = data.get('modele_pompe', '')
    if marque_pompe and modele_pompe:
        elements.append(Paragraph("Pompe", styles["gras"]))
        pompe_table = Table(
            [["Marque", "Modèle"], [str(marque_pompe), str(modele_pompe)]],
            colWidths=[8.5 * cm, 8.5 * cm]
        )
        pompe_table.setStyle(style_tableau_equipement())
        elements.append(pompe_table)
        elements.append(Spacer(1, 0.2 * cm))

    if hasPV:
        marque_pan  = equipements.get('marque_panneau', '')
        modele_pan  = equipements.get('modele_panneau', '')
        nb_panneaux = data.get('nb_panneaux_calcul', '')

        if marque_pan:
            elements.append(Paragraph("Panneau solaire", styles["gras"]))
            pan_table = Table(
                [["Marque", "Modèle", "Nombre calculé"],
                 [str(marque_pan), str(modele_pan),
                  unite_nb(nb_panneaux, 'panneau', 'panneaux')]],
                colWidths=[5.0 * cm, 8.0 * cm, 4.0 * cm]
            )
            pan_table.setStyle(style_tableau_equipement())
            elements.append(pan_table)
            elements.append(Spacer(1, 0.2 * cm))

        if source == 'hybride_batteries':
            marque_bat = equipements.get('marque_batterie', '')
            modele_bat = equipements.get('modele_batterie', '')
            nb_bat     = data.get('energie', {}).get('nb_batteries', '')

            if marque_bat:
                elements.append(Paragraph("Batterie", styles["gras"]))
                bat_table = Table(
                    [["Marque", "Modèle", "Nombre calculé"],
                     [str(marque_bat), str(modele_bat),
                      unite_nb(nb_bat, 'batterie', 'batteries')]],
                    colWidths=[5.0 * cm, 8.0 * cm, 4.0 * cm]
                )
                bat_table.setStyle(style_tableau_equipement())
                elements.append(bat_table)
                elements.append(Spacer(1, 0.2 * cm))

    elements.append(Spacer(1, 0.3 * cm))
    return elements


# ============================================================
# SECTION 8 — COÛT ESTIMATIF
# ============================================================

def section_cout(data, styles):
    elements = []
    cout = data.get('cout') or {}
    if not cout:
        return elements

    elements.append(Paragraph("8. Coût estimatif de l'installation", styles["titre_section"]))
    elements.append(separateur_section())

    tableau_data = [
        ["Poste", "Montant (FCFA)"],
        ["Coût de la pompe",
            "{:,.0f}".format(cout.get('C_pompe', 0)).replace(',', ' ')],
        ["Coût des équipements énergétiques",
            "{:,.0f}".format(cout.get('C_energie', 0)).replace(',', ' ')],
        ["Main d'œuvre & installation (15%)",
            "{:,.0f}".format(cout.get('C_installation', 0)).replace(',', ' ')],
        ["Divers & imprévus (10%)",
            "{:,.0f}".format(cout.get('C_divers', 0)).replace(',', ' ')],
        ["COÛT TOTAL ESTIMATIF",
            "{:,.0f}".format(cout.get('C_total', 0)).replace(',', ' ')],
    ]

    tableau = Table(tableau_data, colWidths=[8.5 * cm, 8.5 * cm])
    tableau.setStyle(TableStyle([
        *style_tableau()._cmds,
        ('FONTNAME',   (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR',  (0, -1), (-1, -1), VERT_TITRE),
        ('LINEABOVE',  (0, -1), (-1, -1), 1.0, VERT_TITRE),
        ('BACKGROUND', (0, -1), (-1, -1), VERT_LEGER),
    ]))
    elements.append(tableau)
    elements.append(Spacer(1, 0.3 * cm))
    return elements


# ============================================================
# SECTION 9 — CONCLUSION
# ============================================================

def section_conclusion(data, styles):
    elements = []
    elements.append(Paragraph("9. Conclusion", styles["titre_section"]))
    elements.append(separateur_section())

    h    = data.get('hydraulique', {})
    p    = data.get('pompe', {})
    src  = data.get('source_energie', '—')
    mp   = data.get('marque_pompe', '—')
    mdl  = data.get('modele_pompe', '—')
    cout = data.get('cout') or {}
    c_total = cout.get('C_total', 0)

    texte = (
        "Le présent rapport présente les résultats du dimensionnement du système de pompage. "
        "Le débit calculé est de <b>" + str(h.get('debit_m3_h', '—')) +
        " m³/h</b> pour une hauteur manométrique totale (HMT) de <b>" +
        str(h.get('HMT_m', '—')) + " m</b>. "
        "La puissance moteur nécessaire est de <b>" + str(p.get('Pm_kW', '—')) +
        " kW</b> (puissance commerciale normalisée : <b>" +
        str(p.get('Pm_commercial_kW', '—')) + " kW</b>). "
        "La source d'énergie retenue est : <b>" +
        str(src).replace('_', ' ').title() + "</b>. "
        "La pompe sélectionnée est la <b>" + str(mp) + " " + str(mdl) + "</b>. "
        "Le coût total estimatif de l'installation est de <b>" +
        "{:,.0f}".format(c_total).replace(',', ' ') + " FCFA</b>."
    )

    style_conc = ParagraphStyle(
        name='Conclusion', fontName='Helvetica', fontSize=9,
        textColor=GRIS_TEXTE, leading=16, alignment=TA_JUSTIFY, spaceAfter=10,
    )
    elements.append(Paragraph(texte, style_conc))
    elements.append(Spacer(1, 0.3 * cm))
    return elements


# ============================================================
# PIED DE PAGE
# ============================================================

def pied_de_page(styles):
    elements = []
    elements.append(Spacer(1, 0.8 * cm))
    elements.append(
        HRFlowable(width="100%", thickness=1.5, color=VERT_TITRE,
                   spaceAfter=6, spaceBefore=2)
    )
    elements.append(
        Paragraph(
            "HydroPump v1.0 · Rapport généré le "
            + datetime.now().strftime("%d/%m/%Y à %H:%M")
            + " · Les résultats sont donnés à titre indicatif "
            "et doivent être validés par un ingénieur qualifié.",
            styles["pied"]
        )
    )
    return elements
