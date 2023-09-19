from dedust import Asset, Factory, PoolType, Provider, JettonRoot, VaultJetton
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

    TON = Asset.native()
    SCALE = Asset.jetton(SCALE_ADDRESS)

    pool = await Factory.get_pool(PoolType.VOLATILE, [TON, SCALE], provider)
 
    scale_vault = await Factory.get_jetton_vault(SCALE_ADDRESS, provider)
    scale_root = JettonRoot.create_from_address(SCALE_ADDRESS)
    scale_wallet = await scale_root.get_wallet(recipient_address, provider)

    swap_amount = int(float(input("Enter swap amount(SCALE): ")) * 1e9)
    swap = scale_wallet.create_transfer_payload(
        destination=scale_vault.address,
        amount=swap_amount,
        response_address=recipient_address,
        forward_amount=int(0.25*1e9),
        forward_payload=VaultJetton.create_swap_payload(pool_address=pool.address)
    )

    seqno = await provider.runGetMethod(address=recipient_address, method="seqno")
    query = wallet.create_transfer_message(to_addr=scale_wallet.address,
                                           amount=int(0.3*1e9),
                                           seqno=seqno[0]["value"],
                                           payload=swap)

    boc = bytes_to_b64str(query["message"].to_boc(False))
    await provider.sendBoc(boc)

asyncio.run(main())
