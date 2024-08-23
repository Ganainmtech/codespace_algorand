from algokit_utils.beta.algorand_client import (
    AlgorandClient,
    AssetCreateParams,
    AssetOptInParams,
    AssetTransferParams,
    PayParams,
)
# Client to connect to localnet

algorand = AlgorandClient.default_local_net()

# Import dispenser from the KMD
dispenser = algorand.account.dispenser()
print("Dispenser Address:", dispenser.address)

creator = algorand.account.random()
print("Creator Address:", creator.address)
print(algorand.account.get_information(creator.address))

#Fund creator account
algorand.send.payment(
    PayParams(
        sender=dispenser.address, 
        receiver =creator.address,
        amount=10_000_000 # 10 M micro algos = 10 algos
    )
)

print(algorand.account.get_information(creator.address))

sent_txn = algorand.sent.asset_create(
    AssetCreateParams(
        sender=creator.address,
        total=100,
        asset_name="Edu4Teen",
        unit_name="E4T"
    )
)

asset_id=sent_txn["confirmation"]["asset-index"]
print("Asset ID", asset_id)

#Fund receiver_accnt account
algorand.send.payment(
    PayParams(
        sender=dispenser.address, 
        receiver =receiver_accnt.address,
        amount=10_000_000 # 10 M micro algos = 10 algos
    )
)

print(algorand.account.get_information(receiver_accnt.address))



#create a group transaction

group_txn = algorand.new_group()

group_txn.add_asset_opt_in(
    AssetOptInParams(
        sender=receiver_accnt,
        asset_id=asset_id
    )
)

group_txn.add_payment(
    PayParams(
        sender=receiver_accnt.address,
        receiver=creator.address,
        amount=10_000_000
    )
)

group_txn.add_asset_transfer(
    AssetTransferParams(
        sender=creator.address,
        receiver=receiver_accnt.address,
        asset_id=asset_id,
        amount=10
    )
)

group_txn.execute()

print("Receiver Account Set Balance:", algorand)
print("Creator Account Set Balance:")