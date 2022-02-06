// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Faucet {

    uint256 constant faucetAmount = 1 ether;
    mapping(address => bool) private receivedAddress;

    function addMoney() public payable returns(uint256) {
        return address(this).balance;
    }

    function getMoney(address payable receiver) public {

        require(receiver == msg.sender, "Your account only");

        if (receivedAddress[receiver]) {
            revert(":(");
        }
        receiver.transfer(faucetAmount);
        receivedAddress[receiver] = true;
    } 


}