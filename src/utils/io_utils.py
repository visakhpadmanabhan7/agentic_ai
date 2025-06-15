import os
from datetime import datetime

BASE_OUTPUT_DIR = os.path.join("outputs", "users")
os.makedirs(BASE_OUTPUT_DIR, exist_ok=True)

def generate_filename(method, user_name):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_user = user_name.strip().lower().replace(" ", "_")
    folder = os.path.join(BASE_OUTPUT_DIR, safe_user, "plans")
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, f"{method}_{safe_user}_{timestamp}.txt")