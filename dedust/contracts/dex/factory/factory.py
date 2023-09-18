from tonsdk.utils import Address, bytes_to_b64str
from tonsdk.boc import begin_cell, Cell
from typing import Union, Type
from ..common.asset import Asset
from ..vault import VaultNative, VaultJetton
from ..liquidity_deposit import LiquidityDeposit
from ...jettons import JettonRoot
from ....api import Provider
from ..pool import Pool, PoolType


class Factory:
    def __init__(
        address: Union[Address, str]
    ):
        self.address = Address(address) if type(address) == str else address
    
    @staticmethod
    def create_from_address(address: Union[address, str]) -> Type["Factory"]:
        return Factory(address)
    
    def create_create_vault_payload(
        asset: Asset,
        query_id: int = 0
    ) -> Cell:
        return begin_cell()\
            .store_uint(0x21cfe02b, 32)\
            .store_uint(query_id, 64)\
            .store_slice(asset.to_slice())\
            .end_cell()
    
    async def get_vault_address(asset: Asset, provider: Provider) -> Address:
        stack = await provider.runGetMethod(address=self.address,
                                            method="get_vault_address",
                                            stack=[[
                                                "tvm.Slice",
                                                bytes_to_b64str(asset.to_slice().to_boc())
                                            ]])
        return stack[0]["value"].read_msg_addr()
    
    async def get_native_vault(provider: Provider) -> VaultNative:
        native_vault_address = await self.get_vault_address(Asset.native(), provider)

        return VaultNative.create_from_address(native_vault_address)

    async def get_jetton_vault(provider: Provider, jetton_root: jettonRoot) -> VaultJetton:
        jetton_vault_address = await self.get_vault_address(Asset.jetton(jetton_root), provider)

        return VaultJetton.create_from_address(jetton_vault_address)
    
    def create_create_volatile_pool_payload(
        assets: [Asset, Asset],
        query_id: int = 0
    ) -> Cell:
        return begin_cell()\
            .store_uint(0x97d51f2f, 32)\
            .store_uint(query_id, 64)\
            .store_slice(assets[0].to_slice())\
            .store_slice(assets[0].to_slice())\
            .end_cell()
    
    async def get_pool_address(
        pool_type: PoolType,
        assets: [Asset, Asset],
        provider: Provider
    ) -> Address:
        stack = await provider.runGetMethod(address=self.address,
                                            method="get_pool_address",
                                            stack=[
                                                [
                                                    "int",
                                                    str(PoolType.value)
                                                ],
                                                [
                                                    "tvm.Slice",
                                                    bytes_to_b64str(assets[0].to_slice().to_boc())
                                                ],
                                                [
                                                    "tvm.Slice",
                                                    bytes_to_b64str(assets[1].to_slice().to_boc())
                                                ]
                                            ])
        return stack[0]["value"].read_msg_addr()

    async def get_pool(
        pool_type: PoolType,
        assets: [Asset, Asset],
        provider: Provider
    ) -> Pool:
        pool_address = await self.get_pool_address(pool_type, assets, provider)

        return Pool.create_from_address(pool_address)
    
    async def get_liquidity_deposit_address(
        owner_address: Address,
        pool_type: PoolType,
        assets: [Asset, Asset]
    ) -> Address:
        stack = await provider.runGetMethod(address=self.address,
                                            method="get_liquidity_deposit_address",
                                            stack=[
                                                [
                                                    "tvm.Slice",
                                                    bytes_to_b64str(begin_cell().store_address(owner_address).end_cell().to_boc())
                                                ]
                                                [
                                                    "int",
                                                    str(PoolType.value)
                                                ],
                                                [
                                                    "tvm.Slice",
                                                    bytes_to_b64str(assets[0].to_slice().to_boc())
                                                ],
                                                [
                                                    "tvm.Slice",
                                                    bytes_to_b64str(assets[1].to_slice().to_boc())
                                                ]
                                            ])
    
    async def get_liquidity_deposit(
        owner_address: Address,
        pool_type: PoolType,
        assets: [Asset, Asset]
    ) -> LiquidityDeposit:
        liquidity_deposit_address = await self.get_liquidity_deposit_address(owner_address, pool_type, assets)

        return LiquidityDeposit.create_from_address(liquidity_deposit_address)
