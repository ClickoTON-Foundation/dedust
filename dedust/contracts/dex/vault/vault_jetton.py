from pytoniq import begin_cell, Cell, Address, LiteBalancer
from typing import Union, Type
from .vault import Vault, SwapParams, SwapStep
from ..common.readiness_status import ReadinessStatus
from ..common.asset import Asset
from ..common.readiness_status import ReadinessStatus
from ..pool import PoolType


class VaultJetton:
    def __init__(
        self, address: Union[Address, str]
    ):
        self.address = Address(address) if type(address) == str else address

    @staticmethod
    def create_from_address(address: Union[Address, str]) -> Type["VaultJetton"]:
        return VaultJetton(address)
    
    async def get_readiness_status(self, provider: LiteBalancer) -> ReadinessStatus:
        state = await provider.get_account_state(self.address)
        state = state.state.type_
        if state != "active":
            return ReadinessStatus.NOT_DEPLOYED

        stack = await provider.run_get_method(address=self.address,
                                              method="is_ready",
                                              stack=[])

        return ReadinessStatus.READY if bool(stack[0]) else ReadinessStatus.NOT_READY

    @staticmethod
    def create_deposit_liquidity_payload(
        poolType: PoolType,
        assets: [Asset, Asset],
        target_balances: [int, int],
        minimal_lp_amount: int = 0,
        fulfill_payload: Union[Cell, None] = None,
        reject_payload: Union[Cell, None] = None
    ) -> Cell:
        return begin_cell()\
            .store_uint(0x40e108d6, 32)\
            .store_uint(poolType.value, 1)\
            .store_cell(assets[0].to_slice())\
            .store_cell(assets[1].to_slice())\
            .store_coins(minimal_lp_amount)\
            .store_coins(target_balances[0])\
            .store_coins(target_balances[1])\
            .store_maybe_ref(fulfill_payload)\
            .store_maybe_ref(reject_payload)\
            .end_cell()

    @staticmethod
    def create_swap_payload(
        pool_address: Address,
        limit: int = 0,
        _next: Address = None,
        swap_params: SwapParams = None
    ) -> Cell:
        return begin_cell()\
            .store_uint(0xe3a0d482, 32)\
            .store_address(pool_address)\
            .store_uint(0, 1)\
            .store_coins(limit)\
            .store_maybe_ref(Vault.pack_swap_step(_next))\
            .store_ref(Vault.pack_swap_params(swap_params))\
            .end_cell()
            