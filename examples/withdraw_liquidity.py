from dedust import Asset, Factory, PoolType, Provider, SwapParams, SwapStep, JettonRoot, JettonWallet, VaultJetton, Pool
import asyncio
from tonsdk.utils import Address, bytes_to_b64str
from tonsdk.contract.wallet import Wallets, WalletVersionEnum

mnemonics = ["your", "mnemonics", "here"]

mnemonics, pub_k, priv_k, wallet = Wallets.from_mnemonics(mnemonics=mnemonics, version=WalletVersionEnum.v4r2,
                                                          workchain=0)

async def main():
    provider = Provider()

    recipient_address = wallet.address

    SCALE_ADDRESS = Address("EQBlqsm144Dq6SjbPI4jjZvA1hqTIP3CvHovbIfW_t-SCALE")

    SCALE = Asset.jetton(SCALE_ADDRESS)
    TON = Asset.native()

    pool = await Factory.get_pool(PoolType.VOLATILE, [TON, SCALE], provider)
    lp_wallet = await pool.get_wallet(recipient_address, provider)

    burn_payload = lp_wallet.create_burn_payload(
        amount=(await lp_wallet.get_balance(provider))
    )

    seqno = await provider.runGetMethod(address=recipient_address, method="seqno")
    query = wallet.create_transfer_message(to_addr=lp_wallet.address,
                                           amount=int(0.5*1e9),
                                           seqno=seqno[0]["value"],
                                           payload=burn_payload)

    boc = bytes_to_b64str(query["message"].to_boc(False))
    await provider.sendBoc(boc)

asyncio.run(main())
