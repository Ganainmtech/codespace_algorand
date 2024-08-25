from algokit_utils.beta.algorand_client import (
    AlgorandClient,
    AssetCreateParams,
    AssetOptInParams,
    AssetTransferParams,
    PayParams   
)

algorand = AlgorandClient.default_local_net()

# Dispenser Account
dispenser = algorand.account.dispenser()
print("Dispenser Address: ", dispenser.address)

# Creator account
creator = algorand.account.random()
print("Creator Address: ",creator.address)
# print(algorand.account.get_information(creator.address))

algorand.send.payment(
    PayParams(
        sender=dispenser.address,
        receiver=creator.address,
        amount=10_000_000
    )
)
# print(algorand.account.get_information(creator.address))

# Asset Creation
sent_txn = algorand.send.asset_create(
    AssetCreateParams(
        sender=creator.address,
        total=1000,
        asset_name="walcruise",
        unit_name="cru",
        manager=creator.address,
        clawback=creator.address,
        freeze=creator.address
    )
)
asset_id = sent_txn["confirmation"]["asset-index"]
print("Asset ID: ",asset_id)

# Create New Group
group_tx = algorand.new_group()

# Number of receivers
num_receivers = 3

# Create and display receiver accounts
receivers = [algorand.account.random() for _ in range(num_receivers)]

for i, receiver in enumerate(receivers, start=1):
    print(f"Receiver{i} Address: {receiver.address}")

    # Send payment to each receiver
    algorand.send.payment(
        PayParams(
            sender=dispenser.address,
            receiver=receiver.address,
            amount=10_000_000
        )
    )
    # print(algorand.account.get_information(receiver.address)) 

    group_tx.add_asset_opt_in(
        AssetOptInParams(
            sender=receiver.address,
            asset_id=asset_id
        )
    )

    group_tx.add_payment(
        PayParams(
            sender=receiver.address,
            receiver=creator.address,
            amount=1_000_000
        )
    )

    group_tx.add_asset_transfer(
        AssetTransferParams(
            sender=creator.address,
            receiver=receiver.address,
            asset_id=asset_id,
            amount=100
        )
    )


group_tx.execute()
print("Before Clawback:")
for i, receiver in enumerate(receivers, start=1):
    print(f"Receiver{i} Account Asset Balance:", algorand.account.get_information(receiver.address)['assets'][0]['amount'])

for i, receiver in enumerate(receivers, start=1):
    # print(algorand.account.get_information(receiver.address))
    # print("Receiver Account Asset Balance: ", algorand.account.get_information(receiver.address)["assets"][0]['amount'])

    # Clawback 2 tokens from receiver
    clawback_txn = algorand.send.asset_transfer(
        AssetTransferParams(
            sender=creator.address,  # Clawback address
            asset_id=asset_id,
            receiver=creator.address,
            clawback_target=receiver.address,
            amount=2
        )
    )

print("After Clawback:")
for i, receiver in enumerate(receivers, start=1):
    print(f"Receiver{i} Account Asset Balance:", algorand.account.get_information(receiver.address)['assets'][0]['amount'])

print("Creator Account Asset Balance:", algorand.account.get_information(creator.address)['assets'][0]['amount'])