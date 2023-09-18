from tonsdk.utils import Address
from tonsdk.boc import begin_cell, Cell
from typing import Union, Type
from ..common.asset import Asset
from ....api import Provider


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
        deadline: int = 0,
        recipient_address: Union[Address, None] = None,
        referral_address: Union[Address, None] = None,
        fulfill_payload: Union[Cell, None] = None,
        reject_payload: Union[Cell, None] = None
    ):
        self.deadline: int = 0,
        self.recipient_address: Union[Address, None] = None,
        self.referral_address: Union[Address, None] = None,
        self.fulfill_payload: Union[Cell, None] = None,
        self.reject_payload: Union[Cell, None] = None

class Vault:
    def __init__(
        self, address: [Address, str]
    ):
        self.address = Address(address) if type(address) == str else address
    
    async def get_asset(self, provider: Provider) -> Asset:
        stack = await provider.runGetMethod(address=self.address,
                                             method="get_asset")
        return Asset.from_slice(stack[0]["value"].begin_parse())

    @staticmethod
    def pack_swap_params(swapParams: SwapParams) -> Cell:
        return begin_cell()\
            .store_uint(swapParams.deadline, 32)\
            .store_address(swapParams.recipientAddress)\
            .store_address(swapParams.referralAddress)\
            .store_maybe_ref(swapParams.fulfillPayload)\
            .store_maybe_ref(swapParams.rejectPayload)\
            .end_cell()

    @staticmethod
    def pack_swap_step(pool_address: Address, limit: int = 0, _next: SwapStep = None) -> Cell:
        return begin_cell()\
            .store_address(pool_address)\
            .store_uint(0, 1)\
            .store_coins(limit)\
            .store_maybe_ref(_next if Vault.pack_swap_step(pool_address, limit, _next) else None)\
            .end_cell()