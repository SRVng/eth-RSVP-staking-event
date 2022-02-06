// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

interface IEVT {
    function mint(address receiver,uint256 amount) external returns(uint256 amount_minted);
    function burn(uint256 n) external returns(uint256 amount_burned);
    function swap() external payable;
    function pay() external payable;
}