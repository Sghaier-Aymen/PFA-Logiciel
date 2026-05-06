import csv

# 1. Génération du fichier ventes.csv
data = [
    ['ID', 'Prix', 'Quantite', 'Remise'],
    [101, 15.0, 3, 10],
    [102, 25.0, 2, 5],
    [103, 10.0, 5, 0]
]

with open('ventes.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(data)

# Lecture et Traitement (Étapes 2 à 6)
resultats = []
ca_total_entreprise = 0
meilleur_benefice = 0
id_meilleur_produit = None

with open('ventes.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Conversion des types
        id_prod = row['ID']
        prix = float(row['Prix'])
        quantite = int(row['Quantite'])
        remise_pct = float(row['Remise'])

        # 2. CA Brut
        ca_brut = prix * quantite
        
        # 3. CA Net (Application de la remise)
        ca_net = ca_brut * (1 - remise_pct / 100)
        
        # 4. TVA (20%)
        tva = ca_net * 0.20
        
        # 5. Calcul pour le CA Total
        ca_total_entreprise += ca_net
        
        # 6. Identification du plus gros bénéfice (basé sur le CA Net ici)
        if ca_net > meilleur_benefice:
            meilleur_benefice = ca_net
            id_meilleur_produit = id_prod

        # Stockage pour l'export
        row.update({
            'CA_Brut': round(ca_brut, 2),
            'CA_Net': round(ca_net, 2),
            'TVA': round(tva, 2)
        })
        resultats.append(row)

# 5. Affichage du CA Total
print(f"Le CA Total de l'entreprise est : {ca_total_entreprise:.2f} DT")
print(f"Produit avec le plus gros bénéfice : ID {id_meilleur_produit}")

# 7. Exportation vers resultats_final.csv
fieldnames = ['ID', 'Prix', 'Quantite', 'Remise', 'CA_Brut', 'CA_Net', 'TVA']
with open('resultats_final.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(resultats)