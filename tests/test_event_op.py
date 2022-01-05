import brownie, pytest, web3
from brownie import accounts, chain
from brownie.test import given, strategy

w3 = web3.Web3(web3.Web3.HTTPProvider('http://127.0.0.1:8545'))
creator_swap = '1 ether'
creator_stake = 100

def test_event_initial_status(RSVP_Event_module_scope):
    Waiting = 0
    Ended = 1
    assert RSVP_Event_module_scope.event_status() == Ended

def test_event_ongoing(accounts, RSVP_Event_module_scope, EventCreated):
    Waiting = 0
    Ended = 1
    assert chain[-1].timestamp < RSVP_Event_module_scope.end_time()
    assert RSVP_Event_module_scope.event_status() == Waiting
    assert RSVP_Event_module_scope.Stake_Check(accounts[0])[1] == creator_stake 
    assert RSVP_Event_module_scope.total_stake()[1] == creator_stake

def test_event_normal_end(accounts, RSVP_Event_module_scope, EventCreated):
    initial_balance = w3.eth.get_balance(str(accounts[0]))
    Waiting, Ended = 0, 1
    chain.sleep((24*60*60)+1)
    RSVP_Event_module_scope.Check_in({'from':accounts[0]})
    chain.sleep(60*60)
    RSVP_Event_module_scope.RSVP_End(accounts[0])
    assert RSVP_Event_module_scope.event_status() == Ended
    assert RSVP_Event_module_scope.end_time() == 0
    assert round(float(w3.fromWei(initial_balance, "ether")), 0) == round(float(w3.fromWei(w3.eth.get_balance(str(accounts[0])), "ether")),0)
