import streamlit as st

import helpers.shared_hacks as shh

shh.page_setup("Sensibility analysis")

st.title("Direct Linear Plot")

st.markdown("Select parameter estimation, data generation or both.")

# Construct the markdown
mkd = """Available equations:"""
for eqn_option in shh.EQUATION_OPTIONS:
    latex_eqn = shh.latex_formula_from_equation_name(eqn_option)
    mkd += f"\n* {eqn_option}"
    mkd += f"\n{latex_eqn}"
# Show the markdown
print(mkd)
st.markdown(mkd)