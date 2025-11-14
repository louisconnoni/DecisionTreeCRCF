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

# --- Helper function for RAM/cores/walltime logic ---
def advanced_requirements():
    ram = st.radio("Do you need more than 512 GB of RAM?", ["Yes", "No"])
    if ram == "Yes":
        st.success("👉 Suggested platform: **NSF ACCESS**")
        return

    cores_192 = st.radio("Do you need more than 192 cores?", ["Yes", "No"])
    if cores_192 == "Yes":
        st.success("👉 Suggested platform: **NSF ACCESS**")
        return

    cores_16 = st.radio("Do you need more than 16 cores?", ["Yes", "No"])
    if cores_16 == "Yes":
        walltime_240 = st.radio("Do you need walltime greater than 240 hours?", ["Yes", "No"])
        if walltime_240 == "Yes":
            st.success("👉 Suggested platform: **NSF ACCESS**")
        else:
            gui = st.radio("Do you require a GUI?", ["Yes", "No"])
            if gui == "Yes":
                st.success("👉 Suggested platform: **NSF ACCESS - JetStream2**")
            else:
                walltime_72 = st.radio("Do you need walltime greater than 72 hours?", ["Yes", "No"])
                if walltime_72 == "Yes":
                    st.success("👉 Suggested platform: **Augie batch w/ long qos**")
                else:
                    st.success("👉 Suggested platform: **Augie Batch**")
    else:
        st.success("👉 Suggested platform: **Possible OSG - See CRCF**")


# --- Logic Tree Start ---
itar_phi = st.radio("Does your research involve ITAR or PHI?", ["Yes", "No"])

if itar_phi == "Yes":
    st.success("👉 Suggested platform: **See UTS**")

else:
    open_source = st.radio("Does your research use open source software?", ["Yes", "No"])

    if open_source == "Yes":
        advanced_requirements()

    else:
        software = st.selectbox("Which software are you using?", ["MATLAB", "COMSOL", "ANSYS", "Other"])

        if software == "MATLAB":
            advanced_requirements()

        elif software == "COMSOL":
            paid_group = st.radio("Are you a member of a paid COMSOL group?", ["Yes", "No"])
            if paid_group == "Yes":
                advanced_requirements()
            else:
                st.success("👉 Suggested platform: **See CRCF**")

        elif software == "ANSYS":
            st.success("👉 Suggested platform: **vDesktop**")

        else:  # Other
            st.success("👉 Suggested platform: **See CRCF**")
