import asyncio
from dedust.api import API
from dedust.tokens import Token

TOKEN = 'EQBlqsm144Dq6SjbPI4jjZvA1hqTIP3CvHovbIfW_t-SCALE'

async def main():
    api = API()
    token = Token(api, TOKEN)
    
    print(f'$SCALE price: {await token.get_price()} TON')
    print(f'Volume: {(await token.get_volume())[0]} TON')
    print(f'Liquidity: {(await token.get_liquidity())[0]} TON')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
