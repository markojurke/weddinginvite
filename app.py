import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection


#st.set_page_config(page_title="Anđela & Marko", page_icon="💍", layout="centered")

css = """
<link href="https://fonts.googleapis.com/css2?family=Italianno&family=Kaushan+Script&family=Zeyada&family=Bellefair&family=Forum&family=Allura&family=EB+Garamond:ital,wght@0,400..800;1,400..800&family=Dancing+Script:wght@700&family=La+Belle+Aurore&family=Lora:ital@0;1&display=swap" rel="stylesheet">
<style>
    /* The starting state: invisible and slightly lower */
    .reveal-on-scroll {
        opacity: 0;
        transform: translateY(30px);
        transition: all 1.0s ease-out;
    }

    /* The visible state: triggered by our script */
    .reveal-on-scroll.visible {
        opacity: 1;
        transform: translateY(0);
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .cursive-name, .quote-text, .event-details, .stButton, .stTextInput {
        animation: fadeIn 1s ease-out forwards;
    }
    /* Stagger the timing so they don't all pop in at once */
    .cursive-name { animation-delay: 0s; }
    .quote-text { animation-delay: 0s; }
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDecoration {display:none !important;}
    .block-container {
        padding-top: 1rem !important; /* Changed from 6rem default to 1rem */
        padding-bottom: 0rem !important;
    }
    .stApp { background-color: #ffffff !important; }

    /* Text Colors */
    html, body, [data-testid="stWidgetLabel"], .stMarkdown p, h1, h2, h3, span, label {
        color: #556B2F !important;
        font-family: 'Roboto', serif !important;
    }

 

    .cursive-name {
        font-family: 'Forum';
        font-size: 55px !important;
        display: block;
        color: #556B2F !important;
        line-height: 0.8 !important;  /* Values below 1.0 pull lines closer */
        margin-bottom: 0px !important; /* Negative margin pulls the next name UP */
    }

    /* INPUT FIELDS */
    .stTextInput input {
        background-color: white !important;
        border: 1px solid #556B2F !important;
        color: #556B2F !important;
    }

    /* BUTTONS - THE FIX */
    /* Target every button to be outline olive */
    div.stButton > button {
        background-color: white !important;
        color: #556B2F !important;
        border: 1px solid #556B2F !important;
        border-radius: 8px !important;
        transition: all 0.3s ease;
    }

    /* Force the last button (Spremi) to be Solid Olive with White Text */
    div.stButton:last-of-type > button {
        background-color: #556B2F !important;
        color: #ffffff !important;
        border: none !important;
        font-weight: bold !important;
    }

    /* Force the specific label inside the button to be white */
    div.stButton:last-of-type > button div p {
        color: #ffffff !important;
    }

    .stRadio > div { display: flex; justify-content: center; gap: 20px; }
    hr { border-top: 1px solid #e2e2d8 !important; }
    
    .quote-text {
        font-family: 'Italianno', cursive !important;
        font-size: 32px !important;
        color: #556B2F !important;
        text-align: center;
        line-height: 1.4;
        margin: 0 0;
        padding: 0 20px;
    }
    [data-testid="stWidgetLabel"] p {
        text-align: center !important;
        width: 100% !important;
        display: block !important;
    }

    
    .stButton {
        display: flex !important;
        justify-content: center !important;
    }

    
    [data-testid="stMarkdownContainer"] + div[role="radiogroup"] {
        justify-content: center !important;
    }

    
    [data-testid="column"] > div {
        align-items: center !important;
    }
    [data-testid="stWidgetLabel"] {
    text-align: center !important;
    justify-content: center !important;
    display: flex !important;
    width: 100% !important;
    }
    .stTextInput input {
    text-align: center !important;
    }
    .stTextInput {
    margin-left: auto !important;
    margin-right: auto !important;
    width: 100% !important;
    max-width: 450px !important; /* Matches your buttons */
    }


    /* 2. Center the Radio Button Options (the horizontal row) */
    [data-testid="stHorizontalBlock"] {
    justify-content: center !important;
    }

    /* 3. Specific fix for the Radio group container */
    div[role="radiogroup"] {
    display: flex !important;
    justify-content: center !important;
    gap: 20px !important; /* Space between 'Dolazim' and 'Nažalost' */
    width: 100% !important;
    }


    div[role="radiogroup"] label {
    justify-content: center !important;
    }
    /* Style the main selectbox container */
    div[data-baseweb="select"] > div {
        background-color: white !important;
        border: 1px solid #556B2F !important;
        border-radius: 8px !important;
        color: #556B2F !important;
    }

    /* Style the text inside the selectbox when it's closed */
    div[data-baseweb="select"] span, div[data-baseweb="select"] div {
        color: #556B2F !important;
    }

    /* Style the drop-down list (the menu that pops open) */
    ul[role="listbox"] {
        background-color: white !important;
        border: 1px solid #556B2F !important;
    }

    /* Style the individual options inside the list */
    li[role="option"] {
        background-color: white !important;
        color: #556B2F !important;
        transition: background-color 0.3s ease;
    }

    /* Change color when you hover over an option */
    li[role="option"]:hover {
        background-color: #f0f2eb !important; /* Very light olive tint on hover */
        color: #556B2F !important;
    }

    /* Center the placeholder and selected text */
    div[data-baseweb="select"] {
        text-align: center !important;
    }
    /* Hide the top right hamburger menu and GitHub icon */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}

    /* Hide the "Made with Streamlit" footer at the bottom */
    footer {visibility: hidden;}
    
    /* Optional: Hide the decoration bar at the very top */
    .stDecoration {display:none !important;}
</style>
"""
st.markdown(css, unsafe_allow_html=True)
st.image("1.jpg", use_container_width=True)



