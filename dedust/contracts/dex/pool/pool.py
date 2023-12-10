from pytoniq import begin_cell, Cell, Address, LiteBalancer
from typing import Union, Type
from .pool_type import PoolType
from ..common.asset import Asset
from ...jettons import JettonWallet
from ..common.readiness_status import ReadinessStatus

class Pool:
    def __init__(
        self,
        address: Union[Address, str]
    ):
        self.address = Address(address) if type(address) == str else address
    
    @staticmethod
    def create_from_address(address: Union[Address, str]) -> Type["Pool"]:
        return Pool(address)
    
    async def get_readiness_status(self, provider: LiteBalancer) -> ReadinessStatus:
        state = await provider.get_account_state(self.address)
        state = state.state.type_
        if state != "active":
            return ReadinessStatus.NOT_DEPLOYED
        
        reserves = await self.get_reserves(provider)
        return ReadinessStatus.READY if reserves[0] > 0 and reserves[1] > 0 else ReadinessStatus.NOT_READY

    async def get_pool_type(self, provider: LiteBalancer) -> PoolType:
        stack = await provider.run_get_method(address=self.address,
                                              method="is_stable",
                                              stack=[])
        return stack[0]
    
    async def get_assets(self, provider: LiteBalancer) -> [Asset, Asset]:
        stack = await provider.run_get_method(address=self.address,
                                              method="get_assets",
                                              stack=[])
        return [
            Asset.from_slice(stack[0]),
            Asset.from_slice(stack[1])
        ]
    
    async def get_estimated_swap_out(
        self,
        asset_in: Asset,
        amount_in: int,
        provider: LiteBalancer
    ) -> list:
        stack = await provider.run_get_method(address=self.address,
                                              method="estimate_swap_out",
                                              stack=[asset_in.to_slice(), amount_in])
        return {
            "asset_out": Asset.from_slice(stack[0]),
            "amount_out": stack[1],
            "trade_fee": stack[2]
        }
    
    async def get_estimate_deposit_out(
        self,
        amounts: [int, int],
        provider: LiteBalancer
    ) -> list:
        stack = await provider.run_get_method(address=self.address,
                                              method="estimate_swap_out",
                                              stack=amounts)

        return {
            "deposits": [stack[0], stack[1]],
            "fair_supply": stack[2]
        }
    
    async def get_reserves(self, provider: LiteBalancer) -> list:
        stack = await provider.run_get_method(address=self.address,
                                              method="get_reserves",
                                              stack=[])
        return [stack[0], stack[1]]
    
    async def get_trade_fee(self, provider: LiteBalancer) -> int:
        stack = await provider.run_get_method(address=self.address,
                                              method="get_trade_fee",
                                              stack=[])

        numerator = stack[0]
        denominator = stack[1]

        return numerator / denominator

    async def get_wallet_address(self, owner_address: Address, provider: LiteBalancer) -> Address:
        stack = await provider.run_get_method(address=self.address,
                                              method="get_wallet_address",
                                              stack=[begin_cell().store_address(owner_address).end_cell().begin_parse()])
        return stack[0].load_address()

    async def get_wallet(self, owner_address: Address, provider: LiteBalancer) -> JettonWallet:
        return JettonWallet.create_from_address(await self.get_wallet_address(owner_address, provider))
