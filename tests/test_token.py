import brownie, pytest
from brownie import accounts
from brownie.test import given, strategy
import web3

w3 = web3.Web3(web3.Web3.HTTPProvider('http://127.0.0.1:8545'))

def test_initial_mint(Token_module_scope):
    assert Token_module_scope.totalSupply() == (10000000 * 1e18)

def test_web3():
    assert w3.isConnected() == True

@given(
    addr = strategy('address'),
    amount = strategy('uint256', max_value=10000)
)
def test_person_mint(Token_module_scope, addr, amount):
    if addr != accounts[0]:
        with brownie.reverts():
            Token_module_scope.mint(addr ,amount * 1e18, {'from':addr})
    else: pass

@given(
    addr = strategy('address'),
    amount = strategy('uint256',max_value=10000)
)
def test_swap(Token_module_scope,addr,amount):
    Token_module_scope.swap({'from':addr,'value':'2 ether'})
    assert Token_module_scope.balanceOf(addr) == 200 * 1e18

@given(
    addr = strategy('address'),
    amount = strategy('uint256',max_value=10000)
)
def test_swap_increase(Token_module_scope,addr,amount):
    balances = Token_module_scope.balanceOf(addr)
    Token_module_scope.swap({'from':addr,'value':'1 ether'})
    assert Token_module_scope.balanceOf(addr) == balances + 100 * 1e18
