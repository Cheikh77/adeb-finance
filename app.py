import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Adeb Finance", layout="wide")

st.markdown(
    """
    <div style="background: linear-gradient(135deg, #101828, #1A535C); padding: 32px; border-radius: 24px; color: white; margin-bottom: 24px;">

        <h1 style="color:white; margin-bottom:10px;">
            💰 Adeb Finance
        </h1>

        <div style="font-size:20px; margin-bottom:14px; color:white;">
            Votre outil de suivi de budget responsable et éthique.
        </div>

        <div style="font-size:15px; color:#D0D5DD; margin-bottom:20px;">
            Adeb Finance vous aide à mieux gérer vos finances au quotidien,
            en respectant un équilibre entre dépenses, épargne et Baraka.
        </div>

        <div style="background-color: rgba(255,255,255,0.1); padding:16px; border-radius:16px; font-size:14px; color:white;">
            📊 Analyse automatique de vos dépenses<br>
            🌱 Suivi de votre épargne<br>
            🕌 Mise en valeur de votre Baraka<br>
            🎯 Conseils personnalisés pour un meilleur équilibre financier
        </div>

    </div>
    """,
    unsafe_allow_html=True
)
c1, c2, c3 = st.columns(3)

with c1:
    st.info("📥 **Importez votre relevé CSV**")

with c2:
    st.info("🧠 **Classification automatique**")

with c3:
    st.info("📊 **Analyse complète de votre budget**")


def nettoyer_montant(serie):
    return pd.to_numeric(
        serie.astype(str)
        .str.replace(" ", "", regex=False)
        .str.replace(",", ".", regex=False)
        .str.replace("€", "", regex=False)
        .str.strip(),
        errors="coerce"
    )


def mapper_adeb(row):
    category = str(row.get("category", "")).strip()
    parent = str(row.get("categoryParent", "")).strip()
    label = str(row.get("label", "")).upper()
    amount = row.get("amount", 0)

    if amount > 0:
        if "Allocation" in parent:
            return "Revenus", "Allocations", "Allocations familiales"
        if "Salaire" in category or "Revenus du travail" in parent:
            return "Revenus", "Salaire", "Salaire fixe"
        return "Revenus", "Autres revenus", "Virement reçu"

    if "REVOLUT" in label:
        return "Epargne", "Sécurité", "Epargne Revolut"

    if parent == "Cadeaux et solidarité":
        return "Baraka", "Sadaqa", category
    if "Famille" in parent:
        return "Baraka", "Aide familiale", category

    if parent == "Logement":
        return "Dépenses", "Logement", category
    if parent == "Abonnements & téléphonie":
        return "Dépenses", "Factures", category
    if parent == "Vie quotidienne":
        if category == "Alimentation":
            return "Dépenses", "Courses", "Alimentation"
        return "Dépenses", "Vie courante", category
    if parent == "Voyages & Transports":
        return "Dépenses", "Transports", category
    if parent == "Loisirs et sorties":
        return "Dépenses", "Loisirs & sorties", category
    if parent == "Services financiers & professionnels":
        return "Dépenses", "Imprévus", category

    return "Dépenses", "Imprévus", "Non catégorisé"


# ==============================
# 🎯 OBJECTIFS AVANT IMPORT
# ==============================

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

    effort_mensuel = (
        reste / objectif_duree
        if objectif_duree > 0
        else 0
    )

    progression = (
        epargne_actuelle / objectif_montant
        if objectif_montant > 0
        else 0
    )

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


# ==============================
# 📥 IMPORT DU RELEVÉ
# ==============================

uploaded_file = st.file_uploader(
    "📥 Importer votre relevé CSV (BoursoBank)",
    type=["csv"]
)

