import brownie, pytest
from brownie import accounts
from brownie.test import given, strategy
import web3

w3 = web3.Web3(web3.Web3.HTTPProvider('http://127.0.0.1:8545'))

@given(
    addr = strategy('address')
)
def test_transfer_receiver(Token_module_scope,addr, accounts):
    amount = 1 * 1e18
    Token_module_scope.swap({'from':accounts[0], 'value':'10 ether'})
    if addr != accounts[0]:
        initial_balance = Token_module_scope.balanceOf(addr)
        Token_module_scope.transfer(addr, amount, {'from':accounts[0]})
        assert Token_module_scope.balanceOf(addr) == initial_balance + amount

@given(
    addr = strategy('address')
)
def test_transfer_transferor(Token_module_scope, addr, accounts):
    amount = 1 * 1e18
    initial_balance = Token_module_scope.balanceOf(accounts[0])
    if addr != accounts[0]:
        Token_module_scope.transfer(addr, amount, {'from':accounts[0]})
        assert Token_module_scope.balanceOf(accounts[0]) == initial_balance - amount

def test_self_transfer(Token_module_scope, accounts):
    amount = 2 * 1e18
    initial_balance = Token_module_scope.balanceOf(accounts[0])
    Token_module_scope.transfer(accounts[0], amount, {'from':accounts[0]})
    assert Token_module_scope.balanceOf(accounts[0]) == initial_balance
