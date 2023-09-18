from tonsdk.utils import Address
from tonsdk.boc import begin_cell, Cell
from typing import Union, Type
from .vault import Vault, SwapParams, SwapStep
from ..common.readiness_status import ReadinessStatus
from ..common.asset import Asset
from ..pool import PoolType
from ....api import Provider


class VaultJetton:
    def __init__(
        self, address: Union[Address, str]
    ):
        self.address = Address(address) if type(address) == str else address

    @staticmethod
    def create_from_address(address: Union[Address, str]) -> Type["VaultJetton"]:
        return VaultJetton(address)
    
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
            .store_uint(0x40e108d6)\
            .store_uint(poolType.value, 1)\
            .store_slice(assets[0].to_slice())\
            .store_slice(assets[1].to_slice())\
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
        swapParams: SwapParams = None,
        _next: SwapStep = None
    ) -> Cell:
        return begin_cell()\
            .store_uint(0xe3a0d482, 32)\
            .store_address(pool_address)\
            .store_uint(0, 1)\
            .store_coins(limit)\
            .store_maybe_ref(begin_cell().end_cell())\
            .store_ref(Vault.pack_swap_params(swapParams))\
            .end_cell()
            