from brownie import accounts

def main():
    myAccount = accounts.load('RSVP.json')

# brownie run loadAccount.py --network fuji --interactive