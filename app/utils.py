import re

def is_valid_btc_address(address):
    # Basic regex for legacy, segwit, and bech32 addresses
    legacy = r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$'
    bech32 = r'^(bc1)[0-9a-z]{25,39}$'
    return re.match(legacy, address) or re.match(bech32, address)
