import streamlit as st


def afficher_recommandations(
    revenus,
    depenses,
    baraka,
    epargne,
    solde,
    repartition_depenses
):
    st.subheader("Recommandations intelligentes")

    recommandations = []

    taux_depenses = depenses / revenus if revenus > 0 else 0
    taux_epargne = epargne / revenus if revenus > 0 else 0
    taux_baraka = baraka / revenus if revenus > 0 else 0

    if solde < 0:
        recommandations.append("Votre solde est négatif ce mois-ci. La priorité est de réduire les dépenses variables.")

    if taux_depenses > 0.65:
        recommandations.append("Vos dépenses représentent plus de 65% de vos revenus. Un ajustement du budget est recommandé.")

    if taux_epargne < 0.10:
        recommandations.append("Votre taux d’épargne est inférieur à 10%. Essayez de sécuriser une épargne minimale régulière.")

    if 0.05 <= taux_baraka <= 0.20:
        recommandations.append("Votre Baraka est équilibrée par rapport à vos revenus.")
    elif taux_baraka < 0.05:
        recommandations.append("Votre part Baraka est faible. Vous pouvez l’augmenter progressivement selon vos moyens.")
    elif taux_baraka > 0.20:
        recommandations.append("Votre Baraka est élevée. C’est généreux, mais vérifiez que cela ne fragilise pas votre équilibre.")

    if not repartition_depenses.empty:
        top_cat = repartition_depenses.iloc[0]["Catégorie"]
        top_montant = repartition_depenses.iloc[0]["Montant"]
        total_depenses = repartition_depenses["Montant"].sum()

        if total_depenses > 0:
            part_top = top_montant / total_depenses

            if part_top > 0.40:
                recommandations.append(
                    f"La catégorie {top_cat} représente {part_top:.1%} de vos dépenses. "
                    "C’est le principal poste à surveiller."
                )

    if recommandations:
        for reco in recommandations:
            st.info(reco)
    else:
        st.success("Votre équilibre financier est bon ce mois-ci. Continuez à suivre votre budget régulièrement.")