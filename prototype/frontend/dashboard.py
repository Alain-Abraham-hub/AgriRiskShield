import streamlit as st
from pathlib import Path
import sys

# Ensure the project `prototype` root is on sys.path so sibling packages
# (like `backend` and `blockchain`) can be imported when running this file directly.
sys.path.append(str(Path(__file__).resolve().parents[1]))

from backend.ai_prediction import predict_prices
from blockchain.ledger import Blockchain
import pandas as pd

st.title("🌾 AgriRiskShield: Oilseed Price Dashboard")

forecast, plot_path = predict_prices(future_days=30)

st.subheader("📈 Price Forecast (Next 30 Days)")
st.line_chart(forecast.set_index('date')['forecasted_price'])

st.subheader("🗓️ Forecast Table")
st.dataframe(forecast)

st.image(plot_path, caption="AI-based Price Forecast Plot", use_container_width=True)

# ==================================================
# ⛓️ Blockchain Ledger Simulation
# ==================================================
st.subheader("🔗 Blockchain Ledger for Forward Contracts")

# Initialize blockchain
ledger = Blockchain()

# Add sample contracts
ledger.add_block({"Farmer": "Ravi", "Crop": "Soybean", "Price": 5200, "Quantity": "10T"})
ledger.add_block({"Farmer": "Meena", "Crop": "Groundnut", "Price": 5100, "Quantity": "5T"})
ledger.add_block({"Farmer": "Suresh", "Crop": "Mustard", "Price": 4950, "Quantity": "8T"})

# Convert to DataFrame for display
ledger_data = pd.DataFrame(ledger.to_dict())
st.dataframe(ledger_data)