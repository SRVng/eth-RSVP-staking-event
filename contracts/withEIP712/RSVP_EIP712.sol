// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

abstract contract RSVP_EIP712 {
    struct BuyData {
        uint256 amount;
        address wallet;
    }

    struct CreateData {
        string name;
        uint256 until;
        address wallet;
    }

    struct RSVPData {
        string name;
        uint256 until;
        uint256 amount;
        address wallet;
    }

    struct EndEventData {
        string name;
        uint256 start;
        uint256 until;
        address owner;
        CreateData eventCreator;
    }

    bytes32 private constant BUY_TYPEHASH = keccak256("BuyData(uint256 amount,address wallet)");
    bytes32 private constant CREATE_TYPEHASH = keccak256("CreateData(string name,uint256 until,address wallet)");
    bytes32 private constant RSVP_TYPEHASH = keccak256("RSVPData(string name,uint256 until,uint256 amount,address wallet)");
    bytes32 private constant ENDEVENT_TYPEHASH = keccak256("EndEventData(string name,uint256 start,uint256 until,address owner,CreateData eventCreator)CreateData(string name,uint256 until,address wallet)");

    uint256 constant chainId = 43113;
    address verifyingContract = address(this);
    address constant salt = 0x790b47Bebe7e135887BAA1c9841048dC6Ca348Ed;

    string private constant EIP712_DOMAIN = "EIP712Domain(string name,string version,uint256 chainId,address verifyingContract,address salt)";

    bytes32 private DOMAIN_SEPERATOR = keccak256(abi.encode(
        keccak256(abi.encodePacked(EIP712_DOMAIN)),
        keccak256("RSVP Event"),
        keccak256("1"),
        chainId,
        verifyingContract,
        salt    
    ));

    function hashBuy(BuyData memory buy) private pure returns (bytes32) {
        return keccak256(abi.encode(
            BUY_TYPEHASH,
            buy.amount,
            buy.wallet
        ));
    }

    function hashCreate(CreateData memory create) private pure returns (bytes32) {
        return keccak256(abi.encode(
            CREATE_TYPEHASH,
            keccak256(bytes(create.name)),
            create.until,
            create.wallet
        ));
    }

    function hashRSVP(RSVPData memory rsvp) private pure returns (bytes32) {
        return keccak256(abi.encode(
            RSVP_TYPEHASH,
            keccak256(bytes(rsvp.name)),
            rsvp.until,
            rsvp.amount,
            rsvp.wallet
        ));
    }

    function hashEndEvent(EndEventData memory endevent) private pure returns (bytes32) {
        return keccak256(abi.encode(
            ENDEVENT_TYPEHASH,
            keccak256(bytes(endevent.name)),
            endevent.start,
            endevent.until,
            endevent.owner,
            hashCreate(endevent.eventCreator)
        ));
    }

    function verifyBuy(address signer, BuyData memory buy,uint8 v,bytes32 r,bytes32 s) public view returns (bool) {
        bytes32 digest = keccak256(abi.encodePacked(
            "\x19\x01",
            DOMAIN_SEPERATOR,
            hashBuy(buy)
        ));
        return signer == ecrecover(digest, v, r, s);
    }
    function verifyCreate(address signer, CreateData memory create,uint8 v,bytes32 r,bytes32 s) public view returns (bool) {
        bytes32 digest = keccak256(abi.encodePacked(
            "\x19\x01",
            DOMAIN_SEPERATOR,
            hashCreate(create)
        ));
        return signer == ecrecover(digest, v, r, s);
    }
    function verifyRSVP(address signer, RSVPData memory rsvp,uint8 v,bytes32 r,bytes32 s) public view returns (bool) {
        bytes32 digest = keccak256(abi.encodePacked(
            "\x19\x01",
            DOMAIN_SEPERATOR,
            hashRSVP(rsvp)
        ));
        return signer == ecrecover(digest, v, r, s);        
    }
    function verifyEndEvent(address signer, EndEventData memory endevent,uint8 v,bytes32 r,bytes32 s) public view returns (bool) {
        bytes32 digest = keccak256(abi.encodePacked(
            "\x19\x01",
            DOMAIN_SEPERATOR,
            hashEndEvent(endevent)
        ));
        return signer == ecrecover(digest, v, r, s);
    }

    function splitSignature(bytes memory signature) internal pure returns (uint8 v, bytes32 r, bytes32 s) {

        assembly {
            r := mload(add(signature, 32))
            s := mload(add(signature, 64))
            v := byte(0, mload(add(signature, 96)))
        }

        return (v,r,s);
    }
}
