from pytoniq import begin_cell, Cell, Builder, Slice, Address, LiteBalancer
from typing import Union, Type
from .asset_type import AssetType
from .asset_error import AssetError

class Asset:
    def __init__(
        self,
        _type: AssetType,
        address: Union[Address, str, None] = None
    ):
        self._type = _type
        self.address = Address(address) if type(address) == str else address

    @staticmethod
    def native() -> Type["Asset"]:
        return Asset(AssetType.NATIVE)
    
    @staticmethod
    def jetton(minter: Union[Address, str]) -> Type["Asset"]:
        return Asset(AssetType.JETTON, minter)

    @staticmethod
    def from_slice(src: Slice) -> Type["Asset"]:
        _type = src.load_uint(4)
        if _type == AssetType.NATIVE.value:
            return Asset.native()

        elif _type == AssetType.JETTON.value:
            return Asset(AssetType.JETTON, f"{src.load_uint(8)}:{src.load_bytes(32).hex()}")

        else:
            return AssetError("Asset is not supported.")
    
    def equals(self, other: Type["Asset"]) -> bool:
        return self.to_string() == other.to_string()
    
    def write_to(self, builder: Builder) -> Builder:
        if self._type == AssetType.NATIVE:
            builder.store_uint(AssetType.NATIVE.value, 4)
            return builder

        elif self._type == AssetType.JETTON:
            builder.store_uint(AssetType.JETTON.value, 4).store_int(self.address.wc, 8).store_bytes(self.address.hash_part)
            return builder

        else:
            return AssetError("Asset is not supported.")
    
    def to_slice(self) -> Slice:
        if self._type == AssetType.NATIVE:
            return begin_cell().store_uint(0, 4).end_cell().begin_parse()

        elif self._type == AssetType.JETTON:
            return begin_cell().store_uint(AssetType.JETTON.value, 4).store_int(self.address.wc, 8).store_bytes(self.address.hash_part).end_cell().begin_parse()

        else:
            return AssetError("Asset is not supported.")
    
    def to_string(self) -> str:
        if self._type == AssetType.NATIVE:
            return "native"

        elif self._type == AssetType.JETTON:
            return f"jetton:{self.address.to_str(0, 0, 0)}"

        else:
            return AssetError("Asset is not supported.")
