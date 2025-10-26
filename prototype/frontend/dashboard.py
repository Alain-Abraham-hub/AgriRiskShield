import sys
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))  # points to 'prototype'

from backend.riskpool import RiskPool
from backend.ai_prediction import predict_prices
from blockchain.ledger import Blockchain
import pandas as pd
import streamlit as st
import streamlit as st
from pathlib import Path
import sys
import pandas as pd

# Ensure the project root is on sys.path so sibling packages can be imported
sys.path.append(str(Path(__file__).resolve().parents[1]))

from backend.ai_prediction import predict_prices
from blockchain.ledger import Blockchain
from backend.riskpool import RiskPool  # New import for Smart Community Risk Pool

# ================================
# 🌾 AgriRiskShield Dashboard
# ================================
st.title("🌾 AgriRiskShield: Oilseed Price Dashboard")

# ================================
# AI-based Price Forecast
# ================================
forecast, plot_path = predict_prices(future_days=30)

st.subheader("📈 Price Forecast (Next 30 Days)")
st.line_chart(forecast.set_index('date')['forecasted_price'])

st.subheader("🗓️ Forecast Table")
st.dataframe(forecast)

st.image(plot_path, caption="AI-based Price Forecast Plot", use_container_width=True)

# ================================
# Blockchain Ledger Simulation
# ================================
st.subheader("🔗 Blockchain Ledger for Forward Contracts")

ledger = Blockchain()

# Sample contracts
ledger.add_block({"Farmer": "Ravi", "Crop": "Soybean", "Price": 5200, "Quantity": "10T"})
ledger.add_block({"Farmer": "Meena", "Crop": "Groundnut", "Price": 5100, "Quantity": "5T"})
ledger.add_block({"Farmer": "Suresh", "Crop": "Mustard", "Price": 4950, "Quantity": "8T"})

ledger_data = pd.DataFrame(ledger.to_dict())
st.dataframe(ledger_data)

# ================================
# 🌐 Smart Community Risk Pool (DeFi for Farmers)
# ================================
st.subheader("🌾 Smart Community Risk Pool (DeFi)")

# Initialize risk pool (for prototype, not persistent)
risk_pool = RiskPool()

# User inputs
login_type = st.selectbox("Login as", ["Farmer", "FPO", "Retailer"])
name = st.text_input("Your Name")
contribution = st.number_input("Contribution Amount (tokens)", min_value=0)

if st.button("Join Pool"):
    if name and contribution > 0:
        risk_pool.join_pool(login_type, name, contribution)
        st.success(f"{name} joined the pool with {contribution} tokens!")
    else:
        st.error("Please enter a name and a positive contribution.")

# Market evaluation (simulate with AI forecast)
if st.button("Evaluate Market"):
    # For demo, use last predicted price as current market price
    current_price = forecast['forecasted_price'].iloc[-1]
    threshold = st.slider("Payout Threshold Price", 20, 10000, 5000)  # Adjust range for oilseeds
    payout = risk_pool.evaluate_market(current_price, threshold)
    if payout > 0:
        st.warning(f"Price drop detected! Each member receives {payout} tokens.")
    else:
        st.info("No price drop. Pool is stable.")

# Display pool summary
summary = risk_pool.get_pool_summary()
st.write(f"**Total Balance:** {summary['total_balance']} tokens")
st.write(f"**Total Members:** {summary['total_members']}")
st.dataframe(summary["members"])

# Dummy price trend graph for visualization
st.line_chart({"Price Trend": [forecast['forecasted_price'].iloc[-6], 
                               forecast['forecasted_price'].iloc[-5],
                               forecast['forecasted_price'].iloc[-4],
                               forecast['forecasted_price'].iloc[-3],
                               forecast['forecasted_price'].iloc[-2],
                               forecast['forecasted_price'].iloc[-1]]})