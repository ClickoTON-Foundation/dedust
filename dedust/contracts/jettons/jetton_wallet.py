from tonsdk.utils import Address
from tonsdk.boc import begin_cell, Cell
from tonsdk.contract.token.ft import JettonWallet
from typing import Union, Type
from ...api import Provider


class JettonWallet:
    def __init__(
        self,
        address: Union[Address, str]
    ):
        self.address = Address(address) if type(address) == str else address
    
    @staticmethod
    def create_from_address(address: Union[Address]) -> Type["JettonWallet"]:
        return JettonWallet(address)

    def create_transfer_payload(
        self,
        destination: Address,
        amount: int,
        query_id: int = 0,
        response_address: Union[Address, None] = None,
        custom_payload: Union[Cell, None] = None,
        forward_amount: int = 0,
        forward_payload: Union[Cell, None] = None
    ) -> Cell:
        return begin_cell()\
            .store_uint(0xf8a7ea5, 32)\
            .store_uint(query_id, 64)\
            .store_coins(amount)\
            .store_address(destination)\
            .store_address(response_address)\
            .store_maybe_ref(custom_payload)\
            .store_coins(forward_amount)\
            .store_maybe_ref(forward_payload)\
            .end_cell()
    
    def create_burn_payload(
        self,
        amount: int,
        query_id: int = 0,
        response_address: Union[Address, None] = None,
        custom_payload: Union[Cell, None] = None
    ) -> Cell:
        return begin_cell()\
            .store_uint(0x595f07bc, 32)\
            .store_uint(query_id, 64)\
            .store_coins(amount)\
            .store_address(response_address)\
            .store_maybe_ref(custom_payload)\
            .end_cell()
    
    async def get_wallet_data(self, provider: Provider) -> list:
        stack = await provider.runGetMethod(address=self.address,
                                            method="get_wallet_data")
        return [stack[0]["value"], # balance
                stack[1]["value"].read_msg_addr(), #owner_address
                stack[2]["value"].read_msg_addr(), # minter_address
                stack[3]["value"]] # wallet_code
    
    async def get_balance(self, provider: Provider):
        balance = (await self.get_wallet_data(provider))[0]
        return balance
