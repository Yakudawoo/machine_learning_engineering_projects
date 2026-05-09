import random
import redis
import time
import json
from datetime import datetime

# --- Redis Configuration ---
HOSTNAME = "redis-10130.crce202.eu-west-3-1.ec2.redns.redis-cloud.com"
PORT = 10130
PASSWORD = "iL5hrgCcDSftFK0Ft08dqbk4sWl863PT"

r = redis.Redis(
    host=HOSTNAME,
    port=PORT,
    password=PASSWORD,
    decode_responses=True,
    socket_timeout=5,
)

# --- ShopNow Product Catalog ---
PRODUCTS = [
    "Wireless Earbuds",
    "Smartwatch",
    "Gaming Keyboard",
    "4K Monitor",
    "Portable Speaker",
    "Fitness Tracker",
    "Mechanical Mouse",
    "Bluetooth Headphones",
    "Power Bank",
    "Smart Home Hub"
]

USERS = [f"user:{i}" for i in range(100, 120)]

# --- Helper Function ---
def generate_sale():
    """Generate a random sale event and push it to Redis Stream."""
    product = random.choice(PRODUCTS)
    base_price = random.uniform(40, 800)
    
    # Apply random discount bias to simulate promotions
    discount = random.choice([0, 0, 0.05, 0.10, 0.15])  
    final_price = round(base_price * (1 - discount), 2)

    event = {
        "user": random.choice(USERS),
        "product": product,
        "value": f"{final_price}",
        "timestamp": datetime.utcnow().isoformat()
    }

    try:
        r.xadd("sales:stream", event)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 💸 New sale → {json.dumps(event)}")
    except redis.RedisError as e:
        print(f"❌ Redis error: {e}")
    return event


# --- Continuous Sale Simulation ---
if __name__ == "__main__":
    print("🚀 Starting ShopNow real-time sales stream... (Ctrl+C to stop)\n")
    while True:
        generate_sale()
        time.sleep(random.uniform(1, 2))  # random interval between 1–2 seconds
