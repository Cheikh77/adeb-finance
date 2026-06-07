import pandas as pd
import plotly.express as px
import streamlit as st


def afficher_objectifs():
    st.subheader("🎯 Objectifs financiers")

    liste_objectifs = [
        "Fonds de sécurité",
        "Voyage",
        "Omra",
        "Hajj",
        "Mariage",
        "Projet immobilier",
        "Investissement halal",
        "Voiture",
        "Études / Formation",
        "Aide familiale",
        "Projet entrepreneurial"
    ]

    nb_objectifs = st.number_input(
        "Nombre d’objectifs",
        min_value=1,
        max_value=5,
        value=2
    )

    objectifs_data = []

    for i in range(nb_objectifs):
        st.markdown(f"### Objectif {i + 1}")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            objectif_nom = st.selectbox(
                "Projet",
                liste_objectifs,
                key=f"objectif_{i}"
            )

        with col2:
            objectif_montant = st.number_input(
                "Montant cible (€)",
                min_value=100,
                value=2000,
                key=f"montant_{i}"
            )

        with col3:
            objectif_duree = st.number_input(
                "Durée (mois)",
                min_value=1,
                value=12,
                key=f"duree_{i}"
            )

        with col4:
            epargne_actuelle = st.number_input(
                "Déjà atteint (€)",
                min_value=0,
                value=0,
                key=f"epargne_{i}"
            )

        reste = max(objectif_montant - epargne_actuelle, 0)
        effort_mensuel = reste / objectif_duree if objectif_duree > 0 else 0
        progression = epargne_actuelle / objectif_montant if objectif_montant > 0 else 0

        objectifs_data.append({
            "Objectif": objectif_nom,
            "Cible (€)": objectif_montant,
            "Atteint (€)": epargne_actuelle,
            "Reste (€)": reste,
            "Effort mensuel (€)": effort_mensuel,
            "Progression": progression
        })

    df_objectifs = pd.DataFrame(objectifs_data)

    st.dataframe(df_objectifs, use_container_width=True)

    st.subheader("📈 Progression des objectifs")

    fig_obj = px.bar(
        df_objectifs,
        x="Progression",
        y="Objectif",
        orientation="h",
        text=df_objectifs["Progression"].apply(lambda x: f"{x:.0%}"),
        color="Progression",
        color_continuous_scale="Teal"
    )

    fig_obj.update_layout(
        yaxis=dict(autorange="reversed"),
        height=400,
        xaxis_title="Progression",
        yaxis_title=None,
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    fig_obj.update_traces(textposition="outside")

    st.plotly_chart(fig_obj, use_container_width=True)

    return df_objectifs