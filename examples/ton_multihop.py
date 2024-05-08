from dedust import Asset, Factory, PoolType, SwapStep, VaultNative, SwapParams
import asyncio
from pytoniq import WalletV4R2, LiteBalancer
import time

mnemonics = ["your", "mnemonics", "here"]


async def main():
    provider = LiteBalancer.from_mainnet_config(1)
    await provider.start_up()

    wallet = await WalletV4R2.from_mnemonic(provider=provider, mnemonics=mnemonics)

    SCALE_ADDRESS = "EQBlqsm144Dq6SjbPI4jjZvA1hqTIP3CvHovbIfW_t-SCALE"
    BOLT_ADDRESS = "EQD0vdSA_NedR9uvbgN9EikRX-suesDxGeFg69XQMavfLqIw"

    TON = Asset.native()
    SCALE = Asset.jetton(SCALE_ADDRESS)
    BOLT = Asset.jetton(BOLT_ADDRESS)

    # TON -> SCALE -> BOLT
    TON_SCALE = await Factory.get_pool(PoolType.VOLATILE, [TON, SCALE], provider)
    SCALE_BOLT = await Factory.get_pool(PoolType.VOLATILE, [SCALE, BOLT], provider)

    swap_amount = int(float(input("Enter swap amount(TON): ")) * 1e9)
    swap_params = SwapParams(deadline=int(time.time() + 60 * 5),
                             recipient_address=wallet.address)

    swap = VaultNative.create_swap_payload(amount=swap_amount,
                                           pool_address=TON_SCALE.address,
                                           swap_params=swap_params,
                                           _next=SwapStep(pool_address=SCALE_BOLT.address))

    await wallet.transfer(destination="EQDa4VOnTYlLvDJ0gZjNYm5PXfSmmtL6Vs6A_CZEtXCNICq_", # native vault
                          amount=int(swap_amount + 0.3*1e9),
                          body=swap)

    await provider.close_all()

asyncio.run(main())
