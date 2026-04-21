# ============================================================
# DATABASE.PY — GESTION BASE DE DONNÉES SQLITE
# ============================================================

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'solarpump.db')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # TABLE UTILISATEURS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS utilisateurs (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            nom           TEXT NOT NULL,
            email         TEXT NOT NULL UNIQUE,
            mot_de_passe  TEXT NOT NULL,
            organisation  TEXT,
            date_creation TEXT DEFAULT (datetime('now'))
        )
    ''')

    # TABLE PROJETS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projets (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id      INTEGER NOT NULL,
            nom_projet   TEXT NOT NULL,
            realise_par  TEXT,
            date_projet  TEXT,
            mode         TEXT,
            source_energie TEXT,
            lat          TEXT,
            lon          TEXT,
            resultats    TEXT,
            date_creation TEXT DEFAULT (datetime('now')),
            date_modif    TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES utilisateurs(id)
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Base de données initialisée.")


# ============================================================
# UTILISATEURS
# ============================================================

def creer_utilisateur(nom, email, mot_de_passe_hash, organisation=''):
    conn = get_db()
    try:
        conn.execute(
            'INSERT INTO utilisateurs (nom, email, mot_de_passe, organisation) VALUES (?, ?, ?, ?)',
            (nom, email, mot_de_passe_hash, organisation)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def get_utilisateur_par_email(email):
    conn = get_db()
    user = conn.execute(
        'SELECT * FROM utilisateurs WHERE email = ?', (email,)
    ).fetchone()
    conn.close()
    return user


def get_utilisateur_par_id(user_id):
    conn = get_db()
    user = conn.execute(
        'SELECT * FROM utilisateurs WHERE id = ?', (user_id,)
    ).fetchone()
    conn.close()
    return user


# ============================================================
# PROJETS
# ============================================================

def sauvegarder_projet(user_id, nom_projet, realise_par, date_projet,
                        mode, source_energie, lat, lon, resultats_json):
    conn = get_db()
    cursor = conn.execute(
        '''INSERT INTO projets
           (user_id, nom_projet, realise_par, date_projet, mode, source_energie, lat, lon, resultats)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (user_id, nom_projet, realise_par, date_projet,
         mode, source_energie, lat, lon, resultats_json)
    )
    projet_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return projet_id


def mettre_a_jour_projet(projet_id, user_id, resultats_json):
    conn = get_db()
    conn.execute(
        '''UPDATE projets SET resultats = ?, date_modif = datetime('now')
           WHERE id = ? AND user_id = ?''',
        (resultats_json, projet_id, user_id)
    )
    conn.commit()
    conn.close()


def get_projets_utilisateur(user_id):
    conn = get_db()
    projets = conn.execute(
        '''SELECT id, nom_projet, realise_par, date_projet, mode,
                  source_energie, lat, lon, date_creation, date_modif
           FROM projets WHERE user_id = ?
           ORDER BY date_modif DESC''',
        (user_id,)
    ).fetchall()
    conn.close()
    return projets


def get_projet_par_id(projet_id, user_id):
    conn = get_db()
    projet = conn.execute(
        'SELECT * FROM projets WHERE id = ? AND user_id = ?',
        (projet_id, user_id)
    ).fetchone()
    conn.close()
    return projet


def supprimer_projet(projet_id, user_id):
    conn = get_db()
    conn.execute(
        'DELETE FROM projets WHERE id = ? AND user_id = ?',
        (projet_id, user_id)
    )
    conn.commit()
    conn.close()


# Initialisation automatique au démarrage
init_db()