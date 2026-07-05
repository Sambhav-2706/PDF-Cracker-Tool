import argparse
import itertools
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import pikepdf
from tqdm import tqdm

CHARSETS = {
    "l": "abcdefghijklmnopqrstuvwxyz",
    "u": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "d": "0123456789",
    "s": "!@#$%^&*()-_=+[]{}|;:',.<>?/"
}
def print_banner():
    banner = r"""
  _____  _____  ______    _____                _             
 |  __ \|  __ \|  ____|  / ____|              | |            
 | |__) | |  | | |__    | |     _ __ __ _  ___| | _____ _ __ 
 |  ___/| |  | |  __|   | |    | '__/ _` |/ __| |/ / _ \ '__|
 | |    | |__| | |      | |____| | | (_| | (__|   <  __/ |   
 |_|    |_____/|_|       \_____|_|  \__,_|\___|_|\_\___|_|   
                                                             
    """
    print(banner)

def try_password(pdf_path, password):
    try:
        with pikepdf.open(pdf_path, password=password) as _:
            return password
    except pikepdf.PasswordError:
        return None
    except Exception:
        return None

def generate_brute_force(charset_flags, min_len, max_len):
    selected_chars = "".join([CHARSETS[flag] for flag in charset_flags if flag in CHARSETS])
    if not selected_chars:
        selected_chars = CHARSETS["d"]
    for length in range(min_len, max_len + 1):
        for item in itertools.product(selected_chars, repeat=length):
            yield "".join(item)

def main():
    print_banner()
    parser = argparse.ArgumentParser(description="Multi-threaded PDF Password Recovery Tool.")
    parser.add_argument("-f", "--file", required=True, help="Path to the password-protected PDF file.")
    parser.add_argument("-w", "--wordlist", help="Path to the password wordlist (Dictionary Attack).")
    parser.add_argument("-b", "--brute", action="store_true", help="Enable Brute-Force Attack mode.")
    parser.add_argument("-c", "--charset", default="d", help="Brute-force characters...")
    parser.add_argument("--min", type=int, default=1, help="Minimum password length...")
    parser.add_argument("--max", type=int, default=4, help="Maximum password length...")
    parser.add_argument("-t", "--threads", type=int, default=4, help="Number of concurrent execution threads.")
    args = parser.parse_args()

if not os.path.exists(args.file):
        print(f" Error: Target file '{args.file}' does not exist.")
        sys.exit(1)
    try:
        with pikepdf.open(args.file) as _:
            print(" Target PDF is not password-protected.")
            sys.exit(0)
    except pikepdf.PasswordError:
        print(" Target confirmed encrypted. Proceeding...")
    except Exception as e:
        print(f" Invalid or corrupted PDF file structural data: {e}")
        sys.exit(1)

passwords = []
    if args.wordlist:
        if not os.path.exists(args.wordlist):
            print(f" Error: Wordlist path '{args.wordlist}' not found.")
            sys.exit(1)
        print(f" Loading dictionary file: {args.wordlist}")
        with open(args.wordlist, "r", encoding="utf-8", errors="ignore") as f:
            passwords = [line.strip() for line in f if line.strip()]          
    elif args.brute:
        print(f" Pre-computing brute-force space...")
        passwords = list(generate_brute_force(args.charset, args.min, args.max))
    else:
        print(" Error: You must specify an attack mode: --wordlist <path> OR --brute")
        sys.exit(1)

total_passwords = len(passwords)
    found_password = None
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        future_to_pass = {executor.submit(try_password, args.file, pwd): pwd for pwd in passwords}
        with tqdm(total=total_passwords, desc="Cracking progress", unit="pwd") as pbar:
            for future in as_completed(future_to_pass):
                result = future.result()
                if result:
                    found_password = result
                    executor.shutdown(wait=False, cancel_futures=True)
                    break
                pbar.update(1)

print("\n" + "="*40)
    if found_password:
        print(f" CRACK SUCCESSFUL!")
        print(f" Password Found: {found_password}")
    else:
        print(" CRACK FAILED: All password combinations exhausted.")
    print("="*40)