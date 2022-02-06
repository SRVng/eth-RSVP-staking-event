//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import '@openzeppelin/contracts/access/Ownable.sol';
import '@openzeppelin/contracts/utils/Counters.sol';
import '@openzeppelin/contracts/utils/math/SafeMath.sol';
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract CreatorERC721 is ERC721, Ownable {
    using SafeMath for uint256;
    using Counters for Counters.Counter;

    Counters.Counter private _tokenIds;

    uint public constant MAX_SUPPLY = 1;

    constructor() ERC721("RSVPCreator", "RSVP") {
        _mintSingleNFT();
    } 

    function _mintSingleNFT() private {
        uint newTokenID = _tokenIds.current();
        _safeMint(address(this), newTokenID);
        _tokenIds.increment();
    }

    function setApprovalForContract(address operator, bool approved) external {
        _setApprovalForAll(address(this),operator, approved);
    }

    function setApprovalForCreator(address creator, address _contract, bool approved) external {
        _setApprovalForAll(creator, _contract, approved);
    }
}