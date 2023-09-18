from tonsdk.utils import Address, bytes_to_b64str
from tonsdk.boc import begin_cell, Cell
from typing import Union, Type
from ..api import Provider
from .jetton_wallet import JettonWallet

class JettonRoot:
    def __init__(
        address: Union[Address, str]
    ):
        self.address = Address(address) if type(address) == str else address
    
    @staticmethod
    def create_from_address(address: Union[Address]) -> Type["JettonWallet"]:
        return JettonRoot(address)

    async def get_wallet_address(owner_address: Address, provider: Provider) -> Address:
        stack = await provider.runGetMethod(address=self.address,
                                            method="get_wallet_address",
                                            stack=[
                                                "tvm.Slice",
                                                bytes_to_b64str(begin_cell().store_address(owner_address).end_cell().to_boc())
                                            ])

        return stack.read_msg_addr()
    
    async def get_wallet(owner_address: Address, provider: Provider) -> Type["JettonRoot"]:
        return JettonWallet.create_from_address(await self.get_wallet_address(owner_address, Address))
    
    async def get_jetton_data(provider: Provider) -> list:
        stack = await provider.runGetMethod(address=self.address,
                                            method="get_jetton_data")
        return {
            "total_supply": stack[0],
            "is_mintable": stack[1] != 0,
            "admin_address": stack[2].read_msg_addr(),
            "content": stack[3],
            "wallet_code": stack[4]
        }