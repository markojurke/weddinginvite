import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Anđela & Marko", page_icon="💍", layout="centered")

# --- CUSTOM CSS ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital@0;1&family=Lora:ital@0;1&display=swap" rel="stylesheet">
    <style>
    .stApp { background-color: #fdfcf0 !important; }
    .header-arch {
        background-color: #ffffff;
        border-bottom-left-radius: 50% 100px;
        border-bottom-right-radius: 50% 100px;
        padding: 60px 20px;
        text-align: center;
        margin-top: -80px;
        margin-left: -20%;
        margin-right: -20%;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.02);
    }
    .names {
        font-family: 'Playfair Display', serif;
        font-size: 50px;
        font-style: italic;
        color: #556B2F !important;
        line-height: 1.2;
    }
    .subtitle {
        font-family: 'Lora', serif;
        font-size: 16px;
        color: #808b72 !important;
        margin-top: 20px;
        font-style: italic;
    }
    p, div, span, label, h1, h2, h3 {
        color: #556B2F !important; 
        font-family: 'Lora', serif;
    }
    .stTextInput input {
        background-color: white !important;
        color: #556B2F !important;
        border: 1px solid #c2ccb5 !important;
        border-radius: 4px !important;
        text-align: center !important;
    }
    div.stButton > button {
        background-color: white !important;
        color: #556B2F !important;
        border: 1px dashed #c2ccb5 !important;
        width: 100% !important;
        font-family: 'Lora', serif;
    }
    div.stButton > button:first-child[kind="primary"] {
        background-color: #6b8e23 !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
    }
    .stRadio > div { display: flex; justify-content: center; }
    </style>
    """, unsafe_allow_html=True)

# --- VISUAL CONTENT ---
st.markdown("""
    <div class="header-arch">
        <div class="names">Anđela & Marko</div>
        <div class="subtitle">S ljubavlju Vas pozivamo da svojim prisustvom uveličate naše vjenčanje!</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<p style="text-align:center; font-size:28px; letter-spacing:5px; margin-top:40px; margin-bottom:0;">22 | 11 | 25</p>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; letter-spacing:3px; color:#808b72; font-size:12px; margin-bottom:40px;">SUBOTA</p>', unsafe_allow_html=True)

st.markdown('<p style="text-align:center; font-size:14px; color:#808b72; letter-spacing:2px;">OBRED VJENČANJA</p>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; font-family:Playfair Display; font-size:24px; margin-bottom:0;">17:30h</p>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; font-size:15px; margin-bottom:40px;">📍 Župa sv. Leopolda Bogdana Mandića, Dubrava</p>', unsafe_allow_html=True)

st.markdown('<p style="text-align:center; font-size:14px; color:#808b72; letter-spacing:2px;">SVEČANA VEČERA</p>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; font-family:Playfair Display; font-size:24px; margin-bottom:0;">20:00h</p>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; font-size:15px; margin-bottom:40px;">📍 Restoran "Gastro Globus", Zagreb</p>', unsafe_allow_html=True)

st.divider()

st.markdown('<h2 style="text-align:center; font-family:Playfair Display; font-style:italic;">Veselimo se Vašem dolasku!</h2>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#808b72; font-size:14px; margin-bottom:30px;">Molimo potvrdite svoj dolazak do 08. studenog.</p>', unsafe_allow_html=True)

# --- APP LOGIC ---
if "guest_list" not in st.session_state:
    st.session_state.guest_list = []

main_name = st.text_input("Ime i prezime", placeholder="Vaše ime i prezime", label_visibility="collapsed")

for i, guest_name in enumerate(st.session_state.guest_list):
    cols = st.columns([9, 1])
    with cols[0]:
        st.session_state.guest_list[i] = st.text_input(f"Gost {i+1}", value=guest_name, key=f"input_{i}", label_visibility="collapsed")
    with cols[1]:
        if st.button("✕", key=f"btn_{i}"):
            st.session_state.guest_list.pop(i)
            st.rerun()

if st.button("➕ Dodaj gosta"):
    st.session_state.guest_list.append("")
    st.rerun()

attendance = st.radio("Dolazak", ["Dolazim", "Nažalost, ne mogu doći"], horizontal=True, label_visibility="collapsed")

if st.button("Spremi!", type="primary", use_container_width=True):
    if not main_name:
        st.error("Molimo upišite vaše ime!")
    else:
        try:
            conn = st.connection("gsheets", type=GSheetsConnection)
            existing_data = conn.read(ttl=0)
            new_rows = [{"Name": main_name, "Attendance": attendance, "Additional_Guests": 0, "Guest_Names": "Glavni"}]
            if attendance == "Dolazim":
                cleaned_extras = [g for g in st.session_state.guest_list if g.strip()]
                for g_name in cleaned_extras:
                    new_rows.append({"Name": g_name, "Attendance": attendance, "Additional_Guests": 0, "Guest_Names": f"Pratnja gosta: {main_name}"})
            updated_df = pd.concat([existing_data, pd.DataFrame(new_rows)], ignore_index=True)
            conn.update(data=updated_df)
            st.balloons()
            st.success("Hvala na prijavi!")
            st.session_state.guest_list = []
        except Exception as e:
            st.error(f"Greška: {e}")

st.caption("v1.6 Anđela Edition")
