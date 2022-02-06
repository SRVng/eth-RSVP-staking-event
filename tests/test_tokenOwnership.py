import brownie, pytest

def test_owner(Token_module_scope, accounts):
    assert Token_module_scope.owner() == accounts[0]

def test_owner_transfer(Token_module_scope, accounts):
    Token_module_scope.transferOwnership(accounts[1], {'from':accounts[0]})
    assert Token_module_scope.owner() == accounts[1]

def test_owner_renounce(Token_module_scope, accounts):
    Token_module_scope.renounceOwnership({'from':accounts[1]})
    assert Token_module_scope.owner() == brownie.ZERO_ADDRESS