from tonsdk.utils import Address
from tonsdk.boc import begin_cell, Cell
from typing import Union, Type
from .Vault import Vault, swapParams
from ..common.readiness_status import ReadinessStatus
from ..common.asset import Asset
from ..pool import PoolType
from ....api import Provider


class VaultJetton:
    def __init__(
        self, address: Union[Address, str]
    ):
        self.address = Address(address) if type(address) == str else address
        self.DEPOSIT_LIQUIDITY = 0x40e108d6
        self.SWAP = 0xe3a0d482
    
    @staticmethod
    def create_from_address(address: Union[Address, str]) -> Type["VaultJetton"]:
        return VaultJetton(address)
    
    @staticmethod
    def create_deposit_liquidity_payload(
        poolType: PoolType,
        assets: [Asset, Asset],
        targetBalances: [int, int],
        minimalLpAmount: int = 0,
        fulfillPayload: Union[Cell, None] = None,
        rejectPayload: Union[Cell, None] = None
    ) -> Cell:
        return begin_cell()\
            .store_uint(self.DEPOSIT_LIQUIDITY)\
            .store_uint(poolType.value, 1)\
            .store_slice(assets[0].toSlice())\
            .store_slice(assets[1].toSlice())\
            .store_coins(minimalLpAmount)\
            .store_coins(targetBalances[0])\
            .store_coins(targetBalances[1])\
            .store_maybe_ref(fulfillPayload)\
            .store_maybe_ref(rejectPayload)\
            .end_cell()

    @staticmethod
    def create_swap_payload(
        poolAddress: Address,
        limit: int = 0,
        swapParams: swapParams
    )