import csv

def automatisation_ventes():
    resultats = []
    ca_total_net = 0
    max_benefice = 0
    id_meilleur_produit = None

    # Lecture du fichier source
    try:
        with open('ventes.csv', mode='r', encoding='utf-8') as fichier:
            lecteur = csv.DictReader(fichier)
            
            for ligne in lecteur:
                # Extraction et conversion des données
                id_prod = ligne['ID']
                prix = float(ligne['Prix'])
                quantite = int(ligne['Quantite'])
                remise_pourcent = float(ligne['Remise'])

                # 2. Calcul du Chiffre d'Affaires Brut [cite: 18]
                ca_brut = prix * quantite
                
                # 3. Application des remises pour le CA Net [cite: 19]
                ca_net = ca_brut * (1 - remise_pourcent / 100)
                
                # 4. Calcul de la TVA (20%) sur le CA Net [cite: 20]
                tva = ca_net * 0.20
                
                # Mise à jour du CA Total de l'entreprise [cite: 21]
                ca_total_net += ca_net

                # 6. Identifier l'ID du produit avec le plus gros bénéfice [cite: 22]
                if ca_net > max_benefice:
                    max_benefice = ca_net
                    id_meilleur_produit = id_prod

                # Préparation des nouvelles données pour l'export [cite: 24]
                ligne['CA_Net'] = round(ca_net, 2)
                ligne['TVA'] = round(tva, 2)
                resultats.append(ligne)

        # 5. Affichage des résultats dans la console [cite: 21, 22]
        print(f"--- Rapport de Ventes ---")
        print(f"CA Total de l'entreprise : {round(ca_total_net, 2)} DT")
        print(f"Produit le plus rentable (ID) : {id_meilleur_produit}")

        # 7. Exportation vers resultats_final.csv 
        champs = ['ID', 'Prix', 'Quantite', 'Remise', 'CA_Net', 'TVA']
        with open('resultats_final.csv', mode='w', newline='', encoding='utf-8') as export:
            scripteur = csv.DictWriter(export, fieldnames=champs)
            scripteur.writeheader()
            scripteur.writerows(resultats)
        print("\nExportation réussie dans 'resultats_final.csv'")

    except FileNotFoundError:
        print("Erreur : Le fichier 'ventes.csv' est introuvable.")

if __name__ == "__main__":
    automatisation_ventes()