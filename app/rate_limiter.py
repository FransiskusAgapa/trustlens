import time

# evict clients idle longer than this many seconds
EVICTION_WINDOW = 300 # 5 minutes

class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.clients = {}

    def _evict_idle(self, current_time):
        # remove entries that haven't been seen in EVICTION_WINDOW seconds
        # this prevents the dict from growing forever with spoofed IPs
        idle = [ ip for ip, data in self.clients.items()
                    if current_time - data["last_refill"] > EVICTION_WINDOW ]
        for ip in idle:
            del self.clients[ip]
            
    def is_allowed(self, request):
        forwarded_for = request.headers.get("X-Forwarded-For")
        client_ip = forwarded_for.split(",")[0].strip() if forwarded_for else request.client.host

        current_time = time.time()

        if client_ip not in self.clients:
            self.clients[client_ip] = {
                "tokens": self.capacity,
                "last_refill": current_time
            }

        client = self.clients[client_ip]
        elapsed = current_time - client["last_refill"]
        client["tokens"] = min(self.capacity, client["tokens"] + elapsed * self.refill_rate)
        client["last_refill"] = current_time
        self._evict_idle(current_time)

        if client["tokens"] >= 1:
            client["tokens"] -= 1
            return True
        return False