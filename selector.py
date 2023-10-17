import os
import re
import json
import argparse
from web3 import Web3

def get_selector(error_signature: str) -> str:
    hashed = Web3.keccak(text=error_signature)
    return hashed[:4].hex()

def extract_error_signatures(file_path: str) -> list:
    with open(file_path, 'r') as file:
        content = file.read()
    error_signatures = re.findall(r'error\s+([a-zA-Z0-9_]+\(\));', content)
    return error_signatures

def scan_repo_for_error_signatures(repo_path: str) -> list:
    error_data = []
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith('.sol'):
                file_path = os.path.join(root, file)
                error_signatures = extract_error_signatures(file_path)
                for error_signature in error_signatures:
                    error_name = error_signature.split("(")[0]
                    selector = get_selector(error_signature)
                    error_data.append({"name": error_name, "signature": error_signature, "selector": selector})
    return error_data

def save_to_json(error_data: list, file_name: str):
    with open(file_name, 'w') as f:
        json.dump(error_data, f, indent=4)

def main():
    parser = argparse.ArgumentParser(description='Scan a repo for Solidity error signatures and generate a JSON file with selectors.')
    parser.add_argument('repo_path', help='Path to the repository to scan')
    parser.add_argument('output_file', help='Name of the output JSON file')
    args = parser.parse_args()

    error_data = scan_repo_for_error_signatures(args.repo_path)
    save_to_json(error_data, args.output_file)

if __name__ == '__main__':
    main()
