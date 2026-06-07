import streamlit as st


def afficher_navbar():
    st.sidebar.markdown("""
    <div style="
        padding: 18px;
        border-radius: 18px;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.12);
        margin-bottom: 22px;
    ">
        <div style="
            font-size: 24px;
            font-weight: 850;
            color: white;
            margin-bottom: 4px;
        ">
            Adeb Finance
        </div>

        <div style="
            font-size: 12px;
            color: #CBD5E1;
            line-height: 1.5;
        ">
            Finance responsable<br>
            Pilotage personnel
        </div>
    </div>
    """, unsafe_allow_html=True)

    page = st.sidebar.radio(
        "Menu",
        [
            "Dashboard",
            "Objectifs",
            "Zakat"
        ],
        label_visibility="collapsed"
    )

    return page