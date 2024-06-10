from algokit_utils.beta.algorand_client import (
    AlgorandClient,
    AssetCreateParams,
    AssetOptInParams,
    AssetTransferParams,
    PayParams,   
)

algorand = AlgorandClient.default_local_net()

dispenser = algorand.account.dispenser()

creator = algorand.account.random()

algorand.send.payment(
    PayParams(
        sender= dispenser.address,
        receiver= creator.address,
        amount= 10_000_000
    )
)


sent_txn = algorand.send.asset_create(
    AssetCreateParams(
        sender=creator.address,
        total=1000,
        asset_name="BUILDH3R",
        unit_name="H3R",
        manager=creator.address,
        clawback=creator.address,
        freeze=creator.address
    )
)


asset_id = sent_txn["confirmation"]["asset-index"]

receiver_acc = algorand.account.random()

algorand.send.payment(
    PayParams(
        sender= dispenser.address,
        receiver= receiver_acc.address,
        amount= 10_000_000
    )
)


group_txn = algorand.new_group()

group_txn.add_asset_opt_in(
    AssetOptInParams(
        sender=receiver_acc.address,
        asset_id=asset_id
    )
)

group_txn.add_payment(
    PayParams(
        sender=receiver_acc.address,
        receiver=creator.address,
        amount=1_000_000
    )
)

group_txn.add_asset_transfer(
    AssetTransferParams(
        sender=creator.address,
        receiver=receiver_acc.address,
        asset_id=asset_id,
        amount=500
    )
)

group_txn.execute()

print("Receiver Account Asset Balance", algorand.account.get_information(receiver_acc.address)['assets'][0]['amount'])
print("Creator Account Asset Balance", algorand.account.get_information(creator.address)['assets'][0]['amount'])

# Clawback 1 tokens from receiver_acc
clawback_txn = algorand.send.asset_transfer(
    AssetTransferParams(
        sender=creator.address,  # Clawback address
        asset_id=asset_id,
        receiver=creator.address,
        clawback_target=receiver_acc.address,
        amount=1
    )
)

print("Post Clawback:")
print("Receiver Account Asset Balance", algorand.account.get_information(receiver_acc.address)['assets'][0]['amount'])
print("Creator Account Asset Balance", algorand.account.get_information(creator.address)['assets'][0]['amount'])
