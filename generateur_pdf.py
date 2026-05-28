# ============================================================
# MODULE GÉNÉRATION PDF — HydroPump v1.0
# Rapport professionnel de dimensionnement
# ============================================================

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, HRFlowable, KeepTogether, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from io import BytesIO
from datetime import datetime

# ============================================================
# NUMÉROTATION DES PAGES
# ============================================================

class NumerotationPages:
    def __init__(self, doc):
        self.doc = doc

    def __call__(self, canv, doc):
        canv.saveState()
        canv.setFont('Helvetica', 8)
        canv.setFillColorRGB(0.58, 0.64, 0.70)  # GRIS_PIED
        page_num = "Page %d" % doc.page
        canv.drawRightString(
            doc.pagesize[0] - doc.rightMargin,
            1.0 * cm,
            page_num
        )
        canv.restoreState()


# ============================================================
# PALETTE
# ============================================================

VERT_FONCE  = colors.HexColor("#166534")
VERT_MOYEN  = colors.HexColor("#15803d")
VERT_ACCENT = colors.HexColor("#22c55e")
VERT_LEGER  = colors.HexColor("#f0fdf4")
VERT_BORD   = colors.HexColor("#bbf7d0")
GRIS_TEXTE  = colors.HexColor("#475569")
GRIS_LIGNE  = colors.HexColor("#e2e8f0")
GRIS_FOND   = colors.HexColor("#f8fafc")
GRIS_PIED   = colors.HexColor("#94a3b8")
NOIR        = colors.HexColor("#0f172a")
BLANC       = colors.white

PAGE_W = 17.0 * cm  # largeur utile (A4 - marges 2cm)

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
    return str(v) if v and str(v) not in ('—', 'None', '') else 'Non calculé'


def pluriel(valeur, sing, plur):
    try:
        nb = int(float(str(valeur)))
        return str(nb) + " " + (sing if nb <= 1 else plur)
    except Exception:
        return str(valeur)


def fmt_fcfa(valeur):
    try:
        return "{:,.0f}".format(float(valeur)).replace(',', ' ')
    except Exception:
        return str(valeur)


# ============================================================
# STYLES PARAGRAPHES
# ============================================================

def creer_styles():
    pied = ParagraphStyle(
        name='Pied', fontName='Helvetica', fontSize=8,
        textColor=GRIS_PIED, alignment=TA_CENTER,
    )
    gras = ParagraphStyle(
        name='Gras', fontName='Helvetica-Bold', fontSize=9,
        textColor=NOIR, spaceAfter=4,
    )
    conclusion = ParagraphStyle(
        name='Conclusion', fontName='Helvetica', fontSize=9,
        textColor=GRIS_TEXTE, leading=16,
        alignment=TA_JUSTIFY, spaceAfter=10,
    )
    return {"pied": pied, "gras": gras, "conclusion": conclusion}


# ============================================================
# COMPOSANTS RÉUTILISABLES
# ============================================================

def bandeau(texte, bg=None, fg=BLANC, taille=10, padding_v=8, padding_h=10, gras=True):
    """Crée un bandeau coloré avec texte — utilisé pour titres de sections."""
    bg = bg or VERT_FONCE
    style = ParagraphStyle(
        name='Bandeau', fontName='Helvetica-Bold' if gras else 'Helvetica',
        fontSize=taille, textColor=fg, alignment=TA_LEFT,
    )
    t = Table([[Paragraph(texte, style)]], colWidths=[PAGE_W])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, -1), bg),
        ('TOPPADDING',    (0, 0), (-1, -1), padding_v),
        ('BOTTOMPADDING', (0, 0), (-1, -1), padding_v),
        ('LEFTPADDING',   (0, 0), (-1, -1), padding_h),
        ('RIGHTPADDING',  (0, 0), (-1, -1), padding_h),
    ]))
    return t


