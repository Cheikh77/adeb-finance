import streamlit as st

from components.header import afficher_header
from components.navbar import afficher_navbar

from modules.recommandations import afficher_recommandations
from modules.import_data import importer_releve, filtrer_mois, classifier_transactions
from modules.objectifs import afficher_objectifs
from modules.zakat import afficher_zakat
from modules.dashboard import afficher_kpis, afficher_graphiques_budget, afficher_baraka
from modules.analyse import (
    calculer_ratios,
    afficher_statut_mois,
    afficher_objectifs_mois,
    afficher_score_financier,
    afficher_analyse_intelligente
)
from modules.non_classifiees import afficher_transactions_non_classifiees


st.set_page_config(page_title="Adeb Finance", layout="wide")


from pathlib import Path

def load_css(file_path):
    css_path = Path(__file__).parent / file_path

    if css_path.exists():
        with open(css_path, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css("assets/style.css")

afficher_header()

page = afficher_navbar()

st.sidebar.markdown("""
---

### Philosophie

Adeb Finance vise un équilibre entre :

- dépenses,
- épargne,
- générosité,
- vision long terme.
""")


if page == "Objectifs":
    afficher_objectifs()


elif page == "Dashboard":

    st.markdown("### Profil utilisateur")

    col_nom, col_prenom = st.columns(2)

    with col_nom:
        nom_utilisateur = st.text_input("Nom", key="nom_utilisateur")

    with col_prenom:
        prenom_utilisateur = st.text_input("Prénom", key="prenom_utilisateur")

    profil_complet = bool(nom_utilisateur.strip()) and bool(prenom_utilisateur.strip())

    if not profil_complet:
        st.warning("Veuillez renseigner votre nom et votre prénom avant d’importer votre relevé bancaire.")
        st.stop()

    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("Importez votre relevé CSV")

    with c2:
        st.info("Classification automatique")

    with c3:
        st.info("Analyse complète de votre budget")

    uploaded_file = st.file_uploader(
        "Importer votre relevé CSV BoursoBank",
        type=["csv"]
    )

    if uploaded_file:

        df = importer_releve(uploaded_file)
        df = filtrer_mois(df)

        df = classifier_transactions(
            df,
            nom_utilisateur=nom_utilisateur,
            prenom_utilisateur=prenom_utilisateur
        )

        afficher_transactions_non_classifiees(df)

        df_budget = df[df["type_adeb"] != "Transfert"]

        revenus = df_budget[df_budget["type_adeb"] == "Revenus"]["amount"].sum()

        depenses = abs(
            df_budget[df_budget["type_adeb"] == "Dépenses"]["amount"].sum()
        )

        baraka = abs(
            df_budget[df_budget["type_adeb"] == "Baraka"]["amount"].sum()
        )

        epargne = abs(
            df_budget[df_budget["type_adeb"] == "Epargne"]["amount"].sum()
        )

        solde = revenus - depenses - baraka - epargne

        taux_depenses, taux_epargne, taux_baraka = calculer_ratios(
            revenus,
            depenses,
            baraka,
            epargne
        )

        repartition_depenses = (
            df_budget[df_budget["type_adeb"] == "Dépenses"]
            .groupby("categorie_adeb")["amount"]
            .sum()
            .abs()
            .sort_values(ascending=False)
            .reset_index()
        )

        repartition_depenses.columns = ["Catégorie", "Montant"]

        tab1, tab2, tab3, tab4 = st.tabs([
            "Vue générale",
            "Dépenses",
            "Baraka",
            "Transactions"
        ])

        with tab1:
            afficher_kpis(
                revenus,
                depenses,
                baraka,
                epargne,
                solde
            )

            afficher_statut_mois(
                taux_depenses,
                taux_epargne,
                taux_baraka
            )

            taux_logement, taux_fixes = afficher_objectifs_mois(
                df_budget,
                revenus
            )

            afficher_score_financier(
                taux_depenses,
                taux_epargne,
                taux_baraka,
                taux_fixes,
                solde
            )

            afficher_analyse_intelligente(
                solde,
                taux_logement,
                taux_fixes,
                taux_depenses,
                taux_epargne,
                taux_baraka,
                repartition_depenses
            )

            afficher_recommandations(
                revenus,
                depenses,
                baraka,
                epargne,
                solde,
                repartition_depenses
            )

        with tab2:
            afficher_graphiques_budget(
                df_budget,
                depenses,
                baraka,
                epargne,
                solde,
                key_suffix="depenses"
            )

        with tab3:
            afficher_baraka(
                df_budget,
                key_suffix="baraka"
            )

        with tab4:
            st.subheader("Transactions classifiées")

            st.dataframe(
                df[
                    [
                        "dateOp",
                        "label",
                        "amount",
                        "type_adeb",
                        "categorie_adeb",
                        "sous_categorie_adeb",
                    ]
                ],
                use_container_width=True
            )