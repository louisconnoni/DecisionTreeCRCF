import streamlit as st

st.title("Research Platform Chooser")

st.subheader(
    "This simple advisor collects a few details about your research job "
    "and suggests a computing platform."
)

st.markdown("""
**Possible outputs include:**
- See UTS  
- See CRCF  
- vDesktop  
- NSF ACCESS  
- Possible OSG - See CRCF  
- NSF ACCESS - JetStream2  
- Augie batch w/ long qos  
- Augie Batch  
""")

with st.expander("What is this doing? (click to expand)"):
    st.markdown(
        """
        **How it works (v1):** The logic behind this app is based
        on a decision flowchart developed by CRCF in September 2025.
        This app implements the flowchart by having users input various
        aspects of their project.
        """
    )


# --- Helper function for RAM/cores/walltime logic ---
def advanced_requirements():
    suggestion = None
    ram = st.radio("Do you need more than 512 GB of RAM?", ["Yes", "No"])
    if ram == "Yes":
        suggestion = "NSF ACCESS"
    else:
        cores_192 = st.radio("Do you need more than 192 cores?", ["Yes", "No"])
        if cores_192 == "Yes":
            suggestion = "NSF ACCESS"
        else:
            cores_16 = st.radio("Do you need more than 16 cores?", ["Yes", "No"])
            if cores_16 == "Yes":
                walltime_240 = st.radio("Do you need walltime greater than 240 hours?", ["Yes", "No"])
                if walltime_240 == "Yes":
                    suggestion = "NSF ACCESS"
                else:
                    gui = st.radio("Do you require a GUI?", ["Yes", "No"])
                    if gui == "Yes":
                        suggestion = "NSF ACCESS - JetStream2"
                    else:
                        walltime_72 = st.radio("Do you need walltime greater than 72 hours?", ["Yes", "No"])
                        if walltime_72 == "Yes":
                            suggestion = "Augie batch w/ long qos"
                        else:
                            suggestion = "Augie Batch"
            else:
                suggestion = "Possible OSG - See CRCF"
    return suggestion

# --- Logic Tree Start ---
itar_phi = st.radio("Does your research involve ITAR or PHI?", ["Yes", "No"])
suggestion = None

if itar_phi == "Yes":
    suggestion = "See UTS"
else:
    open_source = st.radio("Does your research use open source software?", ["Yes", "No"])
    if open_source == "Yes":
        suggestion = advanced_requirements()
    else:
        software = st.selectbox("Which software are you using?", ["MATLAB", "COMSOL", "ANSYS", "Other"])
        if software == "MATLAB":
            suggestion = advanced_requirements()
        elif software == "COMSOL":
            paid_group = st.radio("Are you a member of a paid COMSOL group?", ["Yes", "No"])
            if paid_group == "Yes":
                suggestion = advanced_requirements()
            else:
                suggestion = "See CRCF"
        elif software == "ANSYS":
            suggestion = "vDesktop"
        else:
            suggestion = "See CRCF"

# --- Show result only when button is clicked ---
if st.button("Get Suggested Platform"):
    if suggestion:
        st.success(f"👉 Suggested platform: **{suggestion}**")
    else:
        st.warning("Please answer all questions to get a suggestion.")

