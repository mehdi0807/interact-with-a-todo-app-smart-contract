import web3

def voir_progres(contract: web3._utils.datatypes.Contract) -> list[list]:
    contract.functions.voir_progres().call()

def nombre_taches_accomplies(contract: web3._utils.datatypes.Contract) -> list[list]:
    contract.functions.nombre_taches_accomplies().call()

def nombre_taches_totales(contract: web3._utils.datatypes.Contract) -> list[list]:
    contract.functions.nombre_taches_totoles().call()

def pourcentage_accompli(contract: web3._utils.datatypes.Contract) -> list[list]:
    contract.functions.pourcentage_accompli().call()