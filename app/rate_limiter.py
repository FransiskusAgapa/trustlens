import time

class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.clients = {}
    
    def is_allowed(self, token_ip):
        if token_ip not in self.clients:
            self.clients[token_ip] = {
                "tokens": self.capacity,
                "last_refill": time.time()
            }

        client = self.clients[token_ip]
        current_time = time.time()
        elapsed = current_time - client["last_refill"]
        client["tokens"] = min(self.capacity, client["tokens"] + elapsed * self.refill_rate)
        client["last_refill"] = current_time

        if client["tokens"] >= 1:
            client["tokens"] -= 1
            return True
        return False
