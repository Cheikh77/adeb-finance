import streamlit as st

from components.theme import CARD, BORDER, TEXT, MUTED


def afficher_titre_panel(titre, sous_titre=""):
    st.html(
        f"""
        <div style="
            background:{CARD};
            border:1px solid {BORDER};
            border-radius:24px;
            padding:24px;
            margin-bottom:20px;
            box-shadow:0 10px 25px rgba(16,24,40,0.06);
        ">

            <div style="
                font-size:22px;
                font-weight:800;
                color:{TEXT};
                margin-bottom:6px;
            ">
                {titre}
            </div>

            <div style="
                font-size:14px;
                color:{MUTED};
                margin-bottom:4px;
            ">
                {sous_titre}
            </div>

        </div>
        """
    )