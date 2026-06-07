import streamlit as st


def afficher_zakat():
    st.subheader("Calculateur de zakat")

    st.info(
        "Ce module fournit une estimation simple de la zakat. "
        "Il ne remplace pas l’avis d’un savant ou d’un conseiller spécialisé."
    )

    col1, col2 = st.columns(2)

    with col1:
        liquidites = st.number_input("Liquidités disponibles (€)", min_value=0.0, value=0.0)
        epargne = st.number_input("Épargne (€)", min_value=0.0, value=0.0)
        investissements = st.number_input("Investissements liquides (€)", min_value=0.0, value=0.0)

    with col2:
        or_argent = st.number_input("Or / argent / métaux précieux (€)", min_value=0.0, value=0.0)
        crypto = st.number_input("Crypto-actifs (€)", min_value=0.0, value=0.0)
        dettes_court_terme = st.number_input("Dettes exigibles à court terme (€)", min_value=0.0, value=0.0)

    patrimoine_brut = liquidites + epargne + investissements + or_argent + crypto
    patrimoine_net = max(patrimoine_brut - dettes_court_terme, 0)

    nisab = st.number_input(
        "Nisab estimé (€)",
        min_value=0.0,
        value=5000.0,
        help="À ajuster selon la valeur actuelle de l’or ou de l’argent."
    )

    taux_zakat = 0.025

    zakat_due = patrimoine_net * taux_zakat if patrimoine_net >= nisab else 0

    st.markdown("---")

    c1, c2, c3 = st.columns(3)

    c1.metric("Patrimoine brut", f"{patrimoine_brut:.2f} €")
    c2.metric("Patrimoine net zakatable", f"{patrimoine_net:.2f} €")
    c3.metric("Zakat estimée", f"{zakat_due:.2f} €")

    if patrimoine_net >= nisab:
        st.success("Votre patrimoine net dépasse le nisab estimé. Une zakat est potentiellement due.")
    else:
        st.warning("Votre patrimoine net est inférieur au nisab estimé. Aucune zakat n’est estimée avec ces paramètres.")

    st.markdown("### Lecture responsable")

    st.write(
        "La zakat est généralement calculée à 2,5 % du patrimoine zakatable "
        "lorsqu’il atteint le nisab et qu’une année lunaire s’est écoulée. "
        "Ce module est une première estimation destinée à aider l’utilisateur "
        "à mieux organiser ses obligations financières."
    )