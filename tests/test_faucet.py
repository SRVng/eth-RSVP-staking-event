import brownie, pytest
from brownie import Faucet, accounts

def test_add_money(accounts, Faucet_module_scope):
    Faucet_module_scope.addMoney({'from': accounts[1], 'value':brownie.web3.toWei(5, 'ether')})
    assert Faucet_module_scope.balance() == brownie.web3.toWei(5, 'ether')

def test_get_money(accounts, Faucet_module_scope):
    balances = brownie.web3.eth.get_balance(str(accounts[2]))
    Faucet_module_scope.getMoney(accounts[2], {'from': accounts[2]})
    assert brownie.web3.eth.get_balance(str(accounts[2])) == balances + brownie.web3.toWei(1, 'ether')

def test_wrong_account(accounts, Faucet_module_scope):
    with brownie.reverts("Your account only"):
        Faucet_module_scope.getMoney(accounts[4], {'from': accounts[3]})

def test_get_money_again(accounts, Faucet_module_scope):
    with brownie.reverts(":("):
        Faucet_module_scope.getMoney(accounts[2], {'from': accounts[2]})