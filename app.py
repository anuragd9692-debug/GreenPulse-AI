
import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

st.set_page_config(
    page_title="GreenPulse AI",
    page_icon="🌱",
    layout="wide"
)

st.title("GreenPulse AI")
st.subheader("Intelligent Energy Optimization & Carbon Reduction Assistant")

st.write(
    "GreenPulse AI analyzes energy consumption, identifies "
    "high-consumption appliances and provides sustainability recommendations."
)

# Create dataset
data = {
    "Appliance": [
        "Air Conditioner",
        "Refrigerator",
        "Washing Machine",
        "Television",
        "Fans",
        "Lights",
        "Computer"
    ],
    "Hours_Per_Day": [6, 24, 1.5, 4, 8, 5, 6],
    "Power_Watts": [1500, 200, 500, 120, 75, 60, 200]
}

df = pd.DataFrame(data)

# Energy calculations
df["Daily_Energy_kWh"] = (
    df["Hours_Per_Day"] * df["Power_Watts"] / 1000
)

df["Monthly_Energy_kWh"] = (
    df["Daily_Energy_kWh"] * 30
)

ELECTRICITY_RATE = 7.5
EMISSION_FACTOR = 0.7

df["Monthly_Cost_INR"] = (
    df["Monthly_Energy_kWh"] * ELECTRICITY_RATE
)

df["Monthly_CO2_kg"] = (
    df["Monthly_Energy_kWh"] * EMISSION_FACTOR
)

# Machine learning clustering
features = df[
    ["Hours_Per_Day", "Power_Watts", "Daily_Energy_kWh"]
]

scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

kmeans = KMeans(
    n_clusters=3,
    random_state=42,
    n_init=10
)

df["Cluster"] = kmeans.fit_predict(scaled_features)

cluster_energy = (
    df.groupby("Cluster")["Daily_Energy_kWh"]
    .mean()
    .sort_values()
)

level_mapping = {
    cluster_energy.index[0]: "Low",
    cluster_energy.index[1]: "Medium",
    cluster_energy.index[2]: "High"
}

df["Consumption_Level"] = df["Cluster"].map(level_mapping)

# Recommendations
def recommendation(appliance):
    recommendations = {
        "Air Conditioner":
        "Reduce unnecessary AC usage, maintain an efficient temperature setting and keep doors/windows closed.",
        "Refrigerator":
        "Avoid unnecessary door opening and check the door seal regularly.",
        "Washing Machine":
        "Use full loads and avoid unnecessary washing cycles.",
        "Television":
        "Switch off the television completely when it is not being used.",
        "Fans":
        "Switch off fans in unoccupied rooms.",
        "Lights":
        "Switch off unused lights and consider energy-efficient LED lighting.",
        "Computer":
        "Enable sleep or power-saving mode when the computer is not actively being used."
    }

    return recommendations.get(
        appliance,
        "Consider reducing unnecessary energy usage."
    )

df["AI_Recommendation"] = df["Appliance"].apply(recommendation)

# Summary
total_daily = df["Daily_Energy_kWh"].sum()
total_monthly = df["Monthly_Energy_kWh"].sum()
total_cost = df["Monthly_Cost_INR"].sum()
total_co2 = df["Monthly_CO2_kg"].sum()

top = df.loc[df["Daily_Energy_kWh"].idxmax()]

# Dashboard
st.markdown("---")
st.header("Energy Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Daily Energy", f"{total_daily:.2f} kWh")

with col2:
    st.metric("Monthly Energy", f"{total_monthly:.2f} kWh")

with col3:
    st.metric("Estimated Cost", f"₹{total_cost:.2f}")

with col4:
    st.metric("Estimated CO₂", f"{total_co2:.2f} kg")

st.markdown("---")
st.header("Highest Energy Consumer")

st.write(f"### {top['Appliance']}")
st.write(f"Daily consumption: **{top['Daily_Energy_kWh']:.2f} kWh**")
st.write(f"Monthly consumption: **{top['Monthly_Energy_kWh']:.2f} kWh**")
st.write(f"Consumption level: **{top['Consumption_Level']}**")

st.markdown("---")
st.header("GreenPulse AI Recommendation")
st.info(top["AI_Recommendation"])

st.markdown("---")
st.header("⚡ Daily Energy Consumption")

chart_data = df.set_index("Appliance")["Daily_Energy_kWh"]
st.bar_chart(chart_data)

st.markdown("---")
st.header("Detailed Analysis")

display_columns = [
    "Appliance",
    "Hours_Per_Day",
    "Power_Watts",
    "Daily_Energy_kWh",
    "Monthly_Energy_kWh",
    "Monthly_Cost_INR",
    "Monthly_CO2_kg",
    "Consumption_Level"
]

st.dataframe(
    df[display_columns],
    use_container_width=True
)

st.markdown("---")
st.header("Ask GreenPulse AI")

question = st.text_input(
    "Ask a sustainability question:",
    placeholder="How can I reduce my electricity consumption?"
)

if st.button("Get Recommendation"):

    q = question.lower()

    if "ac" in q or "air conditioner" in q:
        answer = recommendation("Air Conditioner")

    elif "light" in q:
        answer = recommendation("Lights")

    elif "refrigerator" in q:
        answer = recommendation("Refrigerator")

    elif "washing" in q:
        answer = recommendation("Washing Machine")

    elif "computer" in q:
        answer = recommendation("Computer")

    elif "fan" in q:
        answer = recommendation("Fans")

    elif "television" in q or "tv" in q:
        answer = recommendation("Television")

    else:
        answer = (
            f"Your highest energy consumer is {top['Appliance']}. "
            f"Focus on reducing unnecessary usage of this appliance first."
        )

    st.success(answer)

st.markdown("---")
st.caption(
    "GreenPulse AI | AI for Sustainability | Prototype Project"
)
