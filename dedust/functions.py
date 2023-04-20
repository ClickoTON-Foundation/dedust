import aiohttp


async def get_pools() -> list[dict]:
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.dedust.io/v2/pools') as resp:
            pools: dict = await resp.json()
    
    return pools

async def get_token(address: str, pools: dict) -> tuple[dict, int]:
    for pool in pools:
        ton, jetton = False, False
        for i, asset in enumerate(pool['assets']):
            if asset['type'] == 'native' and asset['metadata']['symbol'] == 'TON':
                ton = True
            elif asset['type'] == 'jetton' and asset['address'] == address:
                jetton = True
                jetton_index = i
        
        if ton and jetton:
            break
    
    return pool, jetton_index


async def get_reserves(pool: dict) -> tuple[int, float]:
    return tuple(map(int, pool['reserves']))

async def get_liquidity(pool: dict, jetton_index: int) -> float:
    ton_index = int(not jetton_index)
    
    reserves = await get_reserves(pool)
    
    return reserves[ton_index] / 10 ** 9, reserves[jetton_index] / 10 ** 9

async def get_price(liquidity: tuple) -> float:
    price = liquidity[0] / liquidity[1]
    
    return price

async def get_volume(pool: dict, jetton_index: int) -> tuple[int, float]:
    ton_index = int(not jetton_index)
    
    raw_volume = pool['stats']['volume']
    volume = tuple(map(int, raw_volume))
    
    return volume[ton_index] / 10 ** 9, volume[jetton_index] / 10 ** 9
