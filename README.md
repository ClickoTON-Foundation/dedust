# DeDust API for Python

Library for connecting DeDust API to Python apps.

## Description

You can get token prices, volumes and liquidity.

## Getting Started

### Dependencies

* aiohttp

### Installing

```
git clone https://github.com/ClickoTON-Foundation/dedust.git
pip install -e dedust
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


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```

## Authors

[@Vlad10081](https://t.me/dalvgames)

## Version History

* 0.0.1
    * Initial Beta

## License

This project is licensed under the Apache License 2.0 - see the LICENSE.md file for details

## Donate

If you liked the library, I will be glad to donate.

* TON: EQCgphx8rTI0PukwmgpVqiPgqguTujhQscg2h7jgc4U0t347

## Acknowledgments

* [dedust-docs](https://api.dedust.io)
