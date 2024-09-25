# Variables d'entrée

# === Temporalité ===
mois_debut_mission = 1  # Mois de début de mission (1 pour janvier, 12 pour décembre)
duree_projection = 12  # Nombre total de mois pour la projection (12 mois après le début de mission)
mois_actuel_de_reference = 1  # Mois actuel de référence (facultatif, 1 pour janvier)
delai_premiere_vente_souhaitee = 4  # Délai en mois après le début de la prospection pour la première vente souhaitée (facultatif)

# === Coûts de la prestation BAAX ===
cout_audit_mois1 = 4000  # Coût initial d'audit (premier mois de la mission)
cout_mensuel_mois2_3 = 3000  # Coût mensuel fixe pour les mois 2 et 3 de la mission
cout_mensuel_fixe = 3000  # Coût mensuel fixe à partir du mois 4 de la mission
cout_variable_par_rdv = 300  # Coût variable par rendez-vous qualifié
mois_debut_remuneration_variable = 1  # Mois de début de la rémunération variable (relatif au début de la mission)

# === Statistiques du Business Development ===
nb_prospects_mensuel = 500  # Nombre de nouveaux prospects contactés par mois
taux_ouverture = 0.60  # Taux d'ouverture des emails (60%)
taux_reponse = 0.10  # Taux de réponse des prospects ayant ouvert l'email (10%)
taux_reponses_positives = 0.30  # Taux de réponses positives parmi les réponses reçues (30%)
taux_prise_rdv = 0.50  # Taux de prise de rendez-vous sur les réponses positives (50%)
taux_rdv_qualifies = 0.90  # Pourcentage de rendez-vous réalisés qui sont qualifiés (90%)

# Taux réduits pour les mois de mai, août et décembre
taux_ouverture_mois_reduits = 0.50  # Taux d'ouverture réduit (50%)
taux_reponse_mois_reduits = 0.08    # Taux de réponse réduit (8%)
taux_reponses_positives_mois_reduits = 0.25  # Taux de réponses positives réduit (25%)

# === Chiffres du client ===
taux_conversion_ventes = 0.20  # Taux de conversion des rendez-vous qualifiés en ventes (20%)
delais_conversion_ventes = [3] * duree_projection  # Délai de conversion des ventes (3 mois pour chaque mois)
panier_moyen = 100000  # Panier moyen par vente
taux_de_marge = 0.25  # Taux de marge sur le panier moyen (25%)

# === Calculs Préliminaires ===

# Mois de début de la prospection
mois_debut_prospection = mois_debut_mission + 1  # La prospection commence le mois suivant le début de mission

# Mois de début des coûts variables (rémunération variable)
mois_debut_couts_variables = mois_debut_mission + mois_debut_remuneration_variable - 1

# Calcul du mois de la première vente souhaitée (mois relatif à la mission)
if delai_premiere_vente_souhaitee is not None:
    mois_premiere_vente_souhaitee = (mois_debut_prospection - mois_debut_mission + 1) + delai_premiere_vente_souhaitee - 1
else:
    mois_premiere_vente_souhaitee = None

# Initialisation du nombre de prospects sollicités par défaut pour chaque mois
prospects_solicites_par_mois = [0] * duree_projection  # Initialiser avec 0 prospects sollicités
for mois_de_mission in range(1, duree_projection + 1):
    if mois_de_mission >= (mois_debut_prospection - mois_debut_mission + 1):
        prospects_solicites_par_mois[mois_de_mission - 1] = nb_prospects_mensuel

calcul_possible = True  # Variable pour contrôler la suite du programme

