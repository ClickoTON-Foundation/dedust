import dedust
import time
from tonsdk.utils import Address, bytes_to_b64str

amount = 1*1e9

swap_params = dedust.SwapParams(deadline=int(time.time() + 60 * 5),
                                recipient_address=Address("EQAsl59qOy9C2XL5452lGbHU9bI3l4lhRaopeNZ82NRK8nlA"))
swap = dedust.VaultNative.create_swap_payload(amount=amount, pool_address=Address("EQDcm06RlreuMurm-yik9WbL6kI617B77OrSRF_ZjoCYFuny"), swapParams=swap_params)

boc = bytes_to_b64str(swap.to_boc(False))
print(f"Use these link: https://app.tonkeeper.com/transfer/EQDa4VOnTYlLvDJ0gZjNYm5PXfSmmtL6Vs6A_CZEtXCNICq_?amount={amount + 0.25*1e9}&bin={boc}")