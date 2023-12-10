from pytoniq import begin_cell, Cell, Address, LiteBalancer
from typing import Union, Type
from ..pool import PoolType
from ..common import Asset
from ..common.readiness_status import ReadinessStatus


class LiquidityDeposit:
    def __init__(
        self,
        address: Union[Address, str]
    ):
        self.address = Address(address) if type(address) == str else address
    
    @staticmethod
    def create_from_address(address: Union[Address, str]) -> Type["LiquidityDeposit"]:
        return LiquidityDeposit(address)

    async def get_readiness_status(self, provider: LiteBalancer) -> ReadinessStatus:
        state = await provider.get_account_state(self.address)
        state = state.state.type_
        if state != "active":
            return ReadinessStatus.NOT_DEPLOYED
  
        return ReadinessStatus.READY

    async def get_owner_address(self, provider: LiteBalancer) -> Address:
        stack = await provider.run_get_method(address=self.address,
                                              method="get_owner_addr",
                                              stack=[])
        return stack[0].load_address()
    
    async def get_pool_address(self, provider: LiteBalancer) -> Address:
        stack = await provider.run_get_method(address=self.address,
                                              method="get_pool_addr",
                                              stack=[])
        return stack[0].load_address()
    
    async def get_pool_params(self, provider: LiteBalancer) -> list:
        stack = await provider.run_get_method(address=self.address,
                                              method="get_pool_params",
                                              stack=[])
        pool_type = stack[0].load_address()
        assets: [Asset, Asset] = [
            Asset.from_slice(stack[1].begin_parse()),
            Asset.from_slice(stack[2].begin_parse())
        ]

        return [
            pool_type,
            assets
        ]
    
    async def get_target_balances(self, provider: LiteBalancer) -> list:
        stack = await provider.run_get_method(address=self.address,
                                              method="get_target_balances",
                                              stack=[])
        return [stack[0], stack[1]]

    async def get_balances(self, provider: LiteBalancer) -> list:
        stack = await provider.run_get_method(address=self.address,
                                            method="get_balances",
                                            stack=[])
        return [stack[0], stack[1]]

    async def get_is_processing(self, provider: LiteBalancer) -> bool:
        stack = await provider.run_get_method(address=self.address,
                                              method="is_processing",
                                              stack=[])
        return bool(stack[0])
    
    async def get_minimal_lp_amount(self, provider: LiteBalancer) -> int:
        stack = await provider.run_get_method(address=self.address,
                                              method="get_min_lp_amount",
                                              stack=[])
        return stack[0]
    
    def create_cancel_deposit_payload(
        self,
        query_id: int = 0,
        payload: Union[Cell, None] = None
    ) -> Cell:
        return begin_cell()\
            .store_uint(0x166cedee, 32)\
            .store_uint(query_id, 64)\
            .store_maybe_ref(payload)\
            .end_cell()
            