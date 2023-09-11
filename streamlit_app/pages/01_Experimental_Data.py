import streamlit as st
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

try:
    st.set_page_config(layout="wide")
except:
    pass

st.subheader("Parameter estimation")
st.caption("Experimental data")

c1, c2 = st.columns(2)
eqn_sel = c1.selectbox("Select equation", 
                        [
                        #"", 
                        "Michaelis-Menten", "Competitive Inhibition by S", "Competitive Inhibition by P", "Mixed Inhibition"],
                        key="parameter_estimation_eqn_sel")

if eqn_sel == "Michaelis-Menten":
    c2.markdown("");c2.markdown("") # For alignment
    c2.markdown("""$$ v = \\frac{V_{max} S}{K_m + S}$$""")

    c1, c2 = st.columns(2)
    c2.markdown("");c2.markdown("") # For alignment
    with c2.expander("File format:"):
        st.markdown("Provide an excel file with the following structure")
        df = pd.DataFrame({"s": ["s_1", "s_2", "...", "s_n"], "v": ["v_1", "v_2", "...", "v_n"]})
        st.dataframe(df)
    from scripts.michaelis_menten import solver
    uploaded_file = c1.file_uploader("Upload data file", type=["xlsx"])
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        # Do some checks on data

        # Offer the option to plot the data or obtain the parameters
        opt_sel = st.radio("Select option", ["Plot data", "Estimate parameters"], horizontal=True)
        if opt_sel=="Plot data":
            # Plot the data
            fig, ax = plt.subplots(1, 1, figsize=(12, 6))
            ax.plot(df["s"], df["v"], "o")
            ax.set_xlabel("s")
            ax.set_ylabel("v")
            # Show the plot
            st.pyplot(fig)        
        elif opt_sel=="Estimate parameters":
            solution = solver(df)
            c1, c2 = st.columns(2)
            c1.markdown(f"""
            **Direct Linear Plot**:
            * $Vmax = {solution['direct_linear_plot']['Vmax']:.3f} $
            * $K_m = {solution['direct_linear_plot']['Km']:.3f} $
            """)
            c2.markdown(f"""
            **Linear Regression**:
            * $Vmax = {solution['linear_regression']['Vmax']:.3f} $
            * $K_m = {solution['linear_regression']['Km']:.3f} $
            """)
        else:
            st.error("Unknown option")