# app.py

import streamlit as st
import pandas as pd

# === Fonction Principale ===
def calculateur():
    # === Calculs Préliminaires ===

    # Liste des noms des mois
    noms_mois = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin',
                 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']

    # Mois de début de la prospection
    mois_debut_prospection = mois_debut_mission + 1  # La prospection commence le mois suivant le début de mission

    # Mois de début des coûts variables (rémunération variable)
    mois_debut_couts_variables = mois_debut_mission + mois_debut_remuneration_variable - 1

    # Calcul du mois de la première vente souhaitée (mois relatif à la mission)
    if delai_premiere_vente_souhaitee is not None and delai_premiere_vente_souhaitee > 0:
        mois_premiere_vente_souhaitee = mois_debut_mission + delai_premiere_vente_souhaitee - 1
    else:
        mois_premiere_vente_souhaitee = None

    # Initialisation du nombre de prospects sollicités par défaut pour chaque mois
    prospects_solicites_par_mois = [0] * duree_projection  # Initialiser avec 0 prospects sollicités
    for mois_de_mission_iter in range(1, duree_projection + 1):
        if mois_de_mission_iter >= (mois_debut_prospection - mois_debut_mission + 1):
            prospects_solicites_par_mois[mois_de_mission_iter - 1] = nb_prospects_mensuel

    calcul_possible = True  # Variable pour contrôler la suite du programme

    # Calcul du nombre de prospects nécessaires si delai_premiere_vente_souhaitee est défini
    if mois_premiere_vente_souhaitee is not None:
        delai_conversion = delais_conversion_ventes_input  # Supposons que le délai est constant
        mois_rdv_necessaire = mois_premiere_vente_souhaitee - delai_conversion
        if mois_rdv_necessaire < mois_debut_prospection:
            st.error("Impossible d'obtenir une vente au mois souhaité en raison des délais et du mois de début de prospection.")
            calcul_possible = False
        else:
            # Calcul du nombre de prospects nécessaires au mois_rdv_necessaire
            mois_rel_mission = mois_rdv_necessaire - mois_debut_mission + 1
            mois_effectif = ((mois_debut_mission + mois_rel_mission - 2) % 12) + 1  # Mois calendaire effectif
            if mois_effectif in [5, 8, 12]:
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
            for mois_index in range(mois_debut_prospection - mois_debut_mission, mois_rdv_necessaire - mois_debut_mission):
                prospects_solicites_par_mois[mois_index] = required_nb_prospects

    # Initialisation des listes pour stocker les résultats
    mois_list = []
    mois_nom_list = []
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

        for mois_de_mission_iter in range(1, duree_projection + 1):
            # Mois de mission
            mois_list.append(mois_de_mission_iter)

            # Calcul du mois calendaire effectif
            mois_effectif = ((mois_debut_mission + mois_de_mission_iter - 2) % 12) + 1
            mois_nom = noms_mois[mois_effectif -1]
            mois_nom_list.append(mois_nom.capitalize())

            # Calcul des coûts fixes
            if mois_de_mission_iter == 1:
                cout_fixe = cout_audit_mois1
            elif mois_de_mission_iter in [2, 3]:
                cout_fixe = cout_mensuel_mois2_3
            elif mois_de_mission_iter >= 4:
                cout_fixe = cout_mensuel_fixe
            else:
                cout_fixe = 0  # Avant le début de la mission (cas improbable ici)
            couts_fixes_list.append(cout_fixe)

            # Index pour les listes
            index = mois_de_mission_iter - 1

            # Nombre de prospects sollicités
            prospects_solicites = prospects_solicites_par_mois[index]
            prospects_solicites_list.append(prospects_solicites)

            # Vérifier si le mois est mai, août ou décembre
            if mois_effectif in [5, 8, 12]:
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
            if mois_de_mission_iter >= mois_debut_remuneration_variable:
                cout_variable = nb_rdv_qualifies * cout_variable_par_rdv
            else:
                cout_variable = 0
            couts_variables_list.append(cout_variable)

            # Coût total pour le mois
            cout_total = cout_fixe + cout_variable
            couts_totaux_list.append(cout_total)

            # Calcul des ventes attendues, en tenant compte du délai de conversion spécifique au mois
            delai_conversion = delais_conversion_ventes_input  # Supposons que le délai est constant

            if mois_de_mission_iter > delai_conversion:
                index_rdv = mois_de_mission_iter - int(delai_conversion) - 1
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
        st.header("Résultats Mensuels")
        data = {
            'Mois de mission': mois_list,
            'Mois': mois_nom_list,
            'Coûts Fixes (€)': couts_fixes_list,
            'Coûts Variables (€)': couts_variables_list,
            'Coûts Totaux (€)': couts_totaux_list,
            'Prospects Sol.': prospects_solicites_list,
            'Emails Ouverts': emails_ouverts_list,
            'Réponses Reçues': reponses_recues_list,
            'Réponses Positives': reponses_positives_list,
            'RDV Réalisés': rdv_realises_list,
            'RDV Qualifiés': rdv_qualifies_list,
            'Ventes Attendues': ventes_attendues_list,
            'Revenus (€)': revenus_list,
            'Profit Net (€)': profit_net_list
        }

        df = pd.DataFrame(data)
        st.dataframe(df.style.format({
            'Coûts Fixes (€)': '{:,.2f}',
            'Coûts Variables (€)': '{:,.2f}',
            'Coûts Totaux (€)': '{:,.2f}',
            'Revenus (€)': '{:,.2f}',
            'Profit Net (€)': '{:,.2f}',
            'Emails Ouverts': '{:,.0f}',
            'Réponses Reçues': '{:,.0f}',
            'Réponses Positives': '{:,.2f}',
            'RDV Réalisés': '{:,.2f}',
            'RDV Qualifiés': '{:,.2f}',
            'Ventes Attendues': '{:,.2f}',
        }))

        # Affichage des cumuls
        st.header("Cumul des Coûts, Revenus et Profits")
        cumul_data = {
            'Mois de mission': mois_list,
            'Mois': mois_nom_list,
            'Cumul Coûts (€)': cumul_couts_list,
            'Cumul Revenus (€)': cumul_revenus_list,
            'Cumul Profit Net (€)': cumul_profit_net_list
        }
        cumul_df = pd.DataFrame(cumul_data)
        st.dataframe(cumul_df.style.format({
            'Cumul Coûts (€)': '{:,.2f}',
            'Cumul Revenus (€)': '{:,.2f}',
            'Cumul Profit Net (€)': '{:,.2f}',
        }))

        # Affichage des graphiques
        st.header("Graphiques")
        st.line_chart(df.set_index('Mois de mission')[['Coûts Totaux (€)', 'Revenus (€)', 'Profit Net (€)']])

    else:
        st.error("Calcul non effectué en raison d'une impossibilité d'atteindre l'objectif.")

