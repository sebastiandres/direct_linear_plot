import streamlit as st

EQUATION_OPTIONS = [
                    "Michaelis-Menten", 
                    "Uncompetitive Inhibition by S", 
                    "Competitive Inhibition by P", 
                    "Uncompetitive Inhibition by P", 
                    "Mixed Inhibition by P"
                    ]

def page_setup(page_title):
    """
    Sets up the page title, favicon and page icon.
    It also does some css fixing
    """
    try:
        st.set_page_config(layout="wide")
    except:
        pass

    # padding-top: 3rem !important;
    # padding-bottom: 3rem !important;    
    st.markdown("""
    <style>
    ul.eczjsme9  {
        max-height: 50vh;  
        }
    </style>
    """, unsafe_allow_html=True)

def equation_selection(debug=False):
    eqn_sel = st.sidebar.selectbox("Select equation", 
                        EQUATION_OPTIONS,
                        index=None,
                        key="error_analysis_eqn_sel")
    if debug:
        st.warning(eqn_sel)
    if eqn_sel!=None:
        latex_formula = latex_formula_from_equation_name(eqn_sel)
        st.sidebar.markdown(latex_formula)
    return eqn_sel

def latex_formula_from_equation_name(equation_name):
    if equation_name==EQUATION_OPTIONS[0]: # Michaelis-Menten
        latex_formula = """
        $$ v = \\frac{V_{max} S}{K_m + S}$$
        """
    elif equation_name==EQUATION_OPTIONS[1]: # Uncompetitive Inhibition by S
        latex_formula = """
        $$ v = \\frac{V_{max} S}{K_m + S + S^2/K_s}$$
        """
    elif equation_name==EQUATION_OPTIONS[2]: # Competitive Inhibition by P
        latex_formula = """
        $$ v = \\frac{V_{max} S}{K_m ( 1 + \\frac{P}{K_i} ) + S}$$
        """
    elif equation_name==EQUATION_OPTIONS[3]: # Uncompetitive Inhibition by P
        latex_formula = """
        $$ v = \\frac{V_{max} S}{K_m + S ( 1 + \\frac{P}{K_j} )}$$        
        """
    elif equation_name==EQUATION_OPTIONS[4]: # Mixed Inhibition by P
        latex_formula = """
        $$ v = \\frac{V_{max} S}{K_m ( 1 + \\frac{P}{K_i} ) + S ( 1 + \\frac{P}{K_j} )}$$        
        """
    return latex_formula