import streamlit as st
from streamlit_option_menu import option_menu

def streamlit_menu():
    with st.sidebar:
        selected = option_menu(
            menu_title="Menu",
            options=["Preferences", "Search", "Recommendation"],
            icons=["house", "search", "list"],
            default_index=0,
        )
    return selected
