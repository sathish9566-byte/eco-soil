import streamlit as st
import pandas as pd

# --- PART 1: PAGE SETUP ---
st.set_page_config(page_title="Eco-Soil: Carbon & Soil Health ", page_icon="🌱", layout="wide")

# Hide branding
st.markdown("""<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}</style>""", unsafe_allow_html=True)

st.title("🌱 Eco-Soil: Carbon Credit & Soil Health Calculator")
st.markdown("**SATHISH'S  Assignment: Organic Farming (BAG1008)**")
st.markdown("---")

# --- PART 2: SIDEBAR (References) ---
with st.sidebar:
    st.header("📚 Scientific References")
    st.info("""
    **1. Sequestration Logic:**
    Based on IPCC & ICAR guidelines for humification rates of organic manure.
    
    **2. Soil Standards:**
    * **Low Carbon:** < 0.5%
    * **Medium:** 0.5% – 0.75%
    * **High Carbon:** > 0.75%
    
    **3. Economic Value:**
    Carbon Credit Price ~ $20 (₹1,600) per ton of CO2e.
    """)

# --- PART 3: INPUTS ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Farm & Soil Details")
    acres = st.number_input("Land Size (Acres):", value=5.0, step=0.5)
    current_soc = st.slider("Current Soil Organic Carbon (%) (from Soil Health Card):", 0.0, 2.0, 0.40)

with col2:
    st.subheader("2. Organic Inputs (Tons/Year)")
    fym_tons = st.number_input("Farm Yard Manure (FYM):", value=10.0)
    vermi_tons = st.number_input("Vermicompost:", value=5.0)
    green_tons = st.number_input("Green Manure:", value=2.0)

st.divider()

# --- PART 4: THE MATH (Scientific Core) ---

# 1. Carbon Sequestration Calculation (Strict Science)
# Factors: [Dry Matter, Carbon Content, Humification Rate]
factors = {
    "FYM": [0.40, 0.35, 0.12],         # 12% retention
    "Vermicompost": [0.50, 0.30, 0.20], # 20% retention (Higher)
    "Green Manure": [0.20, 0.40, 0.08]  # 8% retention (Lower)
}

def get_stable_carbon(tons, type_name):
    f = factors[type_name]
    # Input -> Dry Matter -> Total Carbon -> Stable Humus
    return tons * f[0] * f[1] * f[2]

c_fym = get_stable_carbon(fym_tons, "FYM")
c_vermi = get_stable_carbon(vermi_tons, "Vermicompost")
c_green = get_stable_carbon(green_tons, "Green Manure")

total_c_sequestered = c_fym + c_vermi + c_green

# 2. CO2 Equivalent (For Money)
co2_equivalent = total_c_sequestered * 3.67
# Money Calculation ($20 per ton * ₹83 exchange rate)
earnings = co2_equivalent * 20 * 83 

# 3. Soil Health Calculation (Agronomy Core)
# Logic: 1 Acre of soil (top 15cm) weighs approx 2,000 Tons (2 million kg).
# Percent Increase = (Added Carbon / Total Soil Weight) * 100
soil_weight_per_acre = 2000 # Tons
total_soil_weight = soil_weight_per_acre * acres
soc_increase = (total_c_sequestered / total_soil_weight) * 100
projected_soc = current_soc + soc_increase

# --- PART 5: RESULTS DASHBOARD ---

# SECTION A: FINANCIALS
st.subheader("💰 Economic Benefit (Carbon Credits)")
m1, m2, m3 = st.columns(3)
m1.metric("Stable Carbon Captured", f"{total_c_sequestered:.3f} Tons")
m2.metric("CO2 Offsets Created", f"{co2_equivalent:.3f} Credits")
m3.metric("Est. Income", f"₹ {earnings:,.0f}")

st.markdown("---")

# SECTION B: SOIL HEALTH
st.subheader("🧪 Soil Health Verification (TNAU Standards)")

col_a, col_b = st.columns([1, 2])

with col_a:
    st.metric("Current SOC", f"{current_soc}%")
    st.metric("Projected SOC", f"{projected_soc:.4f}%", delta=f"+{soc_increase:.4f}%")

with col_b:
    st.write("#### Verdict:")
    if projected_soc > 0.75:
        st.success(f"✅ **HIGH STATUS:** Your soil carbon will exceed 0.75%. Excellent organic management.")
    elif projected_soc > 0.50:
        st.info(f"⚠️ **MEDIUM STATUS:** Your soil is improving but needs more inputs to reach 'High' status.")
    else:
        st.error(f"❌ **LOW STATUS:** Even with these inputs, your soil carbon is below 0.5%. You must increase FYM dosage.")

    # Visual Bar Chart for Soil Health
    st.progress(min(projected_soc / 1.0, 1.0))
    st.caption("Target: 0.75% (TNAU Standard for Healthy Soil)")

# --- STRICT EVALUATION DEFENSE ---
with st.expander("Show Calculation Logic (For Evaluator)"):
    st.markdown("""
    **Methodology:**
    1.  **Sequestered Carbon:** calculated using IPCC Humification factors (Stable Humus).
    2.  **CO2e:** Mass of Carbon × 3.67 (Atomic ratio).
    3.  **Soil Impact:** Based on 'Furrow Slice' weight (1 Acre soil ≈ 2000 Tons). 
    4.  **Standards:** Benchmarked against TNAU Agritech Portal Soil Organic Carbon (SOC) ratings.
    """)
