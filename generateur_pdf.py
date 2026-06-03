# ============================================================
# MODULE GÉNÉRATION PDF — HydroPump v2.0
# Compatible ancien flux (/generer_pdf) ET nouveau (/generer_pdf2)
# ============================================================

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, HRFlowable, KeepTogether, PageBreak
)
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
        canv.setFillColorRGB(0.58, 0.64, 0.70)
        canv.drawRightString(
            doc.pagesize[0] - doc.rightMargin,
            1.0 * cm,
            "Page %d" % doc.page
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
OR_FOND     = colors.HexColor("#fffbeb")
OR_BORD     = colors.HexColor("#fbbf24")

PAGE_W = 17.0 * cm

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
        return "{:,.0f}".format(float(valeur or 0)).replace(',', ' ')
    except Exception:
        return str(valeur)


def sv(d, key, unite='', fallback='—'):
    """Extrait une valeur de dict avec unité, retourne fallback si absent/vide."""
    v = (d or {}).get(key) if isinstance(d, dict) else None
    if v is None or str(v) in ('', 'None', '—'):
        return fallback
    return str(v) + (' ' + unite if unite else '')


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
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [BLANC, GRIS_FOND]),
        ('GRID',          (0, 0), (-1, -1), 0.3, GRIS_LIGNE),
        ('LINEBELOW',     (0, 0), (-1, 0),  1.0, VERT_FONCE),
    ]
    t.setStyle(TableStyle(cmds))
    return t


