from tonsdk.utils import Address
from tonsdk.boc import Cell, begin_cell
from typing import Union, Type
from ..pool import PoolType
from ..common import Asset
from ..common.readiness_status import ReadinessStatus
from ....api import Provider


class LiquidityDeposit:
    def __init__(
        address: Union[Address, str]
    ):
        self.address = Address(address) if type(address) == str else address
    
    @staticmethod
    def create_from_address(address: Union[Address, str]) -> Type["LiquidityDeposit"]:
        return LiquidityDeposit(address)

    async def get_readiness_status(provider: Provider) -> ReadinessStatus:
        state = await provider.getState(self.address)
        if state != "active":
            return ReadinessStatus.NOT_DEPLOYED
  
        return ReadinessStatus.READY

    async def get_owner_address(self, provider: Provider) -> Address:
        stack = await provider.runGetMethod(address=self.address,
                                            method="get_owner_addr")
        return stack[0]["value"].read_msg_addr()
    
    async def get_pool_address(self, provider: Provider) -> Address:
        stack = await provider.runGetMethod(address=self.address,
                                            method="get_pool_addr")
        return stack[0]["value"].read_msg_addr()
    
    async def get_pool_params(self, provider: Provider) -> list:
        stack = await provider.runGetMethod(address=self.address,
                                            method="get_pool_params")
        pool_type = stack[0]["value"]
        assets: [Asset, Asset] = [
            Asset.from_slice(stack[1]["value"].begin_parse()),
            Asset.from_slice(stack[2]["value"].begin_parse())
        ]

        return [
            pool_type,
            assets
        ]
    
    async def get_target_balances(self, provider: Provider) -> list:
        stack = await provider.runGetMethod(address=self.address,
                                            method="get_target_balances")
        return [stack[0]["value"], stack[1]["value"]]

    async def get_balances(self, provider: Provider) -> list:
        stack = await provider.runGetMethod(address=self.address,
                                            method="get_balances")
        return [stack[0]["value"], stack[1]["value"]]

    async def get_is_processing(self, provider: Provider) -> bool:
        stack = await provider.runGetMethod(address=self.address,
                                            method="is_processing")
        return bool(stack[0]["value"])
    
    async def get_minimal_lp_amount(self, provider: Provider) -> int:
        stack = await provider.runGetMethod(address=self.address,
                                            method="get_min_lp_amount")
        return stack[0]["value"]
    
    async def create_cancel_deposit_payload(
        self,
        query_id: int = 0,
        payload: Union[Cell, None] = None
    ) -> Cell:
        return begin_cell()\
            .store_uint(0x166cedee, 32)\
            .store_uint(query_id, 64)\
            .store_maybe_ref(payload)\
            .end_cell()
            