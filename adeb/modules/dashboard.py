import pandas as pd
import plotly.express as px
import streamlit as st

from components.kpi_cards import afficher_kpi_card
from components.panel import afficher_titre_panel

def afficher_kpis(revenus, depenses, baraka, epargne, solde):
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        afficher_kpi_card("Revenus", f"{revenus:.2f} €", "Total des entrées du mois", "#1A535C")

    with col2:
        afficher_kpi_card("Dépenses", f"{depenses:.2f} €", "Total des sorties courantes", "#E74C3C")

    with col3:
        afficher_kpi_card("Baraka", f"{baraka:.2f} €", "Aide, dons et solidarité", "#D4A017")

    with col4:
        afficher_kpi_card("Épargne", f"{epargne:.2f} €", "Montant mis de côté", "#27AE60")

    with col5:
        couleur_solde = "#27AE60" if solde >= 0 else "#E74C3C"
        afficher_kpi_card("Solde", f"{solde:.2f} €", "Reste disponible du mois", couleur_solde)


def afficher_graphiques_budget(df, depenses, baraka, epargne, solde, key_suffix="default"):
    afficher_titre_panel(
    "Analyse du budget",
    "Répartition des dépenses, épargne et Baraka."
    )

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown("### Répartition du budget")

        budget_repartition = pd.DataFrame({
            "Poste": ["Dépenses", "Baraka", "Épargne"],
            "Montant": [depenses, baraka, epargne]
        })

        fig_budget = px.pie(
            budget_repartition,
            names="Poste",
            values="Montant",
            hole=0.55,
            color="Poste",
            color_discrete_map={
                "Dépenses": "#E74C3C",
                "Baraka": "#D4A017",
                "Épargne": "#27AE60"
            }
        )

        fig_budget.update_traces(
            textposition="inside",
            textinfo="label+percent",
            textfont_size=14
        )

        fig_budget.update_layout(
            showlegend=False,
            height=350,
            margin=dict(l=10, r=10, t=10, b=10)
        )

        st.plotly_chart(
            fig_budget,
            use_container_width=True,
            key=f"fig_budget_{key_suffix}"
        )

        afficher_kpi_card(
            "Reste disponible",
            f"{solde:.2f} €",
            "Solde après dépenses, épargne et Baraka",
            "#1A535C" if solde >= 0 else "#E74C3C"
        )

    with chart_col2:
        st.markdown("### Dépenses par catégorie")

        repartition_depenses = (
            df[df["type_adeb"] == "Dépenses"]
            .groupby("categorie_adeb")["amount"]
            .sum()
            .abs()
            .sort_values(ascending=False)
            .reset_index()
        )

        repartition_depenses.columns = ["Catégorie", "Montant"]

        if not repartition_depenses.empty:
            fig_depenses = px.bar(
                repartition_depenses,
                x="Montant",
                y="Catégorie",
                orientation="h",
                text=repartition_depenses["Montant"].apply(lambda x: f"{x:.0f} €"),
                color="Montant",
                color_continuous_scale="Blues"
            )

            fig_depenses.update_layout(
                yaxis=dict(autorange="reversed"),
                height=350,
                showlegend=False,
                plot_bgcolor="white",
                paper_bgcolor="white",
                margin=dict(l=10, r=10, t=10, b=10),
                xaxis_title=None,
                yaxis_title=None,
            )

            fig_depenses.update_traces(textposition="outside")

            st.plotly_chart(
                fig_depenses,
                use_container_width=True,
                key=f"fig_depenses_{key_suffix}"
            )
        else:
            st.info("Aucune dépense trouvée pour ce mois.")
    
    return repartition_depenses


def afficher_baraka(df, key_suffix="default"):
    st.subheader("Répartition de la Baraka")

    baraka_detail = (
        df[df["type_adeb"] == "Baraka"]
        .groupby("categorie_adeb")["amount"]
        .sum()
        .abs()
        .sort_values(ascending=False)
        .reset_index()
    )

    baraka_detail.columns = ["Catégorie", "Montant"]

    if not baraka_detail.empty:
        fig_baraka = px.pie(
            baraka_detail,
            names="Catégorie",
            values="Montant",
            hole=0.55,
            color="Catégorie",
            color_discrete_map={
                "Aide familiale": "#1A535C",
                "Sadaqa": "#D4A017",
                "Hadiya": "#27AE60",
                "Zakat": "#8E44AD",
                "Baraka": "#95D5B2"
            }
        )

        fig_baraka.update_traces(
            textposition="inside",
            textinfo="label+percent",
            textfont_size=14
        )

        fig_baraka.update_layout(
            showlegend=False,
            height=350,
            margin=dict(l=10, r=10, t=10, b=10)
        )

        st.plotly_chart(
            fig_baraka,
            use_container_width=True,
            key=f"fig_baraka_{key_suffix}"
        )

        aide_familiale = baraka_detail[
            baraka_detail["Catégorie"] == "Aide familiale"
        ]["Montant"].sum()

        part_aide = aide_familiale / baraka_detail["Montant"].sum()

        st.info(f"L’aide familiale représente {part_aide:.1%} de ta Baraka.")
    else:
        st.info("Aucune dépense Baraka trouvée pour ce mois.")