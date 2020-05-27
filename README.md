# ScroogeCoin
Design of a cryptocurrency similar to ScroogeCoin

### Table of Contents
- [The Main Idea](#the-main-idea)
- [How to use the code](#how-to-use-the-code)
- [Docs](#docs)
  * [Digital Signature](#digital-signature)
  * [Classes](#classes)
- [The Main Function](#the-main-function)
- [Output Format](#output-format)
- [Example for output](#example-for-output)


# The Main Idea
In this project, we will design a cryptocurrency similar to ScroogeCoin. A network of 100 users will simulate the transaction processes. Initially each user will have 10 ScroogCoins. As long as the system is running, a random transaction with random amount (within the range of amount the user has) will be created from User A to User B. The transaction is signed by the private-key of the sender. Scrooge get notified by every transaction. Scrooge verifies the signature before accumulating the transaction. Once Scrooge accumulates 10 transaction, he can form a block and attach it to the blockchain

# How to use the code
You can simply run
```
python ScroogeCoin.py
```
However, there are some optional parameters if you want :
```
python ScroogeCoin.py -h
usage: ScroogeCoin.py [-h] [--name NAME] [--dontprint] [--initial]

ScroogeCoin

optional arguments:
  -h, --help            show this help message and exit
  --name NAME, -n NAME  The output file name
  --dontprint, -d       If you don't want to print anything (and just save the
                        output in --name)
  --initial, -i         print the initial transactions (The ones where scrooge
                        creates the coins and pays the users)
```

- using `-n` Name to modify the output.txt name to be Name.txt (or whatever you want)
- using `-d` in order to stop printing to the console and just saving the output eventually to output.txt (**Note that the code runs much faster this way**)
- using `-i` prints the initial transactions where scrooge sends the coins to the users

# Docs
## Digital Signature
For digital signature the liberary
[Elliptic Curve Digital Signature Algorithm (Python-ecdsa)](https://github.com/warner/python-ecdsa) was used.
- `generate_keys()` generates a pair of public `ecdsa.VerifyingKey` and private keys `ecdsa.SigningKey`, with the default curve `NIST192p` (you can use any other curve, such as `BRAINPOOLP512r1`, but for the purpose of this demo and to be much faster with only 192 bits instead of 512 bits), and you can also specify the hashing function (the default was used `sha1`).
- `sign(private_key, message)` signs the string `message` with the `private_key`, returns an encoded signature of the hash of `message`.
- `verify_signature(public_key, message, signature)` given the `public_key`, the `message` and the `signature`, this function returns `True` if the signature is valid, and `False` otherwise.

## Classes
- `Coin` a class representing the ScroogeCoin with a CoinID for each coin.
- `User` a class representing the user, and the public-private-key pair along with the coins this user have for each user.
- `Transaction` a class representing the transaction, with the transaction ID, a hashpointer to the previous transaction, the coins in this transaction, and the sender's and the receiver's public keys.
- `Hash_Pointer` a class to simplify hashpointer as a pair of a hash and a pointer.
- `Block` a class representing the block in the blockchain, where each block consists of 10 transactions. Each block has an ID, 10 transactions, a hash of the block and a hashpointer to he previous block.
- `Scrooge` a class representing the designated entity “Scrooge”   that publishes an append-only ledger(The blockchain) that contains all the history of transactions.

# The Main Function
First, `Scrooge` object is created with its public-private-key pair, to handle the blockchain. A network of 100 `User`s is then created in order to simulate the transaction processes. `Scrooge` will then create 10 `Coin`s for each user and sign them, then create a transaction to each user with the 10 coins.

After transferring 10 coins for each user, we print the users' info (the public key (which we use as an ID for each user) and the amount of coins each user have (which will be 10)). And then we start an infinite loop with random transactions.

We pick 2 random users, a sender and a receiver (sender != receiver), to make a transaction with random amount of what the sender has to the receiver. Once a transaction is created it is signed by the sender's private key and scrooge gets notified.

Scrooge then verifies the signature and verify that the coins in the transaction really belongs to the sender and not been spent before. If verified, Scrooge adds the transaction to a block under construction. Double spending can only happen before the transaction is published. We print the block under construction along with the transactions' details for each new valid transaction added.

If the block under construction reaches 10 transactions, scrooge creates a block and sign it, and add it to the blockchain. We print the blockchain for each new block added.

**Notes*: 
  - Accourding to piazza I can include only 1 coin in each transaction -which I did but can be improved to add more than 1 coin in each transaction-, therefore, don't be surprised when you find the blockchain huge (1k transactions for creating the coins and giving them to users i.e. 100 blocks initially)
  - Again accourding to piazza, the ID of the transaction and the block is the hash of them, however, there's a value for each of them called __counter, which is unique in all transactions/blocks.

# Output Format
Values inside `{}` are variable.
- User Info (printed after the transactions for the 10 coins for all users are made) :
```
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
User {User count (not the id, since we use the public key as the id)}
-----BEGIN PUBLIC KEY-----
{User's public key}
-----END PUBLIC KEY-----

Amount of coins this user has : {Amount of coins (since the info is printed only initially the amount of coins for each user should be 10)} coins.
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
```
- Transaction (printed inside Block under construction) :
    - for newly generated coins by Scrooge (only printed if -i (--initial ) is used ):
        ```
        ------------------------------------------------
        Transaction {TransactionID}
        Hash : {TransactionHash}
        Sender : Scrooge *COINBASE (Newly Generated Coins)*
        Receiver : {Receiver's Public key}
        Amount : {AmountOfCoins} SC
        CoinID : {CoinID in the transaction}
        ------------------------------------------------
        ```
    - for transactions from sender to receiver :
        ```
        ------------------------------------------------
        Transaction {TransactionID}
        Hash : {TransactionHash}
        Previous Transaction Hashpointer : {hashpointer to the previous transaction}
        Sender : {Sender's Public key}
        Receiver : {Receiver's Public key}
        Amount : {AmountOfCoins} SC
        CoinID : {CoinID in the transaction}
        ------------------------------------------------
        ```
- Block under construction (printed when a new transaction is added):
```
################################################
A new transaction added !
Block under construction :
------------------------------------------------
{Transactions}
------------------------------------------------
################################################
```
- The Blockchain (printed when a new block is added to the blockchain) :
```
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A new block appended !
The current blockchain :
<--( BlockID : {BlockID} BlockHash : {BlockHash} || Block Transactions' IDs : {BlockTransIDs})
<--( BlockID : {BlockID} BlockHash : {BlockHash} || Block Transactions' IDs : {BlockTransIDs})
<--
.
.
.
<-- ( Final H() : {Hashpointer to the final block} , signature : {Scrooge's signature on the final hash pointer}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
```

# Example for output
Three dots (. . .) vertically means that the output is trimmed here.

- Without using -i :
```
###############      Start       ###############
###############  Creating coins  ###############
#############  Users' Initial Info  ############

$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
User 1
-----BEGIN PUBLIC KEY-----
MEkwEwYHKoZIzj0CAQYIKoZIzj0DAQEDMgAErUWvqzI8rZGbatx+j5sFYxFR09ut
7qUizLcW2O5SJCt6OxRARzecqc9WZn4297PZ
-----END PUBLIC KEY-----

Amount of coins this user has : 10 coins.
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
User 2
-----BEGIN PUBLIC KEY-----
MEkwEwYHKoZIzj0CAQYIKoZIzj0DAQEDMgAEykbmAY0xMfJmQ9DiBKeMb6CckcQj
AXInMSKolykp1GcOk5mpVnG1ZH2sphzXkdXC
-----END PUBLIC KEY-----

Amount of coins this user has : 10 coins.
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
.
.
.
########  Starting random transactions  ########
########  To stop press the key ‘Space’ ########
################################################
A new transaction added !
Block under construction :
------------------------------------------------
Transaction 1000
Hash : 843c29200cc1f73fccdb5a8be943d0f787705b1f3f50aa51e00768568f528515
Previous Transaction Hashpointer : d92a01570a8901182d76090bc2096a28370b428e5895069169b97365f4b9e09a
Sender : 1bf9a33f55a0519d6168b769c39d6219b4a4aa62d0972cebf6913db9e99c55c8ff50c486e37d9c3967f8e268dd284306
Receiver : 36b43948ff610c7c927d0ca8b308974164b4c73b52cd0d89eda84aa7e491076239b1a2bbbd9f50e0905d76b9cca3b854
Amount : 1 SC
CoinID : 990
------------------------------------------------
################################################
.
.
.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A new block appended !
The current blockchain :
<--( BlockID : 0 BlockHash : b10dfec9d5dfe0444beec76ef02667a9d4d4dedadcee920fed0b7b88674c1dbd || Block Transactions' IDs : 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
.
.
.
<--(PrevHash : 57e7f9320fbe288ea19032e37225f8fc2df93ee9b8b70e5c37ed6b05c57e6038 PrevID : 99 BlockID : 100 BlockHash : 1275df4592b45dca1a017c9b2f9048fd11b932c2911b07a361ad35ca2c4fafc3 || Block Transactions' IDs : 1000, 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009)
<-- ( Final H() : 1275df4592b45dca1a017c9b2f9048fd11b932c2911b07a361ad35ca2c4fafc3 , signature : c4b008873b8a6c3393637d219d11ecc0dfaff76c01557d3773e95b5c9038d3a372525ae96af1d3446f41cdae34f331f4
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
############  Terminating the code  ############
## Saving all the printed data to a text file ##
Output saved to output.txt
```

- With using -i :
```
###############      Start       ###############
###############  Creating coins  ###############
################################################
A new transaction added !
Block under construction :
------------------------------------------------
Transaction 0
Hash : 9ea86e581b8e9c81974dcfc8280ec83a2e527eedf91ff880ba741ca75cecf6b3
Sender : Scrooge *COINBASE (Newly Generated Coins)*
Receiver : b9332de2494a572eb72da59df65fc2169f3b8f4e8e4879cc767203b85f9192bafeedee23b9aa01becc74aa249b250961
Amount : 1 SC
CoinID : 0
------------------------------------------------
################################################
.
.
.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A new block appended !
The current blockchain :
<--( BlockID : 0 BlockHash : 8d9f3d58269710cac594415da8b2f813a2009a598026550c1d3d82970e992f33 || Block Transactions' IDs : 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
<--(PrevHash : 8d9f3d58269710cac594415da8b2f813a2009a598026550c1d3d82970e992f33 PrevID : 0 BlockID : 1 BlockHash : c98c783417c5ca8af3edde88699d45ed51823035dbdeb9f89a60aef1a1abba22 || Block Transactions' IDs : 10, 11, 12, 13, 14, 15, 16, 17, 18, 19)
<--(PrevHash : c98c783417c5ca8af3edde88699d45ed51823035dbdeb9f89a60aef1a1abba22 PrevID : 1 BlockID : 2 BlockHash : 50265f696e97d7e122046099edca171dd9e4780821e3ff9094c05ec8aea81a5d || Block Transactions' IDs : 20, 21, 22, 23, 24, 25, 26, 27, 28, 29)
<-- ( Final H() : 50265f696e97d7e122046099edca171dd9e4780821e3ff9094c05ec8aea81a5d , signature : 8eb5b5614b1524d2f899ea171874a3da35578573172e7d6c128ff2836fa54f6a9ea478a9850f6f8d3485733908055e3f
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.
.
.
#############  Users' Initial Info  ############

$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
User 1
-----BEGIN PUBLIC KEY-----
MEkwEwYHKoZIzj0CAQYIKoZIzj0DAQEDMgAEuTMt4klKVy63LaWd9l/CFp87j06O
SHnMdnIDuF+Rkrr+7e4juaoBvsx0qiSbJQlh
-----END PUBLIC KEY-----

Amount of coins this user has : 10 coins.
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
User 2
-----BEGIN PUBLIC KEY-----
MEkwEwYHKoZIzj0CAQYIKoZIzj0DAQEDMgAEIFwg4QKfznKIoPEZ83V3xTi7ssvr
2EwHv8oNJ1n9IamLmxDnkwx3ezlwMCsnETj7
-----END PUBLIC KEY-----

Amount of coins this user has : 10 coins.
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
.
.
.
########  Starting random transactions  ########
########  To stop press the key ‘Space’ ########
################################################
A new transaction added !
Block under construction :
------------------------------------------------
Transaction 1000
Hash : 843c29200cc1f73fccdb5a8be943d0f787705b1f3f50aa51e00768568f528515
Previous Transaction Hashpointer : d92a01570a8901182d76090bc2096a28370b428e5895069169b97365f4b9e09a
Sender : 1bf9a33f55a0519d6168b769c39d6219b4a4aa62d0972cebf6913db9e99c55c8ff50c486e37d9c3967f8e268dd284306
Receiver : 36b43948ff610c7c927d0ca8b308974164b4c73b52cd0d89eda84aa7e491076239b1a2bbbd9f50e0905d76b9cca3b854
Amount : 1 SC
CoinID : 990
------------------------------------------------
################################################
.
.
.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A new block appended !
The current blockchain :
<--( BlockID : 0 BlockHash : b10dfec9d5dfe0444beec76ef02667a9d4d4dedadcee920fed0b7b88674c1dbd || Block Transactions' IDs : 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
.
.
.
<--(PrevHash : 57e7f9320fbe288ea19032e37225f8fc2df93ee9b8b70e5c37ed6b05c57e6038 PrevID : 99 BlockID : 100 BlockHash : 1275df4592b45dca1a017c9b2f9048fd11b932c2911b07a361ad35ca2c4fafc3 || Block Transactions' IDs : 1000, 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009)
<-- ( Final H() : 1275df4592b45dca1a017c9b2f9048fd11b932c2911b07a361ad35ca2c4fafc3 , signature : c4b008873b8a6c3393637d219d11ecc0dfaff76c01557d3773e95b5c9038d3a372525ae96af1d3446f41cdae34f331f4
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
############  Terminating the code  ############
## Saving all the printed data to a text file ##
Output saved to output.txt
```