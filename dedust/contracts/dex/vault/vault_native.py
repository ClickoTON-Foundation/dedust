from pytoniq import begin_cell, Cell, Address, LiteBalancer
from typing import Union, Type
from .vault import Vault, SwapParams, SwapStep
from ..common.readiness_status import ReadinessStatus
from ..common.asset import Asset
from ..common.readiness_status import ReadinessStatus
from ..pool import PoolType


class VaultNative:
    def __init__(
        self, address: Union[Address, str]
    ):
        self.address = Address(address) if type(address) == str else address
    
    @staticmethod
    def create_from_address(address: Union[Address, str]) -> Type["VaultJetton"]:
        return VaultNative(address)
    
    async def get_readiness_status(self, provider: LiteBalancer) -> ReadinessStatus:
        state = await provider.get_account_state(self.address)
        state = state.state.type_
        if state != "active":
            return ReadinessStatus.NOT_DEPLOYED
  
        return ReadinessStatus.READY

    @staticmethod
    def create_deposit_liquidity_payload(
        pool_type: PoolType,
        assets: [Asset, Asset],
        target_balances: [int, int],
        amount: int,
        query_id: int = 0,
        minimal_lp_amount: int = 0,
        fulfill_payload: Union[Cell, None] = None,
        reject_payload: Union[Cell, None] = None
    ) -> Cell:
        return begin_cell()\
            .store_uint(0xd55e4686, 32)\
            .store_uint(query_id, 64)\
            .store_coins(amount)\
            .store_uint(pool_type.value, 1)\
            .store_cell(assets[0].to_slice())\
            .store_cell(assets[1].to_slice())\
            .store_ref(
                begin_cell()\
                .store_coins(minimal_lp_amount)\
                .store_coins(target_balances[0])\
                .store_coins(target_balances[1])\
                .end_cell()\
            )\
            .store_maybe_ref(fulfill_payload)\
            .store_maybe_ref(reject_payload)\
            .end_cell()

    @staticmethod
    def create_swap_payload(
        amount: int,
        pool_address: Address,
        limit: int = 0,
        query_id: int = 0,
        swap_params: SwapParams = None,
        _next: SwapStep = None
    ) -> Cell:
        return begin_cell()\
            .store_uint(0xea06185d, 32)\
            .store_uint(query_id, 64)\
            .store_coins(amount)\
            .store_address(pool_address)\
            .store_uint(0, 1)\
            .store_coins(limit)\
            .store_maybe_ref(Vault.pack_swap_step(_next))\
            .store_ref(Vault.pack_swap_params(swap_params))\
            .end_cell()
