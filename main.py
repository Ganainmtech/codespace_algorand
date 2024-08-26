from algokit_utils.beta.algorand_client import (
    AlgorandClient,
    AssetCreateParams,
    AssetOptInParams,
    AssetTransferParams,
    PayParams,
)

#Client to connect to localnet
algorand = AlgorandClient.default_local_net()

#import dispenser from KMD
dispenser = algorand.account.dispenser()
#print("Disp Add:", dispenser.address)

creator = algorand.account.random()
#print("Creat Add:", creator.address)
#print(algorand.account.get_information(creator.address))

# Fund Creat Ac
algorand.send.payment(
    PayParams(
        sender=dispenser.address,
        receiver=creator.address,
        amount=10_000_000 #10 algos

    )
)
#print(algorand.account.get_information(creator.address))
sent_txn = algorand.send.asset_create(
    AssetCreateParams(
        sender=creator.address,
        total=100,
        asset_name="Edu4Teen_Gopal",
        unit_name="E4TGopal",
    )
)

asset_id=sent_txn["confirmation"]["asset-index"]
#print("Asset ID:", asset_id)

receiver_ac = algorand.account.random()
algorand.send.payment(
    PayParams(
        sender=dispenser.address,
        receiver=receiver_ac.address,
        amount=10_000_000 #10 algos

    )
)
#print(algorand.account.get_information(receiver_ac.address))


 # create a group transaction
group_txn = algorand.new_group()

group_txn.add_asset_opt_in(
 AssetOptInParams(
  sender=receiver_ac.address,
  asset_id=asset_id
 )
)

group_txn.add_payment(
 PayParams(
  sender=receiver_ac.address,
  receiver=creator.address,
  amount=1_000_000 #1 algo
 )
)

group_txn.add_asset_transfer(
    AssetTransferParams(
        sender=creator.address,
        receiver=receiver_ac.address,
        asset_id=asset_id,
        amount=10
    )
)

group_txn.execute()

print("Rec. Ac Asset Bal:", algorand.account.get_information(receiver_ac.address)['assets'][0]['amount'])
print("Creat. Ac Asset Bal:", algorand.account.get_information(creator.address)['assets'][0]['amount'])