from algokit_utils.beta.algorand_client import (
    AlgorandClient,
    AssetCreateParams,
    AssetOptInParams,
    AssetTransferParams,
    PayParams,
)

# Client to connect to the local net
algorand = AlgorandClient.default_local_net()

dispenser = algorand.account.dispenser()
# print("Dispenser:", dispenser.address)

# Generate creator wallet 
creator = algorand.account.random()
# print("Creator:", creator.address)
# print(algorand.account.get_information(creator.address))

# Fund creator address with algo
algorand.send.payment(
    PayParams(
        sender=dispenser.address,
        receiver=creator.address,
        amount=10_100_100  # 10 algos,
    )
)

print(algorand.account.get_information(creator.address))

sent_txn = algorand.send.asset_create(
    AssetCreateParams(
        sender=creator.address,
        total=100,
        asset_name="Edu4Teen",
        unit_name="E4T",
    )
)

asset_id = sent_txn["confirmation"]["asset-index"]
# print("Asset ID", asset_id)

receiver_acct = algorand.account.random()

algorand.send.payment(
    PayParams(
        sender=dispenser.address,
        receiver=receiver_acct.address,
        amount=10_000_000 # 10 algos
    )
)
print(algorand.account.get_information(receiver_acct.address))

# Create a new tnx group
group_tx = algorand.new_group()

group_tx.add_asset_opt_in(
    AssetOptInParams(
        sender=receiver_acct.address,
        asset_id=asset_id
    )    
)
group_tx.add_payment(
    PayParams(
        sender=receiver_acct.address,
        receiver=creator.address,
        amount=1_000_000 # 1 algo
    )
)
group_tx.add_asset_transfer(
    AssetTransferParams(
        sender=creator.address,
        receiver=receiver_acct.address,
        asset_id=asset_id,
        amount=10,
    )
)
group_tx.execute()

print(algorand.account.get_information(receiver_acct.address))

print("Receiver Account Asset Balance:", algorand.account.get_information(receiver_acct.address)['assets'][0]['amount'])
print("Creator Account Asset Balance:", algorand.account.get_information(creator.address)['assets'][0]['amount'])
