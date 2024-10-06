from constants import RUPEES_SYMBOL
import uuid

def extract_price_from_rupees(price):
    try:
        _, amount = price.split(RUPEES_SYMBOL)
        return float(amount)
    except Exception:
        raise ValueError(f"Can not extract price from {price}")
    
def get_unique_id():
    return str(uuid.uuid4())
