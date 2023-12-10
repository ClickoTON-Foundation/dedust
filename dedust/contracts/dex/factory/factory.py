from pytoniq import begin_cell, Cell, Address, LiteBalancer
from typing import Union, Type
from ..common.asset import Asset
from ..vault import VaultNative, VaultJetton
from ..liquidity_deposit import LiquidityDeposit
from ..pool import Pool, PoolType
from ...jettons import JettonRoot
from ....constants import MAINNET_FACTORY_ADDR


class Factory:
    @staticmethod
    def create_from_address(address: Union[Address, str]) -> Type["Factory"]:
        return Factory(address)
    
    @staticmethod
    def create_create_vault_payload(
        asset: Asset,
        query_id: int = 0
    ) -> Cell:
        return begin_cell()\
            .store_uint(0x21cfe02b, 32)\
            .store_uint(query_id, 64)\
            .store_slice(asset.to_slice())\
            .end_cell()
    
    @staticmethod
    async def get_vault_address(asset: Asset, provider: LiteBalancer) -> Address:
        stack = await provider.run_get_method(address=MAINNET_FACTORY_ADDR,
                                              method="get_vault_address",
                                              stack=[asset.to_slice()])
        return stack[0].load_address()
    
    @staticmethod
    async def get_native_vault(provider: LiteBalancer) -> VaultNative:
        native_vault_address = await Factory.get_vault_address(Asset.native(), provider)

        return VaultNative.create_from_address(native_vault_address)

    @staticmethod
    async def get_jetton_vault(jetton_root: JettonRoot, provider: LiteBalancer) -> VaultJetton:
        jetton_vault_address = await Factory.get_vault_address(Asset.jetton(jetton_root), provider)

        return VaultJetton.create_from_address(jetton_vault_address)
    
    @staticmethod
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
    
    @staticmethod
    async def get_pool_address(
        pool_type: PoolType,
        assets: [Asset, Asset],
        provider: LiteBalancer
    ) -> Address:
        stack = await provider.run_get_method(address=MAINNET_FACTORY_ADDR,
                                              method="get_pool_address",
                                              stack=[pool_type.value,
                                                     assets[0].to_slice(), assets[1].to_slice()]
                                              )
        return stack[0].load_address()

    @staticmethod
    async def get_pool(
        pool_type: PoolType,
        assets: [Asset, Asset],
        provider: LiteBalancer
    ) -> Pool:
        pool_address = await Factory.get_pool_address(pool_type, assets, provider)

        return Pool.create_from_address(pool_address)

    @staticmethod
    async def get_liquidity_deposit_address(
        owner_address: Address,
        pool_type: PoolType,
        assets: [Asset, Asset],
        provider: LiteBalancer
    ) -> Address:
        stack = await provider.run_get_method(address=MAINNET_FACTORY_ADDR,
                                              method="get_liquidity_deposit_address",
                                              stack=[begin_cell().store_address(owner_address).end_cell().begin_parse(),
                                                     pool_type.value,
                                                     assets[0].to_slice(),
                                                     assets[1].to_slice()
                                                ]
                                              )
        return stack[0].load_address()
    
    @staticmethod
    async def get_liquidity_deposit(
        owner_address: Address,
        pool_type: PoolType,
        assets: [Asset, Asset],
        provider: LiteBalancer
    ) -> LiquidityDeposit:
        liquidity_deposit_address = await Factory.get_liquidity_deposit_address(owner_address, pool_type, assets, provider)

        return LiquidityDeposit.create_from_address(liquidity_deposit_address)