# === Début du Script Streamlit ===

st.subheader("Daft Punk presents :")
st.title("Calculateur Financier BAAX")

# === Temporalité ===
with st.expander("Temporalité"):
    mois_debut_mission = st.number_input("Mois de début de mission (1 pour janvier - 12 pour décembre)", min_value=1, max_value=12, value=1)
    duree_projection = st.number_input("Durée de la projection (en mois)", min_value=1, max_value=60, value=12)
    delai_premiere_vente_souhaitee = st.number_input("Facultatif : Délai pour la première vente souhaitée (en mois)", min_value=0, max_value=60, value=0)

# === Coûts de la prestation BAAX ===
with st.expander("Coût de la prestation BAAX"):
    cout_audit_mois1 = st.number_input("Coût audit mois 1 (€)", min_value=0, value=4000)
    cout_mensuel_mois2_3 = st.number_input("Coût mensuel mois 2-3 (€)", min_value=0, value=3000)
    cout_mensuel_fixe = st.number_input("Coût mensuel fixe à partir du mois 4 (€)", min_value=0, value=3000)
    cout_variable_par_rdv = st.number_input("Coût variable par rendez-vous (€)", min_value=0, value=300)
    mois_debut_remuneration_variable = st.number_input("Mois de début de la rémunération variable", min_value=1, max_value=60, value=1)

# === Statistiques du Business Development ===
with st.expander("Statistiques du Business Development"):
    nb_prospects_mensuel = st.number_input("Nombre de prospects mensuels", min_value=1, value=500)
    taux_ouverture = st.number_input("Taux d'ouverture", min_value=0.0, max_value=1.0, value=0.60)
    taux_reponse = st.number_input("Taux de réponse", min_value=0.0, max_value=1.0, value=0.10)
    taux_reponses_positives = st.number_input("Taux de réponses positives", min_value=0.0, max_value=1.0, value=0.30)
    taux_prise_rdv = st.number_input("Taux de prise de rendez-vous", min_value=0.0, max_value=1.0, value=0.50)
    taux_rdv_qualifies = st.number_input("Taux de rendez-vous qualifiés", min_value=0.0, max_value=1.0, value=0.90)

    st.markdown("**Taux réduits pour les mois de mai, août et décembre**")
    taux_ouverture_mois_reduits = st.number_input("Taux d'ouverture réduit", min_value=0.0, max_value=1.0, value=0.50)
    taux_reponse_mois_reduits = st.number_input("Taux de réponse réduit", min_value=0.0, max_value=1.0, value=0.08)
    taux_reponses_positives_mois_reduits = st.number_input("Taux de réponses positives réduit", min_value=0.0, max_value=1.0, value=0.25)

# === Chiffres du client ===
with st.expander("Chiffres du client"):
    taux_conversion_ventes = st.number_input("Taux de conversion des ventes", min_value=0.0, max_value=1.0, value=0.20)
    delais_conversion_ventes_input = st.number_input("Délai de conversion des ventes (mois)", min_value=1, max_value=60, value=3)
    panier_moyen = st.number_input("Panier moyen (€)", min_value=0, value=100000)
    taux_de_marge = st.number_input("Taux de marge", min_value=0.0, max_value=1.0, value=0.25)

# Bouton pour lancer le calcul
if st.button("Let's Rock !"):
    calculateur()

