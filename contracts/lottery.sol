//SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";

contract lottery is VRFConsumerBase, Ownable {
    address payable[] public players;
    uint256 public minimumUSD;
    bytes32 public keyHash;
    uint256 public fee;

    uint256 randomness;
    AggregatorV3Interface public priceFeed;
    LOTTERY_STATE public lottery_state;
    enum LOTTERY_STATE {
        CLOSED,
        OPEN,
        CALCULAING_WINNER
    }

    constructor(
        address _priceFeed,
        address _vrfAddress,
        address _link,
        bytes32 _keyHash,
        uint256 _fee
    ) public VRFConsumerBase(_vrfAddress, _link) {
        minimumUSD = 50 * 10**18;
        priceFeed = AggregatorV3Interface(_priceFeed);
        lottery_state = LOTTERY_STATE.CLOSED;
        keyHash = _keyHash;
        fee = _fee;
    }

    function enter() public payable {
        require(
            lottery_state == LOTTERY_STATE.OPEN,
            "Lottery is not open yet!"
        );
        require(msg.value > minimumValue(), "Not Enough value!");
        players.push(payable(msg.sender));
    }

    function minimumValue() public view returns (uint256) {
        (, int256 price, , , ) = priceFeed.latestRoundData();
        uint256 adjPrice = uint256(price * 10**10);
        uint256 fee = (minimumUSD * 10**18) / adjPrice;
        return fee;
    }

    function start() public onlyOwner {
        require(
            lottery_state == LOTTERY_STATE.CLOSED,
            "Lottery can not be open yet!"
        );
        lottery_state = LOTTERY_STATE.OPEN;
    }

    function end() public onlyOwner returns (bytes32 requestId) {
        lottery_state = LOTTERY_STATE.CALCULAING_WINNER;
        bytes32 requestId = requestRandomness(keyHash, fee);
        //emit RequestRandomness(requestId);
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomness)
        internal
        override
    {
        require(lottery_state == LOTTERY_STATE.CALCULAING_WINNER);
        require(_randomness > 0, "Random number not found!");
        uint256 winner = _randomness % players.length;
        address payable recentWinner = players[winner];
        recentWinner.transfer(address(this).balance);
        players = new address payable[](0);
        lottery_state = LOTTERY_STATE.CLOSED;
        randomness = _randomness;
    }
}
