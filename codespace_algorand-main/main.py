from algokit_utils.beta.algorand_client import(
    AlgorandClient,
    AssetCreateParams,
    AssetOptInParams,
    PayParams, 
    AssetTransferParams
)
algorand=AlgorandClient.default_local_net()

dispenser=algorand.account.dispenser()
# print("Dispenser: ", dispenser.address)

maker=algorand.account.random()
# print("maker: ", maker.address)

# print(algorand.account.get_information(maker.address))

algorand.send.payment(
    PayParams(
        sender=dispenser.address,
        receiver=maker.address,
        amount=10_000_000
    )
)

# print(algorand.account.get_information(maker.address))

sent_txn=algorand.send.asset_create(
    AssetCreateParams(
        sender=maker.address,
        total=100,
        asset_name="Edu4Teen",
        unit_name="E4T"
    )
)

asset_id=sent_txn["confirmation"]["asset-index"]
# print("Asset ID: ", asset_id)

receiver_acct = algorand.account.random()
algorand.send.payment(
    PayParams(
        sender=dispenser.address,
        receiver=receiver_acct.address,
        amount=10_000_000
    )
)

# print(algorand.account.get_information(receiver_acct.address))

group_txn=algorand.new_group()

group_txn.add_asset_opt_in(
    AssetOptInParams(
        sender=receiver_acct.address,
        asset_id=asset_id
    )
)

group_txn.add_payment(
    PayParams(
        sender=receiver_acct.address,
        receiver=maker.address,
        amount=2_000_000
    )
)

group_txn.add_asset_transfer(
    AssetTransferParams(
        sender=maker.address,
        receiver=receiver_acct.address,
        asset_id=asset_id,
        amount=18
    )
)

group_txn.execute()
print(algorand.account.get_information(receiver_acct.address))
print("Receiver assets: ", algorand.account.get_information(receiver_acct.address)["assets"][0]["amount"])
print("maker assets: ", algorand.account.get_information(maker.address)["assets"][0]["amount"])