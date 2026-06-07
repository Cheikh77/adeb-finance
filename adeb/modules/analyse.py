import streamlit as st


def calculer_ratios(revenus, depenses, baraka, epargne):
    taux_depenses = depenses / revenus if revenus > 0 else 0
    taux_epargne = epargne / revenus if revenus > 0 else 0
    taux_baraka = baraka / revenus if revenus > 0 else 0

    return taux_depenses, taux_epargne, taux_baraka


def afficher_statut_mois(taux_depenses, taux_epargne, taux_baraka):
    st.subheader("Statut du mois")

    statut_depenses = (
        "Dépenses maîtrisées"
        if taux_depenses <= 0.65
        else "Dépenses élevées"
    )

    statut_epargne = (
        "Épargne correcte"
        if taux_epargne >= 0.10
        else "Épargne faible"
    )

    if taux_baraka < 0.05:
        statut_baraka = "Baraka faible"

    elif taux_baraka <= 0.20:
        statut_baraka = "Baraka équilibrée"

    else:
        statut_baraka = "Baraka très élevée"

    statut_global = (
        "Bon équilibre"
        if taux_depenses <= 0.65 and taux_epargne >= 0.10
        else "À améliorer"
    )

    s1, s2, s3, s4 = st.columns(4)

    s1.metric("Équilibre global", statut_global)
    s2.metric("Dépenses", statut_depenses)
    s3.metric("Épargne", statut_epargne)
    s4.metric("Baraka", statut_baraka)


def afficher_objectifs_mois(df, revenus):
    st.subheader("Analyse des charges essentielles")

    logement = abs(
        df[
            (df["type_adeb"] == "Dépenses") &
            (df["categorie_adeb"] == "Logement")
        ]["amount"].sum()
    )

    factures = abs(
        df[
            (df["type_adeb"] == "Dépenses") &
            (df["categorie_adeb"] == "Factures")
        ]["amount"].sum()
    )

    depenses_fixes = logement + factures

    taux_logement = logement / revenus if revenus > 0 else 0
    taux_fixes = depenses_fixes / revenus if revenus > 0 else 0

    statut_logement = (
        "Très maîtrisé" if taux_logement <= 0.30
        else "Zone acceptable" if taux_logement <= 0.40
        else "Loyer trop élevé"
    )

    statut_fixes = (
        "Charges fixes maîtrisées"
        if taux_fixes <= 0.50
        else "Charges fixes trop élevées"
    )

    o1, o2 = st.columns(2)

    o1.metric(
    "Logement / revenus",
    f"{taux_logement:.1%}",
    statut_logement,
    delta_color="inverse"
    if taux_logement > 0.40
    else "normal"
   )

    o2.metric(
        "Charges fixes / revenus",
        f"{taux_fixes:.1%}",
        statut_fixes,
        delta_color="inverse"
        if taux_fixes > 0.50
        else "normal"
    )

    return taux_logement, taux_fixes


def afficher_score_financier(
    taux_depenses,
    taux_epargne,
    taux_baraka,
    taux_fixes,
    solde
):
    st.subheader("Score financier")

    score = 0

    if taux_depenses <= 0.65:
        score += 3

    if taux_epargne >= 0.10:
        score += 3

    if 0.05 <= taux_baraka <= 0.20:
        score += 2

    if taux_fixes <= 0.50:
        score += 2

    if solde < 0:
        score = min(score, 4)

    niveau_score = (
        "Solde négatif — à corriger en priorité"
        if solde < 0
        else "Excellent équilibre"
        if score >= 8
        else "Bon équilibre"
        if score >= 6
        else "À surveiller"
        if score >= 4
        else "Fragile"
    )

    st.metric(
    label="Score financier",
    value=f"{score}/10",
    delta=niveau_score,
    delta_color="inverse" if (solde < 0 or score < 4) else "normal"
    )


def afficher_analyse_intelligente(
    solde,
    taux_logement,
    taux_fixes,
    taux_depenses,
    taux_epargne,
    taux_baraka,
    repartition_depenses
):
    st.subheader("Analyse intelligente")

    recommandations = []

    if solde < 0:
        recommandations.append(
            "Votre solde est négatif ce mois-ci. "
            "Priorité : réduire certaines dépenses variables."
        )

    if taux_logement > 0.40:
        recommandations.append(
            "Le logement dépasse 40% de vos revenus. "
            "Cela pèse fortement sur votre équilibre financier."
        )

    if taux_fixes > 0.50:
        recommandations.append(
            "Les charges fixes dépassent 50% des revenus. "
            "Votre marge de manœuvre devient réduite."
        )

    if taux_depenses > 0.65:
        recommandations.append(
            "Les dépenses dépassent 65% des revenus. "
            "Il serait utile d’identifier les postes compressibles."
        )

    if taux_epargne < 0.10:
        recommandations.append(
            "L’épargne reste faible. "
            "Essayez de viser progressivement 10% des revenus."
        )

    if taux_baraka < 0.05:
        recommandations.append(
            "La part Baraka est faible. "
            "Vous pouvez l’augmenter progressivement selon vos moyens."
        )

    elif taux_baraka > 0.20:
        recommandations.append(
            "La part Baraka est très élevée. "
            "Vérifiez qu’elle ne fragilise pas votre équilibre financier."
        )

    if not repartition_depenses.empty:

        top_cat = repartition_depenses.iloc[0]["Catégorie"]

        part_top = (
            repartition_depenses.iloc[0]["Montant"] /
            repartition_depenses["Montant"].sum()
        )

        if part_top > 0.50:

            recommandations.append(
                f"{top_cat} représente {part_top:.1%} des dépenses. "
                "C’est le principal poste à surveiller."
            )

    if recommandations:

        for reco in recommandations:
            st.info(reco)

    else:

        st.success(
            "Très bon équilibre ce mois-ci. "
            "Continuez à suivre votre budget régulièrement."
        )
        