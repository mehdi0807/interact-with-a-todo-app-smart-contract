import streamlit as st
from web3 import Web3
import pandas as pd
import os
import json

from src.read_functions import *
from src.write_functions import *

infura_url = "https://data-seed-prebsc-1-s1.binance.org:8545"
w3 = Web3(Web3.HTTPProvider(infura_url))

f = open(os.path.join('src', 'abi.json'))
contract_abi = json.load(f)
contract_address = "0x1881ef0Eb82142873f6751B76C5400D08369694f"
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

st.sidebar.title('Les informations relatives à votre wallet')
wallet = st.sidebar.text_input("Entrez l'adresse de votre wallet")
private_key = st.sidebar.text_input("Entrez la clé privé")
connecter = st.sidebar.button('Se connecter')

st.title('To-do App')

if wallet:
    if private_key:
        if connecter:
            taches = voir_progres(contract)[0]
            progress = voir_progres(contract)[1]

            df_list = []
            for i in range(len(taches)):
                df_list.append([taches[i], progress[i]])
            df = pd.DataFrame(df_list, columns=['Tache', 'Etat'])
            st.write(df)

            tache_ajoutée = st.text_input('Une tache à ajouter')
            boutton = st.button('Ajouter la tache')
            if tache_ajoutée:
                if boutton:
                    ajouter_tache(contract, w3, wallet, private_key, tache_ajoutée)
                    st.experimental_rerun()

            _tache_accomplie = st.selectbox('Choisis une tache qui est accomplie',taches)
            if st.button('Tache accomplie'):
                tache_accomplie(contract, w3, wallet, private_key, _tache_accomplie)
                st.experimental_rerun()

            pourcentage = pourcentage_accompli(contract)
            st.progress(pourcentage, text=f'{pourcentage}% des taches sont accomplies')
            if st.button('reset'):
                reset(contract, w3, wallet, private_key)
                st.experimental_rerun()
        else:
            st.info("Clique sur 'Se connecter'")

    else:
        st.info("Pour utiliser l'application, vous devez entrez une adresse et sa clé privée appropriée")
else:
    st.info("Pour utiliser l'application, vous devez entrez une adresse et sa clé privée appropriée")