def tableau_donnees_avec_total(lignes, col_g=9.5*cm, col_d=7.5*cm):
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
        ('FONTNAME',      (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR',     (0, -1), (-1, -1), VERT_FONCE),
        ('BACKGROUND',    (0, -1), (-1, -1), VERT_LEGER),
        ('LINEABOVE',     (0, -1), (-1, -1), 1.0, VERT_FONCE),
    ]
    t.setStyle(TableStyle(cmds))
    return t


def tableau_equipement(lignes, col_widths=None):
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


def tableau_cout_detaille(lignes):
    """Tableau coût 4 colonnes : Désignation | Qté | P.U. | Total"""
    cols = [7.5*cm, 2.0*cm, 3.5*cm, 4.0*cm]
    t = Table(lignes, colWidths=cols)
    n = len(lignes)
    cmds = [
        # En-tête
        ('BACKGROUND',    (0, 0), (-1, 0), VERT_FONCE),
        ('TEXTCOLOR',     (0, 0), (-1, 0), BLANC),
        ('FONTNAME',      (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE',      (0, 0), (-1, -1), 9),
        ('TOPPADDING',    (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        # Données
        ('FONTNAME',      (0, 1), (-1, -1), 'Helvetica'),
        ('FONTNAME',      (3, 1), (3, -1),  'Helvetica-Bold'),
        ('TEXTCOLOR',     (0, 1), (0, -1),  GRIS_TEXTE),
        ('TEXTCOLOR',     (3, 1), (3, -1),  NOIR),
        ('ALIGN',         (0, 0), (0, -1), 'LEFT'),
        ('ALIGN',         (1, 0), (1, -1), 'CENTER'),
        ('ALIGN',         (2, 0), (2, -1), 'RIGHT'),
        ('ALIGN',         (3, 0), (3, -1), 'RIGHT'),
        ('TOPPADDING',    (0, 1), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 7),
        ('LEFTPADDING',   (0, 0), (-1, -1), 8),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [BLANC, GRIS_FOND]),
        ('GRID',          (0, 0), (-1, -1), 0.3, GRIS_LIGNE),
        ('LINEBELOW',     (0, 0), (-1, 0),  1.0, VERT_FONCE),
        # Dernière ligne = total en vert
        ('FONTNAME',      (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR',     (0, -1), (-1, -1), VERT_FONCE),
        ('BACKGROUND',    (0, -1), (-1, -1), VERT_LEGER),
        ('LINEABOVE',     (0, -1), (-1, -1), 1.5, VERT_FONCE),
    ]
    # Avant-dernière et avant-avant-dernière (divers + main d'oeuvre) → fond doux
    if n >= 4:
        cmds += [
            ('BACKGROUND', (0, -3), (-1, -2), OR_FOND),
            ('TEXTCOLOR',  (0, -3), (0, -2), GRIS_TEXTE),
        ]
    t.setStyle(TableStyle(cmds))
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

    def ajouter(fn):
        bloc = fn(data, styles)
        if bloc:
            contenu.append(KeepTogether(bloc))

    ajouter(section_identification)
    ajouter(section_localisation)
    ajouter(section_besoins)
    ajouter(section_hydraulique)
    ajouter(section_pompe)
    ajouter(section_energie)
    ajouter(section_equipements)
    ajouter(section_cables)
    ajouter(section_cout)
    ajouter(section_conclusion)
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

    elements.append(Spacer(1, 1.5*cm))
    elements.append(Paragraph("RAPPORT TECHNIQUE", titre_s))
    elements.append(Paragraph("Dimensionnement système de pompage", sous_s))
    elements.append(Spacer(1, 0.4*cm))
    elements.append(ligne_verte())
    elements.append(Spacer(1, 0.8*cm))

    elements.append(Paragraph("CLIENT", section_s))
    elements.append(ligne_grise())
    elements.append(row("Nom", nom_client))
    if tel_client:
        elements.append(row("Téléphone", tel_client))
    elements.append(Spacer(1, 0.6*cm))

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
        ["Logiciel",        "HydroPump v2.0 — Dimensionnement pompage solaire"],
        ["Date de génération", datetime.now().strftime("%d/%m/%Y à %H:%M")],
    ]
    elements.append(tableau_donnees(lignes))
    elements.append(esp())
    return elements


def section_localisation(data, styles):
    elements = [bandeau("2. Localisation et données climatiques"), sep()]
    # Support ET0 (nouveau) et ET0_max (ancien)
    et0 = data.get('ET0') or data.get('ET0_max', '—')
    lignes = [
        ["Paramètre", "Valeur"],
        ["Latitude",  str(data.get('lat','—')) + "°"],
        ["Longitude", str(data.get('lon','—')) + "°"],
        ["Température maximale", str(data.get('temperature_max','—')) + " °C"],
        ["Température minimale", str(data.get('temperature_min','—')) + " °C"],
        ["Irradiation (mois critique)",
            str(data.get('irradiation','—')) + " kWh/m²/jour"],
        ["ET0 maximale (Penman-Monteith FAO-56)",
            str(et0) + " mm/jour"],
        ["Mois critique", str(data.get('mois_critique','—'))],
    ]
    elements.append(tableau_donnees(lignes))
    elements.append(esp())
    return elements


def section_besoins(data, styles):
    elements = [bandeau("3. Besoins en eau"), sep()]
    b = data.get('besoins', {}) or {}
    lignes = [
        ["Paramètre", "Valeur"],
        ["ETc / Besoin journalier",
            str(b.get('ETc','—')) + " mm/jour ou m³/jour"],
        ["Besoin net en eau",
            str(b.get('besoin_net_m3_jour','—')) + " m³/jour"],
        ["Besoin brut en eau",
            str(b.get('besoin_brut_m3_jour','—')) + " m³/jour"],
        ["Besoin par session",
            str(b.get('besoin_session_m3','—')) + " m³"],
    ]
    if b.get('kc_utilise'):
        lignes.append(["Coefficient cultural Kc", str(b['kc_utilise'])])
    if data.get('heures_pompage'):
        lignes.append(["Heures de pompage / jour", str(data['heures_pompage']) + " h"])
    elements.append(tableau_donnees(lignes))
    elements.append(esp())
    return elements


def section_hydraulique(data, styles):
    elements = [bandeau("4. Dimensionnement hydraulique"), sep()]
    h = data.get('hydraulique', {}) or {}
    debit_ls = val_ou_nc(h.get('debit_L_s'))
    vitesse  = val_ou_nc(h.get('vitesse_m_s'))
    lignes = [
        ["Paramètre", "Valeur"],
        ["Débit Q",
            str(h.get('debit_m3_h','—')) + " m³/h" +
            (" (" + debit_ls + " L/s)" if debit_ls != 'Non calculé' else "")],
        ["Hauteur géométrique",
            str(h.get('hauteur_geo_m','—')) + " m"],
        ["Pertes de charge",
            str(h.get('pertes_charge_m','—')) + " m"],
        ["HMT totale",
            str(h.get('HMT_m','—')) + " m"],
    ]
    if vitesse != 'Non calculé':
        lignes.insert(-1, ["Vitesse dans la canalisation", vitesse + " m/s"])
    elements.append(tableau_donnees(lignes))
    elements.append(esp())
    return elements


def section_pompe(data, styles):
    elements = [bandeau("5. Dimensionnement de la pompe"), sep()]
    p   = data.get('pompe', {}) or {}
    src = data.get('source_energie', '')
    lignes = [
        ["Paramètre", "Valeur"],
        ["Puissance hydraulique Ph",           str(p.get('Ph_kW','—')) + " kW"],
        ["Puissance absorbée Pp",              str(p.get('Pp_kW','—')) + " kW"],
        ["Puissance moteur calculée Pm",       str(p.get('Pm_kW','—')) + " kW"],
        ["Puissance commerciale normalisée",   str(p.get('Pm_commercial_kW','—')) + " kW"],
    ]
    # Ancien format pompe sélectionnée
    mp  = data.get('marque_pompe','')
    mdl = data.get('modele_pompe','')
    if mp and mdl:
        lignes.append(["Pompe sélectionnée", mp + " — " + mdl])
    # SBEE / réseau : courant de ligne
    if src in ('sbee', 'reseau'):
        lignes.append(["Courant de ligne Ia", str(p.get('Ia_A','—')) + " A"])
        lignes.append(["Type d'alimentation", str(p.get('type_alimentation','—'))])
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
    return '—'


def section_energie(data, styles):
    elements = [bandeau("6. Dimensionnement énergétique"), sep()]
    e   = data.get('energie', {}) or {}
    src = data.get('source_energie', 'solaire')

    # Helpers pour lire champ nouveau OU ancien
    def nb_pan():
        v = data.get('nbr_panneaux')
        return v if v else e.get('nb_panneaux_300Wc', '—')

    def cfg_pv():
        ns = data.get('nbr_pv_serie')
        np = data.get('nbr_pv_parallele')
        if ns and np:
            return str(ns) + "S × " + str(np) + "P"
        return '—'

    if src == "solaire":
        lignes = [
            ["Paramètre", "Valeur"],
            ["Source d'énergie", "Solaire photovoltaïque"],
            ["Irradiation utilisée", str(data.get('irradiation','—')) + " kWh/m²/j"],
            ["Performance Ratio Pr", str(data.get('pr_ratio', e.get('pr_ratio','—')))],
            ["Énergie journalière",
                str(e.get('energie_jour_kWh','—')) + " kWh/jour"],
            ["Puissance crête calculée",
                str(e.get('puissance_crete_kWp','—')) + " kWc"],
            ["Tension système Usyst", _tension_str(e, data)],
            ["Nombre de panneaux", pluriel(nb_pan(), 'panneau','panneaux')],
            ["Configuration PV", cfg_pv()],
        ]

    elif src in ("groupe", "groupe_electrogene"):
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
        sol = e.get('solaire', {})
        grp = e.get('groupe', {})
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
        sol = e.get('solaire', e)   # nouveau format : champs directs sur e
        lignes = [
            ["Paramètre", "Valeur"],
            ["Source d'énergie", "Hybride — Solaire + Batteries"],
            ["Énergie journalière",
                str(e.get('energie_jour_kWh',
                    sol.get('energie_jour_kWh','—'))) + " kWh/jour"],
            ["Puissance crête solaire",
                str(e.get('puissance_crete_kWp',
                    sol.get('puissance_crete_kWp','—'))) + " kWc"],
            ["Tension système Usyst", _tension_str(e, data)],
            ["Nombre de panneaux", pluriel(nb_pan(), 'panneau','panneaux')],
            ["Configuration PV", cfg_pv()],
            ["Capacité totale batteries",
                str(data.get('ctot') or e.get('capacite_totale_Ah','—')) + " Ah"],
            ["Nombre de batteries",
                pluriel(data.get('nbat_tot') or e.get('nb_batteries','—'),
                        'batterie','batteries')],
            ["Configuration batteries",
                str(data.get('nbat_serie','—')) + "S × " +
                str(data.get('nbat_par','—')) + "P"],
            ["Jours d'autonomie",
                str(data.get('jours_autonomie',
                    e.get('jours_autonomie','—'))) + " jour(s)"],
        ]

    elif src in ("sbee", "reseau"):
        lignes = [
            ["Paramètre", "Valeur"],
            ["Source d'énergie", "Réseau électrique / SBEE"],
            ["Puissance souscrite Ps",
                str(e.get('puissance_souscrite_kW','—')) + " kW"],
            ["Type d'alimentation",
                str(e.get('type_reseau','—'))],
            ["Courant de ligne Ia",
                str((data.get('pompe') or {}).get('Ia_A','—')) + " A"],
        ]
    else:
        lignes = [["Paramètre", "Valeur"], ["Source d'énergie", str(src)]]

    elements.append(tableau_donnees(lignes))
    elements.append(esp())
    return elements


def section_equipements(data, styles):
    src   = data.get('source_energie', '')
    equip = data.get('equipements', {}) or {}
    hasPV = src in ['solaire', 'hybride_batteries', 'hybride_groupe']

    # Détecter le format (nouveau ou ancien)
    new_format = bool(equip.get('pompe') or equip.get('controleur') or equip.get('panneau'))

    # Ancien format fallback
    mp_old  = data.get('marque_pompe', '')
    mdl_old = data.get('modele_pompe', '')

    if not new_format and not mp_old and not hasPV:
        return []

    elements = [bandeau("7. Équipements sélectionnés"), sep()]

    if new_format:
        p   = equip.get('pompe', {}) or {}
        c   = equip.get('controleur', {}) or {}
        pan = equip.get('panneau', {}) or {}
        bat = equip.get('batterie', {}) or {}
        type_ctrl = equip.get('type_ctrl', '')

        # — Pompe —
        if p:
            elements.append(Paragraph("Pompe", styles["gras"]))
            lignes = [
                ["Paramètre", "Valeur"],
                ["Marque / Modèle",
                    str(p.get('marque','')) + " " + str(p.get('modele',''))],
                ["Type", str(p.get('type_pompe','—'))],
                ["Débit max",
                    str(p.get('debit_max_m3h','—')) + " m³/h"],
                ["HMT max",
                    str(p.get('HMT_max_m','—')) + " m"],
                ["Puissance nominale",
                    str(p.get('puissance_kW','—')) + " kW"],
                ["Tension / Alimentation",
                    str(p.get('tension_V','—'))],
                ["Type alimentation",
                    str(p.get('type_alimentation', equip.get('mode_alim','—')))],
            ]
            elements.append(tableau_donnees(lignes))
            elements.append(sep())

        # — Contrôleur / VFD —
        if c:
            titre_ctrl = "Régulateur MPPT" if type_ctrl == 'MPPT' else "Variateur de fréquence (VFD)"
            elements.append(Paragraph(titre_ctrl, styles["gras"]))
            if type_ctrl == 'MPPT':
                lignes = [
                    ["Paramètre", "Valeur"],
                    ["Marque / Modèle",
                        str(c.get('marque','')) + " " + str(c.get('modele',''))],
                    ["Courant max", str(c.get('courant_max_A','—')) + " A"],
                    ["Tension système", str(c.get('tension_systeme','—'))],
                    ["Plage tension PV", str(c.get('plage_tension_pv','—'))],
                ]
            else:
                lignes = [
                    ["Paramètre", "Valeur"],
                    ["Modèle", str(c.get('modele','—'))],
                    ["Puissance", str(c.get('puissance_kW','—')) + " kW"],
                    ["Courant sortie", str(c.get('courant_sortie_A','—')) + " A"],
                    ["Type sortie", str(c.get('type_sortie','—'))],
                ]
            elements.append(tableau_donnees(lignes))
            elements.append(sep())

        # — Panneaux —
        if pan and hasPV:
            elements.append(Paragraph("Panneaux solaires", styles["gras"]))
            lignes = [
                ["Paramètre", "Valeur"],
                ["Marque / Modèle",
                    str(pan.get('marque','')) + " " + str(pan.get('modele',''))],
                ["Type", str(pan.get('type','—'))],
                ["Puissance unitaire", str(pan.get('puissance_W','—')) + " Wc"],
                ["Voc", str(pan.get('Voc_V','—')) + " V"],
                ["Isc", str(pan.get('Isc_A','—')) + " A"],
                ["Vmp", str(pan.get('Vmp_V','—')) + " V"],
                ["Nombre / Configuration",
                    pluriel(data.get('nbr_panneaux','—'), 'panneau','panneaux') +
                    " — " + str(data.get('nbr_pv_serie','—')) + "S × " +
                    str(data.get('nbr_pv_parallele','—')) + "P"],
            ]
            elements.append(tableau_donnees(lignes))
            elements.append(sep())

        # — Batterie —
        if bat and src == 'hybride_batteries':
            elements.append(Paragraph("Batteries", styles["gras"]))
            lignes = [
                ["Paramètre", "Valeur"],
                ["Marque / Technologie",
                    str(bat.get('marque','')) + " — " + str(bat.get('technologie',''))],
                ["Capacité unitaire", str(bat.get('capacite_Ah','—')) + " Ah"],
                ["Tension unitaire",  str(bat.get('tension_V','—')) + " V"],
                ["DoD",               str(round((bat.get('dod',0.5) or 0.5)*100)) + " %"],
                ["Capacité totale",   str(round(data.get('ctot',0) or 0)) + " Ah"],
                ["Nombre / Configuration",
                    pluriel(data.get('nbat_tot','—'), 'batterie','batteries') +
                    " — " + str(data.get('nbat_serie','—')) + "S × " +
                    str(data.get('nbat_par','—')) + "P"],
                ["Jours d'autonomie", str(data.get('jours_autonomie','—')) + " jour(s)"],
            ]
            elements.append(tableau_donnees(lignes))
            elements.append(sep())

    else:
        # Ancien format
        if mp_old and mdl_old:
            elements.append(Paragraph("Pompe", styles["gras"]))
            elements.append(tableau_equipement(
                [["Marque", "Modèle"], [mp_old, mdl_old]],
                col_widths=[8.5*cm, 8.5*cm]
            ))
            elements.append(Spacer(1, 0.25*cm))

        if hasPV:
            mp2 = equip.get('marque_panneau', '')
            md2 = equip.get('modele_panneau', '')
            nb2 = data.get('nb_panneaux_calcul', '')
            if mp2:
                elements.append(Paragraph("Panneau solaire", styles["gras"]))
                elements.append(tableau_equipement(
                    [["Marque","Modèle","Nombre calculé"],
                     [mp2, md2, pluriel(nb2,'panneau','panneaux')]]
                ))
                elements.append(Spacer(1, 0.25*cm))

            if src == 'hybride_batteries':
                mb  = equip.get('marque_batterie', '')
                mdb = equip.get('modele_batterie', '')
                nb3 = data.get('energie', {}).get('nb_batteries', '')
                if mb:
                    elements.append(Paragraph("Batterie", styles["gras"]))
                    elements.append(tableau_equipement(
                        [["Marque","Modèle","Nombre calculé"],
                         [mb, mdb, pluriel(nb3,'batterie','batteries')]]
                    ))

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

    elements.append(esp())
    return elements


def section_cables(data, styles):
    """Section câbles et protections — nouveau flux uniquement."""
    cables     = data.get('cables_resultats', [])
    parafoudres = data.get('parafoudres', {}) or {}
    if not cables and not parafoudres:
        return []

    elements = [bandeau("8. Câbles et protections"), sep()]

    if cables:
        col_w = [4.0*cm, 1.8*cm, 1.8*cm, 1.8*cm, 4.2*cm, 3.4*cm]
        lignes = [["Tronçon", "I (A)", "L (m)", "S (mm²)", "Câble", "Disjoncteur"]]
        for t in cables:
            cab = t.get('cable', {}) or {}
            dj  = t.get('disjoncteur', {}) or {}
            lignes.append([
                str(t.get('troncon', '—')),
                str(round(float(t.get('I_A', 0) or 0), 1)),
                str(t.get('L_m', 0)),
                str(t.get('S_normalisee', '—')) + " mm²",
                str(cab.get('designation', '—')),
                str(dj.get('designation', '—')) +
                    ("\n" + str(dj.get('calibre','')) if dj.get('calibre') else ''),
            ])
        elements.append(tableau_equipement(lignes, col_widths=col_w))
        elements.append(sep())

    if parafoudres:
        elements.append(Paragraph("Parafoudres recommandés", styles["gras"]))
        lignes_p = [["Type", "Désignation", "Calibre", "Prix (FCFA)"]]
        for k, p in parafoudres.items():
            if p:
                lignes_p.append([
                    str(k),
                    str(p.get('designation', '—')),
                    str(p.get('calibre', '—')),
                    fmt_fcfa(p.get('prix', 0)),
                ])
        elements.append(tableau_equipement(
            lignes_p, col_widths=[2.5*cm, 6.5*cm, 4.5*cm, 3.5*cm]
        ))
        elements.append(sep())

    elements.append(esp())
    return elements


def section_cout(data, styles):
    cout  = data.get('cout') or {}
    equip = data.get('equipements', {}) or {}
    if not cout:
        return []

    elements = [bandeau("9. Coût estimatif de l'installation"), sep()]

    src      = data.get('source_energie', '')
    p        = equip.get('pompe', {}) or {}
    c        = equip.get('controleur', {}) or {}
    pan      = equip.get('panneau', {}) or {}
    bat      = equip.get('batterie', {}) or {}
    type_ctrl = equip.get('type_ctrl', '')
    nbr_pan  = data.get('nbr_panneaux', 0) or 0
    nbat_tot = data.get('nbat_tot', 0) or 0

    # Nouveau format : tableau 4 colonnes
    if p or c or pan:
        lignes = [["Désignation", "Qté", "P.U. (FCFA)", "Total (FCFA)"]]

        if cout.get('C_pompe', 0):
            nom_p = (p.get('marque','') + " " + p.get('modele','')).strip() or "Pompe"
            lignes.append([nom_p, "1",
                           fmt_fcfa(p.get('prix',0)), fmt_fcfa(cout['C_pompe'])])

        if cout.get('C_controleur', 0):
            nom_c = ("Rég. MPPT " if type_ctrl == 'MPPT' else "VFD ") + str(c.get('modele',''))
            lignes.append([nom_c.strip(), "1",
                           fmt_fcfa(c.get('prix',0)), fmt_fcfa(cout['C_controleur'])])

        if cout.get('C_panneaux', 0) and pan:
            nom_pan = str(pan.get('marque','')) + " " + str(pan.get('puissance_W','')) + " Wc"
            lignes.append([("Panneau " + nom_pan).strip(), str(nbr_pan),
                           fmt_fcfa(pan.get('prix',0)), fmt_fcfa(cout['C_panneaux'])])

        if cout.get('C_batteries', 0) and bat:
            nom_bat = str(bat.get('marque','')) + " " + str(bat.get('capacite_Ah','')) + " Ah"
            lignes.append([("Batterie " + nom_bat).strip(), str(nbat_tot),
                           fmt_fcfa(bat.get('prix',0)), fmt_fcfa(cout['C_batteries'])])

        c_cdb = (cout.get('C_cables', 0) or 0) + (cout.get('C_disjoncteurs', 0) or 0)
        if c_cdb > 0:
            lignes.append(["Câbles et disjoncteurs", "—", "—", fmt_fcfa(c_cdb)])

        if cout.get('C_parafoudres', 0):
            lignes.append(["Parafoudres", "—", "—", fmt_fcfa(cout['C_parafoudres'])])

        lignes.append(["SOUS-TOTAL ÉQUIPEMENTS", "", "", fmt_fcfa(cout.get('C_equipements',0))])
        lignes.append(["Main d'œuvre & installation (15%)", "15%", "", fmt_fcfa(cout.get('C_installation',0))])
        lignes.append(["Frais divers & imprévus (10%)", "10%", "", fmt_fcfa(cout.get('C_divers',0))])
        lignes.append(["COÛT TOTAL ESTIMATIF", "", "", fmt_fcfa(cout.get('C_total',0))])
        elements.append(tableau_cout_detaille(lignes))

    else:
        # Ancien format — 2 colonnes
        lignes = [
            ["Poste", "Montant (FCFA)"],
            ["Coût de la pompe",                      fmt_fcfa(cout.get('C_pompe',0))],
            ["Coût des équipements énergétiques",      fmt_fcfa(cout.get('C_energie',0))],
            ["Main d'œuvre & installation (15%)",      fmt_fcfa(cout.get('C_installation',0))],
            ["Divers & imprévus (10%)",                fmt_fcfa(cout.get('C_divers',0))],
            ["COÛT TOTAL ESTIMATIF",                   fmt_fcfa(cout.get('C_total',0))],
        ]
        elements.append(tableau_donnees_avec_total(lignes))

    elements.append(esp())
    return elements


def section_conclusion(data, styles):
    elements = [bandeau("10. Conclusion"), sep()]
    h    = data.get('hydraulique', {}) or {}
    p    = data.get('pompe', {}) or {}
    equip = data.get('equipements', {}) or {}
    src  = data.get('source_energie', '—')
    cout = data.get('cout') or {}

    # Pompe
    pompe_d = equip.get('pompe', {})
    if pompe_d:
        pompe_str = pompe_d.get('marque','') + " " + pompe_d.get('modele','')
    else:
        pompe_str = data.get('marque_pompe','—') + " " + data.get('modele_pompe','')
    pompe_str = pompe_str.strip() or '—'

    texte = (
        "Le présent rapport présente les résultats du dimensionnement "
        "du système de pompage. "
        "Le débit calculé est de <b>" + str(h.get('debit_m3_h','—')) +
        " m³/h</b> pour une hauteur manométrique totale (HMT) de <b>" +
        str(h.get('HMT_m','—')) + " m</b>. "
        "La puissance moteur nécessaire est de <b>" +
        str(p.get('Pm_kW','—')) + " kW</b> (puissance commerciale : <b>" +
        str(p.get('Pm_commercial_kW','—')) + " kW</b>). "
        "La source d'énergie retenue est : <b>" +
        str(src).replace('_',' ').title() + "</b>. "
        "La pompe sélectionnée est la <b>" + pompe_str + "</b>."
    )
    if cout.get('C_total'):
        texte += (
            " Le coût total estimatif de l'installation est de <b>" +
            fmt_fcfa(cout['C_total']) + " FCFA</b>, "
            "incluant la main d'œuvre (15%) et les frais divers (10%)."
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

    hdr_data = [[Paragraph("LE TECHNICIEN", lbl), Paragraph("LE CLIENT", lbl)]]
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

    txt_tech = ("Je soussigné(e), <b>" + realise_par + "</b>, certifie avoir réalisé "
                "cette étude conformément aux règles de l'art.")
    txt_cli  = ("Je soussigné(e), <b>" + nom_client + "</b>, déclare avoir pris "
                "connaissance de ce rapport de dimensionnement.")

    corps_t = Table([[Paragraph(txt_tech, txt), Paragraph(txt_cli, txt)]],
                    colWidths=[8.5*cm, 8.5*cm])
    corps_t.setStyle(TableStyle([
        ('VALIGN',       (0,0),(-1,-1), 'TOP'),
        ('LEFTPADDING',  (0,0),(-1,-1), 6),
        ('RIGHTPADDING', (0,0),(-1,-1), 6),
    ]))
    elements.append(corps_t)
    elements.append(Spacer(1, 1.2*cm))

    sig_style = ParagraphStyle(
        name='SigLine', fontName='Helvetica', fontSize=9, textColor=GRIS_TEXTE,
    )
    sig_data = [
        [Paragraph("Signature :", sig_style), Paragraph("Signature :", sig_style)],
        [Spacer(1, 1.5*cm), Spacer(1, 1.5*cm)],
        [HRFlowable(width=7*cm, thickness=0.5, color=GRIS_LIGNE, spaceAfter=8, spaceBefore=2),
         HRFlowable(width=7*cm, thickness=0.5, color=GRIS_LIGNE, spaceAfter=8, spaceBefore=2)],
        [Paragraph("Date : " + date_str, sig_style), Paragraph("Date : " + date_str, sig_style)],
        [Spacer(1, 0.6*cm), Spacer(1, 0.6*cm)],
        [HRFlowable(width=7*cm, thickness=0.5, color=GRIS_LIGNE, spaceAfter=8, spaceBefore=2),
         HRFlowable(width=7*cm, thickness=0.5, color=GRIS_LIGNE, spaceAfter=8, spaceBefore=2)],
        [Paragraph("Cachet :", sig_style), Paragraph("", sig_style)],
        [Spacer(1, 2.0*cm), Spacer(1, 0.5*cm)],
        [HRFlowable(width=4*cm, thickness=0.5, color=GRIS_LIGNE, spaceAfter=2, spaceBefore=2),
         Paragraph("", sig_style)],
    ]
    sig_t = Table(sig_data, colWidths=[8.5*cm, 8.5*cm])
    sig_t.setStyle(TableStyle([
        ('VALIGN',       (0,0),(-1,-1), 'TOP'),
        ('TOPPADDING',   (0,0),(-1,-1), 4),
        ('BOTTOMPADDING',(0,0),(-1,-1), 4),
        ('LEFTPADDING',  (0,0),(-1,-1), 6),
        ('RIGHTPADDING', (0,0),(-1,-1), 6),
    ]))
    elements.append(sig_t)
    return elements


def pied_de_page(styles):
    return []
