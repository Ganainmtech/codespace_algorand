from algokit_utils.beta.algorand_client import(
 AlgorandClient,
 AssetCreateParams,
 AssetOptInParams,
 AssetTransferParams,
 PayParams
)

algorand = AlgorandClient.default_local_net()

dispenser = algorand.account.dispenser()
print('Dispenser Address:', dispenser.address)

creator = algorand.account.random()
print("Creator Address: ",creator.address)

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
        total= 100,
        asset_name="Web3Pak",
        unit_name="W3P",
    )
)

asset_id= sent_txn["confirmation"]["asset-index"]
print("Asset ID: ", asset_id)

receiver_acct = algorand.account.random()
print("Receiver Account: ", receiver_acct.address)

algorand.send.payment(
    PayParams(
        sender=dispenser.address,
        receiver=receiver_acct.address,
        amount=10_000_000
    )
)

print(algorand.account.get_information(receiver_acct.address))


group_tx = algorand.new_group()

group_tx.add_asset_opt_in(
    AssetOptInParams(
        sender=receiver_acct.address, 
        asset_id=asset_id               # The ID of the asset to opt in to
    )
)

group_tx.add_payment(
    PayParams(
        sender=receiver_acct.address,  
        receiver=creator.address,       
        amount=1_000_000               
    )
)

group_tx.add_asset_transfer(
    AssetTransferParams(
        sender=creator.address,         
        receiver=receiver_acct.address, 
        asset_id=asset_id,              
        amount=10                       
    )
)

group_tx.execute()

# Print the entire information from the Receiver Account
print(algorand.account.get_information(receiver_acct.address))

# Print the amount of the asset the receiver account holds after the transactions
print("Receiver Account Asset Balance:",algorand.account.get_information(receiver_acct.address)['assets'][0]['amount'])

# Print the remaining balance of the creator account after the transactions
print("Creator Account Balance:", algorand.account.get_information(creator.address)['amount'])
