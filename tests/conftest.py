import brownie, pytest, random
from brownie import accounts, chain
from brownie.test import given, strategy
import web3

creator_swap = '1 ether'
creator_stake = 100
w3 = web3.Web3(web3.Web3.HTTPProvider('http://127.0.0.1:8545'))

@pytest.fixture(scope='module')
def Token_module_scope(EVT_Token):
    token = EVT_Token.deploy(brownie.web3.toWei(10000000, 'ether'),{'from': accounts[0]})
    return token

@pytest.fixture(scope='module')
def RSVP_Event_module_scope(EVT_Token,RSVP_Event, CreatorERC721, accounts):
    return RSVP_Event.deploy(EVT_Token[-1],CreatorERC721[-1], accounts[0], {'from':accounts[0]})

@pytest.fixture(scope='module')
def Faucet_module_scope(Faucet):
    return Faucet.deploy({'from': accounts[0]})

@pytest.fixture(scope='module')
def creatorNFT_module_scope(CreatorERC721):
    return CreatorERC721.deploy({'from': accounts[0]})

@pytest.fixture(scope="module", autouse=True)
def shared_setup(module_isolation):
    pass

@pytest.fixture(scope='module')
def EventCreated(Token_module_scope,RSVP_Event_module_scope, accounts, chain):
    end_time = chain[-1].timestamp + (24 * 60 * 60)
    Token_module_scope.swap({'from':accounts[0], 'value':creator_swap})
    RSVP_Event_module_scope.RSVP_Create("Testing", end_time, '100', {'from':accounts[0], 'value':'0.1 ether'})

@pytest.fixture(scope='module')    
def EventEnded_1_time(accounts,Token_module_scope, RSVP_Event_module_scope, EventCreated):
    addr = accounts[1]
    amount = 300
    Token_module_scope.swap({'from':addr, 'value':'3 ether'})
    RSVP_Event_module_scope.RSVP(amount, {'from':addr})
    chain.sleep(24*60*60)
    RSVP_Event_module_scope.Check_in({'from':accounts[0]})
    RSVP_Event_module_scope.Check_in({'from':addr})
    chain.sleep(60*60)
    RSVP_Event_module_scope.RSVP_End(accounts[0])

@pytest.fixture(scope='module')
def swap_multiple(accounts, Token_module_scope):
    swap_amount = ['0.5 ether', '0.1 ether', '1 ether', '2 ether', '3 ether', '90 ether', '50 ether',
                    '70 ether', '62 ether', '5 ether', '0.01 ether', '3.25 ether', '0.1 ether']

    for i in accounts[1:]:
        random_swap = random.choice(swap_amount)
        Token_module_scope.swap({'from':i, 'value':random_swap})


    