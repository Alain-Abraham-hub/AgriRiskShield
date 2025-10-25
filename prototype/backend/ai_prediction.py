# ==================================================
# 📈 Oilseed Price Forecasting (Date vs Price)
# ==================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import os

def predict_prices(future_days=30):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, '..', 'data', 'soybean_prices.csv')
    df = pd.read_csv(data_path)
    df.columns = df.columns.str.lower()
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    df = df.dropna()
    df['days'] = (df['date'] - df['date'].min()).dt.days

    X = df[['days']]
    y = df['price']
    model = LinearRegression()
    model.fit(X, y)

    last_day = df['days'].max()
    future_X = np.arange(last_day + 1, last_day + future_days + 1).reshape(-1, 1)
    future_dates = pd.date_range(start=df['date'].max(), periods=future_days + 1)[1:]
    future_prices = model.predict(future_X)

    forecast = pd.DataFrame({'date': future_dates, 'forecasted_price': future_prices})

    # Optional: Save a plot for dashboard
    plt.figure(figsize=(10, 5))
    plt.plot(df['date'], df['price'], label='Actual Price', color='blue')
    plt.plot(future_dates, future_prices, label='Predicted Price', color='orange', linestyle='--')
    plt.xlabel('Date')
    plt.ylabel('Price (₹/quintal)')
    plt.title('Oilseed Price Forecast (Prototype)')
    plt.legend()
    plt.tight_layout()

    # Save the plot as an image for the dashboard to display
    plot_path = os.path.join(script_dir, '..', 'frontend', 'price_forecast.png')
    plt.savefig(plot_path)
    plt.close()

    return forecast, plot_path

if __name__ == "__main__":
    forecast, plot_path = predict_prices(30)
    print("\n📅 Future 5-day Forecast Preview:\n")
    print(forecast.head())