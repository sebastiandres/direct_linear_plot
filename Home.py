import streamlit as st

import helpers.shared_hacks as shh

shh.page_setup("Sensibility analysis")

st.title("Direct Linear Plot")

st.markdown("""
Select the type of analysis from the sidebar:
* **Experimental data**: Upload experimental data to estimate the parameters using the Direct Linear Plot and Linear Regression method.
* **Error Analysis**: Generate synthetic data with known parameters and error, and estimate the parameters using the Direct Linear Plot and Linear Regression method.
* **Sensibility Analysis**: Generate synthetic data with known parameters and error, and estimate the parameters using the Direct Linear Plot and Linear Regression method. Allows to have a larger error on a particular measurement to test the sensitivity to error.
""")

# Construct the markdown
mkd = """Available equations:"""
for eqn_option in shh.EQUATION_OPTIONS:
    latex_eqn = shh.latex_formula_from_equation_name(eqn_option)
    mkd += f"\n* {eqn_option}"
    mkd += f"\n\n{'&nbsp;'*20}{latex_eqn}"
# Show the markdown
st.markdown(mkd)