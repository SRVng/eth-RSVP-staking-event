// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

import '@openzeppelin/contracts/token/ERC20/ERC20.sol';
import '@openzeppelin/contracts/utils/math/SafeMath.sol';
import '@openzeppelin/contracts/access/Ownable.sol';

contract EVT_Token is ERC20, Ownable {
    using SafeMath for uint256;
    
    //Create a ERC-20 token
    constructor() ERC20("EVENT", "EVT") {}

    //Primary ERC20 Function
    
    function mint(uint256 n) public onlyOwner returns (uint256 amount_minted) {
        _mint(address(this), n.mul(1e18));
        emit Minted("Token minted");
        return n;
    }

    function burn(uint256 n) public onlyOwner returns (uint256 amount_burned) {
        _burn(address(this), n.mul(1e18));
        return n;
    }

    function EVT_totalSupply() public view returns (uint256) {
        return totalSupply().div(1e18);
    }

    function EVT_balanceOf(address account) public view returns (uint256) {
        return balanceOf(account).div(1e18);
    }

    //Other function

    function swap() public payable {
        uint256 evt_price = 0.01 ether;
        _transfer(address(this),msg.sender,msg.value.div(evt_price).mul(1e18));
    }

    function pay()  payable public {}
    
    //Event
    event Minted(string Description);
    event Distributed(string Description);
    
}

