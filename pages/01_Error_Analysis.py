import streamlit as st
import pandas as pd

st.title("Direct Linear Plot - Error Analysis")

c1, c2 = st.columns(2)
eqn_sel = c1.selectbox("Select equation", 
                        ["", "Michaelis-Menten", "Competitive Inhibition by S", "Competitive Inhibition by P", "Mixed Inhibition"],
                        key="error_analysis_eqn_sel")

if eqn_sel == "Michaelis-Menten":
    c2.markdown("");c2.markdown("") # For alignment
    c2.markdown("""$$ v = \\frac{V_{max} S}{K_m + S}$$""")
    st.markdown("Select the value for the parameters")
    c1, c2, c3 = st.columns(3)
    Vmax = c1.number_input("Vmax", value=1.0)
    Km = c2.number_input("Km", value=1.0)
    N = c3.number_input("Number of measurements", value=100)
    # Error type
    error_type = c1.selectbox("Select error type", ["Normal (Gaussian)", "Uniform"])
    if error_type == "Normal (Gaussian)":
        mu = c2.number_input("Mean", value=0.0)
        sigma = c3.number_input("Standard deviation", value=0.1)
    elif error_type == "Uniform":
        a = c2.number_input("Lower bound", value=-0.1)
        b = c3.number_input("Upper bound", value=0.1)
    st.markdown("Click the button to generate the data")
    if st.button("Generate analysis"):
        st.markdown("TO BE IMPLEMENTED")