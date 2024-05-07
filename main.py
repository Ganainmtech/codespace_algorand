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

print("\n")

# Task Submission

# 1. Create new accounts
account1 = algorand.account.random()
print(account1.address)
account2 = algorand.account.random()
print(account2.address)
account3 = algorand.account.random()
print(account3.address)


algorand.send.payment(
    PayParams(
        sender=dispenser.address,
        receiver=account1.address,
        amount=10_000_000
    )
)
print(algorand.account.get_information(account1.address))

algorand.send.payment(
    PayParams(
        sender=dispenser.address,
        receiver=account2.address,
        amount=10_000_000
    )
)
print(algorand.account.get_information(account2.address))

algorand.send.payment(
    PayParams(
        sender=dispenser.address,
        receiver=account3.address,
        amount=10_000_000
    )
)
print(algorand.account.get_information(account3.address))

# 2. Create a new asset

sent_second_txn = algorand.send.asset_create(
    AssetCreateParams(
        sender=creator.address,
        asset_name="BUILDHER",
        unit_name="HER",
        total=333
    )
)

second_asset_id = sent_second_txn["confirmation"]["asset-index"]
print("Created asset Id: ", second_asset_id)



# 3. Opt-in to the asset and transfer to created accounts with inner transactions

algorand.new_group().add_asset_opt_in(
    AssetOptInParams(
        sender=account1.address,
        asset_id=second_asset_id
    )
).add_asset_transfer(
    AssetTransferParams(
        sender=creator.address,
        receiver=account1.address,
        asset_id=second_asset_id,
        amount=100
    )
).add_asset_opt_in(
    AssetOptInParams(
        sender=account2.address,
        asset_id=second_asset_id
    )
).add_asset_transfer(
    AssetTransferParams(
        sender=creator.address,
        receiver=account2.address,
        asset_id=second_asset_id,
        amount=100
    )
).add_asset_opt_in(
    AssetOptInParams(
        sender=account3.address,
        asset_id=second_asset_id
    )
).add_asset_transfer(
    AssetTransferParams(
        sender=creator.address,
        receiver=account3.address,
        asset_id=second_asset_id,
        amount=100
    )
).execute()

# 5. Check the balance of accounts

print(algorand.account.get_information(account1.address))
print(algorand.account.get_information(account2.address))
print(algorand.account.get_information(account3.address))