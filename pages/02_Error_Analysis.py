import streamlit as st
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

try:
    st.set_page_config(layout="wide")
except:
    pass

if "parameter_checksum" not in st.session_state:
    st.session_state["parameter_checksum"] = ""
if "DLP" not in st.session_state:
    st.session_state["DLP"] = {}
if "LR" not in st.session_state:
    st.session_state["LR"] = {}

st.subheader("Error analysis")
st.caption("Error analysis on synthetic data generated with known parameters")

eqn_sel = st.sidebar.selectbox("Select equation", 
                        [
                        #"", 
                        "Michaelis-Menten", 
                        "Competitive Inhibition by S", 
                        "Competitive Inhibition by P", 
                        "Mixed Inhibition"],
                        key="error_analysis_eqn_sel")

if eqn_sel == "Michaelis-Menten":
    #c2.markdown("");c2.markdown("") # For alignment
    st.sidebar.markdown("""$$ v = \\frac{V_{max} s}{K_m + s}$$""")
    # Parameters
    c1, c2, _, _ = st.columns(4)
    Vmax = c1.number_input("Vmax", value=1.0)
    Km = c2.number_input("Km", value=1.0)
    # Error type
    c1, c2, c3, c4 = st.columns(4)
    mu = c1.number_input("Mean", value=0.0)
    sigma = c2.number_input("Standard deviation", value=0.1)
    N = c3.number_input("Number of experiments", value=1000)

    # Create a checksum to check if the parameters have changed
    parameter_checksum = f"{eqn_sel}_{Vmax}_{Km}_{mu}_{sigma}_{N}"
    if st.session_state["parameter_checksum"] != parameter_checksum:
        st.session_state["parameter_checksum"] = parameter_checksum
        st.session_state["DLP"] = {}
        st.session_state["LR"] = {}

    # Generate data
    st.markdown("Click the button to generate the data")
    if st.button("Generate analysis", key="error_analysis"):
        from scripts.michaelis_menten import error_analysis
        DLP, LR = error_analysis(Vmax, Km, mu, sigma, N)
        # Store the results
        st.session_state["DLP"] = DLP
        st.session_state["LR"] = LR

    if len(st.session_state["DLP"]) and len(st.session_state["LR"]):
        opt_sel = st.radio("Select option", ["Plot estimations", "Plot errors"], horizontal=True)
        DLP = st.session_state["DLP"]
        LR = st.session_state["LR"]
        if opt_sel=="Plot estimations":
            # Plot the results on a graph
            fig, ax = plt.subplots(1, 2, figsize=(12, 6))
            # First plot
            xmin = min(DLP["Vmax"].min(), LR["Vmax"].min())
            xmax = max(DLP["Vmax"].max(), LR["Vmax"].max())
            ymin = min(DLP["Vmax"].min(), LR["Vmax"].min())
            ymax = max(DLP["Vmax"].max(), LR["Vmax"].max())
            xymax = max(xmax, ymax)
            ax[0].set_xlabel("Vmax estimated using Direct Linear Plot")
            ax[0].set_ylabel("Vmax estimated using Linear Regression")
            ax[0].plot([-xymax, xymax*1.1], [-xymax, xymax*1.1], "k", alpha=0.25)
            ax[0].plot([-xymax, Vmax], [Vmax, Vmax], "r", alpha=0.5)
            ax[0].plot([Vmax, Vmax], [-xymax, Vmax], "r", alpha=0.5)
            ax[0].plot(DLP["Vmax"], LR["Vmax"], "o", label="Vmax", alpha=0.25)
            ax[0].set_xlim(xmin, xmax)
            ax[0].set_ylim(xmin, xmax)
            # Second plot
            xmin = min(DLP["Km"].min(), LR["Km"].min())
            xmax = max(DLP["Km"].max(), LR["Km"].max())
            ymin = min(DLP["Km"].min(), LR["Km"].min())
            ymax = max(DLP["Km"].max(), LR["Km"].max())
            xymax = max(xmax, ymax)
            ax[1].set_xlabel("Kmax estimated using Direct Linear Plot")
            ax[1].set_ylabel("Kmax estimated using Linear Regression")
            ax[1].plot([-xymax, xymax*1.1], [-xymax, xymax*1.1], "k", alpha=0.25)
            ax[1].plot([-xymax, Km], [Km, Km], "r", alpha=0.5)
            ax[1].plot([Km, Km], [-xymax, Km], "r", alpha=0.5)
            ax[1].set_xlim(xmin, xmax)
            ax[1].set_ylim(xmin, xmax)
            ax[1].plot(DLP["Km"], LR["Km"], "o", label="Vmax", alpha=0.25)
            # Show the plot
            c1, c2 = st.columns([2,1])
            c1.pyplot(fig)
            c2.markdown(f"""
            Parameters used on plot:
            * $Vmax = {Vmax:.3f} $ (True value)
            * $K_m = {Km:.3f} $ (True value)
            * $\\mu = {mu:.3f} $
            * $\\sigma = {sigma:.3f} $
            * $N = {N} $
            """)
        elif opt_sel=="Plot errors":
            # Another plot
            fig, ax = plt.subplots(1, 2, figsize=(12, 6))
            # First plot
            x = np.abs(DLP["Vmax"]-Vmax)
            y = np.abs(LR["Vmax"]-Vmax)
            m = x < y # DLP < LR means DLP is more precise
            xmax = max(x.max(), y.max())
            ax[0].plot(x[m], y[m], "gs", label="Vmax", alpha=0.25)
            ax[0].plot(x[~m], y[~m], "bs", label="Vmax", alpha=0.25)
            ax[0].set_xlabel("Absolute error in Vmax estimated using Direct Linear Plot")
            ax[0].set_ylabel("Absolute error in Vmax estimated using Linear Regression")
            ax[0].plot([0, xmax], [0, xmax], "k", alpha=0.25)
            ax[0].set_xlim(0, xmax)
            ax[0].set_ylim(0, xmax)
            ax[0].set_title(f"Vmax: DLP is more precise than LR \nin {m.sum()}/{N} = {100*m.sum()/N}% of experiments")
            # Second plot
            x = np.abs(DLP["Km"]-Km)
            y = np.abs(LR["Km"]-Km)
            m = x < y # DLP < LR means DLP is more precise
            ax[1].plot(x[m], y[m], "gs", label="Km", alpha=0.25)
            ax[1].plot(x[~m], y[~m], "bs", label="Km", alpha=0.25)
            ax[1].set_xlabel("Absolute error in Km estimated using Direct Linear Plot")
            ax[1].set_ylabel("Absolute error in Km estimated using Linear Regression")
            ax[1].set_title(f"Km: DLP is more precise than LR \n in {m.sum()}/{N} = {100*m.sum()/N}% of experiments")
            # Show the plot
            c1, c2 = st.columns([2,1])
            c1.pyplot(fig)
            c2.markdown(f"""
            Parameters used on plot:
            * $Vmax = {Vmax:.3f} $ (True value)
            * $K_m = {Km:.3f} $ (True value)
            * $\\mu = {mu:.3f} $
            * $\\sigma = {sigma:.3f} $
            * $N = {N} $
            """)
        else:
            st.error("Unknown option")