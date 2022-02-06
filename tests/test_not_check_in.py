import brownie, pytest, web3, random
from brownie import accounts, chain
from brownie.test import given, strategy

w3 = web3.Web3(web3.Web3.HTTPProvider('http://127.0.0.1:8545'))

def test_multiple_stake_and_time_skip(accounts,creatorNFT_module_scope, Token_module_scope,RSVP_Event_module_scope, EventCreated, swap_multiple):
    for i in accounts[1:]:
        balances = Token_module_scope.balanceOf(i) / 1e18
        RSVP_Event_module_scope.RSVP(balances, {'from':i})
    chain.sleep(24 * 60 * 60) # 24 hr pass
    assert chain.time() > RSVP_Event_module_scope.end_time()

def test_multiple_stake_partial_check_in(accounts, RSVP_Event_module_scope, EventCreated):
    for i in accounts[:-3]:
        RSVP_Event_module_scope.Check_in({'from':i})
        with brownie.reverts("No stake balances"):
            RSVP_Event_module_scope.Reward_Check({'from':i}).return_value[0]
    assert len(RSVP_Event_module_scope.Whitelist()) == 3

def test_multiple_stake_after_check_in(accounts, RSVP_Event_module_scope, EventCreated):
    for i in range(len(accounts)):
        with brownie.reverts():
            if i < (len(accounts) - 3):
                RSVP_Event_module_scope.withdraw_reward({'from':accounts[i]})
                RSVP_Event_module_scope.Check_in({'from':accounts[i]})
            if i >= (len(accounts) - 3):
                RSVP_Event_module_scope.RSVP(1, {'from':accounts[i]})

def test_multiple_stake_reward_share(accounts, Token_module_scope, RSVP_Event_module_scope, EventCreated):
    chain.sleep(2*60*60)
    wallet_balances = {}
    stake_balances = {}

    for i in accounts:
        wallet_balances[i] = Token_module_scope.balanceOf(i)
    for i in accounts[-3:]:
        stake_balances[i] = RSVP_Event_module_scope.Stake_Check(i)[0]

    share_rewards = RSVP_Event_module_scope.RSVP_End(accounts[0], {'from':accounts[0]}).return_value
    assert share_rewards != 0

    assert RSVP_Event_module_scope.total_stake()[0] == 0
    for i in range(len(accounts)):
        addr = accounts[i]
        if i < (len(accounts) - 3):
            assert Token_module_scope.balanceOf(addr) == wallet_balances[addr] + share_rewards, i
        if i >= (len(accounts) - 3):
            assert Token_module_scope.balanceOf(addr) == wallet_balances[addr] + (0.9 * stake_balances[addr])

def test_multiple_stake_pool_cleared(accounts, RSVP_Event_module_scope):
    assert RSVP_Event_module_scope.total_unclaimed_reward().return_value[0] == 0
    assert RSVP_Event_module_scope.total_stake()[0] == 0