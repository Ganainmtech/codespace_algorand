from algokit_utils.beta.algorand_client import (
    AlgorandClient,
    AssetCreateParams,
    AssetOptInParams,
    AssetTransferParams,
    PayParams
)

algorand = AlgorandClient.default_local_net()

# Task Submission 2

# Create new account
creator = algorand.account.random()

print("Account Address: ", creator.address)

# Create dispenser address
dispenser = algorand.account.dispenser()

algorand.send.payment(
    PayParams(
        sender=dispenser.address,
        receiver=creator.address,
        amount=10_000_000
    )
)

print(algorand.account.get_information(creator.address))

# Create asset

sent_txn = algorand.send.asset_create(
    AssetCreateParams(
        sender=creator.address,
        total=1_000,
        asset_name="Buildh3r",
        unit_name="Bh3r",
        manager=creator.address,
        clawback=creator.address,
        freeze=creator.address,
        reserve=creator.address
    )
)

asset_identity = sent_txn['confirmation']['asset-index']
print("Asset ID: ", asset_identity)

receiver_addr = algorand.account.random()

print("Receiver Address: ", receiver_addr.address)

algorand.send.payment(
    PayParams(
        sender=dispenser.address,
        receiver=receiver_addr.address,
        amount=10_000_000
    )
)

algorand.account.get_information(receiver_addr.address)

group_txn = algorand.new_group()

group_txn.add_asset_opt_in(
    AssetOptInParams(
        sender=receiver_addr.address,
        asset_id=asset_identity
    )
)

group_txn.add_asset_transfer(
    AssetTransferParams(
        sender=creator.address,
        receiver=receiver_addr.address,
        asset_id=asset_identity,
        amount=10
    )
)


group_txn.execute()

print("Receiver Account state: ", algorand.account.get_information(receiver_addr.address))

print("Creator Account Asset: ", algorand.account.get_information(creator.address)['assets'][0]['amount'])
print("Receiver Account Asset: ", algorand.account.get_information(receiver_addr.address)['assets'][0]['amount'])
print("\n")

group_txn1 = algorand.new_group()

group_txn1.add_asset_transfer(
    AssetTransferParams(
        sender=creator.address,
        amount=5,
        receiver=creator.address,
        asset_id=asset_identity,
        clawback_target=receiver_addr.address
    )
)

group_txn1.execute()

print("Creator Account Asset: ", algorand.account.get_information(creator.address)['assets'][0]['amount'])
print("Receiver Account Asset: ", algorand.account.get_information(receiver_addr.address)['assets'][0]['amount'])
print("\n")