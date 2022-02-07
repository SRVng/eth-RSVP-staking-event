import json
from brownie import RSVP_Event, EVT_Token, Faucet, CreatorERC721, accounts

def main():
    myAccount = accounts.load('RSVP.json')

    token = EVT_Token.deploy(10000000 * 1e18, {'from': myAccount})
    faucet = Faucet.deploy({'from': myAccount})
    NFT = CreatorERC721.deploy({'from': myAccount})
    instance =  RSVP_Event.deploy(token, NFT, myAccount, {'from':myAccount})

    fetch_abi()

def fetch_abi():

    contractList = [EVT_Token, Faucet, CreatorERC721, RSVP_Event]
    contractAbiList = ['tokenAbi', 'faucetAbi', 'nftAbi', 'rsvpAbi']

    for i in range(len(contractList)):
        struct = {
            "CONTRACT_ADDRESS": str(contractList[i][-1]),
            "CONTRACT_ABI": contractList[i][-1].abi
        }

        with open(('./app/src/abi' + contractAbiList[i] + '.json'), 'w', encoding='utf-8') as f:
            json.dump(struct, f, indent=3)