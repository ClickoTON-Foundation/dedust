from pytoniq import begin_cell, Cell, Address, LiteBalancer
from typing import Union, Type
from .jetton_wallet import JettonWallet

class JettonRoot:
    def __init__(
        self,
        address: Union[Address, str]
    ):
        self.address = Address(address) if type(address) == str else address
    
    @staticmethod
    def create_from_address(address: Union[Address, str]) -> Type["JettonWallet"]:
        return JettonRoot(address)

    async def get_wallet_address(self, owner_address: Union[Address, str], provider: LiteBalancer) -> Address:
        stack = await provider.run_get_method(address=self.address,
                                              method="get_wallet_address",
                                              stack=[begin_cell().store_address(owner_address).end_cell().begin_parse()])

        return stack[0].load_address()
    
    async def get_wallet(self, owner_address: Union[Address, str], provider: LiteBalancer) -> JettonWallet:
        return JettonWallet.create_from_address(await self.get_wallet_address(owner_address, provider))
    
    async def get_jetton_data(self, provider: LiteBalancer) -> list:
        stack = await provider.run_get_method(address=self.address,
                                              method="get_jetton_data",
                                              stack=[])
        return {
            "total_supply": stack[0],
            "is_mintable": stack[1] != 0,
            "admin_address": stack[2].begin_parse().load_address(),
            "content": stack[3],
            "wallet_code": stack[4]
        }