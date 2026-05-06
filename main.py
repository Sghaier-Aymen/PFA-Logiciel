import csv
import sys

# ─────────────────────────────────────────────
# 1. Génération du fichier ventes.csv
# ─────────────────────────────────────────────
data = [
    ['ID', 'Prix', 'Quantite', 'Remise'],
    [101, 15.0, 3, 10],
    [102, 25.0, 2, 5],
    [103, 10.0, 5, 0]
]

with open('ventes.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(data)

print("✅ ventes.csv généré avec succès.")

# ─────────────────────────────────────────────
# Lecture et Traitement (Étapes 2 à 6)
# Bonus : lecture dynamique (n'importe quel CSV)
# ─────────────────────────────────────────────
csv_file = sys.argv[1] if len(sys.argv) > 1 else 'ventes.csv'

resultats = []
ca_total_entreprise = 0.0
meilleur_benefice = 0.0
id_meilleur_produit = None

with open(csv_file, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        id_prod    = row['ID']
        prix       = float(row['Prix'])
        quantite   = int(row['Quantite'])
        remise_pct = float(row['Remise'])

        # 2. CA Brut
        ca_brut = prix * quantite

        # 3. CA Net (après remise)
        ca_net = ca_brut * (1 - remise_pct / 100)

        # 4. TVA 20%
        tva = ca_net * 0.20

        # 5. CA Total
        ca_total_entreprise += ca_net

        # 6. Meilleur bénéfice
        if ca_net > meilleur_benefice:
            meilleur_benefice   = ca_net
            id_meilleur_produit = id_prod

        row.update({
            'CA_Brut': round(ca_brut, 2),
            'CA_Net':  round(ca_net,  2),
            'TVA':     round(tva,     2)
        })
        resultats.append(row)

# ─────────────────────────────────────────────
# 5. Affichage
# ─────────────────────────────────────────────
print(f"\n📊 Résultats d'analyse :")
print(f"   CA Total de l'entreprise : {ca_total_entreprise:.2f} DT")
print(f"   Produit avec le plus gros bénéfice : ID {id_meilleur_produit} "
      f"({meilleur_benefice:.2f} DT)")

# ─────────────────────────────────────────────
# 7. Export resultats_final.csv
# ─────────────────────────────────────────────
fieldnames = ['ID', 'Prix', 'Quantite', 'Remise', 'CA_Brut', 'CA_Net', 'TVA']
with open('resultats_final.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(resultats)

print("\n✅ resultats_final.csv exporté avec succès.")

# ─────────────────────────────────────────────
# BONUS : Graphiques Matplotlib
# ─────────────────────────────────────────────
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import numpy as np

    ids      = [r['ID']      for r in resultats]
    ca_bruts = [r['CA_Brut'] for r in resultats]
    ca_nets  = [r['CA_Net']  for r in resultats]
    tvas     = [r['TVA']     for r in resultats]

    x     = np.arange(len(ids))
    width = 0.28

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.patch.set_facecolor('#0F172A')

    # ── Graphique 1 : Barres groupées CA Brut / CA Net / TVA ──
    ax1 = axes[0]
    ax1.set_facecolor('#1E293B')
    b1 = ax1.bar(x - width, ca_bruts, width, label='CA Brut',   color='#38BDF8', alpha=0.9)
    b2 = ax1.bar(x,          ca_nets,  width, label='CA Net',    color='#34D399', alpha=0.9)
    b3 = ax1.bar(x + width,  tvas,     width, label='TVA (20%)', color='#FB923C', alpha=0.9)

    ax1.set_title('Comparaison CA par Produit', color='white', fontsize=13, fontweight='bold', pad=12)
    ax1.set_xlabel('Produit (ID)',  color='#94A3B8', fontsize=10)
    ax1.set_ylabel('Montant (DT)', color='#94A3B8', fontsize=10)
    ax1.set_xticks(x)
    ax1.set_xticklabels([f'ID {i}' for i in ids], color='white')
    ax1.tick_params(colors='#94A3B8')
    ax1.spines[:].set_color('#334155')
    ax1.legend(facecolor='#1E293B', edgecolor='#334155', labelcolor='white')

    for bar in [*b1, *b2, *b3]:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, h + 0.3, f'{h:.1f}',
                 ha='center', va='bottom', color='white', fontsize=7.5)

    # ── Graphique 2 : Camembert CA Net par produit ──
    ax2 = axes[1]
    ax2.set_facecolor('#1E293B')
    colors_pie = ['#38BDF8', '#34D399', '#FB923C']
    wedges, texts, autotexts = ax2.pie(
        ca_nets,
        labels=[f'ID {i}' for i in ids],
        autopct='%1.1f%%',
        colors=colors_pie,
        startangle=140,
        wedgeprops=dict(edgecolor='#0F172A', linewidth=2),
        textprops={'color': 'white', 'fontsize': 11}
    )
    for at in autotexts:
        at.set_fontsize(10)
        at.set_color('#0F172A')
        at.set_fontweight('bold')

    ax2.set_title('Répartition du CA Net', color='white', fontsize=13, fontweight='bold', pad=12)

    plt.tight_layout(pad=2.5)
    plt.savefig('graphiques_ventes.png', dpi=150, bbox_inches='tight',
                facecolor='#0F172A')
    plt.close()
    print("✅ graphiques_ventes.png généré (bonus Matplotlib).")

except ImportError:
    print("⚠️  Matplotlib non installé — graphiques ignorés.")
