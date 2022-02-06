import brownie
from brownie import RSVP_Event, EVT_Token, Faucet, CreatorERC721, accounts
import json

def main():
    myAccount = accounts[0]
    token = EVT_Token.deploy(brownie.web3.toWei(10000000, 'ether'), {'from': myAccount})
    faucet = Faucet.deploy({'from': myAccount})
    NFT = CreatorERC721.deploy({'from': myAccount})
    instance =  RSVP_Event.deploy(token, NFT, myAccount, {'from':myAccount})

    token.swap({'from': myAccount, 'value': brownie.web3.toWei(5, 'ether')})
    instance.RSVP_Create("Test", brownie.chain.time() + 10000, 10, {'from': myAccount, 'value': brownie.web3.toWei(0.1, 'ether')})

    brownie.chain.sleep(10001)

    instance.Check_in({'from': myAccount})

    brownie.chain.sleep(50000)

    instance.RSVP_End(myAccount, {'from': myAccount})