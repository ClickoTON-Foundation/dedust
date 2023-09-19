from dedust import Asset, Factory, PoolType, Provider, JettonRoot, JettonWallet, VaultJetton
import asyncio
from tonsdk.utils import Address, bytes_to_b64str
from tonsdk.contract.wallet import Wallets, WalletVersionEnum

mnemonics = ["your", "mnemonics", "here"]

mnemonics, pub_k, priv_k, wallet = Wallets.from_mnemonics(mnemonics=mnemonics, version=WalletVersionEnum.v4r2,
                                                          workchain=0)

async def main():
    provider = Provider(toncenter_api_key="6b0862cc1f56a87e70a73923d420a5e43de57faf567dca61de6c2b733452bcb5")

    recipient_address = wallet.address

    SCALE_ADDRESS = Address("EQBlqsm144Dq6SjbPI4jjZvA1hqTIP3CvHovbIfW_t-SCALE")

    SCALE = Asset.jetton(SCALE_ADDRESS)
    TON = Asset.native()

    assets = [TON, SCALE]
    target_balances = [int(float(input("Ton amount: ")) * 1e9),
                       int(float(input("Scale amount: "))*1e9)]

    scale_vault = await Factory.get_jetton_vault(SCALE_ADDRESS, provider)
    scale_root = JettonRoot.create_from_address(SCALE_ADDRESS)
    scale_wallet = await scale_root.get_wallet(recipient_address, provider)

    ton_vault = await Factory.get_native_vault(provider)
    
    # Deposit TON to vault
    ton_payload = ton_vault.create_deposit_liquidity_payload(pool_type=PoolType.VOLATILE,
                                                             assets=assets,
                                                             target_balances=target_balances,
                                                             amount=target_balances[0])

    seqno = await provider.runGetMethod(address=recipient_address, method="seqno")
    query = wallet.create_transfer_message(to_addr=ton_vault.address,
                                           amount=target_balances[0] + (0.15*1e9),
                                           seqno=seqno[0]["value"],
                                           payload=ton_payload)
    boc = bytes_to_b64str(query["message"].to_boc(False))
    await provider.sendBoc(boc)

    await asyncio.sleep(3) # waiting

    scale_root = JettonRoot.create_from_address(SCALE_ADDRESS)
    scale_wallet = await scale_root.get_wallet(recipient_address, provider)

    # Deposit SCALE to vault
    scale_payload = scale_wallet.create_transfer_payload(
        destination=scale_vault.address,
        amount=target_balances[1],
        response_address=recipient_address,
        forward_amount=int(0.4*1e9),
        forward_payload=VaultJetton.create_deposit_liquidity_payload(poolType=PoolType.VOLATILE,
                                                                     assets=assets,
                                                                     target_balances=target_balances)
    )

    seqno = await provider.runGetMethod(address=recipient_address, method="seqno")
    query = wallet.create_transfer_message(to_addr=scale_wallet.address,
                                           amount=int(0.5*1e9),
                                           seqno=seqno[0]["value"],
                                           payload=scale_payload)

    boc = bytes_to_b64str(query["message"].to_boc(False))
    await provider.sendBoc(boc)

asyncio.run(main())
