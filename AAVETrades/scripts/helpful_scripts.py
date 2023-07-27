from brownie import (accounts, interface, network, config, Contract, 
                     MyV2FlashLoan, testings) 
from web3 import Web3
import numpy as np
import shutil, os, sys

# global variables:
w3 = Web3(Web3.HTTPProvider("https://eth-sepolia.g.alchemy.com/v2/QUhbF0JeaaHCTWmZdPWDQ8TTjX2mv4zE"))


#=========================================================
#------------------------------------------ GET ACCOUNT(S)
TESTNETS = ['sepolia', 'avax-test','polygon-test']
def get_account():
    NETWORK = network.show_active()
    # !! **input(f'network: {config["networks"][network.show_active()]}')
    if NETWORK in TESTNETS:
        account = accounts.add(config["wallets"]["from_key"])
        #print(f'my gas balance: {w3.eth.get_balance(account.address)*1e-18} ETH')
        return account
    if NETWORK == "development":
        account = accounts[0]
        #print(f'my gas balance: {account.balance()*1e-18} ETH')
        return account
    print('[helpful_scripts.py - get_account]: get_account only configured for development [ganache], sepolia, avax-test [fuji] or polygon-test [Mumbai]')
    sys.exit(0)
account = get_account()

#------------------------------------------  GET CONTRACT(S)
contract_to_mock = {"FlashLoan_": MyV2FlashLoan,
                    "testing_": testings}

def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]
    contract_address = config["networks"][network.show_active()][contract_name]
    contract = Contract.from_abi(
        contract_type._name, contract_address, contract_type.abi)
    return contract


#---------------------  DEPLOYMENT; UPDATE CONFIG  ADDRESSES
def UpdateConfigAdresses(FlashLoanContract):

    NETWORK = network.show_active()
    _dir = os.getcwd() #; print(f'current dir: {_dir}')
    _config = _dir + '\\brownie-config.yaml' ; print(f'\n_config: {_config}\n')
    dummy_file    = _config + '.bak'
    
    with open(_config, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        
        READ_LINES  = read_obj.readlines() # file to be read
        data = []
        i = 0
        while i < len(READ_LINES):  
            
            line = READ_LINES[i]
            data.append(line)
            if NETWORK in line:
                j = i+1; kill = False
                while kill == False:
                    line = READ_LINES[j]
                    if 'FlashLoan_' in line:
                        line = F'    FlashLoan_    : "{FlashLoanContract.address}"\n'
                        kill = True
                    data.append(line)
                
                    j += 1
                i=j-1
            i += 1
            

        #write new file:
        i = 0
        while i < len(data):
            write_obj.write(data[i]) # this is 'a' object
            i += 1

    # replace current file with new debugging file
    os.remove(_config)
    os.rename(dummy_file, _config)
    print('config file updated w/ deployment addresses\n\n')

    #----------------------------


#---------------------------------------------------- TOKENS
def depositTokens(TokenContract, DepositAmount):
    # deposit AVAX into an ERC-20 compatable token 
    print(f'\ndepositing {TokenContract.symbol()}...')
    tx_hash = TokenContract.deposit({"value": DepositAmount, "from": account})
    tx_hash.wait(1)
    print(f'deposited {DepositAmount*1e-18} {TokenContract.symbol()}!')


def withdrawTokens(TokenContract, WithdrawAmount):
    # deposit AVAX into an ERC-20 compatable token 
    print(f'\nwithdrawing {TokenContract.symbol()}...')
    tx_hash = TokenContract.withdraw(WithdrawAmount, {"from": account})
    tx_hash.wait(1)
    print(f'withdrew {WithdrawAmount*1e-18} {TokenContract.symbol()}!')

    
def token_balance(token_contract, address):
    token_bal =  token_contract.balanceOf(address)
    return token_bal


#----------------------------------- LENDING POOL FUNCTIONS
def get_lending_pool():
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"])
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool

def getConversionRate(_str): #https://docs.chain.link/data-feeds/historical-data/
    price_feed_address = config["networks"][network.show_active()][_str]
    price_feed = interface.AggregatorV3Interface(price_feed_address)
    latest_price = price_feed.latestRoundData()[1]
    converted_latest_price = Web3.fromWei(latest_price, "ether")
    return float(converted_latest_price)

def get_borrowable_data(lending_pool, account):
    (
        total_collateral_eth,
        total_debt_eth,
        available_borrow_eth,
        current_liquidation_threshold,
        ltv,
        health_factor,
    ) = lending_pool.getUserAccountData(account.address)

    print('\nborrowable data:')
    print(f"    deposited: {total_collateral_eth}  ")
    print(f"    debt     : {total_debt_eth}  .")
    print(f"    borrowabl: {available_borrow_eth}  .")
    return (float(total_collateral_eth), float(available_borrow_eth), float(total_debt_eth))

def approve_erc20(amount, spender, erc20_address):
    print("Approving ERC20 token...")
    erc20 = interface.IERC20(erc20_address)
    tx    = erc20.approve(spender, amount, {"from": account})
    tx.wait(1)
    print("Approved!!")
    return tx









