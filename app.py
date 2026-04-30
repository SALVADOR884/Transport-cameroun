import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="Transport Cameroun - Collecte & Analyse",
    page_initial_sidebar_state="expanded",
    layout="wide"
)

# Style CSS personnalisé
st.markdown("""
    <style>
    .main-header {
        background-color: #2E86C1;
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton > button {
        background-color: #F39C12;
        color: white;
        font-weight: bold;
    }
    .css-1v0mbdj e115fcil1 {
        background-color: #f0f2f6;
    }
    footer {
        visibility: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# Titre
st.markdown('<div class="main-header"><h1>🚐 Collecte & Analyse - Transports Cameroun</h1><p>Agences, destinations et tarifs</p></div>', unsafe_allow_html=True)

# Initialisation de la session (stockage des données en mémoire)
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Agence", "Destination", "Tarif (FCFA)", "Date de saisie"])

# ------------------- SECTION SAISIE -------------------
with st.expander("➕ Ajouter une nouvelle course", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        agence = st.selectbox("Agence", ["Touristique Express", "Cameroun Voyages", "Reliance", "Voyageur Cameroun", "Général Express"])
    with col2:
        destination = st.selectbox("Destination", ["Yaoundé", "Douala", "Bafoussam", "Garoua", "Maroua", "Limbé", "Kribi", "Foumban", "Ngaoundéré"])
    with col3:
        tarif = st.number_input("Tarif (FCFA)", min_value=500, max_value=50000, step=500, value=5000)
    
    if st.button("📥 Enregistrer la course"):
        new_row = pd.DataFrame({
            "Agence": [agence],
            "Destination": [destination],
            "Tarif (FCFA)": [tarif],
            "Date de saisie": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        })
        st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)
        st.success("✅ Course enregistrée avec succès !")
        st.balloons()

# ------------------- SECTION VISUALISATION DES DONNÉES -------------------
st.markdown("---")
st.subheader("📋 Données collectées")
if not st.session_state.data.empty:
    st.dataframe(st.session_state.data, use_container_width=True)
    
    # Exporter en CSV
    csv = st.session_state.data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📎 Télécharger les données (CSV)",
        data=csv,
        file_name="transports_cameroun.csv",
        mime="text/csv",
    )
else:
    st.info("Aucune donnée pour le moment. Utilisez le formulaire ci-dessus pour ajouter des courses.")

# ------------------- SECTION ANALYSE DESCRIPTIVE -------------------
st.markdown("---")
st.subheader("📊 Analyse descriptive")

if not st.session_state.data.empty:
    # Métriques globales
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🏢 Nombre total de courses", len(st.session_state.data))
    with col2:
        st.metric("💰 Tarif moyen", f"{st.session_state.data['Tarif (FCFA)'].mean():,.0f} FCFA")
    with col3:
        st.metric("💵 Tarif max", f"{st.session_state.data['Tarif (FCFA)'].max():,.0f} FCFA")

    # Analyse par agence
    st.subheader("📍 Tarif moyen par agence")
    moy_agence = st.session_state.data.groupby("Agence")["Tarif (FCFA)"].mean().sort_values(ascending=False)
    st.bar_chart(moy_agence)

    # Analyse par destination
    st.subheader("🗺️ Tarif moyen par destination")
    moy_dest = st.session_state.data.groupby("Destination")["Tarif (FCFA)"].mean().sort_values(ascending=False)
    st.bar_chart(moy_dest)

    # Histogramme des tarifs
    st.subheader("📈 Distribution des tarifs")
    fig, ax = plt.subplots()
    ax.hist(st.session_state.data["Tarif (FCFA)"], bins=10, color='#2E86C1', edgecolor='black')
    ax.set_xlabel("Tarif (FCFA)")
    ax.set_ylabel("Fréquence")
    st.pyplot(fig)

    # Tableau croisé
    st.subheader("🧮 Tableau croisé : Agence vs Destination (tarif moyen)")
    pivot = pd.pivot_table(st.session_state.data, values="Tarif (FCFA)", index="Agence", columns="Destination", aggfunc="mean", fill_value=0)
    st.dataframe(pivot.style.format("{:.0f}"), use_container_width=True)
    
else:
    st.warning("Ajoutez des données pour voir les analyses.")

# Pied de page
st.markdown("---")
st.caption("Application de collecte et analyse descriptive - Transports Cameroun | Projet étudiant")