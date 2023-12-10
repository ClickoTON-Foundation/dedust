from dedust import Asset, Factory, PoolType, JettonRoot, JettonWallet, VaultJetton
import asyncio
from pytoniq import WalletV4R2, LiteBalancer

mnemonics = ["your", "mnemonics", "here"]

async def main():
    provider = LiteBalancer.from_mainnet_config(1)
    await provider.start_up()

    wallet = await WalletV4R2.from_mnemonic(provider=provider, mnemonics=mnemonics)

    SCALE_ADDRESS = "EQBlqsm144Dq6SjbPI4jjZvA1hqTIP3CvHovbIfW_t-SCALE"

    SCALE = Asset.jetton(SCALE_ADDRESS)
    TON = Asset.native()

    assets = [TON, SCALE]
    target_balances = [int(float(input("Ton amount: ")) * 1e9),
                       int(float(input("Scale amount: ")) * 1e9)]

    scale_vault = await Factory.get_jetton_vault(SCALE_ADDRESS, provider)
    scale_root = JettonRoot.create_from_address(SCALE_ADDRESS)
    scale_wallet = await scale_root.get_wallet(wallet.address, provider)

    ton_vault = await Factory.get_native_vault(provider)
    
    # Deposit TON to vault
    ton_payload = ton_vault.create_deposit_liquidity_payload(pool_type=PoolType.VOLATILE,
                                                             assets=assets,
                                                             target_balances=target_balances,
                                                             amount=target_balances[0])

    await wallet.transfer(destination=ton_vault.address,
                          amount=int(target_balances[0] + (0.15*1e9)),
                          body=ton_payload)

    await asyncio.sleep(15) # waiting

    scale_root = JettonRoot.create_from_address(SCALE_ADDRESS)
    scale_wallet = await scale_root.get_wallet(wallet.address, provider)

    # Deposit SCALE to vault
    scale_payload = scale_wallet.create_transfer_payload(
        destination=scale_vault.address,
        amount=target_balances[1],
        response_address=wallet.address,
        forward_amount=int(0.4*1e9),
        forward_payload=VaultJetton.create_deposit_liquidity_payload(poolType=PoolType.VOLATILE,
                                                                     assets=assets,
                                                                     target_balances=target_balances)
    )

    await wallet.transfer(destination=scale_wallet.address,
                          amount=int(0.5*1e9),
                          body=scale_payload)

asyncio.run(main())
