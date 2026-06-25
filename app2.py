import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration de la page
st.set_page_config(page_title="Lacto-Sim - BIOFILMS", layout="wide")

# ==========================================
# CHARTE GRAPHIQUE POLYTECH (CSS INJECTION)
# ==========================================
polytech_blue = "#009EE0"
polytech_grey = "#4A4A4A"

st.markdown(f"""
    <style>
    /* Titres aux couleurs de l'école */
    h1, h2, h3, h4 {{
        color: {polytech_blue} !important;
        font-family: 'Arial', sans-serif;
    }}
    /* Style de la barre latérale */
    [data-testid="stSidebar"] {{
        border-right: 3px solid {polytech_blue};
    }}
    /* Mise en évidence des valeurs des métriques */
    [data-testid="stMetricValue"] {{
        color: {polytech_blue} !important;
    }}
    /* Séparateurs personnalisés */
    hr {{
        border-top: 2px solid {polytech_blue};
    }}
    /* Ajustement de l'alignement de l'image (logo) vers la droite */
    [data-testid="stImage"] {{
        display: flex;
        justify-content: flex-end;
        align-items: center;
        margin-top: 10px;
    }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# EN-TÊTE : TITRE ET LOGO (Haut de page)
# ==========================================
# Création de deux colonnes asymétriques pour le titre et le logo
col_title, col_logo = st.columns([4, 1.5])

with col_title:
    st.title("🧀 BIOFILMS — Lacto-Sim v2.0")
    st.markdown("### Outil de Pilotage de Bioconversion & Modélisation de Biomatériaux")

with col_logo:
    # Utilisation du fichier local importé sur JupyterHub (Taille corrigée)
    st.image(r"C:\Users\chloe\OneDrive\Bureau\hackaton\logo_polytech.png", width=2000)
    st.markdown("---")

# ==========================================
# SECTION 1 : LOGISTIQUE & ÉCONOMIE CIRCULAIRE
# ==========================================
st.sidebar.header("⚙️ 1. Paramètres de Production")
vol_lactoserum = st.sidebar.number_input("Volume de lactosérum du jour (Litres)", min_value=100, max_value=50000, value=5000, step=100)
valorisation_permeat = st.sidebar.radio("Valorisation du Perméat", ["Méthanisation (Biogaz)", "Fermentation (PLA)"])

# Modèle économique simplifié
poids_plastique_kg = vol_lactoserum / 100  # Règle : 100L = 1kg de protéine filmogène
nb_fromages = poids_plastique_kg * 350
eau_vache = vol_lactoserum * 0.93

st.subheader("♻️ Bilan d'Économie Circulaire (Fromagerie in-situ)")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Bioplastique produit", f"{poids_plastique_kg:.1f} kg")
col2.metric("Meules emballées", f"{int(nb_fromages)} unités")
col3.metric("Eau de Vache (NEP)", f"{int(eau_vache)} Litres")

if valorisation_permeat == "Méthanisation (Biogaz)":
    col4.metric("Énergie récupérée", "Autonomie Thermique")
else:
    col4.metric("Co-produit généré", "Acide Lactique (PLA)")

st.markdown("---")

# ==========================================
# SECTION 2 : FORMULATION & MODÉLISATION (R&D)
# ==========================================
st.subheader("🔬 Modélisation des Propriétés du Film")

col_params, col_results = st.columns([1, 2])

with col_params:
    st.markdown("**Ajustement de la Formulation**")
    materiau_cible = st.selectbox("Matériau de référence", ["Lactosérum (BIOFILMS)", "Chitosane (Référence)"])

    wpi = st.slider("Concentration (Protéine/Polysaccharide % p/v)", 5.0, 15.0, 10.0, step=0.5)
    glycerol = st.slider("Ratio de Plastifiant (Glycérol % p/p)", 10, 60, 35, step=1)
    temperature = st.slider("Température de procédé (°C)", 40, 100, 80, step=5)

# Modèles mathématiques (Régressions simulées)
if materiau_cible == "Lactosérum (BIOFILMS)":
    activation_thermique = 1.0 if temperature >= 75 else 0.2
    ts_val = ((wpi * 1.5) - (glycerol * 0.15)) * activation_thermique
    wvp_val = 0.5 + (glycerol * 0.03) - (wpi * 0.02)
    elongation = glycerol * 1.2
else:
    ts_val = (wpi * 2.0) - (glycerol * 0.10)
    wvp_val = 0.3 + (glycerol * 0.02) - (wpi * 0.01)
    elongation = glycerol * 0.8

# Sécurisation des valeurs minimales
ts_val = max(0.1, ts_val)
wvp_val = max(0.1, wvp_val)

with col_results:
    st.markdown(f"**Performances Physiques estimées pour : {materiau_cible}**")
    
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Résistance à la traction (TS)", f"{ts_val:.2f} MPa")
    kpi2.metric("Élongation à la rupture", f"{elongation:.1f} %")
    kpi3.metric("Perméabilité (WVP)", f"{wvp_val:.2f} g.mm/m².j.kPa")
    
    # Diagnostic d'état
    if materiau_cible == "Lactosérum (BIOFILMS)" and temperature < 75:
        st.error("❌ Échec de la réticulation : La température est trop basse pour créer les ponts disulfures (-S-S-).")
    elif glycerol < 20:
        st.warning("⚠️ État critique : Film trop cassant (Manque de plastifiant).")
    elif ts_val < 1.0:
        st.warning("⚠️ État instable : Résistance mécanique insuffisante pour un emballage industriel.")
    else:
        st.success("✅ Formulation optimale : Matrice polymérique stable et souple.")

# ==========================================
# SECTION 3 : VISUALISATION DES DONNÉES (Seaborn)
# ==========================================
st.markdown("---")
st.subheader("📊 Analyse du compromis Résistance / Flexibilité")

# Génération d'un dataset simulé pour le graphique
gly_range = np.linspace(10, 60, 50)
ts_list = []
el_list = []

for g in gly_range:
    if materiau_cible == "Lactosérum (BIOFILMS)":
        ts = max(0.1, ((wpi * 1.5) - (g * 0.15)) * (1.0 if temperature >= 75 else 0.2))
        el = g * 1.2
    else:
        ts = max(0.1, (wpi * 2.0) - (g * 0.10))
        el = g * 0.8
    ts_list.append(ts)
    el_list.append(el)

df_sim = pd.DataFrame({
    'Glycérol (%)': gly_range,
    'Résistance TS (MPa)': ts_list,
    'Élongation (%)': el_list
})

# Création du graphique avec Seaborn et Matplotlib
fig, ax1 = plt.subplots(figsize=(10, 4))

sns.set_theme(style="whitegrid")
# Ligne de résistance (Bleu Polytech)
sns.lineplot(data=df_sim, x='Glycérol (%)', y='Résistance TS (MPa)', color=polytech_blue, ax=ax1, label='Résistance (TS)', linewidth=2.5)
ax1.set_ylabel('Résistance à la traction (MPa)', color=polytech_blue, fontweight='bold')
ax1.tick_params(axis='y', labelcolor=polytech_blue)

# Deuxième axe Y pour l'élongation (Gris foncé)
ax2 = ax1.twinx()
sns.lineplot(data=df_sim, x='Glycérol (%)', y='Élongation (%)', color=polytech_grey, ax=ax2, label='Élongation', linewidth=2.5)
ax2.set_ylabel('Élongation à la rupture (%)', color=polytech_grey, fontweight='bold')
ax2.tick_params(axis='y', labelcolor=polytech_grey)

plt.title("Le paradoxe du plastifiant : Évolution des propriétés mécaniques", pad=15, color=polytech_grey, fontweight='bold')
fig.tight_layout()

st.pyplot(fig)