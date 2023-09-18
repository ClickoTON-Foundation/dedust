from tonsdk.utils import Address
from tonsdk.boc import begin_cell, Cell
from typing import Union
from ..common.asset import Asset
from ....api import Provider


class SwapStep:
    def __init__(
        self,
        pool_address: Address,
        limit: int = 0,
        next: Union[SwapStep, None] = None
    ):
        self.pool_address = pool_address
        self.limit = limit
        self.next = next
        
class SwapParams:
    def __init__(
        self,
        deadline: int = 0,
        recipientAddress: Union[Address, None] = None,
        referralAddress: Union[Address, None] = None,
        fulfillPayload: Union[Cell, None] = None,
        rejectPayload: Union[Cell, None] = None
    ):
        self.deadline: int = 0,
        self.recipientAddress: Union[Address, None] = None,
        self.referralAddress: Union[Address, None] = None,
        self.fulfillPayload: Union[Cell, None] = None,
        self.rejectPayload: Union[Cell, None] = None

class Vault:
    def __init__(
        self, address: [Address, str]
    ):
        self.address = Address(address) if type(address) == str else address
    
    async def get_asset(self, provider: Provider) -> Asset:
        stack = await provider.runGetMethod(address=self.address,
                                             method="get_asset")
        return Asset.fromSlice(stack[0]["value"].begin_parse())

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
    def pack_swap_step(poolAddress: Address, limit: int = 0, _next=False) -> Cell:
        return begin_cell()\
            .store_address(poolAddress)\
            .store_uint(0, 1)\
            .store_coins(limit)\
            .store_maybe_ref(_next if Vault.pack_swap_step(poolAddress, _next) else None)\
            .end_cell()