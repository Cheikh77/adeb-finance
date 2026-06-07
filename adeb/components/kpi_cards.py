import streamlit as st

from components.theme import (
    CARD,
    BORDER,
    TEXT,
    MUTED
)


def afficher_kpi_card(
    titre,
    valeur,
    sous_titre="",
    couleur="#1A535C"
):

    st.html(f"""
    <div style="
        background: {CARD};
        border: 1px solid {BORDER};
        border-top: 4px solid {couleur};
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 10px 25px rgba(16, 24, 40, 0.06);
        min-height: 140px;
    ">

        <div style="
            font-size: 12px;
            font-weight: 700;
            color: {MUTED};
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 14px;
        ">
            {titre}
        </div>

        <div style="
            font-size: 34px;
            font-weight: 850;
            color: {TEXT};
            margin-bottom: 10px;
            line-height: 1;
        ">
            {valeur}
        </div>

        <div style="
            font-size: 13px;
            color: {MUTED};
            line-height: 1.5;
        ">
            {sous_titre}
        </div>

    </div>
    """)