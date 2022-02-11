import json
from brownie import RSVP_Event_With_EIP_712, EVT_Token, CreatorERC721, accounts

def main():
    myAccount = accounts.load('RSVP.json', '1234')
    
    instance =  RSVP_Event_With_EIP_712.deploy(
        "0x790b47Bebe7e135887BAA1c9841048dC6Ca348Ed", 
        "0x7c92b7C9e122Dbe1E992d937f4A78e6a896aB4d4", 
        myAccount, 
        {'from':myAccount}
        )

    struct = {
        "CONTRACT_ADDRESS": str(instance),
        "CONTRACT_ABI": instance.abi
    }

    with open('./app/src/abi/rsvpAbi.json', 'w', encoding='utf-8') as f:
        json.dump(struct, f, indent=3)