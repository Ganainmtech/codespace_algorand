from algokit_utils.beta.algorand_client import(
    AlgorandClient,
    AssetCreateParams,
    AssetOptInParams,
    AssetTransferParams,
    PayParams,
)

algorand = AlgorandClient.default_local_net()

dispenser = algorand.account.dispenser()
#print(dispenser.address)

creator = algorand.account.random()
#print(creator.address)

algorand.send.payment(
    PayParams(
        sender=dispenser.address,
        receiver=creator.address,
        amount=10_000_000
    )
)

#print(algorand.account.get_information(creator.address))

sent_txn = algorand.send.asset_create(
    AssetCreateParams(
        sender=creator.address,
        total=666,
        asset_name="SERENITYPET",
        unit_name="SP",
    )
)

asset_id= sent_txn["confirmation"]["asset-index"]

account_one = algorand.account.random()
account_two = algorand.account.random()
account_three = algorand.account.random()

algorand.send.payment(
    PayParams(
        sender=dispenser.address,
        receiver=account_one.address,
        amount=10_000_000
    )
)

algorand.send.payment(
    PayParams(
        sender=dispenser.address,
        receiver=account_two.address,
        amount=10_000_000
    )
)

algorand.send.payment(
    PayParams(
        sender=dispenser.address,
        receiver=account_three.address,
        amount=10_000_000
    )
)

algorand.send.asset_opt_in(
    AssetOptInParams(
        sender=account_one.address,
        asset_id=asset_id
    )
)

algorand.send.asset_opt_in(
    AssetOptInParams(
        sender=account_two.address,
        asset_id=asset_id
    )
)

algorand.send.asset_opt_in(
    AssetOptInParams(
        sender=account_three.address,
        asset_id=asset_id
    )
)

asset_transfer = algorand.send.asset_transfer(
    AssetTransferParams(
        sender=creator.address,
        receiver=account_one.address,
        asset_id=asset_id,
        amount=111
    )
)

asset_transfer = algorand.send.asset_transfer(
    AssetTransferParams(
        sender=creator.address,
        receiver=account_two.address,
        asset_id=asset_id,
        amount=111
    )
)

asset_transfer = algorand.send.asset_transfer(
    AssetTransferParams(
        sender=creator.address,
        receiver=account_three.address,
        asset_id=asset_id,
        amount=111,
        last_valid_round=1000
    )
)

print("Account one: " + account_one.address)
print(algorand.account.get_information(account_one.address))

print("\nAccount two: " + account_two.address)
print(algorand.account.get_information(account_two.address))

print("\nAccount three: " +  account_three.address)
print(algorand.account.get_information(account_three.address))

