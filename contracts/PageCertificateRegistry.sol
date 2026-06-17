// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract PageCertificateRegistry {
    struct Certificate {
        bytes32 certHash;
        uint16 scoreBps;
        uint16 thresholdBps;
        address curator;
        address evaluator;
        string pageId;
        uint256 timestamp;
    }

    mapping(bytes32 => Certificate) public certificates;

    event PageCertified(
        bytes32 indexed pageHash,
        bytes32 indexed certHash,
        uint16 scoreBps,
        uint16 thresholdBps,
        address indexed curator,
        address evaluator,
        string pageId,
        uint256 timestamp
    );

    function certifyPage(
        string calldata pageId,
        bytes32 pageHash,
        bytes32 certHash,
        uint16 scoreBps,
        uint16 thresholdBps,
        address evaluator
    ) external {
        require(scoreBps <= 10000, "score out of range");
        require(thresholdBps <= 10000, "threshold out of range");
        certificates[pageHash] = Certificate({
            certHash: certHash,
            scoreBps: scoreBps,
            thresholdBps: thresholdBps,
            curator: msg.sender,
            evaluator: evaluator,
            pageId: pageId,
            timestamp: block.timestamp
        });
        emit PageCertified(pageHash, certHash, scoreBps, thresholdBps, msg.sender, evaluator, pageId, block.timestamp);
    }
}
