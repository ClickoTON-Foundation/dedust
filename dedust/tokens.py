from .functions import get_reserves, get_liquidity, get_price, get_volume
from .api import API

class Token():
    def __init__(self, api: API, address: str):
        self.api = api
        self.address = address
    
    async def get_data(self):
        return await self.api.get_token(self.address)
    
    async def update(self):
        self.pool, self.index = await self.get_data()
        self.reserves = await get_reserves(self.pool)
    
    async def get_liquidity(self):
        await self.update()
        
        return await get_liquidity(self.pool, self.index)
    
    async def get_price(self):
        await self.update()
        
        return await get_price(await self.get_liquidity())
    
    async def get_volume(self):
        await self.update()
        
        return await get_volume(self.pool, self.index)
