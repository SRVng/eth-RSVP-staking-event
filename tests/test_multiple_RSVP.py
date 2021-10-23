import brownie, pytest, web3, random
from brownie import accounts, chain
from brownie.test import given, strategy

w3 = web3.Web3(web3.Web3.HTTPProvider('http://127.0.0.1:8545'))

    #Test Subject
    # 1 : 10 people staking
    # 2 : Ending with someone not check-in
    # 3 : End the first event and create new, do everything the same
    # 4 : Measure the reward rate ex: 2 person stake rate > 5 person stake

def test_multiple_stake(accounts, RSVP_Event_module_scope, EventCreated, swap_multiple):
    total_stake = RSVP_Event_module_scope.total_stake()[0] #Stake of event creator
    for i in accounts[1:]:
        balances = RSVP_Event_module_scope.EVT_balanceOf(i)
        RSVP_Event_module_scope.RSVP(balances, {'from':i})
        total_stake += RSVP_Event_module_scope.Stake_Check(i)[0]
    assert total_stake == RSVP_Event_module_scope.total_stake()[0]

def test_multiple_stake_reward(accounts, RSVP_Event_module_scope, EventCreated):
    total_unclaimed_0 = RSVP_Event_module_scope.total_unclaimed_reward().return_value[0]
    chain.sleep(60*60) # 1 hr pass
    assert total_unclaimed_0 < RSVP_Event_module_scope.total_unclaimed_reward().return_value[0]

def test_multiple_reward_claim(accounts, RSVP_Event_module_scope, EventCreated):
    chain.sleep(6*60*60) # 7 hr pass
    for i in accounts[:5]:
        initial_unclaimed = RSVP_Event_module_scope.total_unclaimed_reward().return_value[1]
        individual_reward = RSVP_Event_module_scope.Reward_Check({'from':i}).return_value[1]
        individual_balance = RSVP_Event_module_scope.EVT_balanceOf(i)
        RSVP_Event_module_scope.withdraw_reward({'from':i})
        assert RSVP_Event_module_scope.Reward_Check({'from':i}).return_value[1] == 0
        assert RSVP_Event_module_scope.total_unclaimed_reward().return_value[1] == initial_unclaimed - individual_reward
        assert RSVP_Event_module_scope.EVT_balanceOf(i) - (individual_balance + (individual_reward / 2)) <= 1

def test_multiple_stake_check_in(accounts, RSVP_Event_module_scope, EventCreated):
    chain.sleep(17*60*60) #24 hr pass
    assert chain.time() > RSVP_Event_module_scope.end_time()
    for i in accounts:
        initial_balance = RSVP_Event_module_scope.balanceOf(i) + RSVP_Event_module_scope.Stake_Check(i)[0]
        _reward = RSVP_Event_module_scope.Reward_Check({'from':i}).return_value[0]
        RSVP_Event_module_scope.Check_in({'from':i})
        assert RSVP_Event_module_scope.balanceOf(i) == initial_balance + _reward

def test_multiple_stake_after_check_in(accounts, RSVP_Event_module_scope, EventCreated):
    for i in range(len(accounts)):
        with brownie.reverts():
            RSVP_Event_module_scope.Reward_Check({'from':accounts[i]})
            RSVP_Event_module_scope.withdraw_reward({'from':accounts[i]})
            RSVP_Event_module_scope.RSVP(300, {'from':accounts[i]})
            RSVP_Event_module_scope.Check_in({'from':accounts[i]})

def test_multiple_stake_pool_cleared(accounts, RSVP_Event_module_scope, EventCreated):
    assert RSVP_Event_module_scope.total_unclaimed_reward().return_value[0] == 0
    assert RSVP_Event_module_scope.total_stake()[0] == 0

def test_multiple_stake_event_end(accounts, RSVP_Event_module_scope, EventCreated):
    initial_balance = w3.eth.get_balance(str(accounts[0]))
    Waiting, Ended = 0, 1
    
    chain.sleep(60*60)
    RSVP_Event_module_scope.RSVP_End(accounts[0])

    assert RSVP_Event_module_scope.event_status() == Ended
    assert RSVP_Event_module_scope.end_time() == 0
    assert round(float(w3.fromWei(initial_balance, "ether")) + 0.1, 2) == round(float(w3.fromWei(w3.eth.get_balance(str(accounts[0])), "ether")),2)
    
