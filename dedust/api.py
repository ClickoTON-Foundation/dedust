from httpx import AsyncClient
from tonsdk.utils import Address
from tonsdk.boc import Cell, Slice
from base64 import b64decode
import warnings


class Provider:
    def __init__(
        self, toncenter_url = "https://mainnet.tonhubapi.com", toncenter_api_key=None
    ):
        self.toncenter_url = toncenter_url
        self.headers = {"X-API-Key": toncenter_api_key} if toncenter_api_key != None else None
        self.client = AsyncClient(headers=self.headers)

    async def request(self, request_method: str, method: str, **kwargs):
        try:
            request = await self.client.request(
                method = request_method,
                url = self.toncenter_url + "/" + method.replace("/", ""),
                **kwargs
            )
            try:
                res = request.json()
            except BaseException:
                return {"error": "Invalid response", "context": request.text}
            
            if res.get("error"):
                raise Exception(res["error"])
            
            return res
        except BaseException as e:
            return {"error": f"{e}"}

    async def runGetMethod(self, address, method, stack = []):
        payload = {
            "address": address.to_string(1, 1, 1) if type(address) == Address else address,
            "method": method,
            "stack": stack
        }

        r = await self.request("POST",
                                "runGetMethod",
                                json=payload)

        stack = []
        for s in r["result"]["stack"]:
            if s[0] == "num":
                stack.append({"type": "int", "value": int(s[1], 16)})
            elif s[0] == "null":
                stack.append({"type": "null"})
            elif s[0] == "cell":
                stack.append({"type": "cell", "value": Cell.one_from_boc(b64decode(s[1]["bytes"])).begin_parse()})
            elif s[0] == "slice":
                stack.append({"type": "slice", "value": Cell.one_from_boc(b64decode(s[1]["bytes"])).begin_parse()})
            elif s[0] == "builder":
                stack.append({"type": "builder", "value": Cell.one_from_boc(b64decode(s[1]["bytes"]))})
        return stack

    async def getState(self, address):
        r = await self.request("GET",
                                "getAddressInformation",
                                params={"address": address.to_string(1, 1, 1) if type(address) == Address else address})
        return r["result"]["account_state"]

    async def sendBoc(self, boc):
        r = await self.request("POST",
                                "sendBoc",
                                json={"boc": boc})
        return r

warnings.filterwarnings("ignore", category=UserWarning, module="httpx._client") # Way to ignore httpx warning