if uploaded_file:

    df = pd.read_csv(uploaded_file, sep=";")
    st.success("Fichier importé avec succès ✅")

    df["amount"] = nettoyer_montant(df["amount"])

    df["dateOp"] = pd.to_datetime(df["dateOp"], dayfirst=True, errors="coerce")
    df["mois"] = df["dateOp"].dt.strftime("%B %Y")

    mois_selectionne = st.selectbox(
        "📅 Choisir le mois d’observation",
        sorted(df["mois"].dropna().unique())
    )

    df = df[df["mois"] == mois_selectionne]

    df[["type_adeb", "categorie_adeb", "sous_categorie_adeb"]] = df.apply(
        mapper_adeb,
        axis=1,
        result_type="expand"
    )
    transactions_non_classifiees = df[
        (df["categorie_adeb"] == "Imprévus") &
        (df["sous_categorie_adeb"] == "Non catégorisé")
    ]

    nb_non_classifiees = len(transactions_non_classifiees)
    montant_non_classifie = abs(transactions_non_classifiees["amount"].sum())

    if nb_non_classifiees > 0:
        st.warning(
            f"⚠️ {nb_non_classifiees} transaction(s) non classifiée(s) détectée(s), "
            f"pour un montant total de {montant_non_classifie:.2f} €."
        )

        with st.expander("Voir les transactions non classifiées"):
            st.dataframe(
                transactions_non_classifiees[
                    ["dateOp", "label", "amount", "category", "categoryParent"]
                ],
                use_container_width=True
            )
    else:
        st.success("✅ Toutes les transactions ont été classifiées.")

    revenus = df[df["type_adeb"] == "Revenus"]["amount"].sum()
    depenses = abs(df[df["type_adeb"] == "Dépenses"]["amount"].sum())
    baraka = abs(df[df["type_adeb"] == "Baraka"]["amount"].sum())
    epargne = abs(df[df["type_adeb"] == "Epargne"]["amount"].sum())
    solde = revenus - depenses - baraka - epargne

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("💰 Revenus", f"{revenus:.2f} €")
    col2.metric("💸 Dépenses", f"{depenses:.2f} €")
    col3.metric("🕌 Baraka", f"{baraka:.2f} €")
    col4.metric("🌱 Épargne", f"{epargne:.2f} €")
    col5.metric("💳 Solde", f"{solde:.2f} €")

    st.subheader("🧭 Statut du mois")

    taux_depenses = depenses / revenus if revenus > 0 else 0
    taux_epargne = epargne / revenus if revenus > 0 else 0
    taux_baraka = baraka / revenus if revenus > 0 else 0

    statut_depenses = "✅ Dépenses maîtrisées" if taux_depenses <= 0.65 else "⚠️ Dépenses élevées"
    statut_epargne = "✅ Épargne correcte" if taux_epargne >= 0.10 else "⚠️ Épargne faible"

    if taux_baraka < 0.05:
        statut_baraka = "⚠️ Baraka faible"
    elif taux_baraka <= 0.20:
        statut_baraka = "✅ Baraka équilibrée"
    else:
        statut_baraka = "⚠️ Baraka très élevée"

    statut_global = (
        "✅ Bon équilibre"
        if taux_depenses <= 0.65 and taux_epargne >= 0.10
        else "⚠️ À améliorer"
    )

    s1, s2, s3, s4 = st.columns(4)

    s1.metric("Équilibre global", statut_global)
    s2.metric("Dépenses", statut_depenses)
    s3.metric("Épargne", statut_epargne)
    s4.metric("Baraka", statut_baraka)

    st.subheader("🎯 Objectifs financiers du mois")

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
        "✅ Très maîtrisé" if taux_logement <= 0.30
        else "✅ Zone acceptable" if taux_logement <= 0.40
        else "⚠️ Loyer trop élevé"
    )

    statut_fixes = (
        "✅ Charges fixes maîtrisées"
        if taux_fixes <= 0.50
        else "⚠️ Charges fixes trop élevées"
    )

    o1, o2 = st.columns(2)

    o1.metric(
        "🏠 Logement / revenus",
        f"{taux_logement:.1%}",
        statut_logement
    )

    o2.metric(
        "📌 Charges fixes / revenus",
        f"{taux_fixes:.1%}",
        statut_fixes
    )

    st.subheader("⭐ Score financier")

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
        "🔴 Solde négatif — à corriger en priorité" if solde < 0
        else "🟢 Excellent équilibre" if score >= 8
        else "🟡 Bon équilibre" if score >= 6
        else "🟠 À surveiller" if score >= 4
        else "🔴 Fragile"
    )

    st.metric("Score financier", f"{score}/10", niveau_score)

    st.subheader("📊 Analyse du budget")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown("### 🧩 Répartition du budget")

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
                "Dépenses": "#FF6B6B",
                "Baraka": "#4ECDC4",
                "Épargne": "#1A535C"
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

        st.plotly_chart(fig_budget, use_container_width=True)

        st.metric("💳 Reste disponible", f"{solde:.2f} €")

    with chart_col2:
        st.markdown("### 📊 Dépenses par catégorie")

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

            st.plotly_chart(fig_depenses, use_container_width=True)
        else:
            st.info("Aucune dépense trouvée pour ce mois.")

    if not repartition_depenses.empty:
        top_cat = repartition_depenses.iloc[0]["Catégorie"]
        part = repartition_depenses.iloc[0]["Montant"] / repartition_depenses["Montant"].sum()
        st.info(f"💡 {top_cat} représente {part:.1%} de tes dépenses.")

    st.subheader("🧠 Analyse intelligente")

    recommandations = []

    if solde < 0:
        recommandations.append("🔴 Ton solde est négatif ce mois-ci. Priorité : réduire certaines dépenses variables ou reporter les dépenses non urgentes.")

    if taux_logement > 0.40:
        recommandations.append("🏠 Le logement dépasse 40% de tes revenus. C’est une charge lourde : attention à l’équilibre global.")

    if taux_fixes > 0.50:
        recommandations.append("📌 Tes charges fixes dépassent 50% de tes revenus. Cela réduit fortement ta marge de manœuvre.")

    if taux_depenses > 0.65:
        recommandations.append("💸 Tes dépenses dépassent 65% de tes revenus. Il serait utile d’identifier les postes compressibles.")

    if taux_epargne < 0.10:
        recommandations.append("🌱 Ton épargne est faible. Essaie de viser progressivement au moins 10% de tes revenus.")

    if taux_baraka < 0.05:
        recommandations.append("🕌 Ta Baraka est faible. Si ta situation le permet, tu peux augmenter progressivement cette part.")
    elif taux_baraka > 0.20:
        recommandations.append("🕌 Ta Baraka est très élevée. C’est généreux, mais vérifie que cela ne fragilise pas ton équilibre financier.")

    if not repartition_depenses.empty:
        top_cat = repartition_depenses.iloc[0]["Catégorie"]
        part_top = repartition_depenses.iloc[0]["Montant"] / repartition_depenses["Montant"].sum()

        if part_top > 0.50:
            recommandations.append(f"📊 {top_cat} représente {part_top:.1%} de tes dépenses. C’est le poste principal à surveiller.")

    if recommandations:
        for reco in recommandations:
            st.info(reco)
    else:
        st.success("✅ Très bon équilibre ce mois-ci. Continue à suivre ton budget avec régularité.")

    st.subheader("🕌 Répartition de la Baraka")

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
                "Sadaqa": "#4ECDC4",
                "Hadiya": "#FFE66D",
                "Zakat": "#9B5DE5",
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

        st.plotly_chart(fig_baraka, use_container_width=True)

        aide_familiale = baraka_detail[
            baraka_detail["Catégorie"] == "Aide familiale"
        ]["Montant"].sum()

        part_aide = aide_familiale / baraka_detail["Montant"].sum()

        st.info(
            f"💡 L’aide familiale représente {part_aide:.1%} de ta Baraka."
        )
    else:
        st.info("Aucune dépense Baraka trouvée pour ce mois.")

    st.subheader("📋 Transactions classifiées")

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