# Create a single column and center the content using CSS
_, col_center, _ = st.columns([1, 6, 1])

with col_center:
    st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
    
   

    # 1. Gather Inputs
    main_name = st.text_input("Vaše ime i prezime", placeholder="Upišite ovdje...")

    if "guests" not in st.session_state:
        st.session_state.guests = []

    for i, g in enumerate(st.session_state.guests):
        st.session_state.guests[i] = st.text_input(f"Gost {i+1}", value=g, key=f"guest_{i}")
        if st.button(f"Ukloni gosta {i+1}", key=f"rm_{i}", use_container_width=True):
            st.session_state.guests.pop(i)
            st.rerun()

    if st.button("➕ Dodaj još jednu osobu", use_container_width=True):
        st.session_state.guests.append("")
        st.rerun()

    st.write("") 

    attendance = st.selectbox(
	    "Dolazak", 
	    ["Odaberite opciju...", "Dolazim", "Ne dolazim"],
	    index=0,
 	   help=None # Keeping it clean
	)

    st.write("") 

    # 2. THE SAVE LOGIC (This is the part that was missing)
    if st.button("Spremi potvrdu", use_container_width=True):
        if not main_name or main_name.strip() == "":
            st.warning("Molimo unesite Vaše ime.")
        elif attendance == "Odaberite opciju...":
            st.warning("Molimo odaberite dolazite li.")
        else:
            try:
                # Connect to Google Sheets
                conn = st.connection("gsheets", type=GSheetsConnection)
                
                # Read current data (ttl=0 ensures we don't use old cached data)
                df_existing = conn.read(ttl=0)
                
                # Create a list of names (Main Person + any guests with names typed in)
                valid_guests = [g for g in st.session_state.guests if g.strip()]
                all_guests_to_save = [main_name] + valid_guests
                
                # Prepare the new rows
                new_data = []
                for name in all_guests_to_save:
                    new_data.append({
                        "Name": name, 
                        "Attendance": attendance, 
                        "Group": main_name
                    })
                
                # Combine with old data and update the sheet
                df_new = pd.concat([df_existing, pd.DataFrame(new_data)], ignore_index=True)
                conn.update(data=df_new)
                
                # Visual Feedback
                st.success(f"Hvala Vam! Potvrda za {len(all_guests_to_save)} osoba/e je spremljena.")
                
                # Clear guest list for next time
                st.session_state.guests = []
                
            except Exception as e:
                st.error(f"Došlo je do pogreške pri spremanju: {e}")

    st.markdown('</div>', unsafe_allow_html=True)
