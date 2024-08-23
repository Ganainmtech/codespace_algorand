from algokit_utils.beta.algorand_client import(
    AlgorandClient,
    AssetCreateParams,
    AssetOptInParams,
    AssetTransferParams,
    PayParams
)

#client to connect to local net
algorand = AlgorandClient.default_local_net()

#import dispenser from kmd
dispenser = algorand.account.dispenser()
print("Dispenser address: ", dispenser.address)

creator = algorand.account.random()
# print("Creator address: ", creator.address)
# print(algorand.account.get_information(creator.address))

#fund creator account
algorand.send.payment(
    PayParams(
        sender = dispenser.address,
        receiver = creator.address,
        amount = 10_000_000 #10 algos
    )
)
print(algorand.account.get_information(creator.address))

sent_txn = algorand.send.asset_create(
    AssetCreateParams(
        sender = creator.address,
        total = 100,
        asset_name = "paisa",
        unit_name = "pa",
    )
)

asset_id = sent_txn["confirmation"]["asset-index"]
print("asset_id",asset_id)

receiver_acc = algorand.account.random()

#fund receiver_acc account
algorant.send.payment(
    PayParams(
        sender = dispenser.address,
        receiver = receiver_acc.address,
        amount = 10_000_000
    )
)

print(algorand.account.get_information(receiver_acc.address))

asset_transfer = algorand.send.asset_transfer(
    AssetTransferParams(
        sender = creator.address,
        receiver = receiver_acc.address,
        asset_id = asset_id,
        amount = 10
    )
)

#create a group txn
group_txn = algorand.new_group()

group_txn.add_asset_opt_in(
    AssetOptInParams(
        
    )
)