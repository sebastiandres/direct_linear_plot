import streamlit as st
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from os.path import basename

import helpers.shared_hacks as shh

shh.page_setup("Sensibility analysis")
eqn_sel = shh.equation_selection()

st.subheader("Parameter estimation")
st.caption("Experimental data")

if eqn_sel == "Michaelis-Menten":
    
    from scripts.michaelis_menten import solver
    from scripts.michaelis_menten import v_generation
    
    c1, c2 = st.columns(2)
    c2.markdown("");c2.markdown("") # For alignment

    with c2.expander("File format:"):
        st.markdown("Provide an excel file with the following structure")
        df = pd.DataFrame({"s": ["s_1", "s_2", "...", "s_n"], "v": ["v_1", "v_2", "...", "v_n"]})
        st.dataframe(df)
        c1_expander, c2_expander = st.columns(2)
        template_file = "data/template_MM.xlsx"
        c1_expander.download_button("Download template", 
                                    data=open(template_file, "rb").read(), 
                                    file_name=basename(template_file)
                                    )
        example_file = "data/example_MM.xlsx"
        c2_expander.download_button("Download example", 
                                    data=open(example_file, "rb").read(), 
                                    file_name=basename(example_file)
                                    )

    uploaded_file = c1.file_uploader("Upload data file", type=["xlsx"])

    if uploaded_file is not None:
        xl_file = pd.ExcelFile(uploaded_file)
        # Get dataframes for all the sheets
        dfs = {sheet_name: xl_file.parse(sheet_name) for sheet_name in xl_file.sheet_names}
        sheet_sel = c1.selectbox("Select sheet", list(dfs.keys()))
        df = dfs[sheet_sel]
        df.columns = [_.lower().split(" ")[0] for _ in df.columns]
        if "s" not in df.columns or "v" not in df.columns:
            st.error("The data file should have columns named 's' and 'v'")
            st.stop()
        else:
            df = df[["s", "v"]]
            df = df.dropna()
            df = df.astype(float)
            df = df.sort_values(by="s")
            df = df.reset_index(drop=True)            
        # Do some checks on data

        # Solve
        solution = solver(df)

        # Offer the option to plot the data or obtain the parameters
        opt_sel = st.radio("Select option", ["Data", "Plot data", "Estimate parameters"], horizontal=True)
        if opt_sel=="Data":
            st.dataframe(df)
        elif opt_sel=="Plot data":
            c1, c2, _ = st.columns(3)
            include_DPL = c1.toggle("Plot DLP based fit", False)
            include_LR = c2.toggle("Fit LR based fit", False)
            # Plot the data
            fig, ax = plt.subplots(1, 1, figsize=(12, 6))
            s_array = np.linspace(0, df["s"].max(), 100)
            ax.plot(df["s"], df["v"], "o")
            if include_DPL:
                Vmax = solution['direct_linear_plot']['Vmax']
                Km = solution['direct_linear_plot']['Km']
                v_DLP = v_generation(Vmax, Km, s_array)
                ax.plot(s_array, v_DLP, ":", label="DLP")
            if include_LR:
                Vmax = solution['linear_regression']['Vmax']
                Km = solution['linear_regression']['Km']
                v_LR = v_generation(Vmax, Km, s_array)
                ax.plot(s_array, v_LR, "--", label="LR")
            ax.set_xlabel("s")
            ax.set_ylabel("v")
            ax.set_xlim(0, 1.1*df["s"].max())
            ax.set_ylim(0, 1.1*df["v"].max())

            # Show the plot
            st.pyplot(fig)        
        elif opt_sel=="Estimate parameters":
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