import streamlit as st


def afficher_transactions_non_classifiees(df):

    transactions_non_classifiees = df[
        (df["categorie_adeb"] == "Imprévus") &
        (df["sous_categorie_adeb"] == "Non catégorisé")
    ]

    nb_non_classifiees = len(transactions_non_classifiees)

    if nb_non_classifiees > 0:

        montant_non_classifie = abs(
            transactions_non_classifiees["amount"].sum()
        )

        st.warning(
            f"{nb_non_classifiees} transaction(s) non classifiée(s) détectée(s), "
            f"pour un montant total de {montant_non_classifie:.2f} €."
        )

        with st.expander("Voir les transactions non classifiées"):

            st.dataframe(
                transactions_non_classifiees[
                    [
                        "dateOp",
                        "label",
                        "amount",
                        "category",
                        "categoryParent"
                    ]
                ],
                use_container_width=True
            )

    else:

        st.success(
            "Toutes les transactions ont été classifiées."
        )

    return transactions_non_classifiees