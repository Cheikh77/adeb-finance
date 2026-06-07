import pandas as pd
import streamlit as st

from modules.classification import nettoyer_montant, mapper_adeb


def importer_releve(uploaded_file):
    df = pd.read_csv(uploaded_file, sep=";")

    df["amount"] = nettoyer_montant(df["amount"])

    df["dateOp"] = pd.to_datetime(
        df["dateOp"],
        dayfirst=True,
        errors="coerce"
    )

    df["mois"] = df["dateOp"].dt.strftime("%B %Y")

    return df


def filtrer_mois(df):
    mois_selectionne = st.selectbox(
        "Choisir le mois d’observation",
        sorted(df["mois"].dropna().unique())
    )

    return df[df["mois"] == mois_selectionne]

def detecter_virements_neutres(df, delai_jours=7):
    
    # On travaille sur une copie pour ne pas modifier
    # le dataframe d'origine directement
    df = df.copy()

    # Colonne qui indiquera si la transaction est un
    # virement neutre (argent reçu puis renvoyé)
    df["virement_neutre"] = False

    # On récupère uniquement les transactions
    # contenant "VIR" dans le libellé
    virements = df[
        df["label"].astype(str).str.upper().str.contains("VIR", na=False)
    ].copy()

    # On crée le montant absolu :
    # +2625 devient 2625
    # -2625 devient 2625
    virements["montant_abs"] = virements["amount"].abs().round(2)

    # On parcourt tous les virements
    for i, ligne in virements.iterrows():

        # Montant de la transaction courante
        montant = ligne["amount"]

        # Valeur absolue du montant
        montant_abs = round(abs(montant), 2)

        # Date de la transaction
        date_ligne = ligne["dateOp"]

        # Recherche d'un virement correspondant :
        # - même montant absolu
        # - signe opposé (+ / -)
        # - dans une fenêtre de quelques jours
        candidats = virements[
            (virements.index != i) &
            (virements["montant_abs"] == montant_abs) &
            (virements["amount"] * montant < 0) &
            (
                (virements["dateOp"] - date_ligne)
                .abs()
                <= pd.Timedelta(days=delai_jours)
            )
        ]

        # Si on trouve un candidat
        if not candidats.empty:

            # On prend le premier candidat trouvé
            index_candidat = candidats.index[0]

            # On marque les deux transactions
            # comme virements neutres
            df.loc[i, "virement_neutre"] = True
            df.loc[index_candidat, "virement_neutre"] = True

    return df
def classifier_transactions(df):
    df[["type_adeb", "categorie_adeb", "sous_categorie_adeb"]] = df.apply(
        mapper_adeb,
        axis=1,
        result_type="expand"
    )
    df = detecter_virements_neutres(df)

    df.loc[
        df["virement_neutre"],
        ["type_adeb", "categorie_adeb", "sous_categorie_adeb"]
    ] = [
        "Transfert",
        "Virement neutre",
        "Argent reçu puis renvoyé"
    ]
    return df