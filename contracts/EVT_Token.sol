// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

import '@openzeppelin/contracts/token/ERC20/ERC20.sol';
import '@openzeppelin/contracts/utils/math/SafeMath.sol';
import '@openzeppelin/contracts/access/Ownable.sol';

import '../interfaces/IEVT.sol';

contract EVT_Token is IEVT,ERC20('EVENT','EVT'), Ownable {
    using SafeMath for uint256;

    constructor (uint256 initial_mint) {
        mint(address(this), initial_mint);
    }

    //Primary ERC20 Function
    
    function mint(address receiver, uint256 amount) public onlyOwner returns (uint256 amount_minted) {
        _mint(receiver, amount);
        emit Minted("Token minted");
        return amount;
    }

    function burn(uint256 n) public onlyOwner returns (uint256 amount_burned) {
        _burn(address(this), n);
        return n;
    }

    function approveFromContract(address owner,address spender, uint256 amount) public returns(bool) {        
        _approve(owner, spender, amount);
        return true;
    }

    //Other function

    function swap() public payable {
        uint256 evt_price = 0.01 ether;
        _transfer(address(this),msg.sender,msg.value.div(evt_price).mul(1e18));
    }

    function pay() public payable {}
    
    //Event
    event Minted(string Description);
    event Distributed(string Description);
    
}

