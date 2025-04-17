def convert_percentage(value_str):
    """Convert Percentage ('17.67%') to demical (0.1767)"""
    try:
        value_str = value_str.strip()
        sign = -1 if value_str.startswith('-') else 1
        numeric_part = value_str.replace('%', '').replace('+', '').replace('-', '')
        return round(float(numeric_part) / 100, 6) * sign
    except:
        return None

def convert_market_cap(value_str):
    """Convert market cap to real number (π.χ. '16.089T' → 16089000000000)"""
    multipliers = {'T': 1_000_000_000_000, 'B': 1_000_000_000, 'M': 1_000_000}
    try:
        num = float(value_str[:-1])
        unit = value_str[-1].upper()
        return int(num * multipliers.get(unit, 1))
    except:
        return None

def convert_integer(value_str):
    try:
        return int(value_str.replace(",", ""))
    except:
        return None
