import brownie, pytest
from brownie import accounts
from brownie.test import given, strategy
import web3

w3 = web3.Web3(web3.Web3.HTTPProvider('http://127.0.0.1:8545'))

def test_initial_mint(RSVP_Event_module_scope):
    assert RSVP_Event_module_scope.totalSupply() == (10000000 * 1e18)

def test_web3():
    assert w3.isConnected() == True

@given(
    addr = strategy('address'),
    amount = strategy('uint256', max_value=10000)
)
def test_person_mint(RSVP_Event_module_scope, addr, amount):
    if addr != accounts[0]:
        with brownie.reverts():
            RSVP_Event_module_scope.mint(amount, {'from':addr})
    else: pass

@given(
    addr = strategy('address'),
    amount = strategy('uint256',max_value=10000)
)
def test_swap(RSVP_Event_module_scope,addr,amount):
    RSVP_Event_module_scope.swap({'from':addr,'value':'2 ether'})
    assert RSVP_Event_module_scope.EVT_balanceOf(addr) == 200

@given(
    addr = strategy('address'),
    amount = strategy('uint256',max_value=10000)
)
def test_swap_increase(RSVP_Event_module_scope,addr,amount):
    balances = RSVP_Event_module_scope.EVT_balanceOf(addr)
    RSVP_Event_module_scope.swap({'from':addr,'value':'1 ether'})
    assert RSVP_Event_module_scope.EVT_balanceOf(addr) == balances + 100
