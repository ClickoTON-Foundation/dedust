from dedust import Asset, Factory, PoolType, Provider
import asyncio
from tonsdk.utils import Address

async def main():
    provider = Provider()

    SCALE_ADDRESS = Address("EQBlqsm144Dq6SjbPI4jjZvA1hqTIP3CvHovbIfW_t-SCALE")

    TON = Asset.native()
    SCALE = Asset.jetton(SCALE_ADDRESS)

    pool = await Factory.get_pool(pool_type=PoolType.VOLATILE,
                                  assets=[TON, SCALE],
                                  provider=provider)
                                    
    price = (await pool.get_estimated_swap_out(asset_in=TON,
                                               amount_in=int(10*1e9),
                                               provider=provider))["amount_out"]
    print(f"10 TON = {price / 1e9} SCALE")

asyncio.run(main())