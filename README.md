# RSVP Contract with Staking

## About
This is my practice project for Solidity and Python.
While writing this project I learn how to write tests and how to design and work around with smart contracts. (Even though it still not perfect)

In a nutshell: Swap a token, create an event, let people stake in it, if anyone forget about this you earn their reward.

What did I use: Openzeppelin for both ERC20 and ERC721, ERC20 token is "EVT" which is a token for staking also ERC721 token "RSVP" is a NFT that identify who is the owner of the event.

### Details 
Swap a token using native chain token, Create an event by paying a collateral of 0.1 native token along with some "EVT" to ensure that atleast one person is staking(the owner). 
After create an event the creator also receive ERC721 to identify that him/her is the owner, then let people who also interest in the event participate by staking the "EVT" token which will reward them if they come back to check-in the event.
If someone who RSVP but don't show up they lose all of their reward and 10% of the staked amount, the amount of penalty for someone who don't show up will be share amongst the others that show up.

## Build
`brownie compile`

## Test
`brownie test -v`

## Deploy
###### Using scripts 
`brownie run deploy.py`
**The scripts need your private key save as RSVP.json file**