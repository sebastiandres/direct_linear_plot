import streamlit as st

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
