from algokit_utils.beta.algorand_client import (
    AlgorandClient,
    AssetCreateParams,
    AssetOptInParams,
    AssetTransferParams,
    PayParams
)

#connect client to the localnet
algorand = AlgorandClient.default_local_net()

dispenser = algorand.account.dispenser()
# print("Dispanser:", dispenser.address)


#generate creator wallet
creator = algorand.account.random()
# print("creator wallet:", creator.address)
# print(algorand.account.get_information(creator.address))


#fund creator address with algo
algorand.send.payment(
    PayParams(
        sender= dispenser.address,
        receiver= creator.address,
        amount= 10_000_000    # 10 algos
    )
)
#print(algorand.account.get_information(creator.address))

sent_txn = algorand.send.asset_create(
    AssetCreateParams(
        sender= creator.address,
        total=100,
        asset_name= "web3pak",
        unit_name="W3P"
    )
)

asset_id = sent_txn["confirmation"]["asset-index"]
# print("Asset Id",asset_id )

receiver_acc = algorand.account.random()
algorand.send.payment(
    PayParams(
        sender= dispenser.address,
        receiver= receiver_acc.address,
        amount= 10_000_000    # 10 algos
    )
)


# create a new txn group for multiple transaction in one go
group_tx = algorand.new_group()

group_tx.add_asset_opt_in(
    AssetOptInParams(
        sender =receiver_acc.address,
        asset_id=asset_id
    )
)
group_tx.add_payment(
    PayParams(
        sender= receiver_acc.address,
        receiver= creator.address,
        amount= 1_000_000    # 10 algos
    )
)
group_tx.add_asset_transfer(
    AssetTransferParams(
        sender = creator.address,
        receiver=receiver_acc.address,
        asset_id =asset_id,
        amount = 10
    )
)

group_tx.execute()
print(algorand.account.get_information(receiver_acc.address))
print("Receiver Account Asset Balance:", algorand.account.get_information(receiver_acc.address)['assets'][0]['amount'])
print("Creator Account Asset Balance:", algorand.account.get_information(creator.address)['assets'][0]['amount'])