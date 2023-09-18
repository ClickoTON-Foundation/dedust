from tonsdk.utils import Address
from tonsdk.boc import begin_cell
from typing import Union, Type


class JettonWallet:
    def __init__(
        address: Union[Address, str]
    ):
        self.address = Address(address) if type(address) == str else address
    
    @staticmethod
    def create_from_address(address: Union[Address]) -> Type["JettonWallet"]:
        return JettonWallet(address)

        