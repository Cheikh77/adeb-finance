import pandas as pd
import streamlit as st

from modules.classification import nettoyer_montant, mapper_adeb

print("IMPORT_DATA CHARGÉ")

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
    """
    Détecte les virements reçus puis renvoyés.

    Exemple :
    +2625 € reçu
    -2625 € renvoyé

    Impact financier réel = 0 €.
    Ces opérations doivent donc être exclues des revenus et dépenses.
    """

    df = df.copy()

    df["virement_neutre"] = False

    virements = df[
        df["label"]
        .astype(str)
        .str.upper()
        .str.contains("VIR", na=False)
    ].copy()

    virements["montant_abs"] = virements["amount"].abs().round(2)

    for i, ligne in virements.iterrows():

        montant = ligne["amount"]
        montant_abs = round(abs(montant), 2)
        date_ligne = ligne["dateOp"]

        candidats = virements[
            (virements.index != i) &
            (virements["montant_abs"] == montant_abs) &
            (virements["amount"] * montant < 0) &
            (
                (virements["dateOp"] - date_ligne).abs()
                <= pd.Timedelta(days=delai_jours)
            )
        ]

        if not candidats.empty:
            index_candidat = candidats.index[0]

            df.loc[i, "virement_neutre"] = True
            df.loc[index_candidat, "virement_neutre"] = True

    return df


def detecter_virements_personnels(
    df,
    nom_utilisateur="",
    prenom_utilisateur=""
):
    """
    Détecte les virements où le nom/prénom de l'utilisateur apparaît
    dans le libellé.

    Objectif :
    identifier les transferts entre comptes personnels afin de ne pas
    les considérer comme de vrais revenus ou de vraies dépenses.
    """

    df = df.copy()

    nom_utilisateur = str(nom_utilisateur).upper().strip()
    prenom_utilisateur = str(prenom_utilisateur).upper().strip()

    if not nom_utilisateur and not prenom_utilisateur:
        df["virement_personnel"] = False
        return df

    nom_complet = f"{prenom_utilisateur} {nom_utilisateur}".strip()
    nom_inverse = f"{nom_utilisateur} {prenom_utilisateur}".strip()

    label_upper = df["label"].astype(str).str.upper()

    masque_virement = label_upper.str.contains("VIR", na=False)

    masque_nom = (
        label_upper.str.contains(nom_complet, na=False)
        if nom_complet
        else False
    )

    masque_nom_inverse = (
        label_upper.str.contains(nom_inverse, na=False)
        if nom_inverse
        else False
    )

    df["virement_personnel"] = (
        masque_virement &
        (masque_nom | masque_nom_inverse)
    )

    return df


def classifier_transactions(
    df,
    nom_utilisateur="",
    prenom_utilisateur=""
):
    df = df.copy()

    df[[
        "type_adeb",
        "categorie_adeb",
        "sous_categorie_adeb"
    ]] = df.apply(
        mapper_adeb,
        axis=1,
        result_type="expand"
    )

    df = detecter_virements_neutres(df)

    df = detecter_virements_personnels(
        df,
        nom_utilisateur=nom_utilisateur,
        prenom_utilisateur=prenom_utilisateur
    )

    df.loc[
        df["virement_neutre"],
        ["type_adeb", "categorie_adeb", "sous_categorie_adeb"]
    ] = [
        "Transfert",
        "Virement neutre",
        "Argent reçu puis renvoyé"
    ]

    df.loc[
        df["virement_personnel"],
        ["type_adeb", "categorie_adeb", "sous_categorie_adeb"]
    ] = [
        "Transfert",
        "Virement personnel",
        "Transfert entre comptes personnels"
    ]

    return df