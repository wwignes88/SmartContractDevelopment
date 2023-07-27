
from scripts.helpful_scripts import *
from brownie import interface, config, network
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("https://eth-sepolia.g.alchemy.com/v2/QUhbF0JeaaHCTWmZdPWDQ8TTjX2mv4zE"))
NETWORK = network.show_active()
account = get_account()

#---------------------------------- MISC. CONTRACTS/ ADDRESSES
# Lending contracts:
try:
    FlashLoan    = get_contract("FlashLoan_") 
    flashAddr    = FlashLoan.address
except:
    print('FlashLoan.sol not deployed.')
    
lending_pool = get_lending_pool() 

# Token contracts:
Wmatic  = interface.IERC20(config["networks"][NETWORK]["WMatic_token"])
Weth    = interface.IERC20(config["networks"][NETWORK]["weth_token"])
link    = interface.IERC20(config["networks"][NETWORK]["link_token"])
ATokens    = True
StableDebt = False
if ATokens:
    Amatic  = interface.IERC20(config["networks"][NETWORK]["aMatic_token"])
    Aweth   = interface.IERC20(config["networks"][NETWORK]["aWeth_token"])
if StableDebt:
    Amatic  = interface.IERC20(config["networks"][NETWORK]["StableMatic"])
    Aweth   = interface.IERC20(config["networks"][NETWORK]["StableWeth"])

# Currency conversion rates [using V3 Aggregator]
matic_to_usd   =   getConversionRate("matic_to_usd")
eth_to_usd     =   getConversionRate("eth_to_usd")
matic_to_eth   =   matic_to_usd/eth_to_usd
link_to_matic  =   getConversionRate("link_to_matic")
link_to_usd    =   getConversionRate("link_to_usd")

def printConversionRates():
    print('\nConversion rates:')
    print(f'    matic_to_eth  : {matic_to_eth}') 
    print(f'    matic_to_usd  : {matic_to_usd}')  
    print(f'    eth_to_usd    : {eth_to_usd}')  
    print(f'    link_to_matic : {link_to_matic}')  
    print(f'    link_to_usd   : {link_to_usd}')  


# *note this is overkill. FlashLoan contract only needs Wmatic.
# we don't NEED to check all these.
def getContractBalances(contract):
    print(f'\n-----\n{contract.symbol()} contract balances:')
    contract_address = contract.address
    print(f'     MATIC Balance: {contract.balance()*1e-18}')
    print(f'     ETH  Balance : {w3.eth.get_balance(contract_address)*1e-18}')
    print('Token Balances:')
    WmatBal = token_balance(Wmatic, contract_address)
    AmatBal = token_balance(Amatic, contract_address)
    print(f'     WMATIC Balance: {WmatBal*1e-18}')
    print(f'     AMATIC Balance: {AmatBal*1e-18}')
    print('-----\n')
    