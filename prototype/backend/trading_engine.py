# ==================================================
# 🏦 Virtual Trading / Forward Contract Simulation
# ==================================================
from datetime import datetime
import pandas as pd

class Contract:
    def __init__(self, farmer, quantity, locked_price, date_created=None):
        self.farmer = farmer
        self.quantity = quantity
        self.locked_price = locked_price
        self.date_created = date_created if date_created else datetime.now()

class TradingEngine:
    def __init__(self):
        self.contracts = []

    def create_contract(self, farmer, quantity, locked_price):
        contract = Contract(farmer, quantity, locked_price)
        self.contracts.append(contract)
        return contract

    def calculate_pnl(self, market_price):
        """
        Compute profit/loss for all contracts given the current market price
        """
        pnl = []
        for c in self.contracts:
            profit = (market_price - c.locked_price) * c.quantity
            pnl.append({'farmer': c.farmer, 'quantity': c.quantity,
                        'locked_price': c.locked_price, 'market_price': market_price,
                        'profit_loss': profit})
        return pd.DataFrame(pnl)

# ===== Example usage =====
if __name__ == "__main__":
    engine = TradingEngine()
    engine.create_contract("Farmer A", 100, 5200)
    engine.create_contract("Farmer B", 50, 5150)

    # Suppose current market price is 5300
    pnl = engine.calculate_pnl(5300)
    print(pnl)