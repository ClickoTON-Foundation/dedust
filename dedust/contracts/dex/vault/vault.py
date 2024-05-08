from pytoniq import begin_cell, Cell, Address, LiteBalancer
from typing import Union, Type
from ..common.asset import Asset


class SwapStep:
    def __init__(
        self,
        pool_address: Address,
        limit: int = 0,
        _next: Union[Type["SwapStep"], None] = None
    ):
        self.pool_address = pool_address
        self.limit = limit
        self._next = _next
        
class SwapParams:
    def __init__(
        self,
        deadline = 0,
        recipient_address: Union[Address, str, None] = None,
        referral_address: Union[Address, str, None] = None,
        fulfill_payload: Union[Address, str, None] = None,
        reject_payload: Union[Address, str, None] = None
    ):
        self.deadline = deadline
        self.recipient_address = recipient_address
        self.referral_address = referral_address
        self.fulfill_payload = fulfill_payload
        self.reject_payload = reject_payload

class Vault:
    def __init__(
        self, address: [Address, str]
    ):
        self.address = Address(address) if type(address) == str else address
    
    async def get_asset(self, provider: LiteBalancer) -> Asset:
        stack = await provider.run_get_method(address=self.address,
                                              method="get_asset",
                                              stack=[])
        return Asset.from_slice(stack[0].begin_parse())

    @staticmethod
    def pack_swap_params(swap_params: Union[SwapParams, None]) -> Cell:
        if swap_params is None:
            return begin_cell()\
                .store_uint(0, 32)\
                .store_address(None)\
                .store_address(None)\
                .store_maybe_ref(None)\
                .store_maybe_ref(None)\
                .end_cell()
        else:
            return begin_cell()\
                .store_uint(swap_params.deadline, 32)\
                .store_address(swap_params.recipient_address)\
                .store_address(swap_params.referral_address)\
                .store_maybe_ref(swap_params.fulfill_payload)\
                .store_maybe_ref(swap_params.reject_payload)\
                .end_cell()

    @staticmethod
    def pack_swap_step(_next: SwapStep = None) -> Cell:
        if _next is None:
            return None

        return begin_cell()\
            .store_address(_next.pool_address)\
            .store_uint(0, 1)\
            .store_coins(_next.limit)\
            .store_maybe_ref(Vault.pack_swap_step(_next._next) if _next._next else None)\
            .end_cell()
            