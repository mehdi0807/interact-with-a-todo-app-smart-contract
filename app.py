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
contract_address = "0x660aCEc32977F30aEe4A8637FE489dA43be3302e"
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

st.sidebar.title('Les informations relatives à votre wallet')
wallet = st.sidebar.text_input("Entrez l'adresse de votre wallet")
private_key = st.sidebar.text_input("Entrez la clé privé")

st.title('To-do App')

if wallet:
    if private_key:
        taches = voir_progres(contract)[0]
        progress = voir_progres(contract)[1]

        df_list = []
        for i in range(len(taches)):
            df_list.append([taches[i], progress[i]])
        df = pd.DataFrame(df_list, columns=['Tache', 'Etat'])
        st.write(df)

        tache_ajoutée = st.text_input('Une tâche à ajouter')
        boutton = st.button('Ajouter la tâche')
        if tache_ajoutée:
            if boutton:
                ajouter_tache(contract, w3, wallet, private_key, tache_ajoutée)
                st.experimental_rerun()

        _tache_accomplie = st.selectbox('Choisis une tâche qui est accomplie',[tache for tache in taches if progress[taches.index(tache)]==False])
        if st.button('Tâche accomplie'):
            tache_accomplie(contract, w3, wallet, private_key, _tache_accomplie)
            st.experimental_rerun()

        pourcentage = pourcentage_accompli(contract)
        st.progress(pourcentage, text=f'{pourcentage}% des tâches sont accomplies')
        if pourcentage == 100:
            st.balloons()
            st.success("Félicitations ! Tu as accompli toutes tes tâches avec succès. Un vrai pro de la productivité!")

        if st.button('reset'):
            reset(contract, w3, wallet, private_key)
            st.experimental_rerun()

    else:
        st.info("Pour utiliser l'application, vous devez entrez une adresse et sa clé privée appropriée")
else:
    st.info("Pour utiliser l'application, vous devez entrez une adresse et sa clé privée appropriée")
