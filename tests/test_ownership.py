import brownie, pytest

def test_owner(RSVP_Event_module_scope, accounts):
    assert RSVP_Event_module_scope.owner() == accounts[0]

def test_owner_transfer(RSVP_Event_module_scope, accounts):
    RSVP_Event_module_scope.transferOwnership(accounts[1], {'from':accounts[0]})
    assert RSVP_Event_module_scope.owner() == accounts[1]

def test_owner_renounce(RSVP_Event_module_scope, accounts):
    RSVP_Event_module_scope.renounceOwnership({'from':accounts[1]})
    assert RSVP_Event_module_scope.owner() == brownie.ZERO_ADDRESS