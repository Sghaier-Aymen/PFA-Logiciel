import csv

def traiter_ventes(fichier_entree, fichier_sortie):
    donnees_finales = []
    ca_total_entreprise = 0
    meilleur_produit = {"ID": None, "Benefice": 0}
    tva_taux = 0.20 [cite: 20]

    try:
        with open(fichier_entree, mode='r', newline='', encoding='utf-8') as f:
            lecteur = csv.DictReader(f)
            
            for ligne in lecteur:
                # Conversion des données
                id_prod = ligne['ID']
                prix = float(ligne['Prix'])
                quantite = int(ligne['Quantite'])
                remise_pourcent = float(ligne['Remise'])

                # 2. Calcul du Chiffre d'Affaires Brut [cite: 18]
                ca_brut = prix * quantite
                
                # 3. Application de la remise pour le CA Net [cite: 19]
                ca_net = ca_brut * (1 - remise_pourcent / 100)
                
                # 4. Calcul de la TVA (20%) [cite: 20]
                montant_tva = ca_net * tva_taux
                
                # 5. Cumul pour le CA Total
                ca_total_entreprise += ca_net

                # 6. Identification du plus gros bénéfice [cite: 22]
                if ca_net > meilleur_produit["Benefice"]:
                    meilleur_produit = {"ID": id_prod, "Benefice": ca_net}

                # Préparation de la ligne pour l'export [cite: 23, 24]
                ligne.update({
                    "CA_Brut": round(ca_brut, 2),
                    "CA_Net": round(ca_net, 2),
                    "TVA": round(montant_tva, 2)
                })
                donnees_finales.append(ligne)

        # 5. Affichage des résultats console [cite: 21]
        print(f"--- Résultats de l'Analyse ---")
        print(f"Chiffre d'Affaires Total : {ca_total_entreprise:.2f} DT")
        print(f"Produit le plus performant : ID {meilleur_produit['ID']} ({meilleur_produit['Benefice']:.2f} DT)")

        # 7. Exportation du fichier final [cite: 23]
        champs = list(donnees_finales[0].keys())
        with open(fichier_sortie, mode='w', newline='', encoding='utf-8') as f_out:
            scripteur = csv.DictWriter(f_out, fieldnames=champs)
            scripteur.writeheader()
            scripteur.writerows(donnees_finales)
            
        print(f"\nFichier '{fichier_sortie}' généré avec succès.")

    except FileNotFoundError:
        print("Erreur : Le fichier ventes.csv est introuvable.")

if __name__ == "__main__":
    traiter_ventes('ventes.csv', 'resultats_final.csv')