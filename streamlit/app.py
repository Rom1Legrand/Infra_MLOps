# streamlit/app.py
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import os

# Configuration de la page
st.set_page_config(
    page_title="Fraud Detection Dashboard",
    page_icon="🕵️",
    layout="wide"
)

# Connexion à Neon
@st.cache_resource
def init_connection():
    return create_engine(os.environ["NEON_DATABASE_URL"])

# Récupération des données
