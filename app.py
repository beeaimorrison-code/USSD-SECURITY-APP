import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="USSD Emergency Prototype", page_icon="📱")

# --- CUSTOM CSS FOR MOBILE LOOK ---
st.markdown("""
    <style>
    .stApp {
        max-width: 400px;
        margin: 0 auto;
        border: 2px solid #333;
        border-radius: 20px;
        padding: 20px;
        background-color: #f0f2f6;
    }
    </style>
    """, unsafe_allow_html=True) # FIXED THIS LINE

# --- SESSION STATE INITIALIZATION ---
if 'step' not in st.session_state:
    st.session_state.step = "idle"
if 'incident' not in st.session_state:
    st.session_state.incident = None

# --- USSD LOGIC ---

# 1. Idle State (Start)
if st.session_state.step == "idle":
    st.title("Phone")
    st.write("Dial *123# to report an emergency.")
    if st.button("Dial *123#"):
        st.session_state.step = "main_menu"
        st.rerun()

# 2. Main Menu
elif st.session_state.step == "main_menu":
    st.subheader("USSD Menu")
    st.write("1. Report Security Incident")
    st.write("2. Exit")
    
    choice = st.text_input("Reply:", key="main_choice")
    if st.button("Send"):
        if choice == "1":
            st.session_state.step = "incident_type"
            st.rerun()
        elif choice == "2":
            st.session_state.step = "idle"
            st.rerun()

# 3. Incident Type Selection
elif st.session_state.step == "incident_type":
    st.subheader("Select Incident Type")
    st.write("1. Robbery")
    st.write("2. Kidnapping")
    st.write("3. Suspicious Activity")
    
    choice = st.text_input("Reply:", key="inc_choice")
    if st.button("Send"):
        if choice in ["1", "2", "3"]:
            types = {"1": "Robbery", "2": "Kidnapping", "3": "Suspicious Activity"}
            st.session_state.incident = types[choice]
            st.session_state.step = "location_prompt"
            st.rerun()

# 4. Location Landmark Prompt
elif st.session_state.step == "location_prompt":
    st.subheader("Select Location")
    st.write("1. Market Area")
    st.write("2. School Zone")
    st.write("3. Residential Area")
    
    choice = st.text_input("Reply:", key="loc_choice")
    if st.button("Send"):
        if choice in ["1", "2", "3"]:
            locs = {"1": "Market Area", "2": "School Zone", "3": "Residential Area"}
            final_loc = locs[choice]
            st.session_state.step = "success"
            st.session_state.final_msg = f"ALERT SENT! {st.session_state.incident} reported at {final_loc}."
            st.rerun()

# 5. Success Screen
elif st.session_state.step == "success":
    st.success(st.session_state.final_msg)
    st.info("The backend policymaker has received your landmark-based location.")
    if st.button("Finish"):
        st.session_state.step = "idle"
        st.rerun()
