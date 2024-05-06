from algokit_utils.beta.algorand_client import (
    AlgorandClient,
    AssetCreateParams,
    AssetOptInParams,
    AssetTransferParams,
    PayParams
)

algorand = AlgorandClient.default_local_net()

dispenser = algorand.account.dispenser()
print(dispenser.address)

creator = algorand.account.random()
print(creator.address)

print(algorand.account.get_information(creator.address))

algorand.send.payment(
    PayParams(
        sender=dispenser.address,
        receiver=creator.address,
        amount=10_000_000
    )
)

print(algorand.account.get_information(creator.address))

sent_txn = algorand.send.asset_create(
    AssetCreateParams(
        sender=creator.address,
        total=333,
        asset_name="BUILDH3R",
        unit_name="H3R",
    )
)

asset_id = sent_txn["confirmation"]["asset-index"]
print(asset_id)

receiver_account = algorand.account.random()
print(receiver_account.address)

algorand.send.payment(
    PayParams(
        sender=dispenser.address,
        receiver=receiver_account.address,
        amount=10_000_000
    )
)

algorand.send.asset_opt_in(
    AssetOptInParams(
        sender=receiver_account.address,
        asset_id=asset_id
    )
)

algorand.send.asset_transfer(
    AssetTransferParams(
        sender=creator.address,
        receiver=receiver_account.address,
        asset_id=asset_id,
        amount=111
    )
)

print(algorand.account.get_information(receiver_account.address))