def tableau_donnees(lignes, col_g=9.5*cm, col_d=7.5*cm):
    """Tableau paramètre / valeur avec en-tête vert et alternance."""
    t = Table(lignes, colWidths=[col_g, col_d])
    cmds = [
        # En-tête
        ('BACKGROUND',    (0, 0), (-1, 0), VERT_FONCE),
        ('TEXTCOLOR',     (0, 0), (-1, 0), BLANC),
        ('FONTNAME',      (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE',      (0, 0), (-1, 0), 9),
        ('TOPPADDING',    (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('LEFTPADDING',   (0, 0), (-1, 0), 10),
        ('RIGHTPADDING',  (0, 0), (-1, 0), 10),
        # Données
        ('FONTNAME',      (0, 1), (0, -1), 'Helvetica'),
        ('FONTNAME',      (1, 1), (1, -1), 'Helvetica-Bold'),
        ('FONTSIZE',      (0, 1), (-1, -1), 9),
        ('TEXTCOLOR',     (0, 1), (0, -1), GRIS_TEXTE),
        ('TEXTCOLOR',     (1, 1), (1, -1), NOIR),
        ('ALIGN',         (0, 0), (0, -1), 'LEFT'),
        ('ALIGN',         (1, 0), (1, -1), 'RIGHT'),
        ('TOPPADDING',    (0, 1), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 7),
        ('LEFTPADDING',   (0, 1), (-1, -1), 10),
        ('RIGHTPADDING',  (0, 1), (-1, -1), 10),
        # Alternance
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [BLANC, GRIS_FOND]),
        # Grille légère
        ('GRID',          (0, 0), (-1, -1), 0.3, GRIS_LIGNE),
        ('LINEBELOW',     (0, 0), (-1, 0),  1.0, VERT_FONCE),
    ]
    t.setStyle(TableStyle(cmds))
    return t


def tableau_donnees_avec_total(lignes, col_g=9.5*cm, col_d=7.5*cm):
    """Comme tableau_donnees mais dernière ligne en vert gras."""
    t = Table(lignes, colWidths=[col_g, col_d])
    cmds = [
        ('BACKGROUND',    (0, 0), (-1, 0), VERT_FONCE),
        ('TEXTCOLOR',     (0, 0), (-1, 0), BLANC),
        ('FONTNAME',      (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE',      (0, 0), (-1, 0), 9),
        ('TOPPADDING',    (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('LEFTPADDING',   (0, 0), (-1, 0), 10),
        ('RIGHTPADDING',  (0, 0), (-1, 0), 10),
        ('FONTNAME',      (0, 1), (0, -1), 'Helvetica'),
        ('FONTNAME',      (1, 1), (1, -1), 'Helvetica-Bold'),
        ('FONTSIZE',      (0, 1), (-1, -1), 9),
        ('TEXTCOLOR',     (0, 1), (0, -1), GRIS_TEXTE),
        ('TEXTCOLOR',     (1, 1), (1, -1), NOIR),
        ('ALIGN',         (0, 0), (0, -1), 'LEFT'),
        ('ALIGN',         (1, 0), (1, -1), 'RIGHT'),
        ('TOPPADDING',    (0, 1), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 7),
        ('LEFTPADDING',   (0, 1), (-1, -1), 10),
        ('RIGHTPADDING',  (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [BLANC, GRIS_FOND]),
        ('GRID',          (0, 0), (-1, -1), 0.3, GRIS_LIGNE),
        ('LINEBELOW',     (0, 0), (-1, 0),  1.0, VERT_FONCE),
        # Dernière ligne
        ('FONTNAME',      (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR',     (0, -1), (-1, -1), VERT_FONCE),
        ('BACKGROUND',    (0, -1), (-1, -1), VERT_LEGER),
        ('LINEABOVE',     (0, -1), (-1, -1), 1.0, VERT_FONCE),
    ]
    t.setStyle(TableStyle(cmds))
    return t


def tableau_equipement(lignes, col_widths=None):
    """Tableau équipements avec en-tête gris clair."""
    col_widths = col_widths or [5.5*cm, 8.0*cm, 3.5*cm]
    t = Table(lignes, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, 0),  GRIS_FOND),
        ('TEXTCOLOR',     (0, 0), (-1, 0),  VERT_FONCE),
        ('FONTNAME',      (0, 0), (-1, 0),  'Helvetica-Bold'),
        ('FONTSIZE',      (0, 0), (-1, -1), 9),
        ('FONTNAME',      (0, 1), (0, -1),  'Helvetica'),
        ('FONTNAME',      (1, 1), (-1, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR',     (0, 1), (0, -1),  GRIS_TEXTE),
        ('TEXTCOLOR',     (1, 1), (-1, -1), NOIR),
        ('ALIGN',         (0, 0), (-1, -1), 'LEFT'),
        ('TOPPADDING',    (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING',   (0, 0), (-1, -1), 10),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 10),
        ('ROWBACKGROUNDS',(0, 1), (-1, -1), [BLANC, GRIS_FOND]),
        ('GRID',          (0, 0), (-1, -1), 0.3, GRIS_LIGNE),
        ('LINEBELOW',     (0, 0), (-1, 0),  1.0, VERT_FONCE),
    ]))
    return t


def sep():
    return Spacer(1, 0.15 * cm)


def esp():
    return Spacer(1, 0.4 * cm)


# ============================================================
# FONCTION PRINCIPALE
# ============================================================

def generer_rapport(data):
    buffer = BytesIO()
    styles = creer_styles()

    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        leftMargin=2.0*cm, rightMargin=2.0*cm,
        topMargin=1.5*cm, bottomMargin=2.0*cm,
    )

    contenu = []
    contenu += page_de_garde(data, styles)
    contenu.append(PageBreak())

    def ajouter_section(fn):
        bloc = fn(data, styles)
        if bloc:
            contenu.append(KeepTogether(bloc))

    ajouter_section(section_identification)
    ajouter_section(section_localisation)
    ajouter_section(section_besoins)
    ajouter_section(section_hydraulique)
    ajouter_section(section_pompe)
    ajouter_section(section_energie)
    ajouter_section(section_equipements)
    ajouter_section(section_cout)
    ajouter_section(section_conclusion)
    contenu += pied_de_page(styles)

    numerotation = NumerotationPages(doc)
    doc.build(contenu, onFirstPage=numerotation, onLaterPages=numerotation)
    return buffer


# ============================================================
# PAGE DE GARDE
# ============================================================

def page_de_garde(data, styles):
    elements = []

    nom_projet  = str(data.get('nom_projet',  'Non renseigné'))
    nom_client  = str(data.get('nom_client',  'Non renseigné'))
    tel_client  = str(data.get('tel_client',  ''))
    realise_par = str(data.get('realise_par', 'Non renseigné'))
    date_str    = formater_date(data.get('date_projet', ''))
    lat         = str(data.get('lat', '—'))
    lon         = str(data.get('lon', '—'))
    irr         = str(data.get('irradiation', '—'))
    mois        = str(data.get('mois_critique', '—'))

    titre_s = ParagraphStyle(
        name='GardeTitre', fontName='Helvetica-Bold', fontSize=20,
        textColor=VERT_FONCE, alignment=TA_CENTER, spaceAfter=6,
    )
    sous_s = ParagraphStyle(
        name='GardeSous', fontName='Helvetica', fontSize=12,
        textColor=GRIS_TEXTE, alignment=TA_CENTER, spaceAfter=0,
    )
    section_s = ParagraphStyle(
        name='GardeSection', fontName='Helvetica-Bold', fontSize=10,
        textColor=VERT_FONCE, spaceAfter=4, spaceBefore=4,
    )
    lbl_s = ParagraphStyle(
        name='GardeLbl', fontName='Helvetica', fontSize=9,
        textColor=GRIS_TEXTE,
    )
    val_s = ParagraphStyle(
        name='GardeVal', fontName='Helvetica-Bold', fontSize=9,
        textColor=NOIR,
    )

    # Ligne décorative verte
    def ligne_verte():
        return HRFlowable(width="100%", thickness=2, color=VERT_FONCE,
                          spaceAfter=8, spaceBefore=0)

    def ligne_grise():
        return HRFlowable(width="100%", thickness=0.5, color=GRIS_LIGNE,
                          spaceAfter=6, spaceBefore=0)

    def row(label, valeur):
        t = Table(
            [[Paragraph(label, lbl_s), Paragraph(valeur, val_s)]],
            colWidths=[5.0*cm, 12.0*cm]
        )
        t.setStyle(TableStyle([
            ('TOPPADDING',    (0,0),(-1,-1), 4),
            ('BOTTOMPADDING', (0,0),(-1,-1), 4),
            ('LEFTPADDING',   (0,0),(-1,-1), 0),
            ('RIGHTPADDING',  (0,0),(-1,-1), 0),
            ('VALIGN',        (0,0),(-1,-1), 'TOP'),
        ]))
        return t

    # TITRE
    elements.append(Spacer(1, 1.5*cm))
    elements.append(Paragraph("RAPPORT TECHNIQUE", titre_s))
    elements.append(Spacer(1, 0.4*cm))
    elements.append(ligne_verte())
    elements.append(Spacer(1, 0.8*cm))

    # BLOC CLIENT
    elements.append(Paragraph("CLIENT", section_s))
    elements.append(ligne_grise())
    elements.append(row("Nom", nom_client))
    if tel_client:
        elements.append(row("Téléphone", tel_client))
    elements.append(Spacer(1, 0.6*cm))

    # BLOC LOCALISATION & PROJET
    elements.append(Paragraph("LOCALISATION & PROJET", section_s))
    elements.append(ligne_grise())
    elements.append(row("Latitude",   lat + "°"))
    elements.append(row("Longitude",  lon + "°"))
    elements.append(row("Irradiation", irr + " kWh/m²/j (" + mois + ")"))
    elements.append(row("Projet",     nom_projet))
    elements.append(row("Technicien", realise_par))
    elements.append(row("Date rapport", date_str))
    elements.append(Spacer(1, 0.5*cm))

    return elements


# ============================================================
# SECTIONS
# ============================================================

def section_identification(data, styles):
    elements = [bandeau("1. Identification du projet"), sep()]
    lignes = [
        ["Paramètre", "Valeur"],
        ["Nom du projet",   str(data.get('nom_projet',  'Non renseigné'))],
        ["Nom du client",   str(data.get('nom_client',  'Non renseigné'))],
        ["Réalisé par",     str(data.get('realise_par', 'Non renseigné'))],
        ["Date",            formater_date(data.get('date_projet', ''))],
        ["Logiciel",        "HydroPump v1.0 — Dimensionnement pompage solaire"],
        ["Date de génération", datetime.now().strftime("%d/%m/%Y à %H:%M")],
    ]
    elements.append(tableau_donnees(lignes))
    elements.append(esp())
    return elements


def section_localisation(data, styles):
    elements = [bandeau("2. Localisation et données climatiques"), sep()]
    lignes = [
        ["Paramètre", "Valeur"],
        ["Latitude",            str(data.get('lat','—')) + "°"],
        ["Longitude",           str(data.get('lon','—')) + "°"],
        ["Température maximale", str(data.get('temperature_max','—')) + " °C"],
        ["Température minimale", str(data.get('temperature_min','—')) + " °C"],
        ["Irradiation (mois critique)",
            str(data.get('irradiation','—')) + " kWh/m²/jour"],
        ["ET0 maximale (Penman-Monteith FAO-56)",
            str(data.get('ET0_max','—')) + " mm/jour"],
        ["Mois critique", str(data.get('mois_critique','—'))],
    ]
    elements.append(tableau_donnees(lignes))
    elements.append(esp())
    return elements


def section_besoins(data, styles):
    elements = [bandeau("3. Besoins en eau"), sep()]
    b = data.get('besoins', {})
    lignes = [
        ["Paramètre", "Valeur"],
        ["ETc / Besoin journalier",
            str(b.get('ETc','—')) + " mm/jour"],
        ["Besoin net en eau",
            str(b.get('besoin_net_m3_jour','—')) + " m³/jour"],
        ["Besoin brut en eau",
            str(b.get('besoin_brut_m3_jour','—')) + " m³/jour"],
        ["Besoin par session",
            str(b.get('besoin_session_m3','—')) + " m³"],
    ]
    elements.append(tableau_donnees(lignes))
    elements.append(esp())
    return elements


def section_hydraulique(data, styles):
    elements = [bandeau("4. Dimensionnement hydraulique"), sep()]
    h = data.get('hydraulique', {})
    debit_ls = val_ou_nc(h.get('debit_L_s'))
    vitesse  = val_ou_nc(h.get('vitesse_m_s'))
    lignes = [
        ["Paramètre", "Valeur"],
        ["Débit Q",
            str(h.get('debit_m3_h','—')) + " m³/h  (" +
            (debit_ls + " L/s" if debit_ls != 'Non calculé' else 'Non calculé') + ")"],
        ["Hauteur géométrique",
            str(h.get('hauteur_geo_m','—')) + " m"],
        ["Pertes de charge (Darcy-Weisbach)",
            str(h.get('pertes_charge_m','—')) + " m"],
        ["Vitesse dans la canalisation",
            (vitesse + " m/s") if vitesse != 'Non calculé' else 'Non calculé'],
        ["HMT totale",
            str(h.get('HMT_m','—')) + " m"],
    ]
    elements.append(tableau_donnees(lignes))
    elements.append(esp())
    return elements


def section_pompe(data, styles):
    elements = [bandeau("5. Dimensionnement de la pompe"), sep()]
    p = data.get('pompe', {})
    lignes = [
        ["Paramètre", "Valeur"],
        ["Puissance hydraulique Ph",
            str(p.get('Ph_kW','—')) + " kW"],
        ["Puissance absorbée Pp",
            str(p.get('Pp_kW','—')) + " kW"],
        ["Puissance moteur calculée Pm",
            str(p.get('Pm_kW','—')) + " kW"],
        ["Puissance commerciale normalisée",
            str(p.get('Pm_commercial_kW','—')) + " kW"],
    ]
    mp = data.get('marque_pompe','')
    mp_mod = data.get('modele_pompe','')
    if mp and mp_mod:
        lignes.append(["Pompe sélectionnée", mp + " — " + mp_mod])
    elements.append(tableau_donnees(lignes))
    elements.append(esp())
    return elements


def _tension_str(e, data=None):
    u = e.get('U_syst')
    if u and str(u) not in ('—', '', 'None'):
        return str(u) + " V"
    if data:
        ts = str(data.get('tension_systeme', '') or '')
        if ts and ts not in ('—', '', 'None'):
            v = ts.replace(' V', '').replace('V', '').strip()
            return v + ' V' if v.isdigit() else ts
    tv = str(e.get('tension_pv', '—'))
    return tv if tv != '—' else '—'


def section_energie(data, styles):
    elements = [bandeau("6. Dimensionnement énergétique"), sep()]
    e  = data.get('energie', {})
    src = data.get('source_energie','solaire')

    if src == "solaire":
        lignes = [
            ["Paramètre", "Valeur"],
            ["Source d'énergie", "Solaire photovoltaïque"],
            ["Énergie journalière",
                str(e.get('energie_jour_kWh','—')) + " kWh/jour"],
            ["Puissance crête calculée",
                str(e.get('puissance_crete_kWp','—')) + " kWc"],
            ["Nombre de panneaux",
                pluriel(e.get('nb_panneaux_300Wc','—'), 'panneau','panneaux')],
            ["Tension système PV", _tension_str(e, data)],
            ["Courant total champ PV",
                str(e.get('courant_A','—')) + " A"],
        ]

    elif src == "groupe":
        lignes = [
            ["Paramètre", "Valeur"],
            ["Source d'énergie", "Groupe électrogène"],
            ["Énergie journalière",
                str(e.get('energie_jour_kWh','—')) + " kWh/jour"],
            ["Puissance groupe recommandée",
                str(e.get('puissance_groupe_kW','—')) + " kW"],
            ["Consommation gasoil / jour",
                str(e.get('consommation_jour_litres','—')) + " L"],
            ["Consommation gasoil / mois",
                str(e.get('consommation_mois_litres','—')) + " L"],
        ]

    elif src == "hybride_groupe":
        sol = e.get('solaire',{})
        grp = e.get('groupe',{})
        lignes = [
            ["Paramètre", "Valeur"],
            ["Source d'énergie", "Hybride — Solaire + Groupe"],
            ["Énergie totale journalière",
                str(e.get('energie_totale_kWh','—')) + " kWh/jour"],
            ["— Puissance crête solaire",
                str(sol.get('puissance_crete_kWp','—')) + " kWc"],
            ["— Nombre de panneaux",
                pluriel(sol.get('nb_panneaux_300Wc','—'), 'panneau','panneaux')],
            ["— Tension système", _tension_str(sol, data)],
            ["— Puissance groupe",
                str(grp.get('puissance_groupe_kW','—')) + " kW"],
            ["— Consommation gasoil / jour",
                str(grp.get('consommation_jour_litres','—')) + " L"],
        ]

    elif src == "hybride_batteries":
        sol = e.get('solaire',{})
        lignes = [
            ["Paramètre", "Valeur"],
            ["Source d'énergie", "Hybride — Solaire + Batteries"],
            ["— Énergie journalière",
                str(e.get('energie_jour_kWh',
                    sol.get('energie_jour_kWh','—'))) + " kWh/jour"],
            ["— Puissance crête solaire",
                str(sol.get('puissance_crete_kWp','—')) + " kWc"],
            ["— Nombre de panneaux",
                pluriel(sol.get('nb_panneaux_300Wc','—'), 'panneau','panneaux')],
            ["— Tension système", _tension_str(sol, data)],
            ["— Énergie à stocker",
                str(e.get('energie_stockage_kWh','—')) + " kWh"],
            ["— Capacité totale batteries",
                str(e.get('capacite_totale_Ah','—')) + " Ah"],
            ["— Nombre de batteries",
                pluriel(e.get('nb_batteries','—'), 'batterie','batteries')],
            ["— Jours d'autonomie",
                str(data.get('jours_autonomie',
                    e.get('jours_autonomie','—'))) + " jour(s)"],
        ]
    else:
        lignes = [["Paramètre", "Valeur"], ["Source d'énergie", str(src)]]

    elements.append(tableau_donnees(lignes))
    elements.append(esp())
    return elements


def section_equipements(data, styles):
    src   = data.get('source_energie','')
    equip = data.get('equipements',{})
    hasPV = src in ['solaire','hybride_groupe','hybride_batteries']
    if not hasPV and not data.get('marque_pompe'):
        return []

    elements = [bandeau("7. Équipements sélectionnés"), sep()]

    mp  = data.get('marque_pompe','')
    mdl = data.get('modele_pompe','')
    if mp and mdl:
        elements.append(Paragraph("Pompe", styles["gras"]))
        elements.append(tableau_equipement(
            [["Marque","Modèle"],[mp, mdl]],
            col_widths=[8.5*cm, 8.5*cm]
        ))
        elements.append(Spacer(1, 0.25*cm))

    if hasPV:
        mp2 = equip.get('marque_panneau','')
        md2 = equip.get('modele_panneau','')
        nb2 = data.get('nb_panneaux_calcul','')
        if mp2:
            elements.append(Paragraph("Panneau solaire", styles["gras"]))
            elements.append(tableau_equipement(
                [["Marque","Modèle","Nombre calculé"],
                 [mp2, md2, pluriel(nb2,'panneau','panneaux')]]
            ))
            elements.append(Spacer(1, 0.25*cm))

        if src == 'hybride_batteries':
            mb  = equip.get('marque_batterie','')
            mdb = equip.get('modele_batterie','')
            nb3 = data.get('energie',{}).get('nb_batteries','')
            if mb:
                elements.append(Paragraph("Batterie", styles["gras"]))
                elements.append(tableau_equipement(
                    [["Marque","Modèle","Nombre calculé"],
                     [mb, mdb, pluriel(nb3,'batterie','batteries')]]
                ))

        # Onduleur
        marque_ond = equip.get('marque_onduleur', '')
        modele_ond = equip.get('modele_onduleur', '')
        type_ond   = data.get('type_onduleur', '')
        if marque_ond and type_ond:
            elements.append(Paragraph("Onduleur", styles["gras"]))
            elements.append(tableau_equipement(
                [["Marque", "Modèle", "Type"],
                 [str(marque_ond), str(modele_ond), str(type_ond)]],
                col_widths=[5.5*cm, 8.0*cm, 3.5*cm]
            ))
            elements.append(Spacer(1, 0.25*cm))

    elements.append(esp())
    return elements


def section_cout(data, styles):
    cout = data.get('cout') or {}
    if not cout:
        return []

    elements = [bandeau("8. Coût estimatif de l'installation"), sep()]
    lignes = [
        ["Poste", "Montant (FCFA)"],
        ["Coût de la pompe",
            fmt_fcfa(cout.get('C_pompe',0))],
        ["Coût des équipements énergétiques",
            fmt_fcfa(cout.get('C_energie',0))],
        ["Main d'œuvre & installation (15%)",
            fmt_fcfa(cout.get('C_installation',0))],
        ["Divers & imprévus (10%)",
            fmt_fcfa(cout.get('C_divers',0))],
        ["COÛT TOTAL ESTIMATIF",
            fmt_fcfa(cout.get('C_total',0))],
    ]
    elements.append(tableau_donnees_avec_total(lignes))
    elements.append(esp())
    return elements


def section_conclusion(data, styles):
    elements = [bandeau("9. Conclusion"), sep()]
    h  = data.get('hydraulique',{})
    p  = data.get('pompe',{})
    src = data.get('source_energie','—')
    mp  = data.get('marque_pompe','—')
    mdl = data.get('modele_pompe','—')
    cout = data.get('cout') or {}

    texte = (
        "Le présent rapport présente les résultats du dimensionnement "
        "du système de pompage solaire. "
        "Le débit calculé est de <b>" + str(h.get('debit_m3_h','—')) +
        " m³/h</b> pour une hauteur manométrique totale (HMT) de <b>" +
        str(h.get('HMT_m','—')) + " m</b>. "
        "La puissance moteur nécessaire est de <b>" +
        str(p.get('Pm_kW','—')) + " kW</b> (puissance commerciale : <b>" +
        str(p.get('Pm_commercial_kW','—')) + " kW</b>). "
        "La source d'énergie retenue est : <b>" +
        str(src).replace('_',' ').title() + "</b>. "
        "La pompe sélectionnée est la <b>" + mp + " " + mdl + "</b>."
    )
    if cout.get('C_total'):
        texte += (
            " Le coût total estimatif de l'installation est de <b>" +
            fmt_fcfa(cout['C_total']) + " FCFA</b>."
        )

    elements.append(Paragraph(texte, styles["conclusion"]))
    elements.append(esp())
    return elements


def section_signatures(data, styles):
    elements = [PageBreak(), bandeau("Validation et signatures"), sep()]

    realise_par = str(data.get('realise_par', 'Non renseigné'))
    nom_client  = str(data.get('nom_client',  'Non renseigné'))
    date_str    = formater_date(data.get('date_projet', ''))

    lbl = ParagraphStyle(
        name='SigLbl', fontName='Helvetica-Bold', fontSize=9,
        textColor=BLANC, alignment=TA_CENTER,
    )
    txt = ParagraphStyle(
        name='SigTxt', fontName='Helvetica', fontSize=9,
        textColor=GRIS_TEXTE, leading=16,
    )
    ligne = HRFlowable(width="100%", thickness=0.5, color=GRIS_LIGNE,
                       spaceAfter=4, spaceBefore=12)

    # En-têtes colonnes
    hdr_data = [[
        Paragraph("LE TECHNICIEN", lbl),
        Paragraph("LE CLIENT", lbl),
    ]]
    hdr_t = Table(hdr_data, colWidths=[8.5*cm, 8.5*cm])
    hdr_t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), VERT_FONCE),
        ('TOPPADDING',    (0,0),(-1,-1), 8),
        ('BOTTOMPADDING', (0,0),(-1,-1), 8),
        ('ALIGN',         (0,0),(-1,-1), 'CENTER'),
        ('LINEAFTER',     (0,0),(0,-1),  0.5, VERT_ACCENT),
    ]))
    elements.append(hdr_t)
    elements.append(Spacer(1, 0.4*cm))

    # Texte technicien + client côte à côte
    txt_tech = ("Je soussigné(e), <b>" + realise_par + "</b>, certifie avoir réalisé "
                "cette étude conformément aux règles de l'art.")
    txt_cli  = ("Je soussigné(e), <b>" + nom_client + "</b>, déclare avoir pris "
                "connaissance de ce rapport de dimensionnement.")

    corps_data = [[
        Paragraph(txt_tech, txt),
        Paragraph(txt_cli, txt),
    ]]
    corps_t = Table(corps_data, colWidths=[8.5*cm, 8.5*cm])
    corps_t.setStyle(TableStyle([
        ('VALIGN',        (0,0),(-1,-1), 'TOP'),
        ('TOPPADDING',    (0,0),(-1,-1), 0),
        ('LEFTPADDING',   (0,0),(-1,-1), 6),
        ('RIGHTPADDING',  (0,0),(-1,-1), 6),
    ]))
    elements.append(corps_t)
    elements.append(Spacer(1, 1.2*cm))

    # Lignes signature + date + cachet
    sig_style = ParagraphStyle(
        name='SigLine', fontName='Helvetica', fontSize=9,
        textColor=GRIS_TEXTE,
    )
    sig_data = [
        [Paragraph("Signature :", sig_style),       Paragraph("Signature :", sig_style)],
        [Spacer(1, 1.5*cm),                          Spacer(1, 1.5*cm)],
        [HRFlowable(width=7*cm, thickness=0.5, color=GRIS_LIGNE, spaceAfter=8, spaceBefore=2),
         HRFlowable(width=7*cm, thickness=0.5, color=GRIS_LIGNE, spaceAfter=8, spaceBefore=2)],
        [Paragraph("Date : " + date_str, sig_style), Paragraph("Date : " + date_str, sig_style)],
        [Spacer(1, 0.6*cm),                          Spacer(1, 0.6*cm)],
        [HRFlowable(width=7*cm, thickness=0.5, color=GRIS_LIGNE, spaceAfter=8, spaceBefore=2),
         HRFlowable(width=7*cm, thickness=0.5, color=GRIS_LIGNE, spaceAfter=8, spaceBefore=2)],
        [Paragraph("Cachet :", sig_style),           Paragraph("", sig_style)],
        [Spacer(1, 2.0*cm),                          Spacer(1, 0.5*cm)],
        [HRFlowable(width=4*cm, thickness=0.5, color=GRIS_LIGNE, spaceAfter=2, spaceBefore=2),
         Paragraph("", sig_style)],
    ]
    sig_t = Table(sig_data, colWidths=[8.5*cm, 8.5*cm])
    sig_t.setStyle(TableStyle([
        ('VALIGN',        (0,0),(-1,-1), 'TOP'),
        ('TOPPADDING',    (0,0),(-1,-1), 4),
        ('BOTTOMPADDING', (0,0),(-1,-1), 4),
        ('LEFTPADDING',   (0,0),(-1,-1), 6),
        ('RIGHTPADDING',  (0,0),(-1,-1), 6),
    ]))
    elements.append(sig_t)
    return elements


def pied_de_page(styles):
    return [
        Spacer(1, 0.6*cm),
        HRFlowable(width="100%", thickness=1.5, color=VERT_FONCE,
                   spaceAfter=6, spaceBefore=2),
        Paragraph(
            "HydroPump v1.0  ·  Rapport généré le " +
            datetime.now().strftime("%d/%m/%Y à %H:%M") +
            "  ·  Les résultats sont donnés à titre indicatif "
            "et doivent être validés par un ingénieur qualifié.",
            styles["pied"]
        ),
    ]