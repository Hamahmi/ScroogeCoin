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
  * [Quick Overview](#quick-overview)
  * [Detailed Overview](#detailed-overview)
- [Example for output](#example-for-output)
- [Libraries Used](#libraries-used)


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

Scrooge then verifies the signature and verify that the coins in the transaction really belongs to the sender and not been spent before. If verified, Scrooge adds the transaction to a block under construction. Double spending can only happen before the transaction is published. We print the transactions' details for each new transaction, if the transaction is not valid it won't be added and the reason will be printed, however if the transaction indeed is valid, the block under construction will be printed with the IDs of the transactions in it.

If the block under construction reaches 10 transactions, scrooge creates a block and sign it, and add it to the blockchain. We print the blockchain for each new block added.

**Notes*:
  - Accourding to piazza I can include only 1 coin in each transaction -which I did but can be improved to add more than 1 coin in each transaction-, therefore, don't be surprised when you find the blockchain huge (1k transactions for creating the coins and giving them to users i.e. 100 blocks initially)
  - Again accourding to piazza, the ID of the transaction and the block is the hash of them, however, there's a value for each of them called __counter, which is unique in all transactions/blocks.

# Output Format
_A sample output.txt is included (generated using any of the next commands : `python ScroogeCoin.py` or `python ScroogeCoin.py -d` or `python ScroogeCoin.py -n output` or `python ScroogeCoin.py -n output.txt` or any compinations of the mentioned flages._

## Quick Overview
- User
```
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
```
- Transaction
```
------------------------------------------------
```
- Invalid Transaction
```
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
- Block under construction
```
################################################
```
- The Blockchain
```
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
```


## Detailed Overview
**Values inside `{}` are variable.**
- User Info (printed after the transactions for the 10 coins for all users are made) :
```
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
User {user count (not the id as we use the public key as ID)}

User's public key : {hex representation of the public key}
PEM format :
-----BEGIN PUBLIC KEY-----
{PEM representation of the public ke}
-----END PUBLIC KEY-----

Amount of coins this user has : {number of coins} coins.
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
```
- Transaction (printed for each transaction) :
    - for newly generated coins by Scrooge (only printed if -i (--initial ) is used ):
        ```
        ------------------------------------------------
        Trans ID	: {TransactionID}
        Sender		: Scrooge *COINBASE (Newly Generated Coins)*
        Receiver	: {Receiver's Public key}
        Amount		: {AmountOfCoins} SC
        CoinsIDs	: [ {CoinID for all the coins in the transaction} ]
        ------------------------------------------------
        ```
    - for transactions from sender to receiver :
        ```
        ------------------------------------------------
        Trans ID	: {TransactionID}
        Prev Trans	: {Hashpointer to the previous Transaction}
        Sender		: {Sender's Public key}
        Receiver	: {Receiver's Public key}
        Amount		: {AmountOfCoins} SC
        CoinsIDs	: [ {CoinID for all the coins in the transaction} ]
        ------------------------------------------------
        ```
    - for invalid transactions (double spending or invalid transaction or etc ..) :
        ```
        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        Invalid transaction due to {The Reason (e.g. "double spending problem")}!
        ------------------------------------------------
        Trans ID	: {TransactionID}
        Prev Trans	: {Hashpointer to the previous Transaction}
        Sender		: {Sender's Public key}
        Receiver	: {Receiver's Public key}
        Amount		: {AmountOfCoins} SC
        CoinsIDs	: [ {CoinID for all the coins in the transaction} ]
        ------------------------------------------------
        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

        ```
- Block under construction (printed when a new transaction is added):
```
################################################
A new transaction added !
Block under construction :
Transaction_0 : {TransactionID}
Transaction_1 : {TransactionID}
.
.
.
################################################
```

- The Blockchain (printed when a new block is added to the blockchain) :
```
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A new block appended !
The current blockchain :
<--( BlockID : {BlockID} || Block Transactions' IDs : [ {BlockTransIDs} ])
<--( BlockID : {BlockID} BlockHash : {BlockHash} || Block Transactions' IDs : [ {BlockTransIDs} ])
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

User's public key : 153e1f83ee2fb667cdb5cd90283624b1e846b2255fc5b5fe26466ae3a490b0680813136a304e6452dcad463cde262ce3
PEM format :
-----BEGIN PUBLIC KEY-----
MEkwEwYHKoZIzj0CAQYIKoZIzj0DAQEDMgAEFT4fg+4vtmfNtc2QKDYksehGsiVf
xbX+JkZq46SQsGgIExNqME5kUtytRjzeJizj
-----END PUBLIC KEY-----

Amount of coins this user has : 10 coins.
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
.
.
.
########  Starting random transactions  ########
########  To stop press the key 'Space' ########
------------------------------------------------
Trans ID	: 2210b82e47047e70726afafc637dfa24672c68ce73afd517db64f13aec561484
Prev Trans	: 4878ad9ac4a9ce3efedf4bb9e1b4d4d1200ad3a5f94504e62542cf7d925ee88e
Sender		: 01cbd6232f7e31fbf43d48c6e4721f0e8e84df3cbd76aa4e32f009e4fbe425b86cd66cd7cd677debde8eee3e5d93ee13
Receiver	: e2367bca982cb5d110a80def7421a4a9a3fb23e8c4c888c5843af46bbdfbb96ffc1beb121d6ab29ad1d88cb91be96124
Amount		: 1 SC
CoinsIDs	: [ e4f8c5463854e835c9afbba7c8028b378e69b21554d69b8e72af232183b87166 ]
------------------------------------------------

################################################
A new transaction added !
Block under construction :
Transaction_0 : 2210b82e47047e70726afafc637dfa24672c68ce73afd517db64f13aec561484
################################################
.
.
.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A new block appended !
The current blockchain :
<--( BlockID : 88de4c7c10ae5737dfe665f1ef3e0a8babb32db1f9459b5dbe97fb24fdc4e9cb || Block Transactions' IDs : [ b7e9610bdc1a18aeba630f353e2898805dc4ece1bea3f7b6d5c7c10b0d6af512, 9edb395427a14bd3c7a2cbd4c1d1b0ed17e85ee84b136be767f97ed4649318ac, d9a2ad1b7f32785feba2b216c235dead834109a4df42454b4beb97bd503fe843, 187c1ed97bdf0abbeac0ec927049d6b5934fc4f41352918bf22a873f5ad292a9, ab8c9eaf86bb45013cb7224b8985448a26ec3131b3403f17875b5e926569f7fe, 988c65bed443c34366851ba12aeb5da712afa1d9808d17776a2cc28fdf3f4dd4, c4c217dd4bfeb562edf5f9fe5beff2112d0c01952580820200be1d38ff18d753, b9baf67b3a3cc784ed513f494f2fdfdfb6e4baa7dbd5730320e051fa1231ef4b, 1b53ff3745d82eb8f81d762a8d8eb6cc9f43c26d45068f0a781e6ba1bf9efb5b, 47bc1075623e95f3a11acfccbc2ed10ddaa45205d77143179ee028d7b0491c48 ] )
.
.
.
<--(Previous block : 31ed4b6a9742f89dbfaf9a499aeb78c84ccefc49dc85fe7856daf78657d2de77 BlockID : dff41dfb0c37897c4229d96739625d848442711fe639b2b4f8cef77995d62453 || Block Transactions' IDs : [ 2210b82e47047e70726afafc637dfa24672c68ce73afd517db64f13aec561484, 680eb25b2267732a54d5a7381b1179a2bdfca76615eb5418af9d187aa3b26009, b70660eaba3f2def4dff2011d50c7530ea7b778bf1e46ae4df730e92d3c042ae, 171b07ec3f69b82140ec6d27886efcab11951bdc0f2e134ba4baff46e044b031, 8db8d907d8864726a1b4ac4af9de9503097d4f718e676a0f3db4ca5acc8c0ade, bc939ef2ce7f495ae5204275c56be110e8aa2c2a785981ae6cfb081480e8b2bc, 6bf99abb5f74e3fa79436ce49ac2d702c0e33493d282c24e28b810192d4a8bd8, 3094df85d257304c1e692dcc9670640bf1daad2480a20f9986eb8d99d995db8b, ce655cb3b35ce2978e641ccfda14830500b3c4147c4516a029c2f894d148839a, fbf35893e5274bcbb59e56647bfe2e5d9da52fd0b115830afb40b325c3fcc751 ] )
<-- ( Final H() : dff41dfb0c37897c4229d96739625d848442711fe639b2b4f8cef77995d62453 , signature : 6136ba634a7b47ab99109fcfa6aa381f484aea3d67ffae6a48a2d83357f22927ebf871a7fd5595df0cbf6ef08903ef50
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.
.
.

------------------------------------------------
Trans ID	: 26f4de7e5c47212f695e666ae3a76053ac9c85e74dba05f2b35210e362a1e5a0
Prev Trans	: 0271cb130d92fc94170f3f09a92b1add38ebff3461729a44ca2ef11f5589a5db
Sender		: 0e52ca011c73ae94b0c812e575fdaa6a141d3d1d812bbc98a44f4e768f298c20600bd94cd287a6ee67d0dae4d6219bcd
Receiver	: d32824459de17d9410abf74c0febab84abb3a58c767c3d07f4b358da5c9bce95e8fbf36a0d115099ea36726e612a43ca
Amount		: 1 SC
CoinsIDs	: [ b077b3c80787c780bb7ec9036abe6d17eda906bc70decab90f2605302b699168 ]
------------------------------------------------

################################################
A new transaction added !
Block under construction :
Transaction_0 : 0eab7a0157f606225f2bea76432eeae97aa71a99ebc206e1eac6dd70f58bd7ef
Transaction_1 : 8ad4fc65072796026234c665e152e6ef7be1966038372b26337e055e00b143d5
Transaction_2 : 0a62f743ad2372d217cf591a9233d8293b1d3a9a51a6e08d9e7f11c5ac559c0f
Transaction_3 : 26f4de7e5c47212f695e666ae3a76053ac9c85e74dba05f2b35210e362a1e5a0
################################################

xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Invalid transaction due to double spending problem!
------------------------------------------------
Trans ID	: 4ae9869ce0eea05d148b772d009f5badc5380db3304aa23b496bf2151cca387b
Prev Trans	: 0271cb130d92fc94170f3f09a92b1add38ebff3461729a44ca2ef11f5589a5db
Sender		: 0e52ca011c73ae94b0c812e575fdaa6a141d3d1d812bbc98a44f4e768f298c20600bd94cd287a6ee67d0dae4d6219bcd
Receiver	: 002589cb167ad6f12fc158657f758a2d8145e125791a71e7ef6e867b0d557108aa88f4bd9e909602e6c30c1fa8e91a68
Amount		: 1 SC
CoinsIDs	: [ b077b3c80787c780bb7ec9036abe6d17eda906bc70decab90f2605302b699168 ]
------------------------------------------------
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

------------------------------------------------
Trans ID	: 54beca29ba618b039ca6416aa2210a184bfefdd11a4e4801aa2c76cc3d72d601
Prev Trans	: c8cdcfe5b39ec85332e1bdbf34afa458511753995ded8575b02bac9ecfebbaf9
Sender		: 4a18a2a341de48c1c3af474cd289cfe9dc9f764ee3630fadda63b30ae9855f5e49ac859cca2e8c290b4ef125646daf17
Receiver	: 3f97c7496fc6c7d22b18afc872667548aae43920d63d2fb0ed9371b64d6ade69edccf7e5ae3db5bd1df10ecf3915af41
Amount		: 1 SC
CoinsIDs	: [ 8ceaa9d8152c2682170503e3e93d2b8d7d4b59d902a536261a84aa0615357e92 ]
------------------------------------------------

################################################
A new transaction added !
Block under construction :
Transaction_0 : 0eab7a0157f606225f2bea76432eeae97aa71a99ebc206e1eac6dd70f58bd7ef
Transaction_1 : 8ad4fc65072796026234c665e152e6ef7be1966038372b26337e055e00b143d5
Transaction_2 : 0a62f743ad2372d217cf591a9233d8293b1d3a9a51a6e08d9e7f11c5ac559c0f
Transaction_3 : 26f4de7e5c47212f695e666ae3a76053ac9c85e74dba05f2b35210e362a1e5a0
Transaction_4 : 54beca29ba618b039ca6416aa2210a184bfefdd11a4e4801aa2c76cc3d72d601
################################################
.
.
.
############  Terminating the code  ############
## Saving all the printed data to a text file ##
```
*Note : in the invalid transaction you can see clearly why it is a double spending problem, the user tried to spend the same coin twice, and the previous transaction was in the block under construction with the same coin, thus Scrooge marked the new transaction as invalid and ignored it.*
- With using -i (to print initial transactions of created coins details):
```
###############      Start       ###############
###############  Creating coins  ###############
------------------------------------------------
Trans ID	: b7e9610bdc1a18aeba630f353e2898805dc4ece1bea3f7b6d5c7c10b0d6af512
Sender		: Scrooge *COINBASE (Newly Generated Coins)*
Receiver	: 153e1f83ee2fb667cdb5cd90283624b1e846b2255fc5b5fe26466ae3a490b0680813136a304e6452dcad463cde262ce3
Amount		: 1 SC
CoinsIDs	: [ 47b60a8814151101a1bfaefcfb69e14718e5dcc091dec780375c1f8dd7a8ca93 ]
------------------------------------------------

################################################
A new transaction added !
Block under construction :
Transaction_0 : b7e9610bdc1a18aeba630f353e2898805dc4ece1bea3f7b6d5c7c10b0d6af512
################################################
.
.
.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A new block appended !
The current blockchain :
<--( BlockID : 88de4c7c10ae5737dfe665f1ef3e0a8babb32db1f9459b5dbe97fb24fdc4e9cb || Block Transactions' IDs : [ b7e9610bdc1a18aeba630f353e2898805dc4ece1bea3f7b6d5c7c10b0d6af512, 9edb395427a14bd3c7a2cbd4c1d1b0ed17e85ee84b136be767f97ed4649318ac, d9a2ad1b7f32785feba2b216c235dead834109a4df42454b4beb97bd503fe843, 187c1ed97bdf0abbeac0ec927049d6b5934fc4f41352918bf22a873f5ad292a9, ab8c9eaf86bb45013cb7224b8985448a26ec3131b3403f17875b5e926569f7fe, 988c65bed443c34366851ba12aeb5da712afa1d9808d17776a2cc28fdf3f4dd4, c4c217dd4bfeb562edf5f9fe5beff2112d0c01952580820200be1d38ff18d753, b9baf67b3a3cc784ed513f494f2fdfdfb6e4baa7dbd5730320e051fa1231ef4b, 1b53ff3745d82eb8f81d762a8d8eb6cc9f43c26d45068f0a781e6ba1bf9efb5b, 47bc1075623e95f3a11acfccbc2ed10ddaa45205d77143179ee028d7b0491c48 ] )
<-- ( Final H() : 88de4c7c10ae5737dfe665f1ef3e0a8babb32db1f9459b5dbe97fb24fdc4e9cb , signature : 6190a8a437e5fff8534007dce5f96752ea15281800df85549d9c8737a715fe3f710403d070378949e28e30c4c56eb916
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.
.
.
The rest is the same as without usin -i
```

# Libraries Used
- [ArgumentParser](https://docs.python.org/3/library/argparse.html) : To get command-line options such as -i, --dontprint, etc .
- [ecdsa](https://github.com/warner/python-ecdsa) : To generate public-private-key pairs and for digital signature.
- [hashlib](https://docs.python.org/3/library/hashlib.html) : To hash values suing `sha256`.
- [random](https://docs.python.org/3/library/random.html) : To generate random values (ecdsa actually uses os.urandom but we used random for random values other than those handled by ecdsa).
- [keyboard](https://github.com/boppreh/keyboard) : To listen to keyboard input from the user (used here just to detect the space key pressed in order to terminate the code).