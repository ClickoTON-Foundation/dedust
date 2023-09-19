# DeDust SDK for Python

Analogue of DeDust SDK for Python.

## Description

You can swap tokens, deposit liquidity and many more.

## Getting Started

### Dependencies

* aiohttp
* tonsdk

### Installing

```
pip install dedust
```

### Using

Example of buying $SCALE using SDK.

```python
from dedust import Asset, Factory, PoolType, Provider, SwapParams, VaultNative
import asyncio
import time
from tonsdk.utils import Address, bytes_to_b64str
from tonsdk.contract.wallet import Wallets, WalletVersionEnum

mnemonics = ["your", "mnemonics", "here"]

mnemonics, pub_k, priv_k, wallet = Wallets.from_mnemonics(mnemonics=mnemonics, version=WalletVersionEnum.v4r2,
                                                          workchain=0)
async def main():
    provider = Provider()

    SCALE_ADDRESS = Address("EQBlqsm144Dq6SjbPI4jjZvA1hqTIP3CvHovbIfW_t-SCALE")

    TON = Asset.native()
    SCALE = Asset.jetton(SCALE_ADDRESS)


    pool = await Factory.get_pool(pool_type=PoolType.VOLATILE,
                                  assets=[TON, SCALE],
                                  provider=provider)
                                  
    swap_params = SwapParams(deadline=int(time.time() + 60 * 5),
                             recipient_address=wallet.address)
    swap_amount = float(input("Enter swap TON amount: ")) * 1e9


    swap = VaultNative.create_swap_payload(amount=swap_amount,
                                           pool_address=pool.address,
                                           swap_params=swap_params)

    swap_amount = int(swap_amount + (0.25 * 1e9)) # 0.25 = gas_value

    seqno = await provider.runGetMethod(address=wallet.address, method="seqno")
    query = wallet.create_transfer_message(to_addr=Address("EQDa4VOnTYlLvDJ0gZjNYm5PXfSmmtL6Vs6A_CZEtXCNICq_"),
                                           amount=swap_amount,
                                           seqno=seqno[0]["value"],
                                           payload=swap)

    boc = bytes_to_b64str(query["message"].to_boc(False))
    await provider.sendBoc(boc)

    # or:
    # print(f"https://app.tonkeeper.com/transfer/EQDa4VOnTYlLvDJ0gZjNYm5PXfSmmtL6Vs6A_CZEtXCNICq_?amount={swap_amount}&bin={bytes_to_b64str(swap.to_boc(False))}")

asyncio.run(main())
```

## Authors

[@shibdev](https://t.me/dogpy)
[@VladPavly](https://t.me/dalvpv)

## Version History

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

* TON: EQAsl59qOy9C2XL5452lGbHU9bI3l4lhRaopeNZ82NRK8nlA
       EQCgphx8rTI0PukwmgpVqiPgqguTujhQscg2h7jgc4U0t347

## Acknowledgments

* [dedust-sdk](https://github.com/dedust-io/sdk)
* [dedust-docs](https://api.dedust.io)

