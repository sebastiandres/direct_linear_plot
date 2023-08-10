import streamlit as st
import pandas as pd

st.title("Direct Linear Plot - Parameter Estimation")

c1, c2 = st.columns(2)
eqn_sel = c1.selectbox("Select equation", 
                        ["", "Michaelis-Menten", "Competitive Inhibition by S", "Competitive Inhibition by P", "Mixed Inhibition"],
                        key="parameter_estimation_eqn_sel")

if eqn_sel == "Michaelis-Menten":
    c2.markdown("");c2.markdown("") # For alignment
    c2.markdown("""$$ v = \\frac{V_{max} S}{K_m + S}$$""")

    with st.expander("File format:"):
        st.markdown("Provide an excel file with the following structure")
        df = pd.DataFrame({"s": ["s_1", "s_2", "...", "s_n"], "v": ["v_1", "v_2", "...", "v_n"]})
        st.dataframe(df)
    from scripts.michaelis_menten import solver
    uploaded_file = st.file_uploader("Upload data file", type=["xlsx"])
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        #st.write(df)
        Vmax, Km = solver(df)
        st.write(f"""
        The estimated parameters are:
        * Vmax = {Vmax:.3f}
        * Km = {Km:.3f}
        """)