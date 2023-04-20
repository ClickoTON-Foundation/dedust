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

Example of connecting wallet.

```python
from tonconnect.connector import Connector


connector = Connector('https://tonclick.online/ton-connect.json')
url = connector.connect('tonkeeper', 'test')

print(f'Universal connect url for Tonkeeper: {url}')

address = connector.get_address()
print(f'Successfuly connected {address}.')
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
