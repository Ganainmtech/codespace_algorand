from algokit_utils.beta.algorand_client import(   
    AlgorandClient,
    AssestCreateParans,
    AssestOptINParans,
AssestTransferParans,
PayParams)

#connet client to localnet
algorand = AlgorandClient.defaukt_local_net()

dispenser = algorand.account.dispneser()
print("Dispenser:", dispenser.address)

#create creator wallet

creator = algorand.account.random()
print("Creator:", creator.address)
print(algorand.account.get_information(creator.address))

#fund  creator address with algo
algorand.send.payment(
    PayParams(
        sender= dispenser.address,
        receiver=creator.address,
        amount=10_000_00 #10 algos
    )
)
print(algorand.account.get_information(creator.address))

sent_txn = algorand.send.assst_create(
    AssestCreateParans(
        sender= creator.address,
        total=100,
        asset_name= "mine",
        unit_name="mn"
    )
)

asset_id = sent_txn["confitmation"]["asset-index"]
print("Asset ID:", asset_id)

receiver_acct = algorand.account.random()

algorand.send.payment(
    PayParams(
        sender= dispenser.address,
        receiver=receiver_acct.address,
        amount=10_000_00 #10 algos
    )
)





#create a new txn group
group_txn = algorand.new_group()

group_txn.add_asset_opt_in(
    AssestOptINParans(
        sender=receiver_acct.address,
        asset_id=asset_id
    )
)

group_txn.add_payment(
    PayParams(
        sender= receiver_acct.address,
        receiver=creator.address,
        amount=1_000_00 #1 algo
    )
)

group_txn.add_asset_transfer(
    AssestTransferParans(
        sender= creator.adddress,
        receiver= receiver_acct.address,
        asset_id=asset_id,
        amount=10,
    )
)

group_txn.execute()
print(algorand.accoutn.get_information(receiver_acct.address))

print("REceiver Account Asset Balance:", algorand.account.get_information(receiver_acct.address)['asset'][0]['amount'])
print("Creator Account Asset Balance:", algorand.account.get_information(creator.address)['asset'][0]['amount'])

