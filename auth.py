# ============================================================
# AUTH.PY — GESTION AUTHENTIFICATION
# ============================================================

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
from database import creer_utilisateur, get_utilisateur_par_email

auth = Blueprint('auth', __name__)
bcrypt = Bcrypt()


# ============================================================
# INSCRIPTION
# ============================================================

@auth.route('/inscription', methods=['GET', 'POST'])
def inscription():
    session.clear()
    if request.method == 'POST':
        nom          = request.form.get('nom', '').strip()
        prenom       = request.form.get('prenom', '').strip()
        email        = request.form.get('email', '').strip().lower()
        mdp          = request.form.get('mot_de_passe', '')
        mdp_confirm  = request.form.get('mot_de_passe_confirm', '')

        if not nom or not prenom or not email or not mdp:
            flash('Veuillez remplir tous les champs obligatoires.', 'error')
            return render_template('inscription.html')

        if mdp != mdp_confirm:
            flash('Les mots de passe ne correspondent pas.', 'error')
            return render_template('inscription.html')

        if len(mdp) < 6:
            flash('Le mot de passe doit contenir au moins 6 caractères.', 'error')
            return render_template('inscription.html')

        mdp_hash   = bcrypt.generate_password_hash(mdp).decode('utf-8')
        nom_complet = prenom + ' ' + nom.upper()

        succes = creer_utilisateur(nom_complet, email, mdp_hash)

        if succes:
            user = get_utilisateur_par_email(email)
            session.permanent     = False
            session['user_id']    = user['id']
            session['user_nom']   = nom_complet
            session['user_email'] = email
            session['connecte']   = True
            session['actif']      = True
            return redirect(url_for('dashboard'))
        else:
            flash('Cet email est déjà utilisé.', 'error')
            return render_template('inscription.html')

    return render_template('inscription.html')


# ============================================================
# CONNEXION
# ============================================================

@auth.route('/connexion', methods=['GET', 'POST'])
def connexion():
    session.clear()
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        mdp   = request.form.get('mot_de_passe', '')

        if not email or not mdp:
            flash('Veuillez remplir tous les champs.', 'error')
            return render_template('connexion.html')

        user = get_utilisateur_par_email(email)

        if user and bcrypt.check_password_hash(user['mot_de_passe'], mdp):
            session.permanent     = False
            session['user_id']    = user['id']
            session['user_nom']   = user['nom']
            session['user_email'] = user['email']
            session['connecte']   = True
            session['actif']      = True
            return redirect(url_for('dashboard'))
        else:
            flash('Email ou mot de passe incorrect.', 'error')
            return render_template('connexion.html')

    return render_template('connexion.html')


# ============================================================
# DÉCONNEXION
# ============================================================

@auth.route('/deconnexion')
def deconnexion():
    session.clear()
    return redirect(url_for('index'))