# Calcul du nombre de prospects nécessaires si delai_premiere_vente_souhaitee est défini
if mois_premiere_vente_souhaitee is not None:
    delai_conversion = delais_conversion_ventes[0]  # Supposons que le délai est constant
    mois_rdv_necessaire = mois_premiere_vente_souhaitee - delai_conversion
    if mois_rdv_necessaire < (mois_debut_prospection - mois_debut_mission + 1):
        print("Impossible d'obtenir une vente au mois souhaité en raison des délais et du mois de début de prospection.")
        calcul_possible = False
    else:
        # Calcul du nombre de prospects nécessaires au mois_rdv_necessaire
        mois_calendaire_rdv = (mois_actuel_de_reference + mois_rdv_necessaire - 2) % 12 + 1
        if mois_calendaire_rdv in [5, 8, 12]:
            taux_ouv = taux_ouverture_mois_reduits
            taux_rep = taux_reponse_mois_reduits
            taux_rep_pos = taux_reponses_positives_mois_reduits
        else:
            taux_ouv = taux_ouverture
            taux_rep = taux_reponse
            taux_rep_pos = taux_reponses_positives

        required_rdv_qualifies = 1 / taux_conversion_ventes
        required_rdv_realises = required_rdv_qualifies / taux_rdv_qualifies
        required_reponses_positives = required_rdv_realises / taux_prise_rdv
        required_reponses_recues = required_reponses_positives / taux_rep_pos
        required_emails_ouverts = required_reponses_recues / taux_rep
        required_nb_prospects = required_emails_ouverts / taux_ouv

        # Arrondir au nombre entier supérieur
        required_nb_prospects = int(required_nb_prospects) + 1

        # Mettre à jour le nombre de prospects sollicités pour les mois concernés
        for mois_index in range(mois_debut_prospection - mois_debut_mission, mois_rdv_necessaire):
            prospects_solicites_par_mois[mois_index] = required_nb_prospects

# Initialisation des listes pour stocker les résultats
mois_list = []
couts_fixes_list = []
couts_variables_list = []
couts_totaux_list = []
prospects_solicites_list = []
emails_ouverts_list = []
reponses_recues_list = []
reponses_positives_list = []
rdv_realises_list = []
rdv_qualifies_list = []
ventes_attendues_list = []
revenus_list = []
profit_net_list = []
cumul_couts_list = []
cumul_revenus_list = []
cumul_profit_net_list = []

# Variables pour le cumul
cumul_couts = 0
cumul_revenus = 0
cumul_profit_net = 0

