import streamlit as st
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

import helpers.shared_hacks as shh

shh.page_setup("Sensibility analysis")
eqn_sel = shh.equation_selection(debug=True)


if "parameter_checksum" not in st.session_state:
    st.session_state["parameter_checksum"] = ""
if "DLP" not in st.session_state:
    st.session_state["DLP"] = {}
if "LR" not in st.session_state:
    st.session_state["LR"] = {}

st.subheader("Sensibility analysis")
st.caption("Synthetic data generated with known parameters")

c1, c2 = st.columns(2)
eqn_sel = st.sidebar.selectbox("Select equation", 
                        [
                        #"", 
                        "Michaelis-Menten", 
                        "Competitive Inhibition by S", 
                        "Competitive Inhibition by P", 
                        "Mixed Inhibition"],
                        key="error_analysis_eqn_sel")



if eqn_sel == "Michaelis-Menten":
    st.sidebar.markdown("""$$ v = \\frac{V_{max} s}{K_m + s}$$""")
    # Parameters
    c1, c2, _, _ = st.columns(4)
    Vmax = c1.number_input("Vmax", value=1.0)
    Km = c2.number_input("Km", value=1.0)
    # Error type
    c1, c2, c3, c4 = st.columns(4)
    mu = c1.number_input("Mean", value=0.0, format="%.3f")
    sigma = c2.number_input("Standard deviation", value=0.005, format="%.3f")
    N = c3.number_input("Number of experiments", value=1000)
    # Parameter to vary
    c1, c2, c3, c4 = st.columns(4)
    e_index = c1.number_input("Experiment number", value=3)
    e_max = c2.number_input("Error range", value=0.025, format="%.3f")

    parameter_checksum = f"{eqn_sel}_{Vmax}_{Km}_{mu}_{sigma}_{N}_{e_index}_{e_max}"
    if st.session_state["parameter_checksum"] != parameter_checksum:
        st.session_state["parameter_checksum"] = parameter_checksum
        st.session_state["DLP"] = {}
        st.session_state["LR"] = {}

    # Generate data
    st.markdown("Click the button to generate the data")
    if st.button("Generate analysis", key="sensibility_analysis"):
        from scripts.michaelis_menten import sensitivity_analysis
        DLP, LR = sensitivity_analysis(Vmax, Km, mu, sigma, N, e_index, -e_max, e_max)
        # Store the results
        st.session_state["DLP"] = DLP
        st.session_state["LR"] = LR

    if st.session_state["DLP"] and st.session_state["LR"]:
        DLP = st.session_state["DLP"]
        LR = st.session_state["LR"]
        st.markdown(f"""
        Parameters used on plot:
        * $Vmax = {Vmax:.3f} $ (True value)
        * $K_m = {Km:.3f} $ (True value)
        * $\\mu = {mu:.3f} $
        * $\\sigma = {sigma:.3f} $
        * $N = {N} $
        * $E_{e_index} \in [{-e_max:.3f}, +{e_max:.3f}] $
        """)
        # Plot the results on a graph
        opt_sel = st.radio("Select value", ["Km", "Vmax"], horizontal=True)
        value = opt_sel
        fig, ax = plt.subplots(1, 2, figsize=(12, 6))
        value_max = max(DLP[0][value])
        value_min = min(DLP[0][value])
        k_alpha = (0.5/N)**.4 # alpha for the plot, so that the lines are more visible
        fig.suptitle(f"Estimation of {value} using Direct Linear Plot (DLP) and Linear Regression (LR)")
        for i in DLP.keys():
            ax[0].plot(DLP[i]["Error"], DLP[i][value], "k-", alpha=k_alpha)
            ax[0].set_xlabel("Error E_3")
            ax[0].set_ylabel(f"DLP estimation for {value}")
            ax[1].plot(DLP[i]["Error"], LR[i][value], "k-", alpha=k_alpha)
            ax[1].set_xlabel("Error E_3")
            ax[1].set_ylabel(f"Linear Regression estimation for {value}")
            value_min = min(min(DLP[i][value]), min(LR[i][value]), value_min)
            value_max = max(max(DLP[i][value]), max(LR[i][value]), value_max)
        ax[0].grid(axis="y", alpha=0.25)
        ax[0].plot([0,0], [value_min, value_max], "k", alpha=0.1)
        ax[0].set_ylim(value_min, value_max)
        ax[1].grid(axis="y", alpha=0.25)
        ax[1].plot([0,0], [value_min, value_max], "k", alpha=0.1)
        ax[1].set_ylim(value_min, value_max)
        # Show the plot
        st.pyplot(fig)