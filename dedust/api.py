from .functions import get_pools, get_token


class API():
    def __init__(self):
        pass
    
    async def get_pools(self):
        return await get_pools()
    
    async def get_token(self, token: str):
        return await get_token(token, await self.get_pools())
