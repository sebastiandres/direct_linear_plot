import streamlit as st

st.title("Direct Linear Plot")

st.markdown("Select parameter estimation, data generation or both.")

st.markdown("""Available equations:
* Michaelis-Menten: 
$$ v = \\frac{V_{max} S}{K_m + S}$$
* Acompettive inhibition by S: 
$$ v = \\frac{V_{max} S}{K_m + S + S^2/K_s}$$
* Acompettive inhibition by P: 
$$ v = \\frac{V_{max} S}{K_m ( 1 + \\frac{P}{K_i} ) + S}$$
* Mixed inhibition:
$$ v = \\frac{V_{max} S}{K_m ( 1 + \\frac{P}{K_i} ) + S ( 1 + \\frac{P}{K_j} )}$$
""")