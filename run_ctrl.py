import sqlite3
conn = sqlite3.connect(r'D:\Pompage\solarpump.db')

# Ajouter colonnes si elles n'existent pas
for col in ['ctrl_modele', 'ctrl_plage_tension_pv',
            'ctrl_vmin_V', 'ctrl_vmax_V', 'ctrl_imax_A']:
    try:
        conn.execute(f"ALTER TABLE pompes ADD COLUMN {col} TEXT")
    except: pass

# Données contrôleurs par modèle (sources : fiches techniques fabricants)
ctrl_data = [
    # Lorentz PS2
    ('Lorentz', 'PS2-600 C-SJ3-5',    'PS2-600',   24,  90, 13),
    ('Lorentz', 'PS2-1200 C-SJ5-5',   'PS2-1200',  30, 120, 14),
    ('Lorentz', 'PS2-1800 C-SJ5-7',   'PS2-1800',  30, 120, 14),
    ('Lorentz', 'PS2-1800 C-SJ8-4',   'PS2-1800',  30, 120, 14),
    ('Lorentz', 'PS2-2900 C-SJ5-11',  'PS2-2900',  48, 180, 16),
    ('Lorentz', 'PS2-4000 C-SJ8-8',   'PS2-4000',  60, 240, 18),
    ('Lorentz', 'PS2-4000 C-SJ12-5',  'PS2-4000',  60, 240, 18),
    ('Lorentz', 'PS2-7200 C-SJ8-12',  'PS2-7200',  96, 300, 25),
    ('Lorentz', 'PS2-7200 C-SJ17-7',  'PS2-7200',  96, 300, 25),
    ('Lorentz', 'PS2-15000 C-SJ20-10','PS2-15000', 120, 400, 40),
    # Grundfos SQFlex (CU202 controller)
    ('Grundfos', 'SQFlex 0.6-3',  'CU202', 30, 300, 8),
    ('Grundfos', 'SQFlex 1.2-8',  'CU202', 30, 300, 8),
    ('Grundfos', 'SQFlex 3-65',   'CU202', 30, 300, 8),
    ('Grundfos', 'SQFlex 5-35',   'CU202', 30, 300, 8),
    ('Grundfos', 'SQFlex 11-20',  'CU202', 30, 300, 8),
    ('Grundfos', 'SQFlex 2-115',  'CU202', 30, 300, 8),
    # Shakti SSH
    ('Shakti', 'SSH-370-4',  'Shakti MPPT',  24,  60,  8),
    ('Shakti', 'SSH-750-4',  'Shakti MPPT',  24,  72, 12),
    ('Shakti', 'SSH-1100-4', 'Shakti MPPT',  36,  96, 14),
    ('Shakti', 'SSH-1500-4', 'Shakti MPPT',  48, 120, 16),
    ('Shakti', 'SSH-2200-4', 'Shakti MPPT',  72, 150, 18),
    ('Shakti', 'SSH-3700-6', 'Shakti MPPT',  96, 180, 22),
    ('Shakti', 'SSH-5500-6', 'Shakti MPPT', 120, 240, 28),
    ('Shakti', 'SSH-7500-6', 'Shakti MPPT', 150, 300, 32),
    # Sunpumps SCS
    ('Sunpumps', 'SCS 5-130-60',   'SCS MPPT',  12,  48,  8),
    ('Sunpumps', 'SCS 10-165-160', 'SCS MPPT',  24,  72, 10),
    ('Sunpumps', 'SCS 20-200-240', 'SCS MPPT',  48, 120, 14),
    ('Sunpumps', 'SCS 30-250-350', 'SCS MPPT',  72, 150, 18),
    ('Sunpumps', 'SCS 50-300-500', 'SCS MPPT',  96, 200, 24),
]

maj = 0
for marque, modele, ctrl_mod, vmin, vmax, imax in ctrl_data:
    plage = f"{vmin}-{vmax}V"
    conn.execute("""
        UPDATE pompes
        SET ctrl_modele=?, ctrl_plage_tension_pv=?,
            ctrl_vmin_V=?, ctrl_vmax_V=?, ctrl_imax_A=?
        WHERE marque=? AND modele=?
    """, (ctrl_mod, plage, str(vmin), str(vmax), str(imax), marque, modele))
    maj += 1

conn.commit()
print(f"{maj} pompes traitées (UPDATE tenté)")

# Vérification
rows = conn.execute(
    "SELECT marque, modele, ctrl_modele, ctrl_plage_tension_pv, ctrl_imax_A FROM pompes WHERE ctrl_modele IS NOT NULL"
).fetchall()
print(f"Pompes avec contrôleur renseigné : {len(rows)}")
for r in rows: print(r)
conn.close()
