

import requests
import sys
import os
from colorama import init, Fore, Style

init(autoreset=True)

# Use environment variable for API URL
API_URL = os.environ.get("COINTRACKER_API_URL", "http://127.0.0.1:5000")


def print_menu():
    print(Fore.CYAN + Style.BRIGHT + "\nCoinTracker CLI")
    print(Fore.YELLOW + "1. Add Bitcoin address")
    print(Fore.YELLOW + "2. Remove Bitcoin address")
    print(Fore.YELLOW + "3. List Bitcoin addresses")
    print(Fore.YELLOW + "4. Get address balance")
    print(Fore.YELLOW + "5. Get address transactions")
    print(Fore.YELLOW + "6. Exit")

def add_address():
    address = input(Fore.CYAN + "Enter Bitcoin address (or type 'b' to go back): ")
    if address.lower() == 'b':
        return
    try:
        resp = requests.post(f"{API_URL}/addresses", json={"address": address})
        data = parse_response(resp)
        if resp.status_code == 201:
            print(Fore.GREEN + f"Added address: {data['address']}")
        else:
            print(Fore.RED + f"Error: {data.get('error', data)}")
    except Exception as e:
        print(Fore.RED + f"Network error: {e}")

def remove_address():
    address = input(Fore.CYAN + "Enter Bitcoin address to remove (or type 'b' to go back): ")
    if address.lower() == 'b':
        return
    try:
        resp = requests.delete(f"{API_URL}/addresses/{address}")
        data = parse_response(resp)
        if resp.status_code == 200:
            print(Fore.GREEN + f"Removed address: {address}")
        else:
            print(Fore.RED + f"Error: {data.get('error', data)}")
    except Exception as e:
        print(Fore.RED + f"Network error: {e}")

def list_addresses():
    try:
        resp = requests.get(f"{API_URL}/addresses")
        addresses = parse_response(resp)
        if not addresses:
            print(Fore.RED + "No addresses found.")
            return
        print(Fore.CYAN + "Tracked Bitcoin addresses:")
        for idx, addr in enumerate(addresses, 1):
            print(Fore.YELLOW + f"{idx}. {addr['address']}")
    except Exception as e:
        print(Fore.RED + f"Network error: {e}")

def get_balance():
    try:
        resp = requests.get(f"{API_URL}/addresses")
        addresses = parse_response(resp)
        if not addresses:
            print(Fore.RED + "No addresses found.")
            return
        print(Fore.CYAN + "Select address to get balance:")
        for idx, addr in enumerate(addresses, 1):
            print(Fore.YELLOW + f"{idx}. {addr['address']}")
        print(Fore.YELLOW + f"{len(addresses)+1}. All addresses")
        print(Fore.YELLOW + f"b. Go back")
        choice = input(Fore.CYAN + "Choose an option: ")
        if choice.lower() == 'b':
            return
        try:
            choice = int(choice)
            if 1 <= choice <= len(addresses):
                address = addresses[choice-1]['address']
                resp = requests.get(f"{API_URL}/addresses/{address}/balance")
                data = parse_response(resp)
                if resp.status_code == 200:
                    print(Fore.GREEN + f"Balance for {address}: {data['balance'] / 1e8:.8f} BTC ({data['balance']} satoshis)")
                else:
                    print(Fore.RED + f"Error: {data.get('error', data)}")
            elif choice == len(addresses)+1:
                for addr in addresses:
                    resp = requests.get(f"{API_URL}/addresses/{addr['address']}/balance")
                    data = parse_response(resp)
                    if resp.status_code == 200:
                        print(Fore.GREEN + f"{addr['address']}: {data['balance'] / 1e8:.8f} BTC ({data['balance']} satoshis)")
                    else:
                        print(Fore.RED + f"{addr['address']}: Error: {data.get('error', data)}")
            else:
                print(Fore.RED + "Invalid choice.")
        except Exception as e:
            print(Fore.RED + f"Invalid input: {e}")
    except Exception as e:
        print(Fore.RED + f"Network error: {e}")

