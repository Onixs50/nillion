import os
import random
import subprocess
import time

# Color codes
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
ENDC = '\033[0m'

rpc_endpoints = [
    "https://nillion-testnet-rpc.polkachu.com",
    "https://nillion-testnet.rpc.kjnodes.com",
    "https://nillion-testnet.rpc.nodex.one"
]

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def display_header():
    box_line = "+" + "-"*26 + "+"
    text_line = "| coded by onixia       |"
    print(f"{GREEN}{box_line}\n{text_line}\n{box_line}{ENDC}")

def is_docker_running(container_name):
    try:
        result = subprocess.run(f"docker ps | grep {container_name}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    except Exception as e:
        print(f"{RED}Error checking Docker container: {e}{ENDC}")
        return False

def stop_docker_container(container_name):
    if is_docker_running(container_name):
        os.system(f"docker stop {container_name}")
        print(f"{YELLOW}Stopped running Docker container: {container_name}{ENDC}")

def run_docker(container_name, rpc_endpoint):
    stop_docker_container(container_name)
    os.system(f'docker run -v ./{container_name}:/var/tmp nillion/verifier:v1.0.1 verify --rpc-endpoint "{rpc_endpoint}"')

def run_verifier(container_name, rpc_endpoint):
    while True:
        try:
            run_docker(container_name, rpc_endpoint)
            time.sleep(10)
        except Exception as e:
            print(f"{RED}Verifier failed: {e}{ENDC}")
            new_rpc = random.choice(rpc_endpoints)
            print(f"{BLUE}Switching to new RPC endpoint: {new_rpc}{ENDC}")
            rpc_endpoint = new_rpc

def main():
    clear_screen()
    display_header()
    
    print(f"{BLUE}Do you have an old verifier node or a new verifier node?{ENDC}")
    print(f"{YELLOW}1. Old Verifier Node{ENDC}")
    print(f"{YELLOW}2. New Verifier Node{ENDC}")
    choice = input(f"{GREEN}Please select an option (1 or 2): {ENDC}")

    if choice == '1':
        run_verifier("nillion/accuser", "https://testnet-nillion-rpc.lavenderfive.com")
    elif choice == '2':
        run_verifier("nillion/verifier", "https://testnet-nillion-rpc.lavenderfive.com")
    else:
        print(f"{RED}Invalid option. Please select 1 or 2.{ENDC}")

if __name__ == "__main__":
    main()
