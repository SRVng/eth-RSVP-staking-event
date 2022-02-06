//SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

import './RSVP_Event.sol';
import '@openzeppelin/contracts/token/ERC20/ERC20.sol';
import './EVT_Token.sol';
import '@openzeppelin/contracts/utils/math/SafeMath.sol';

abstract contract Staking {
    using SafeMath for uint256;
    
    //State Variables
    RSVP_Event rsvp_contract;
    EVT_Token public evt;
    uint256 public reward_rate_per_sec = 1;
    uint256 public constant checked_in_period = 1 hours; //for testing purpose
    uint256 public _total_stake; // Using this instead of balanceOf(address(this))
    uint256 public _unclaimed_reward;
    
    //Array
    address[] internal isStaking; //alias: Whitelist, so we know who are currently staking
    address[] internal Checked; //save the address of users that checked-in
    
    uint[] internal timestamps; //Timestamp for everytime the total staked is added
    
    //Mapping address with some uint that needed for staking
    mapping(address => staking_details) stake; //Staking detail of each users
    mapping(address => uint256) staking_reward; //This keep the reward of each users
    mapping(uint256 => uint256) totalstakeAt; //For reward calculation based on totalstake
    mapping(address => bool) stake_once; //This allow users to stake only once
    
    //Create struct to keep the detail of depositor
    struct staking_details {
        uint256 stake_amount_rounded;
        uint256 stake_amount_digits;
        uint256 time;
        uint256 time_end;
    }

    //Constructor
    constructor(EVT_Token _evt) {
        rsvp_contract = RSVP_Event(address(this));
        evt = _evt;
    }
    
    ////////////////////////////////////////////////////////// Function for Whitelist /////////////////////////////////////////////////////////////////////////////////////////////////
    
    function Whitelist() public view returns(address[] memory) {
        return isStaking;
    }
    
    function Whitelist_Check(address _address) private view returns(bool, uint index) {
        for(uint256 id = 0; id < isStaking.length; id += 1) {
            if (isStaking[id] == _address) return(true,id);
        }
        return(false,0);
    }
    
    function addWhitelist(address _stakeholder) private {
       (bool _Whitelist, ) = Whitelist_Check(_stakeholder);
        if(_Whitelist == false) isStaking.push(_stakeholder);
        emit LogWhitelist(_stakeholder,"Given address is now staking");
    }
    
    function removeWhitelist(address _stakeholder) private {
        (bool _Whitelist,uint id) = Whitelist_Check(_stakeholder);
        if (_Whitelist == true) {
            isStaking[id] = isStaking[isStaking.length-1];
            isStaking.pop();
        }
        emit LogWhitelist(_stakeholder,"Given address unstaked");
    }
    
    ////////////////////////////////////////////////////////// Function for Staking /////////////////////////////////////////////////////////////////////////////////////////////////
    
    function Stake_Check(address _stakeholder) public view returns(uint256 amount_digits,uint256 amount_rounded,uint256 time) {
        (bool _Whitelist,) = Whitelist_Check(_stakeholder);
        if(_Whitelist == true) return (stake[_stakeholder].stake_amount_digits, stake[_stakeholder].stake_amount_rounded ,stake[_stakeholder].time);
        else revert();
    }
    
    function total_stake() public view returns(uint256 totalstake_digits, uint256 totalstake_rounded) {
        return (_total_stake, _total_stake.div(1e18));
    }
    
    function deposit_stake(uint256 _stake) internal {
        require(stake_once[msg.sender] == true, "You can stake only once");
        require(evt.balanceOf(tx.origin) >= _stake.mul(1e18) && _stake != 0, "Not enough balance to stake");
        require(stake[msg.sender].stake_amount_rounded == 0, "You can join the event only once");
        
        uint256 _stake_digits = (_stake.mul(1e18));
        uint256 time_end = rsvp_contract.end_time();
        
        addWhitelist(msg.sender);
        _total_stake = _total_stake.add(_stake_digits);
        
        evt.approveFromContract(tx.origin, address(this), _stake_digits);
        evt.transferFrom(tx.origin,address(this), _stake_digits);
        stake[msg.sender] = staking_details(_stake,_stake_digits,block.timestamp,time_end);
        
        timestamps.push(block.timestamp);
        (uint256 digits ,) = total_stake();
        totalstakeAt[block.timestamp] = digits;
        
        stake_once[msg.sender] = false;
        emit LogStake(_stake,msg.sender,"RSVP... Staking...");
    }

    function checkBalance() public {
        emit LogReward(evt.balanceOf(tx.origin), tx.origin, "EVT balance");
    }

    function allowance_check(address owner, address spender) public returns(uint256) {
        return evt.allowance(owner, spender);
    }
    
    function withdraw_stake() internal UpdateReward() {
        (bool _Whitelist,) = Whitelist_Check(msg.sender);
        require(stake[msg.sender].stake_amount_rounded != 0 && _Whitelist == true, "You can't remove stake if you didn't joined the event...");
        require((block.timestamp > stake[msg.sender].time_end  && block.timestamp <= (stake[msg.sender].time_end + checked_in_period)),
                "Please wait for check-in period");
        
        emit LogStake((stake[msg.sender].stake_amount_rounded+staking_reward[msg.sender]),msg.sender,"Unstaking...");
        
        withdraw_reward();
        removeWhitelist(msg.sender);
        
        evt.approveFromContract(address(this),tx.origin,stake[msg.sender].stake_amount_digits);
        evt.transferFrom(address(this),tx.origin,stake[msg.sender].stake_amount_digits);
        _total_stake = _total_stake.sub(stake[msg.sender].stake_amount_digits);
        
        stake[msg.sender] = staking_details(0,0,0,0);
        
        Checked.push(msg.sender);
    }
    
    ////////////////////////////////////////////////////////// Function for Rewards /////////////////////////////////////////////////////////////////////////////////////////////////
    
    function reward_calc() internal {
        
        uint256 time_end = rsvp_contract.end_time();
        uint256 block_distance;
        
        for(uint256 id = 0; id < isStaking.length; id += 1) {
                
            address _stakeholder = isStaking[id];
            staking_reward[_stakeholder] = 0;

            if(block.timestamp < time_end) block_distance = block.timestamp - stake[_stakeholder].time;
            if(block.timestamp >= time_end) block_distance = time_end - stake[_stakeholder].time;
            for(uint256 time = 0; time < timestamps.length; time += 1) {
                uint256 t = timestamps[time];
                staking_reward[_stakeholder] = staking_reward[_stakeholder].add(
                    reward_rate_per_sec.mul(stake[_stakeholder].stake_amount_digits).mul(block_distance).div(100).div(totalstakeAt[t])
                    );
                } 
            }
    }    
    
    function total_unclaimed_reward() public UpdateReward() returns (uint256 unclaimed_with_digits, uint256 unclaimed_rounded) {
        _unclaimed_reward = 0;
        uint256 id = 0;
            while (id < isStaking.length) {
                _unclaimed_reward = _unclaimed_reward.add(staking_reward[isStaking[id]]);
                id += 1;
            }
        return (_unclaimed_reward, _unclaimed_reward.div(1e18));
    }
    
    function Reward_Check() public UpdateReward() returns (uint256 your_reward_with_digits, uint256 your_reward_rounded) {
        require(stake[msg.sender].stake_amount_rounded != 0, "No stake balances");
        return (staking_reward[msg.sender], staking_reward[msg.sender].div(1e18));
    }
    
    
    //People that participate and decrease their risk by claiming the reward before the event but the reward is halved.
    function withdraw_reward() public UpdateReward() {
        require(staking_reward[msg.sender] != 0, "No Reward");
        
        if (block.timestamp < stake[msg.sender].time_end) {
            evt.mint(tx.origin,staking_reward[msg.sender].div(2));
            stake[msg.sender].time = block.timestamp; //This is a reset button for reward calculation
            emit LogReward(staking_reward[msg.sender].div(2).div(1e18), msg.sender, "Rewarded");
        }
        if (block.timestamp > stake[msg.sender].time_end  && block.timestamp <= (stake[msg.sender].time_end + checked_in_period)) {
            evt.mint(tx.origin,staking_reward[msg.sender]);
            emit LogReward(staking_reward[msg.sender].div(1e18), msg.sender, "Rewarded");
        }
        
        staking_reward[msg.sender] = 0;
    }
    
    function reward_share() internal returns(uint256 _digits,uint256 _rounded) {
        //require(EventCreator[msg.sender] == true, "The Creator only");
        (uint256 digits , uint256 rounded) = total_unclaimed_reward();
        if (Checked.length != 0) {
            digits = digits.div(Checked.length);
            rounded = rounded.div(Checked.length);
            emit LogEventEnd(rounded, "Participant that checked in will recieve this shared unclaimed reward");
            
            for (uint checked_id = 0; checked_id < Checked.length; checked_id += 1) {
                 evt.approveFromContract(address(this),Checked[checked_id],digits);
                 evt.transferFrom(address(this),Checked[checked_id],digits);
                
            }
        }
        
        if (isStaking.length != 0) {
            for (uint id = 0; id < isStaking.length; id += 1) {
            
                staking_reward[isStaking[id]] = 0;
                evt.approveFromContract(address(this),isStaking[id],(9 * (stake[isStaking[id]].stake_amount_digits / 10)));
                evt.transferFrom(address(this),isStaking[id],(9 * (stake[isStaking[id]].stake_amount_digits / 10)));
                _total_stake = _total_stake.sub(stake[isStaking[id]].stake_amount_digits);

                stake[isStaking[id]] = staking_details(0,0,0,0);
                
            
            }
        }
        
        delete Checked;
        delete isStaking;
        delete timestamps;
        delete _unclaimed_reward;

        return (digits, rounded);
    }
    
    //Modifier
    modifier UpdateReward() {
        reward_calc();
        _;
    }
    
    //Event
    event LogWhitelist(address _stakeholder, string description);
    event LogStake(uint256 value, address depositor, string description);
    event LogReward(uint256 reward,address depositor, string description);
    event LogEventEnd(uint256 unclaimed_reward, string description);
}