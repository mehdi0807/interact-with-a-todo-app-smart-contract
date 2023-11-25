import web3

def ajouter_tache(contract: web3._utils.contracts, w3:web3.main.Web3, wallet:str, private_key:str, tache:str):
    transaction = contract.functions.ajouter_une_tache(tache).build_transaction(
        {"gasPrice": w3.eth.gas_price, 
        "chainId": w3.eth.chain_id, 
        "from": wallet, 
        "nonce": w3.eth.get_transaction_count(wallet)})
    signed_transaction = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)

def tache_accomplie(contract: web3._utils.contracts, w3:web3.main.Web3, wallet:str, private_key:str, tache:str):
    transaction = contract.functions.tache_accomplie(tache).build_transaction(
        {"gasPrice": w3.eth.gas_price, 
        "chainId": w3.eth.chain_id, 
        "from": wallet, 
        "nonce": w3.eth.get_transaction_count(wallet)})
    signed_transaction = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)

def reset(contract: web3._utils.contracts, w3:web3.main.Web3, wallet:str, private_key:str):
    transaction = contract.functions.reset().build_transaction(
        {"gasPrice": w3.eth.gas_price, 
        "chainId": w3.eth.chain_id, 
        "from": wallet, 
        "nonce": w3.eth.get_transaction_count(wallet)})
    signed_transaction = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)

