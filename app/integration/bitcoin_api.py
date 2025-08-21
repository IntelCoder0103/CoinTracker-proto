import requests


BALANCE_API = "https://blockchain.info/balance?active={}"
TX_API = "https://blockchain.info/rawaddr/{}"

class BitcoinAPI:
    @staticmethod
    def get_balance(address):
        url = BALANCE_API.format(address)
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code != 200:
                return None, f"API error: {resp.status_code}"

            data = resp.json()
            if address not in data:
                return None, "Address not found in API response"
            # Blockchain.com returns balance in satoshis
            return data[address]['final_balance'], None
        except requests.Timeout:
            return None, "API request timed out"
        except Exception as e:
            return None, str(e)

    @staticmethod
    def get_transactions(address, limit=20, offset=0):
        limit = min(int(limit), 50)
        url = f"https://blockchain.info/rawaddr/{address}?offset={offset}&limit={limit}"

        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code != 200:
                return None, f"API error: {resp.status_code}", 0

            data = resp.json()
            txs = data.get('txs', [])
            # Filter only basic fields for each transaction
            filtered = []
            for tx in txs:
                filtered.append({
                    'hash': tx.get('hash'),
                    'time': tx.get('time'),
                    'block_height': tx.get('block_height'),
                    'inputs_count': len(tx.get('inputs', [])),
                    'out_count': len(tx.get('out', [])),
                    'result': tx.get('result'),
                    'balance': tx.get('balance'),
                    'fee': tx.get('fee'),
                    'size': tx.get('size'),
                })

            return filtered, None, len(filtered)
        except requests.Timeout:
            return None, "API request timed out", 0
        except Exception as e:
            return None, str(e), 0
