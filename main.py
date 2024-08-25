from algokit_utils.beta.algorand_client import (
    AlgorandClient,
    AssetCreateParams,
    AssetOptInParams,
    AssetTransferParams,
    PayParams,
)

# Client to connect to the localhost
algorand = AlgorandClient.default_local_net()

dispenser = algorand.account.dispenser()

# print("Dispenser Address: ", dispenser.address)

#Generate creator wallet
creator = algorand.account.random()
# print("Creator Address: ", creator.address)

# print(algorand.account.get_information(creator.address))

# fund creator address with algo
algorand.send.payment(
    PayParams(
        sender=dispenser.address, receiver=creator.address, amount=10_000_000 #10 algos
    )
)

# print(algorand.account.get_information(creator.address))

# Create an asset

sent_txn = algorand.send.asset_create(
    AssetCreateParams(
        sender=creator.address,
        total=100,
        asset_name="Web3Pak",
        unit_name="W3P",
    )
)


asset_id = sent_txn["confirmation"]["asset-index"]
# print("ASSET ID: ", asset_id)

receiver_account = algorand.account.random()

algorand.send.payment(
    PayParams(
        sender=dispenser.address, receiver=receiver_account.address, amount=10_000_000 #10 algos
    )
)

# print(algorand.account.get_information(receiver_account.address))

# asset_transfer = algorand.send.asset_transfer(
#     AssetTransferParams(
#         sender=creator.address,
#         receiver=receiver_account.address,
#         asset_id=asset_id,
#         amount=10,
#     )
# )

# creator a new txn group
group_tx = algorand.new_group()

# Add the asset transfer txn to the group
group_tx.add_asset_opt_in(
    AssetOptInParams(
        sender=receiver_account.address,
        asset_id=asset_id,
    )
)

# Add the payment txn to the group

group_tx.add_payment(
    PayParams(
        sender=dispenser.address, receiver=creator.address, amount=1_000_000 #1 algos
    )
)

group_tx.add_asset_transfer(
    AssetTransferParams(
        sender=creator.address,
        receiver=receiver_account.address,
        asset_id=asset_id,
        amount=10,
    )
)

group_tx.execute()

print(algorand.account.get_information(receiver_account.address))

print("Receiver Account Asset Balance: ",algorand.account.get_information(receiver_account.address)['assets'][0]['amount'])
print("Creator Account Asset Balance: ",algorand.account.get_information(creator.address)['assets'][0]['amount'])
