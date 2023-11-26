import streamlit as st
from web3 import Web3
import pandas as pd
import os
import json

from src.read_functions import *
from src.write_functions import *

# Se connecter au réseau de testnet BNB
testnet_bnb_url = "https://data-seed-prebsc-1-s1.binance.org:8545"
w3 = Web3(Web3.HTTPProvider(testnet_bnb_url))

# Importer le contrat
f = open(os.path.join('src', 'abi.json'))
contract_abi = json.load(f)
contract_address = "0x660aCEc32977F30aEe4A8637FE489dA43be3302e"
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

## App

# Sidebar
st.sidebar.title('Les informations relatives à votre wallet')
wallet = st.sidebar.text_input("Entrez l'adresse de votre wallet")
private_key = st.sidebar.text_input("Entrez la clé privé")

# Home
st.title('To-do App')

if wallet:
    if private_key:  # Si wallet et private_key existent
        try:
            # Verifier si les informations sont correctes
            transaction = contract.functions.reset().build_transaction(
                {"gasPrice": w3.eth.gas_price, 
                "chainId": w3.eth.chain_id, 
                "from": wallet, 
                "nonce": w3.eth.get_transaction_count(wallet)})
            signed_transaction = w3.eth.account.sign_transaction(transaction, private_key=private_key)
            st.sidebar.success("La vérification de la wallet et de la clé privée a réussi.")

            # Variables utiles
            taches = voir_progres(contract)[0]
            progress = voir_progres(contract)[1]

            # Affichage de la liste sous format d'un pandas dataframe
            df_list = []
            for i in range(len(taches)):
                df_list.append([taches[i], progress[i]])
            df = pd.DataFrame(df_list, columns=['Tache', 'Etat'])
            st.write(df)

            # Ajouter une tache
            tache_ajoutée = st.text_input('Une tâche à ajouter')
            boutton = st.button('Ajouter la tâche')
            if tache_ajoutée:
                if boutton:
                    ajouter_tache(contract, w3, wallet, private_key, tache_ajoutée)
                    st.experimental_rerun()

            # Mettre une tache comme accomplie
            _tache_accomplie = st.selectbox('Choisis une tâche qui est accomplie',[tache for tache in taches if progress[taches.index(tache)]==False])
            if st.button('Tâche accomplie'):
                tache_accomplie(contract, w3, wallet, private_key, _tache_accomplie)
                st.experimental_rerun()

            # Affichage du pourcentage d'accomplissement
            pourcentage = pourcentage_accompli(contract)
            st.progress(pourcentage, text=f'{pourcentage}% des tâches sont accomplies')
            if pourcentage == 100:
                st.balloons()
                st.success("Félicitations ! Tu as accompli toutes tes tâches avec succès. Un vrai pro de la productivité!")
            
            # Reset
            if st.button('reset'):
                reset(contract, w3, wallet, private_key)
                st.experimental_rerun()
        
        except Exception as e: # Si la wallet n'est pas valide
            st.error(f"Erreur lors de la vérification de la wallet et de la clé privée : {str(e)}")

    else:  # Si le champ de la clé est vide
        st.info("Pour utiliser l'application, vous devez entrez la clé privée appropriée à votre adress")
else: # Si les deux champs sont vides
    st.info("Pour utiliser l'application, vous devez entrez une adresse et sa clé privée appropriée")
