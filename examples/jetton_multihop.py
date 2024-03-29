from dedust import Asset, Factory, PoolType, SwapStep, JettonRoot, VaultJetton
import asyncio
from pytoniq import WalletV4R2, LiteBalancer

mnemonics = ["your", "mnemonics", "here"]

async def main():
    provider = LiteBalancer.from_mainnet_config(1)
    await provider.start_up()

    wallet = await WalletV4R2.from_mnemonic(provider=provider, mnemonics=mnemonics)

    SCALE_ADDRESS = "EQBlqsm144Dq6SjbPI4jjZvA1hqTIP3CvHovbIfW_t-SCALE"
    BOLT_ADDRESS = "EQD0vdSA_NedR9uvbgN9EikRX-suesDxGeFg69XQMavfLqIw"

    SCALE = Asset.jetton(SCALE_ADDRESS)
    TON = Asset.native()
    BOLT = Asset.jetton(BOLT_ADDRESS)

    # SCALE -> TON -> BOLT
    TON_SCALE = await Factory.get_pool(PoolType.VOLATILE, [SCALE, TON], provider)
    TON_BOLT = await Factory.get_pool(PoolType.VOLATILE, [TON, BOLT], provider)

    scale_vault = await Factory.get_jetton_vault(SCALE_ADDRESS, provider)
    scale_root = JettonRoot.create_from_address(SCALE_ADDRESS)
    scale_wallet = await scale_root.get_wallet(wallet.address, provider)

    swap_amount = int(float(input("Enter swap amount(SCALE): ")) * 1e9)
    swap = scale_wallet.create_transfer_payload(
        destination=scale_vault.address,
        amount=swap_amount,
        response_address=wallet.address,
        forward_amount=int(0.25*1e9),
        forward_payload=VaultJetton.create_swap_payload(pool_address=TON_SCALE.address,
                                                        _next=SwapStep(pool_address=TON_BOLT.address))
    )

    await wallet.transfer(destination=scale_wallet.address,
                          amount=int(0.3*1e9),
                          body=swap)

    await provider.close_all()

asyncio.run(main())
