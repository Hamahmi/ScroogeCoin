# -*- coding: utf-8 -*-

__author__ = "Hamahmi"

from argparse import ArgumentParser

# You are allowed to use predefined hash and digital signature libraries.
# Mention which libraries you used. (sha256 for hashing, ecdsa for DS)
from hashlib import sha256
from random import randint, seed

# Elliptic Curve Digital Signature Algorithm
# https://github.com/warner/python-ecdsa
from ecdsa import SigningKey, VerifyingKey
from keyboard import is_pressed

parser = ArgumentParser(description="ScroogeCoin")
parser.add_argument(
    "--name", "-n", type=str, default="output", help="The output file name"
)
parser.add_argument(
    "--dontprint",
    "-d",
    dest="dontprint",
    action="store_true",
    help="If you don't want to print anything (and just save the output in --name)",
)
parser.add_argument(
    "--initial",
    "-i",
    dest="initial",
    action="store_true",
    help="print the initial transactions (The ones where scrooge creates the coins and pays the users)",
)
args = parser.parse_args()


# ❖ For digital signature, use any of the technique described throughout the course.


def generate_keys():
    private_key = SigningKey.generate()
    public_key = private_key.verifying_key
    return private_key, public_key


def sign(private_key, message):
    message = bytes(message, encoding="ascii")
    signature = private_key.sign(message, hashfunc=sha256)
    return signature


def verify_signature(public_key, message, signature):
    message = bytes(message, encoding="ascii")
    try:
        return public_key.verify(signature, message, hashfunc=sha256)
    except:
        return False


def get_string_key(key):
    return str(key.to_string().hex())


class Coin:

    coin_counter = 0

    def __init__(self):
        # 1- Each coin should have a coin ID.
        self.ID = sha256(
            bytes(("coin" + str(Coin.coin_counter)), encoding="ascii")
        ).hexdigest()

        Coin.coin_counter += 1

    def sign_coin(self, private_key):
        self.signature = sign(private_key, str(self.__hash__()))

    def set_coin_last_trans(self, trans_hash, trans_block):
        self.last_trans = Hash_Pointer(trans_hash, trans_block)


class User:
    def __init__(self):
        self.private_key, self.public_key = generate_keys()
        self.coins = []

    def confirm_transaction(self, coins, consume):
        for coin in coins:
            if consume:
                self.coins.remove(coin)
            else:
                self.coins.append(coin)


class Transaction:

    """
    2- Each transaction should have a transaction ID, a hash pointer to the previous.
        transaction, the amount of coins and signed by the sender.
    """

    trans_counter = 0

    def __init__(self, prev_hash, coins, sender_puk, receiver_puk):
        self.transcount = Transaction.trans_counter
        Transaction.trans_counter += 1
        self.prev_hash = prev_hash
        self.coins = coins
        self.sender_puk = sender_puk
        self.receiver_puk = receiver_puk
        self.hash = sha256(
            bytes(
                (
                    "tx"
                    + str(self.transcount)
                    + str(self.coins)
                    + str(sender_puk)
                    + str(receiver_puk)
                ),
                encoding="ascii",
            )
        ).hexdigest()
        self.ID = self.hash

    def sign_tx(self, private_key):
        self.signature = sign(private_key, str(self.hash))

    def set_tx_block(self, pointer):
        self.block = pointer

    def details(self):
        return (
            "------------------------------------------------"
            + "\n"
            + "Trans ID\t: "
            + str(self.ID)
            + "\n"
            + (
                ("Prev Trans\t: " + str(self.prev_hash.thash) + "\n")
                if self.prev_hash
                else ""
            )
            + (
                ("Sender\t\t: " + get_string_key(self.sender_puk))
                if self.prev_hash
                else "Sender\t\t: Scrooge *COINBASE (Newly Generated Coins)*"
            )
            + "\n"
            + "Receiver\t: "
            + get_string_key(self.receiver_puk)
            + "\n"
            + "Amount\t\t: "
            + str(len(self.coins))
            + " SC"
            + "\n"
            + "CoinsIDs\t: [ "
            + str(self.coins[0].ID)
            + " ]\n"
            + "------------------------------------------------"
        )


class Hash_Pointer:
    def __init__(self, thash, pointer):
        self.thash = thash
        self.pointer = pointer

    def sign_hp(self, private_key):
        self.signature = sign(private_key, str(self.__hash__()))


class Block:

    """
    each block contains transactions, its ID,
    the hash of the block, and a hash pointer to the previous block.
    3- Each block in the blockchain should have a block ID, 10 valid transactions, a hash of the
    block, and a hash pointer to the previous block.
    """

    block_counter = 0

    def __init__(self, transactions, prev_hash):
        self.blockcount = Block.block_counter
        Block.block_counter += 1
        self.transactions = transactions
        self.prev_hash = prev_hash
        self.hash = sha256(
            bytes(
                (str(self.blockcount) + str(self.transactions) + str(prev_hash)),
                encoding="ascii",
            )
        ).hexdigest()
        self.ID = self.hash

    def sign_bk(self, private_key):
        self.signature = sign(private_key, str(self.hash))


