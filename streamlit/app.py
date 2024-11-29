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
@st.cache_data(ttl=600)
def get_recent_transactions():
    conn = init_connection()
    return pd.read_sql("""
        SELECT * FROM recent_transactions 
        WHERE trans_date_trans_time >= NOW() - INTERVAL '24 hours'
        ORDER BY trans_date_trans_time DESC
    """, conn)

@st.cache_data(ttl=600)
def get_daily_stats():
    conn = init_connection()
    return pd.read_sql("""
        SELECT * FROM daily_stats 
        ORDER BY date DESC 
        LIMIT 7
    """, conn)

@st.cache_data(ttl=600)
def get_merchant_stats():
    conn = init_connection()
    return pd.read_sql("""
        SELECT merchant, COUNT(*) AS total_transactions,
               SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) AS fraud_transactions,
               ROUND((SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END)::decimal / COUNT(*)) * 100, 2) AS fraud_rate
        FROM recent_transactions
        GROUP BY merchant
        ORDER BY fraud_rate DESC, total_transactions DESC
        LIMIT 10
    """, conn)

# Header
st.title("🕵️ Fraud Detection Dashboard")
st.subheader("Surveillance en temps réel des transactions")

try:
    # Statistiques quotidiennes
    stats = get_daily_stats()
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Transactions (24h)", stats.iloc[0]["total_transactions"])
    with col2:
        st.metric("Fraudes détectées", stats.iloc[0]["fraud_count"])
    with col3:
        st.metric("Taux de fraude", f"{stats.iloc[0]['fraud_rate']:.2f}%")
    with col4:
        st.metric("Montant total", f"${stats.iloc[0]['total_amount']:,.2f}")
    with col5:
        avg_fraud_prob = stats["fraud_rate"].mean()
        st.metric("Probabilité moyenne de fraude", f"{avg_fraud_prob:.2f}%")

    # Graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Evolution du taux de fraude")
        fig = px.line(stats, x="date", y="fraud_rate", 
                     title="Taux de fraude sur 7 jours")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Montant des transactions")
        fig = px.bar(stats, x="date", y="total_amount",
                    title="Montant total des transactions par jour")
        st.plotly_chart(fig, use_container_width=True)

# Statistiques par marchand
    st.subheader("Top 10 des marchands par taux de fraude")
    merchants = get_merchant_stats()
    st.dataframe(merchants)

    # Dernières transactions avec alerte
    st.subheader("Dernières transactions")
    transactions = get_recent_transactions()
    
    # Alerte visuelle en cas de fraude détectée dans les dernières transactions
    if transactions["is_fraud"].sum() > 0:
        st.error("⚠️ Fraude détectée dans les dernières transactions !")
    
    # Filtres pour l’exploration des transactions
    amount_filter = st.slider("Montant minimum de la transaction", min_value=0, max_value=int(transactions["amt"].max()), value=0)
    fraud_filter = st.checkbox("Afficher seulement les transactions frauduleuses")
    filtered_transactions = transactions[transactions["amt"] >= amount_filter]
    
    if fraud_filter:
        filtered_transactions = filtered_transactions[filtered_transactions["is_fraud"]]
    
    st.dataframe(
        filtered_transactions[["trans_date_trans_time", "merchant", "amt", "city", 
                               "is_fraud", "fraud_probability"]],
        use_container_width=True
    )

except Exception as e:
    st.error(f"Erreur lors de la récupération des données: {str(e)}")
    st.warning("Assurez-vous que la connexion à la base de données est correcte et que les tables existent.")