if calcul_possible:
    # Liste pour stocker le nombre de rendez-vous qualifiés pour calculer les ventes avec le délai
    historique_rdv_qualifies = []

    for mois_de_mission in range(1, duree_projection + 1):
        mois_list.append(mois_de_mission)

        # Calcul des coûts fixes
        if mois_de_mission == 1:
            cout_fixe = cout_audit_mois1
        elif mois_de_mission in [2, 3]:
            cout_fixe = cout_mensuel_mois2_3
        elif mois_de_mission >= 4:
            cout_fixe = cout_mensuel_fixe
        else:
            cout_fixe = 0  # Avant le début de la mission (cas improbable ici)
        couts_fixes_list.append(cout_fixe)

        # Index pour les listes
        index = mois_de_mission - 1

        # Nombre de prospects sollicités
        prospects_solicites = prospects_solicites_par_mois[index]
        prospects_solicites_list.append(prospects_solicites)

        # Calcul du mois calendaire réel
        mois_calendaire = (mois_actuel_de_reference + mois_de_mission - 2) % 12 + 1

        # Vérifier si le mois est mai, août ou décembre
        if mois_calendaire in [5, 8, 12]:
            # Utiliser les taux réduits
            taux_ouv = taux_ouverture_mois_reduits
            taux_rep = taux_reponse_mois_reduits
            taux_rep_pos = taux_reponses_positives_mois_reduits
        else:
            # Utiliser les taux normaux
            taux_ouv = taux_ouverture
            taux_rep = taux_reponse
            taux_rep_pos = taux_reponses_positives

        # Calcul du nombre d'emails ouverts
        emails_ouverts = prospects_solicites * taux_ouv
        emails_ouverts_list.append(emails_ouverts)

        # Calcul du nombre de réponses reçues
        reponses_recues = emails_ouverts * taux_rep
        reponses_recues_list.append(reponses_recues)

        # Calcul du nombre de réponses positives
        reponses_positives = reponses_recues * taux_rep_pos
        reponses_positives_list.append(reponses_positives)

        # Calcul du nombre de rendez-vous réalisés
        rdv_realises = reponses_positives * taux_prise_rdv
        rdv_realises_list.append(rdv_realises)

        # Calcul du nombre de rendez-vous qualifiés
        nb_rdv_qualifies = rdv_realises * taux_rdv_qualifies
        rdv_qualifies_list.append(nb_rdv_qualifies)
        historique_rdv_qualifies.append(nb_rdv_qualifies)

        # Calcul des coûts variables
        if mois_de_mission >= mois_debut_remuneration_variable:
            cout_variable = nb_rdv_qualifies * cout_variable_par_rdv
        else:
            cout_variable = 0
        couts_variables_list.append(cout_variable)

        # Coût total pour le mois
        cout_total = cout_fixe + cout_variable
        couts_totaux_list.append(cout_total)

        # Calcul des ventes attendues, en tenant compte du délai de conversion spécifique au mois
        delai_conversion = delais_conversion_ventes[mois_de_mission - 1]  # Supposons que le délai est constant

        if mois_de_mission > delai_conversion:
            index_rdv = mois_de_mission - int(delai_conversion) - 1
            if index_rdv >= 0:
                nb_rdv_qualifies_pour_ventes = historique_rdv_qualifies[index_rdv]
                ventes_attendues = nb_rdv_qualifies_pour_ventes * taux_conversion_ventes
            else:
                ventes_attendues = 0
        else:
            ventes_attendues = 0
        ventes_attendues_list.append(ventes_attendues)

        # Calcul des revenus
        revenus = ventes_attendues * panier_moyen
        revenus_list.append(revenus)

        # Calcul du profit net
        if taux_de_marge is not None:
            profit_net = (revenus * taux_de_marge) - cout_total
        else:
            profit_net = revenus - cout_total
        profit_net_list.append(profit_net)

        # Mise à jour des cumuls
        cumul_couts += cout_total
        cumul_revenus += revenus
        cumul_profit_net += profit_net

        cumul_couts_list.append(cumul_couts)
        cumul_revenus_list.append(cumul_revenus)
        cumul_profit_net_list.append(cumul_profit_net)

    # Affichage du tableau des résultats mensuels
    print("{:<6} {:<17} {:<20} {:<18} {:<18} {:<18} {:<18} {:<18} {:<18} {:<18} {:<15} {:<15}".format(
        'Mois', 'Coûts Fixes (€)', 'Coûts Variables (€)', 'Coûts Totaux (€)',
        'Prospects Sol.', 'Emails Ouverts', 'Réponses Reçues', 'Réponses Positives',
        'RDV Réalisés', 'RDV Qualifiés', 'Revenus (€)', 'Profit Net (€)'
    ))

    for i in range(duree_projection):
        print("{:<6} {:<17.2f} {:<20.2f} {:<18.2f} {:<18.0f} {:<18.0f} {:<18.0f} {:<18.2f} {:<18.2f} {:<18.2f} {:<15.2f} {:<15.2f}".format(
            mois_list[i], couts_fixes_list[i], couts_variables_list[i], couts_totaux_list[i],
            prospects_solicites_list[i], emails_ouverts_list[i], reponses_recues_list[i],
            reponses_positives_list[i], rdv_realises_list[i], rdv_qualifies_list[i],
            revenus_list[i], profit_net_list[i]
        ))

    # Affichage du cumul des coûts, revenus et profits
    print("\nCumul des Coûts, Revenus et Profits")
    print("{:<6} {:<22} {:<22} {:<22}".format(
        'Mois', 'Cumul Coûts (€)', 'Cumul Revenus (€)', 'Cumul Profit Net (€)'
    ))

    for i in range(duree_projection):
        print("{:<6} {:<22.2f} {:<22.2f} {:<22.2f}".format(
            mois_list[i], cumul_couts_list[i], cumul_revenus_list[i], cumul_profit_net_list[i]
        ))
else:
    print("Calcul non effectué en raison d'une impossibilité d'atteindre l'objectif.")