class Scrooge:

    """
    ❖ A designated entity “Scrooge” publishes an append-only ledger that contains
    all the history of transactions.
    """

    def __init__(self):
        self.private_key, self.public_key = generate_keys()
        # ❖ The ledger is a blockchain
        self.ledger = []
        # another name
        self.block_chain = self.ledger
        self.final_hp = None
        self.temp_block = []
        self.users = []

    def sign_final_hp(self):
        self.final_hp.sign_hp(self.private_key)

    def create_new_block(self):
        new_block = Block(self.temp_block, self.final_hp)
        self.temp_block = []
        new_block.sign_bk(self.private_key)
        self.ledger.append(new_block)
        self.final_hp = Hash_Pointer(new_block.hash, (len(self.ledger) - 1))
        # The final hash pointer is signed by Scrooge.
        # 4- The final hash pointer should be signed by Scrooge.
        self.sign_final_hp()
        # 9- A user cannot confirm a transaction unless it is published on the blockchain.
        self.confirm_new_transactions()
        outret = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
        outret += "A new block appended !\n"
        outret += "The current blockchain :\n"
        for block in self.ledger:
            tids = ""
            for tr in block.transactions:
                tids += str(tr.ID) + ", "
            outret += (
                "<--"
                + (
                    ("(Previous block : " + str(block.prev_hash.thash))
                    if block.prev_hash
                    else "("
                )
                + " BlockID : "
                + str(block.ID)
                + " || Block Transactions' IDs : [ "
                + tids[:-2]
                + " ] )\n"
            )
        outret += (
            "<-- ( Final H() : "
            + str(self.final_hp.thash)
            + " , signature : "
            + str(self.final_hp.signature.hex())
            + "\n"
        )
        outret += "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
        return outret

    def confirm_new_transactions(self):
        senders = []
        receivers = []
        coins = []
        for trans in self.ledger[-1].transactions:
            trans.set_tx_block(len(self.ledger) - 1)
            senders.append(trans.sender_puk)
            receivers.append(trans.receiver_puk)
            coins.append((trans.coins, trans.hash, trans.block))
        for user in self.users:
            if user.public_key in senders:
                for i in range(len(senders)):
                    if user.public_key == senders[i]:
                        user.confirm_transaction(coins[i][0], True)
            if user.public_key in receivers:
                for i in range(len(receivers)):
                    if user.public_key == receivers[i]:
                        coins[i][0][0].set_coin_last_trans(coins[i][1], coins[i][2])
                        user.confirm_transaction(coins[i][0], False)

    def check_transaction(self, transaction):
        """
        returns :   0 if the transaction is valid,
                    1 if the signature is invalid,
                    2 if the transaction is double spending
        """
        # ❖ Upon detecting any transaction, scrooge verifies it by making sure the coin
        # really belongs to the owner and it has not been spent before.

        # Scrooge verifies the signature before accumulating the transaction.
        # 5- Scrooge verifies that the transaction belongs to the owner.
        valid_transaction = verify_signature(
            transaction.sender_puk, str(transaction.hash), transaction.signature
        )
        if not valid_transaction:
            return 1
        # 6- Scrooge verifies that the transaction is not a Double spending.
        for user in self.users:
            if transaction.sender_puk == user.public_key:
                _sender = user
                break
        # the coin really belongs to the owner
        for coin in transaction.coins:
            if not (coin in _sender.coins):
                return 2
        # and it has not been spent before
        for trans in self.temp_block:
            if trans.prev_hash == transaction.prev_hash:
                return 2
        """
        # Double spending can only happen before the transaction is published.
        # Thus, this part is unnecessary, since the blocks in the ledger contains only published transactions.
        for block in self.ledger:
            for trans in block.transactions:
                if trans.prev_hash == transaction.prev_hash:
                    return 2
        """

        # if all checks pass -> valid transaction
        return 0

    def add_trans_to_temp_block(self, new_trans):
        self.temp_block.append(new_trans)
        # ❖ Scoorge should print the block under construction for each new transaction
        # added (include the transaction details)
        outret2 = "################################################\n"
        outret2 += "A new transaction added !\n"
        outret2 += "Block under construction :\n"
        for i in range(len(self.temp_block)):
            outret2 += "Transaction_" + str(i) + " : " + self.temp_block[i].ID + "\n"
        outret2 += "################################################\n"
        return outret2