def print_transaction(tx, idx=None):
    prefix = f"{idx+1}. " if idx is not None else ""
    print(Fore.YELLOW + Style.BRIGHT + f"{prefix}Hash: {tx['hash']}")
    print(Fore.CYAN + f"   Time: {tx['time']}")
    print(Fore.CYAN + f"   Block Height: {tx['block_height']}")
    print(Fore.MAGENTA + f"   Inputs: {tx['inputs_count']} | Outputs: {tx['out_count']}")
    print(Fore.BLUE + f"   Fee: {tx['fee']} satoshis | Size: {tx['size']} bytes")
    if tx.get('result') is not None:
        print(Fore.GREEN + f"   Result: {tx['result']} satoshis")
    if tx.get('balance') is not None:
        print(Fore.GREEN + f"   Balance: {tx['balance']} satoshis")
    print(Fore.WHITE + "-")

def get_transactions():
    try:
        resp = requests.get(f"{API_URL}/addresses")
        addresses = parse_response(resp)
        if not addresses:
            print(Fore.RED + "No addresses found.")
            return
        print(Fore.CYAN + "Select address to get transactions:")
        for idx, addr in enumerate(addresses, 1):
            print(Fore.YELLOW + f"{idx}. {addr['address']}")
        print(Fore.YELLOW + f"{len(addresses)+1}. All addresses")
        print(Fore.YELLOW + f"b. Go back")
        choice = input(Fore.CYAN + "Choose an option: ")
        if choice.lower() == 'b':
            return
        try:
            choice = int(choice)
            if 1 <= choice <= len(addresses):
                address = addresses[choice-1]['address']
                show_transactions_with_paging(address)
            elif choice == len(addresses)+1:
                for addr in addresses:
                    show_transactions_with_paging(addr['address'])
            else:
                print(Fore.RED + "Invalid choice.")
        except Exception as e:
            print(Fore.RED + f"Invalid input: {e}")
    except Exception as e:
        print(Fore.RED + f"Network error: {e}")

def show_transactions_with_paging(address):
    offset = 0
    page_size = 10
    max_limit = 50
    while True:
        limit = min(page_size, max_limit)
        try:
            resp = requests.get(f"{API_URL}/addresses/{address}/transactions?limit={limit}&offset={offset}")
            data = parse_response(resp)
            if 'transactions' in data:
                txs = data['transactions']
                if not txs:
                    print(Fore.YELLOW + f"No transactions found for {address}.")
                    break
                print(Fore.GREEN + f"\nTransactions for {address} (showing {offset+1} to {offset+len(txs)}):")
                for i, tx in enumerate(txs, start=offset):
                    print_transaction(tx, i)
                if len(txs) < page_size or len(txs) < limit:
                    break
                more = input(Fore.CYAN + "Show more? (y/n/b): ")
                if more.lower() == 'y':
                    offset += page_size
                    continue
                elif more.lower() == 'b':
                    break
                else:
                    break
            else:
                print(Fore.RED + f"Error: {data.get('error', data)}")
                break
        except Exception as e:
            print(Fore.RED + f"Network error: {e}")
            break
def parse_response(resp):
    try:
        return resp.json()
    except Exception:
        return {"error": "Invalid response from server"}

def print_help():
    print(Fore.CYAN + "\nCoinTracker CLI Usage:")
    print(Fore.YELLOW + "Commands:")
    print(Fore.YELLOW + "  1. Add Bitcoin address")
    print(Fore.YELLOW + "  2. Remove Bitcoin address")
    print(Fore.YELLOW + "  3. List Bitcoin addresses")
    print(Fore.YELLOW + "  4. Get address balance")
    print(Fore.YELLOW + "  5. Get address transactions")
    print(Fore.YELLOW + "  6. Exit")
    print(Fore.CYAN + "\nYou can also set the API URL with the COINTRACKER_API_URL environment variable.")

if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
    print_help()
    sys.exit(0)

def main():
    while True:
        print_menu()
        choice = input("Choose an option: ")
        if choice == '1':
            add_address()
        elif choice == '2':
            remove_address()
        elif choice == '3':
            list_addresses()
        elif choice == '4':
            get_balance()
        elif choice == '5':
            get_transactions()
        elif choice == '6':
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
