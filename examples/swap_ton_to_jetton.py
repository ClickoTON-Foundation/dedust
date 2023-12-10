from dedust import Asset, Factory, PoolType, SwapParams, VaultNative
from pytoniq import WalletV4R2, LiteBalancer
import asyncio
import time

mnemonics = ["your", "mnemonics", "here"]

async def main():
    provider = LiteBalancer.from_mainnet_config(1)
    await provider.start_up()

    wallet = await WalletV4R2.from_mnemonic(provider=provider, mnemonics=mnemonics)

    SCALE_ADDRESS = "EQBlqsm144Dq6SjbPI4jjZvA1hqTIP3CvHovbIfW_t-SCALE"

    TON = Asset.native()
    SCALE = Asset.jetton(SCALE_ADDRESS)

    pool = await Factory.get_pool(pool_type=PoolType.VOLATILE,
                                  assets=[TON, SCALE],
                                  provider=provider)
                                  
    swap_params = SwapParams(deadline=int(time.time() + 60 * 5),
                             recipient_address=wallet.address)
    swap_amount = int(float(input("Enter swap amount: ")) * 1e9)

    swap = VaultNative.create_swap_payload(amount=swap_amount,
                                           pool_address=pool.address,
                                           swap_params=swap_params)

    swap_amount = int(swap_amount + (0.25*1e9)) # 0.25 = gas_value

    await wallet.transfer(destination="EQDa4VOnTYlLvDJ0gZjNYm5PXfSmmtL6Vs6A_CZEtXCNICq_", # native vault
                          amount=swap_amount,
                          body=swap)

asyncio.run(main())