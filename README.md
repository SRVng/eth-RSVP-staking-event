# RSVP_Staking

This is my first solidity project (Not finished)

Idea : Event Staking (Challenge from https://ethhole.com/challenge)

For simplicity, Any person can create an RSVP event using 0.1 ETH as a collateral and must stake the "EVT" Token (ERC-20) also provide the deadline (for now it is unix time, I will try to change that later on).
After the event was created anyone can be a participant using an EVT token to RSVP (like saying that when the event occured I will be here), participant receive an EVT token as a reward overtime by staking it.

Example: Alice know that next week there are "Ethereum Bangkok 2021" event, Alice will definitely attending that event so Alice create RSVP event for this particular event with 0.1 ETH and staking 100 EVT. Bob want to participate too so Bob RSVP the event with 150 EVT. Charlie also want to participate and RSVP with 300 EVT. Then the time passed until the event occured participant have to check in within the check-in period so Alice and Bob checked in, Alice got the collateral 0.1 ETH and 100 EVT back plus some EVT reward. Bob got the staked 150 EVT back plus some reward. Charlie missed the event and forgot that he was participate in this RSVP.
After the check-in period passed Alice end the event, Charlie got 270 EVT back (90%) but all the reward from his staked are shared amongst the participant who checked-in (Alice and Bob)
