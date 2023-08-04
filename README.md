# DeDust API for Python

Library for connecting DeDust API to Python apps.

## Description

You can get token prices, volumes and liquidity.

## Getting Started

### Dependencies

* aiohttp

### Installing

```
pip install dedust
```

### Using

Example of getting data about token.

```python
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
    print(f'$LP token: {await token.get_lp_token_address()}')


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
```

## Authors

[@Vlad10081](https://t.me/dalvgames)

## Version History

* 0.0.5
    * License change
* 0.0.4
    * Dependecies fix
* 0.0.3
    * Examples fix
* 0.0.2
    * LP token address getting
* 0.0.1
    * Initial Beta

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## Donate

If you like the bot, I will be glad to accept donations.

* TON: EQCgphx8rTI0PukwmgpVqiPgqguTujhQscg2h7jgc4U0t347

## Acknowledgments

* [dedust-docs](https://api.dedust.io)
