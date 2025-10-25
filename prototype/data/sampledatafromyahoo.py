import yfinance as yf
import pandas as pd
import os

# Create data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# Download soybean futures (symbol: ZS=F)
data = yf.download("ZS=F", start="2023-01-01", end="2024-12-31")

# Select relevant columns
df = data[['Close']].reset_index()
df = df.rename(columns={'Date': 'Date', 'Close': 'Price'})

# Save to CSV for use in prediction module
df.to_csv('data/soybean_prices.csv', index=False)

print("✅ Download complete! Saved as data/soybean_prices.csv")
print(df.head())