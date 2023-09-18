from tonsdk.utils import Address, bytes_to_b64str
from tonsdk.boc import begin_cell, Cell
from typing import Union, Type
from ...api import Provider
from .jetton_wallet import JettonWallet

class JettonRoot:
    def __init__(
        self,
        address: Union[Address, str]
    ):
        self.address = Address(address) if type(address) == str else address
    
    @staticmethod
    def create_from_address(address: Union[Address]) -> Type["JettonWallet"]:
        return JettonRoot(address)

    async def get_wallet_address(self, owner_address: Address, provider: Provider) -> Address:
        stack = await provider.runGetMethod(address=self.address,
                                            method="get_wallet_address",
                                            stack=[[
                                                "tvm.Slice",
                                                bytes_to_b64str(begin_cell().store_address(owner_address).end_cell().to_boc())
                                            ]])

        return stack[0]["value"].read_msg_addr()
    
    async def get_wallet(self, owner_address: Address, provider: Provider) -> JettonWallet:
        return JettonWallet.create_from_address(await self.get_wallet_address(owner_address, provider))
    
    async def get_jetton_data(provider: Provider) -> list:
        stack = await provider.runGetMethod(address=self.address,
                                            method="get_jetton_data")
        return {
            "total_supply": stack[0]["value"],
            "is_mintable": stack[1]["value"] != 0,
            "admin_address": stack[2]["value"].read_msg_addr(),
            "content": stack[3]["value"],
            "wallet_code": stack[4]["value"]
        }