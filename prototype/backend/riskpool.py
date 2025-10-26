# ======================================================
# 🌾 Smart Community Risk Pool (DeFi for Farmers)
# ------------------------------------------------------
# Simulates a decentralized risk-pooling mechanism where
# farmers, FPOs, and retailers contribute virtual tokens
# into a shared pool. If prices drop below a threshold,
# automated payouts are recorded on the blockchain ledger.
# ======================================================

import time
from pathlib import Path
import sys

# Import the ledger package using the package-qualified name when running as a module
# but fall back to adding the prototype/ folder to sys.path so the file can be
# executed directly for quick demos.
try:
    from prototype.blockchain.ledger import Block, Blockchain
except ModuleNotFoundError:
    sys.path.append(str(Path(__file__).resolve().parents[1]))
    from blockchain.ledger import Block, Blockchain


class RiskPool:
    def __init__(self):
        """Initialize the community pool and blockchain ledger."""
        self.pool_balance = 0
        self.members = []  # List of dicts: {name, user_type, stake, balance}
        self.blockchain = Blockchain()

    def join_pool(self, user_type: str, name: str, amount: float):
        """Add a new participant to the pool."""
        if amount <= 0:
            raise ValueError("Contribution amount must be greater than zero.")

        member = {
            "user_type": user_type,
            "name": name,
            "stake": amount,
            "balance": amount,
            "joined_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        }

        self.members.append(member)
        self.pool_balance += amount

        # Record transaction in blockchain
        self.blockchain.add_block(f"{name} ({user_type}) contributed {amount} tokens.")
        print(f"[+] {name} joined the pool with {amount} tokens.")

    def evaluate_market(self, current_price: float, threshold: float):
        """
        Evaluate market conditions and trigger payouts if prices fall below threshold.
        This simulates automated smart contract behavior.
        """
        print(f"Evaluating market... Current Price = {current_price}, Threshold = {threshold}")

        if current_price < threshold and len(self.members) > 0:
            price_gap = threshold - current_price
            compensation_per_member = round(price_gap * 10, 2)  # Dummy payout formula

            for member in self.members:
                member["balance"] += compensation_per_member
                self.pool_balance -= compensation_per_member
                self.blockchain.add_block(
                    f"Payout of {compensation_per_member} tokens released to {member['name']} ({member['user_type']})"
                )

            print(f"[!] Price drop detected. Compensation distributed to all members.")
            return compensation_per_member
        else:
            print("[✓] No price drop. Pool remains stable.")
            return 0

    def get_pool_summary(self):
        """Return summary of pool state."""
        return {
            "total_balance": round(self.pool_balance, 2),
            "total_members": len(self.members),
            "members": self.members,
        }


# ======================================================
# 🧪 Test Run (Standalone Demo)
# ======================================================
if __name__ == "__main__":
    pool = RiskPool()

    # Members joining pool
    pool.join_pool("Farmer", "Ramesh", 100)
    pool.join_pool("FPO", "AgriCoop", 300)
    pool.join_pool("Retailer", "FreshMart", 200)

    # Evaluate market with price drop scenario
    pool.evaluate_market(current_price=35, threshold=40)

    # Print pool summary
    print("\n🏦 Pool Summary:")
    print(pool.get_pool_summary())