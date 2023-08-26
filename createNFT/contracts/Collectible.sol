// An NFT Contract
// Where the tokenURI can be one of 3 different dogs
// Randomly selected

// SPDX-License-Identifier: MIT
pragma solidity 0.8.0;

import "node_modules/@chainlink/contracts/src/v0.8/interfaces/LinkTokenInterface.sol";
import "node_modules/@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "node_modules/@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "node_modules/@openzeppelin/contracts/utils/Strings.sol";


contract NFT is ERC721URIStorage{
    LinkTokenInterface internal immutable LINK;
    using Strings for uint256;
    uint256 public tokenCounter;
    string private _baseURIextended;
    mapping (uint256  => string) public _tokenURIs;
	  mapping(uint256 => address) TokenOwners;
    event requestedCollectible(uint256 TokenId_, address requester);

  
