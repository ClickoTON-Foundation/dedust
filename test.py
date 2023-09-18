import dedust
import time
from tonsdk.utils import Address, bytes_to_b64str


nanotons_in_ton = 10 ** 9
amount = 1 * nanotons_in_ton


swap_params = dedust.SwapParams(
    deadline=int(time.time() + 60 * 5),
    recipient_address=Address('EQCgphx8rTI0PukwmgpVqiPgqguTujhQscg2h7jgc4U0t347')
)
swap = dedust.VaultNative.create_swap_payload(
    amount=amount, 
    pool_address=Address('EQDcm06RlreuMurm-yik9WbL6kI617B77OrSRF_ZjoCYFuny'), 
    swapParams=swap_params
)


boc = bytes_to_b64str(swap.to_boc(False))

amount_with_commission = int(amount + 0.25 * nanotons_in_ton)
link = f'https://app.tonkeeper.com/transfer/EQDa4VOnTYlLvDJ0gZjNYm5PXfSmmtL6Vs6A_CZEtXCNICq_?amount={amount_with_commission}&bin={boc}'

print(f'Use these link: {link}')