if __name__ == "__main__":

    output = ""
    printn = "###############      Start       ###############"
    output += printn + "\n"
    print(printn)
    seed(23)
    scrooge = Scrooge()
    # A network of 100 users will simulate the transaction processes.
    for i in range(100):
        scrooge.users.append(User())
    printn = "###############  Creating coins  ###############"
    output += printn + "\n"
    print(printn)
    # Initially each user will have 10 ScroogCoins.
    for user in scrooge.users:
        for i in range(10):
            new_coin = Coin()
            new_coin.sign_coin(scrooge.private_key)
            new_trans = Transaction(
                None, [new_coin], scrooge.public_key, user.public_key
            )
            printn = new_trans.details()
            if args.initial:
                output += printn + "\n\n"
                if not args.dontprint:
                    print(printn + "\n")
            # 8- Scrooge will create and sign the 10 initial scrooge coins for each user.
            new_trans.sign_tx(scrooge.private_key)
            printn = scrooge.add_trans_to_temp_block(new_trans)
            if args.initial:
                output += printn + "\n"
                if not args.dontprint:
                    print(printn)
        # Once Scrooge accumulates 10 transaction, he can form a block and attach it to the blockchain.
        printn = scrooge.create_new_block()
        if args.initial:
            output += printn + "\n"
            if not args.dontprint:
                print(printn)
    # ❖ Print initially the public key and the amount of coins for each user.
    printn = "#############  Users' Initial Info  ############\n"
    output += printn + "\n"
    if not args.dontprint:
        print(printn)
    for x in range(len(scrooge.users)):
        user = scrooge.users[x]
        printn = (
            "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\nUser "
            + str(x + 1)
            + "\n\nUser's public key : "
            + get_string_key(user.public_key)
            + "\nPEM format :\n"
            + user.public_key.to_pem().decode("utf-8")
        )
        output += printn + "\n"
        if not args.dontprint:
            print(printn)
        printn = (
            "Amount of coins this user has : "
            + str(len(user.coins))
            + " coins.\n"
            + "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n"
        )
        output += printn + "\n"
        if not args.dontprint:
            print(printn)
    printn = "########  Starting random transactions  ########"
    output += printn + "\n"
    print(printn)
    printn = "########  To stop press the key 'Space' ########"
    output += printn + "\n"
    print(printn)
    while True:
        if is_pressed(" "):
            printn = "############  Terminating the code  ############"
            output += printn + "\n"
            print(printn)
            printn = "## Saving all the printed data to a text file ##"
            output += printn + "\n"
            print(printn)
            filename = args.name if ".txt" in args.name else args.name + ".txt"
            with open(filename, "w") as f:
                f.write(output)
            print("Output saved to " + filename)
            break
        """
        As long as the system is running,
        a random transaction with random amount
        (within the range of amount the user has)
        will be created from User A to User B.
        ❖ A simulation of the network, with multiple users and the randomized process
        of making a transaction, making each transaction reach an arbitrary user.
        """
        sender_index = randint(0, len(scrooge.users) - 1)
        receiver_index = randint(0, len(scrooge.users) - 1)
        # A != B
        while sender_index == receiver_index:
            receiver_index = randint(0, len(scrooge.users) - 1)

        sender = scrooge.users[sender_index]
        receiver = scrooge.users[receiver_index]
        if len(sender.coins) > 0:
            amount = randint(1, min(len(sender.coins), (10 - len(scrooge.temp_block))))
            for t in range(amount):
                coin = sender.coins[t]
                new_trans = Transaction(
                    coin.last_trans, [coin], sender.public_key, receiver.public_key
                )
                # The transaction is signed by the private-key of the sender.
                new_trans.sign_tx(sender.private_key)
                # Scrooge get notified by every transaction.
                # Scrooge verifies the signature before accumulating the transaction.
                # ❖ Upon detecting any transaction, scrooge verifies it by making sure the coin
                # really belongs to the owner and it has not been spent before.
                # 5- Scrooge verifies that the transaction belongs to the owner.
                # 6- Scrooge verifies that the transaction is not a Double spending.
                valid_transaction_code = scrooge.check_transaction(new_trans)

                # ❖ If verified, Scrooge adds the transaction to the blockchain. Double spending
                # can only happen before the transaction is published.
                if valid_transaction_code == 0:
                    # 0 -> valid transaction
                    printn = new_trans.details()
                    output += printn + "\n\n"
                    if not args.dontprint:
                        print(printn + "\n")
                    printn = scrooge.add_trans_to_temp_block(new_trans)
                    output += printn + "\n"
                    if not args.dontprint:
                        print(printn)
                elif valid_transaction_code == 1:
                    # 1 -> invalid signature
                    printn = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\nInvalid transaction due to invalid signature!"
                    output += printn + "\n"
                    if not args.dontprint:
                        print(printn)
                    printn = new_trans.details()
                    output += printn + "\n"
                    if not args.dontprint:
                        print(printn)
                    printn = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n"
                    output += printn + "\n"
                    if not args.dontprint:
                        print(printn)
                elif valid_transaction_code == 2:
                    # 2 -> double spending
                    printn = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\nInvalid transaction due to double spending problem!"
                    output += printn + "\n"
                    if not args.dontprint:
                        print(printn)
                    printn = new_trans.details()
                    output += printn + "\n"
                    if not args.dontprint:
                        print(printn)
                    printn = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n"
                    output += printn + "\n"
                    if not args.dontprint:
                        print(printn)

        # Once Scrooge accumulates 10 transaction, he can form a block and
        # attach it to the blockchain
        # 7- If 5 and 6 are verified Scrooge publishes the transaction to the block.
        if len(scrooge.temp_block) == 10:
            printn = scrooge.create_new_block()
            output += printn + "\n"
            if not args.dontprint:
                print(printn)
