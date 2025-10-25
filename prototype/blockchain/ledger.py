# ==================================================
# ⛓️ Blockchain Ledger for Virtual Forward Contracts
# ==================================================
import hashlib
import json
import time

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()

    def compute_hash(self):
        return hashlib.sha256(json.dumps(self.__dict__, sort_keys=True).encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.time(), {"message": "Genesis Block"}, "0")

    def add_block(self, data):
        previous_block = self.chain[-1]
        block = Block(len(self.chain), time.time(), data, previous_block.hash)
        self.chain.append(block)
        return block

    def to_dict(self):
        """Return blockchain as a list of dictionaries (for Streamlit display)"""
        blocks = []
        for block in self.chain:
            blocks.append({
                "Index": block.index,
                "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(block.timestamp)),
                "Data": json.dumps(block.data),
                "Hash": block.hash[:12] + "...",
                "Prev Hash": block.previous_hash[:12] + "..."
            })
        return blocks

# Test it directly
if __name__ == "__main__":
    bc = Blockchain()
    bc.add_block({"farmer": "A", "quantity": 100, "price": 5200})
    bc.add_block({"farmer": "B", "quantity": 50, "price": 5150})
    for block in bc.chain:
        print(vars(block))