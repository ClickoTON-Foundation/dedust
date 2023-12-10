from dedust import Asset, Factory, PoolType, SwapParams, SwapStep, JettonRoot, JettonWallet, VaultJetton, Pool
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

    pool = await Factory.get_pool(PoolType.VOLATILE, [TON, SCALE], provider)
    lp_wallet = await pool.get_wallet(wallet.address, provider)

    burn_payload = lp_wallet.create_burn_payload(
        amount=(await lp_wallet.get_balance(provider))
    )
    await wallet.transfer(destination=lp_wallet.address,
                          amount=int(0.5*1e9),
                          body=burn_payload)

asyncio.run(main())
