"""
Limit Order Book core logic for 3D Liquidity Vacuum & Flash Crash Simulator
"""
import numpy as np
from collections import defaultdict, deque

class Order:
    def __init__(self, order_id, side, price, size, agent_id, timestamp):
        self.order_id = order_id
        self.side = side  # 'bid' or 'ask'
        self.price = price
        self.size = size
        self.agent_id = agent_id
        self.timestamp = timestamp

class LimitOrderBook:
    def __init__(self, price_grid):
        self.price_grid = price_grid  # np.array of price levels
        self.bids = defaultdict(deque)  # price: deque of Order
        self.asks = defaultdict(deque)
        self.order_map = {}  # order_id: Order
        self.last_order_id = 0

    def add_order(self, side, price, size, agent_id, timestamp):
        self.last_order_id += 1
        order = Order(self.last_order_id, side, price, size, agent_id, timestamp)
        if side == 'bid':
            self.bids[price].append(order)
        else:
            self.asks[price].append(order)
        self.order_map[self.last_order_id] = order
        return self.last_order_id

    def cancel_order(self, order_id):
        order = self.order_map.get(order_id)
        if not order:
            return False
        book = self.bids if order.side == 'bid' else self.asks
        orders_at_price = book[order.price]
        for i, o in enumerate(orders_at_price):
            if o.order_id == order_id:
                del orders_at_price[i]
                break
        del self.order_map[order_id]
        return True

    def match_orders(self):
        # Simple matching: match best bid/ask until no overlap
        trades = []
        bid_prices = sorted(self.bids.keys(), reverse=True)
        ask_prices = sorted(self.asks.keys())
        while bid_prices and ask_prices and bid_prices[0] >= ask_prices[0]:
            best_bid = bid_prices[0]
            best_ask = ask_prices[0]
            # Skip if deque is empty (can happen after order removal)
            if not self.bids[best_bid] or not self.asks[best_ask]:
                # Remove empty price levels and update price lists
                if not self.bids[best_bid]:
                    del self.bids[best_bid]
                if not self.asks[best_ask]:
                    del self.asks[best_ask]
                bid_prices = sorted(self.bids.keys(), reverse=True)
                ask_prices = sorted(self.asks.keys())
                continue
            bid_order = self.bids[best_bid][0]
            ask_order = self.asks[best_ask][0]
            trade_size = min(bid_order.size, ask_order.size)
            trades.append((bid_order.price, trade_size, bid_order.agent_id, ask_order.agent_id))
            bid_order.size -= trade_size
            ask_order.size -= trade_size
            if bid_order.size == 0:
                self.bids[best_bid].popleft()
                if not self.bids[best_bid]:
                    del self.bids[best_bid]
                del self.order_map[bid_order.order_id]
            if ask_order.size == 0:
                self.asks[best_ask].popleft()
                if not self.asks[best_ask]:
                    del self.asks[best_ask]
                del self.order_map[ask_order.order_id]
            bid_prices = sorted(self.bids.keys(), reverse=True)
            ask_prices = sorted(self.asks.keys())
        return trades

    def get_depth(self):
        # Returns price, bid_depth, ask_depth arrays
        bid_depth = np.array([sum(o.size for o in self.bids[p]) for p in self.price_grid])
        ask_depth = np.array([sum(o.size for o in self.asks[p]) for p in self.price_grid])
        return self.price_grid, bid_depth, ask_depth

    def best_bid(self):
        return max(self.bids.keys()) if self.bids else None

    def best_ask(self):
        return min(self.asks.keys()) if self.asks else None
