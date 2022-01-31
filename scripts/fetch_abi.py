from brownie import RSVP_Event
import json

def main():

    struct = {
        "CONTRACT_ADDRESS": str(RSVP_Event[-1]),
        "CONTRACT_ABI": RSVP_Event[-1].abi
    }

    with open('./app/src/abi.json', 'w', encoding='utf-8') as f:
        json.dump(struct, f, indent=3)