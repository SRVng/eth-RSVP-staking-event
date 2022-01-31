from brownie import RSVP_Event, accounts
import json

def main():
    acct = accounts.load('RSVP.json')
    RSVP_Event.deploy(10000000, {'from':acct})