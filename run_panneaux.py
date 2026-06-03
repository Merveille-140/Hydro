import sqlite3, pandas as pd

df = pd.read_excel(r'D:\Pompage\Equipements nouveaux.xlsx', header=None)
conn = sqlite3.connect(r'D:\Pompage\solarpump.db')

# ── PANNEAUX (pandas iloc 150-185 = Excel rows 151-186) ──────────────────────
# Bornes exactes : premier panel=row151, dernier panel=row185,
# row186 vide, row187="Batteries" -> range strict sans break nécessaire
# col[1]=marque  col[2]=modele  col[3]=type  col[4]=puissW  col[5]=tensV
# col[6]=Voc     col[7]=Isc     col[8]=Vmp   col[9]=Imp
conn.execute("DELETE FROM panneaux")
inseres = 0
for i in range(150, 186):
    row = df.iloc[i]
    marque = str(row[1]).strip() if pd.notna(row[1]) else None
    if not marque or marque == 'nan': continue
    type_p = str(row[3]).strip() if pd.notna(row[3]) else ''
    try:
        puiss = float(row[4]); tens  = float(row[5])
        voc   = float(row[6]); isc   = float(row[7])
        vmp   = float(row[8]); imp   = float(row[9])
    except:
        continue
    prix   = int(puiss * 183)
    modele = f"{marque} {int(puiss)}W {type_p}"
    conn.execute(
        """INSERT INTO panneaux
           (marque, modele, type, puissance_W, tension_V, Voc_V, Isc_A, Vmp_V, Imp_A, prix)
           VALUES (?,?,?,?,?,?,?,?,?,?)""",
        (marque, modele, type_p, puiss, tens, voc, isc, vmp, imp, prix))
    inseres += 1
print(f"Panneaux insérés : {inseres}")

# Vérification
rows12 = conn.execute(
    "SELECT marque, modele, tension_V, Voc_V FROM panneaux WHERE Voc_V < 24"
).fetchall()
print(f"Panneaux 12V (Voc<24V) : {len(rows12)}")
for r in rows12: print(" ", r)

print(f"\nTotal panneaux : {conn.execute('SELECT COUNT(*) FROM panneaux').fetchone()[0]}")
print("Échantillon :")
for r in conn.execute(
    "SELECT marque, modele, puissance_W, tension_V, Voc_V FROM panneaux ORDER BY puissance_W LIMIT 5"
).fetchall():
    print(" ", r)

conn.commit()
conn.close()
