import streamlit as st


def afficher_header():

    st.html("""
    <div style="
        background: linear-gradient(135deg, #0F172A 0%, #123C4A 55%, #1A535C 100%);
        padding: 42px;
        border-radius: 28px;
        color: white;
        margin-bottom: 32px;
        box-shadow: 0 18px 45px rgba(15, 23, 42, 0.25);
    ">

        <div style="
            font-size:13px;
            letter-spacing:1.5px;
            text-transform:uppercase;
            color:#D4A017;
            font-weight:700;
            margin-bottom:12px;
        ">
            Finance éthique • Objectifs • Baraka
        </div>

        <div style="
            font-size:46px;
            font-weight:850;
            margin-bottom:12px;
            color:white;
        ">
            Adeb Finance
        </div>

        <div style="
            font-size:21px;
            font-weight:600;
            color:#E5E7EB;
            margin-bottom:18px;
        ">
            Pilotez votre argent avec clarté, discipline et vision long terme.
        </div>

        <div style="
            font-size:16px;
            line-height:1.7;
            color:#CBD5E1;
            max-width:850px;
            margin-bottom:24px;
        ">
            Une plateforme pensée pour suivre votre budget,
            vos objectifs, votre épargne,
            votre Baraka et votre zakat
            dans une logique responsable et éthique.
        </div>

        <div style="
            display:flex;
            gap:14px;
            flex-wrap:wrap;
        ">

            <div style="
                background:rgba(255,255,255,0.10);
                padding:12px 18px;
                border-radius:999px;
                border:1px solid rgba(255,255,255,0.12);
            ">
                Analyse budget
            </div>

            <div style="
                background:rgba(255,255,255,0.10);
                padding:12px 18px;
                border-radius:999px;
                border:1px solid rgba(255,255,255,0.12);
            ">
                Objectifs financiers
            </div>

            <div style="
                background:rgba(255,255,255,0.10);
                padding:12px 18px;
                border-radius:999px;
                border:1px solid rgba(255,255,255,0.12);
            ">
                Zakat & Baraka
            </div>

        </div>

    </div>
    """)