from algokit_utils.beta.algorand_client import (
    AlgorandClient,
    AssetCreateParams,
    AssetOptInParams,
    AssetTransferParams,
    PayParams
)

# Initialize the Algorand client for connecting to a local network
algorand=AlgorandClient.default_local_net()

# Access the default dispenser account from KMD to use for funding other accounts
dispenser= algorand.account.dispenser()
print("Dispenser Account Address:", dispenser.address)

# Create a new random account to act as the asset creator
creator_account =algorand.account.random()
print("Asset Creator Account Address:", creator_account.address)

# Fund the asset creator account by sending ALGOs from the dispenser
algorand.send.payment(
    PayParams(
        sender=dispenser.address,
        receiver=creator_account.address,
        amount=10_000_000  # Send 10 ALGOs to the creator account
    )
)

# Create a new Algorand Standard Asset (ASA) using the creator account
asset_creation_txn = algorand.send.asset_create(
    AssetCreateParams(
        sender=creator_account.address,
        total=100,  # Set total supply of the asset to 100 units
        asset_name="KnowledgeCoin",  # Name of the asset
        unit_name="KNL"  # Ticker 
    )
)

# Retrieve the Asset ID from the confirmed transaction response
asset_id = asset_creation_txn["confirmation"]["asset-index"]
print("Created Asset ID:", asset_id)

# Generate another random account to receive the asset
receiver_account = algorand.account.random()

# Fund the receiver account with 10 ALGOs from the dispenser
algorand.send.payment(
    PayParams(
        sender=dispenser.address,
        receiver=receiver_account.address,
        amount=10_000_000  # Send 10 ALGOs to the receiver account
    )
)

# Create a group transaction for multiple actions that will be executed atomically
group_txn = algorand.new_group()

# Opt the receiver account into the newly created asset (enabling it to receive the asset)
group_txn.add_asset_opt_in(
    AssetOptInParams(
        sender=receiver_account.address,
        asset_id=asset_id
    )
)

# Add a transaction to send 1 ALGO from the receiver to the creator
group_txn.add_payment(
    PayParams(
        sender=receiver_account.address,
        receiver=creator_account.address,
        amount=1_000_000  # Send 1 ALGO from the receiver to the creator
    )
)

# Transfer 10 units of the newly created asset from the creator to the receiver
group_txn.add_asset_transfer(
    AssetTransferParams(
        sender=creator_account.address,
        receiver=receiver_account.address,
        asset_id=asset_id,
        amount=10  # Transfer 10 units of the asset to the receiver
    )
)

# Execute the group transaction, ensuring all transactions happen together or not at all
group_txn.execute()

# Retrieve and print the updated asset balance for both the receiver and the creator
receiver_asset_balance = algorand.account.get_information(receiver_account.address)["assets"][0]["amount"]
creator_asset_balance = algorand.account.get_information(creator_account.address)["assets"][0]["amount"]

print("Receiver's Asset Balance:", receiver_asset_balance)
print("Creator's Asset Balance:", creator_asset_balance)
