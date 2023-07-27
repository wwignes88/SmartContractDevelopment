
from scripts.helpful_scripts import *
from scripts.LoadContracts import *
from brownie import interface, config, network
import sys

def getAtokens():
    GasBalance = account.balance()  
    print(f'GasBalance balance  : {GasBalance*1e-18} ')
    printConversionRates()


    #---------------- DEPOSIT/ WITHDRAW MATIC
    # if needed, convert MATIC to WMATIC (wrapped Matic) which is
    # an ERC20 token that can be used to execute LendingPool
    # transactions.

    deposit, withdraw = True, False ; amount = 0.01*1e18

    if deposit:
        depositTokens(Wmatic, amount)
    if withdraw:
        withdrawTokens(Wmatic, amount)

    #----------------- GET A-Tokens [deposit to lending pool]
    # if you import the 'aMatic_token' token address into Metamask you will see
    # the 'amWMATIC' balance increase after making the following deposit;
    # WMATIC has been converted into amWMATIC (aTokens). 
    erc20 = Wmatic
    depositTokensToLendingPool = True
    if  depositTokensToLendingPool:
        dep_amount = 0.01*1e18
            
        # approve transaction    
        approve_tx = approve_erc20(dep_amount, 
                                   lending_pool.address, 
                                   erc20.address)

        # make deposit to lending pool
        print(f'\ndepositing {erc20.symbol()} into lending pool...')
        tx = lending_pool.deposit(erc20.address, 
                                  dep_amount, 
                                  account.address, 
                                  0, 
                                  {"from": account})
        tx.wait(1);  print(f'\ndeposited!!')
        

    
def main():
    getAtokens()
