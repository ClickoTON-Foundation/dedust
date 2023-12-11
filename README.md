# DeDust SDK for Python

Analogue of DeDust SDK for Python.

## Description

You can swap tokens, deposit liquidity and many more.

## Getting Started

### Dependencies

* pytoniq

### Installing

```
pip install dedust
```

### Using

Example of buying $SCALE using SDK.

```python
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
```

## Authors

[@shibdev](https://t.me/dogpy)
[@VladPavly](https://t.me/dalvpv)

## Version History

* 1.1.1
    * Removed httpx from dependencies
* 1.1.0
    * Change tonsdk to pytoniq
* 1.0.5
    * Changes
* 1.0.4
    * Bug fix
* 1.0.3
    * Fixes
* 1.0.2
    * Fixes and changes
* 1.0.1
    * Small fix
* 1.0.0
    * Remake to DeDust SDK analogue
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

If you like the library, I will be glad to accept donations.

* TON: EQCgphx8rTI0PukwmgpVqiPgqguTujhQscg2h7jgc4U0t347

## Acknowledgments

* [dedust-sdk](https://github.com/dedust-io/sdk)
* [dedust-docs](https://api.dedust.io)

