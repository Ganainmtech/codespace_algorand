from algokit_utils.beta.algorand_client import (
    AlgorandClient,
    AssetCreateParams,
    AssetOptInParams,
    AssetTransferParams,
    PayParams,
)


# Conectar el cliente a Localnet: (AlgorandClient )
algorand = AlgorandClient.default_local_net()


# Dispenser:
dispenser = algorand.account.dispenser()
# Muestra la address del dispenser: 
print("Dispenser: ",  dispenser.address)


# Generar accounts aleatoria:
creator = algorand.account.random()
# Muestra la address de la account creada: 
print("Creator: ",  creator.address)
# Muestra informacion detallada de la address de la account creada: 
#print("Creator info: ", algorand.account.get_information(creator.address))

# Fondear la address creator con algos: (Primera trx)
algorand.send.payment(
    PayParams(
        sender = dispenser.address,
        receiver = creator.address,
        amount = 10_000_000  # <=> 10 Algos
    )
)
#print("Creator amount: ", algorand.account.get_information(creator.address))

# Crear un asset:
sent_txn = algorand.send.asset_create(
    AssetCreateParams(
        sender = creator.address,  # <-- Creador del Asset.
        total = 100,                 # <-- Cantidad de Tokens a crear.
        asset_name = "JereToken",       # <-- Nombre del Token a crear.
        unit_name = "JDB",              # <-- Nombre Unit del Token a crear.    
    )
)

# Obtener el Asset ID: (extraer confimacion e index del asset [])
asset_id = sent_txn["confirmation"]["asset-index"]
#print("Asset ID: ", asset_id)

# Crear nueva cuenta para transferir el asset: (Receiver)
receiver_acc = algorand.account.random()
# Fondear nueva cuenta para transferir el asset: (Receiver)
algorand.send.payment(
    PayParams(
        sender = dispenser.address,
        receiver = receiver_acc.address,
        amount = 10_000_000  # <=> 10 Algos
    )
)
#print("Creator amount: ", algorand.account.get_information(receiver_acc.address))


# Envviar el asset Token de: Creator al Receiver
"""
asset_transfer = algorand.send.asset_transfer(
    AssetTransferParams(
        sender = creator.address,
        receiver = receiver_acc.address,
        asset_id = asset_id,
        amount = 10,
    )
)
"""
# Transferencia Atomica para hacer OptIn (New tx group):

group_tx = algorand.new_group()

group_tx.add_asset_opt_in(
    AssetOptInParams(
        sender = receiver_acc.address,
        asset_id = asset_id,
    )
)

group_tx.add_payment(
    PayParams(
        sender = receiver_acc.address,
        receiver = creator.address,
        amount = 1_000_000  # <=> 1 Algos
    )
)

group_tx.add_asset_transfer(
    AssetTransferParams(
        sender = creator.address,
        receiver = receiver_acc.address,
        asset_id = asset_id,
        amount = 10,
    )
)

group_tx.execute()

print(algorand.account.get_information(receiver_acc.address))

print("Receiver Account asset balance: ", algorand.account.get_information(receiver_acc.address)["assets"][0]["amount"])
print("Creator Account asset balance: ", algorand.account.get_information(creator.address)["assets"][0]["amount"])
