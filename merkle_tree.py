#blockchain project-merkle tree implementation
#sources: https://www.geeksforgeeks.org/dsa/introduction-to-merkle-tree/
#https://brilliant.org/wiki/merkle-tree/

"""merkle tree is a binary has tree used in blockchains to efficiently and
securely represent all transactions in a block. each transaction is hashed
individually, the leaves, then pairs of hashes are combined and hashed again,
level by level, until a single has remains .... the merkle root

the merkle root is stored in the block header acting as a fingerprint for
the entire set of transactions. if even one chracater in any transaction is
cahnged, the merkle root changes completely, essentially making tampering
detectable
"""

import hashlib
import json

#transaction data
# plain utf-8 string, will be sha-256 hashed
#become a leaf node in merkle tree
transactions = [
    "John pays Charlie 5 BTC",
    "Bob pays Dave 2 BTC",
    "Alice pays Erin 1 BTC",
    "Charlie pays Frank 3 BTC",
    "Dave pays Gina 1 BTC",
    "Erin pays Alice 0.5 BTC",
    "Frank pays Bob 0.25 BTC"]

#sha-256 hash
def sha256(data: str) -> str:
    #sha-256 hash of a UTF-8 string
    #return it as a hex string

    #encode() converts the python string to raw bytes UTF-8
    return hashlib.sha256(data.encode("utf-8")).hexdigest()

#hash transaction/ build leaf layer
#convert each transaction string into its sha-256 hash (leaf nodes)
#in real blockchain, transactions are serialized binary data before hashing
# but we will hash the plain transaction strings directly.
def hash_transactions(transactions: list) -> list:
    print("\nHashing individual transactions (leaf nodes)...")
    print("=" * 70)

    leaf_hashes = []
    for i, tx in enumerate(transactions):
        tx_hash = sha256(tx)        #hash transaction string
        leaf_hashes.append(tx_hash)
        #print short preview so user can see leaf has
        print(f"T{i} | {tx!r}")
        print(f"-> {tx_hash}\n")

    return leaf_hashes

#build merkle tree
#return root
def merkle_tree(leaf_hashes: list) -> tuple:
    tree_levels = [leaf_hashes.copy()]
    current_level = leaf_hashes.copy()      #start @ leaf layer
    level_index = 1

    print("Building Merkle Tree....")
    print("=" * 70)

    #keep combining until only root hash is lefy
    while len(current_level) > 1:
        #handles odd # of nodes; duplicate last hash
        #if there ia an odd # of hashes, cannot form complete pairs
        #bitcoin protocol (&most blockchains) solve this by repeating last
        #hash so it is paired w/ itself
        if len(current_level) % 2 != 0:
            duplicate = current_level[-1]
            current_level.append(duplicate)
            print(f"Level {level_index -1} has an odd # of nodes.")
            print(f"Duplicating last hash: ...{duplicate[-8:]} -> paired with itself.\n")

        #will hold parent hashes for this iteration
        next_level = []

        #pair and has adjacent nodes
        for i in range(0, len(current_level), 2):
            left = current_level[i]     #left child hash
            right = current_level[i + 1]    #right child hash

            #concatenate two child hashes as hex strings
            #and had them to produce parent node.
            #parent = sha256(left_hash_string + right_hand_string)
            parent = sha256(left+right)
            next_level.append(parent)

            #display
            print(f"SHA256(...{left[-8:]} + ...{right[-8:]})")
            print(f"-> {parent[-16:]}\n")

        #move up level
        current_level = next_level
        tree_levels.append(current_level.copy())

        print(f"Level {level_index} - {len(current_level)} node(s)")
        for node in current_level:
            print(f"{node}")
        print()

        level_index += 1

    #the remaining hash is the merkle root
    merkle_root = current_level[0]
    return merkle_root, tree_levels


#display full tree struct
def print_tree(tree_levels: list):
    print("Tree Summary: All levels from leaves to root:")
    print("=" * 70)

    total_levels = len(tree_levels)
    for depth, level in enumerate(tree_levels):
        if depth == 0:
            label = "Leaf Layer (transaction hashes)"
        elif depth == total_levels - 1:
            label = "Root Layer (Merkle Root)"
        else:
            label = f"Level {depth:>2}  ({len(level)} node(s))"

        print(f"\n {label}:")
        for i, node in enumerate(level):
            print(f"[{i}] {node}")

    print("=" * 70)

#block assembly:
def assemble_block(merkle_root: str) -> dict:
    #in a real blockchain, the block header contains:
    #index, miner, previous_has, merkle_root, and transactions

    block = {
        "block_index"       : 1,
        "miner"             : "MinerX",
        "previous_hash"     :"0000089ac61913788b22a3c200e5b68c62ec74b678c515d3962fda09c816689c",
        "merkle_root"       : merkle_root,
        "transactions"      : transactions,
    }
    return block

def main():
    print("=" * 70)
    print("Blockchain Project - Merkle Tree")
    print("=" * 70)
    print(f"\nBlock Index      : 1")
    print(f"Miner           : MinerX")
    print(f"Transactions    : {len(transactions)}")

    leaf_hashes = hash_transactions(transactions)
    merkle_root, tree_levels = merkle_tree(leaf_hashes)
    print_tree(tree_levels)
    block = assemble_block(merkle_root)

    print("\nCompleted Block:")
    print("=" * 70)
    #json.dumps w/ indent=4 provides a clean, human-readable block printout
    #"pretty print"
    print(json.dumps(block, indent=4))
    print("=" * 70)

    print(f"\nMerkle Root = {merkle_root}")
    print("\nIntegrity note:")
    print("Any change to even a single character in any transaction\n"
          "would produce a completely different Merkle Root, immediately\n"
          "revealing that the block's data can be tampered with. This is a\n"
          "big reason why people like to use cryptocurrency.")

if __name__ == "__main__":
    main()

