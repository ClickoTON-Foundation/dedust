import aiohttp
from tonsdk.utils import Address
from tonsdk.boc import Cell, Slice

class Provider:
    def __init__(
        self, toncenter_url = "https://toncenter.com/api/v2", toncenter_api_key=None
    ):
        self.toncenter_url = toncenter_url
        self.headers = {"X-API-Key": toncenter_api_key} if toncenter_api_key != None else None
        self.session = aiohttp.ClientSession(headers=self.headers)

    async def _request(self, method, url, **kwargs):
        r = await self.session.request(method, url, **kwargs)
        return (await r.json())

    async def runGetMethod(address, method, stack = []):
        payload = {
            "address": address.to_string(1, 1, 1) if type(address) == Address else address,
            "method": method,
            "stack": stack
        }

        r = await self._request("POST",
                                f"{self.toncenter_url}/runGetMethod",
                                json=payload)
        stack = []
        for s in r["result"]["stack"]:
            if s[0] == "num":
                stack.append({"type": "int", "value": int(r[1], 16)})
            elif s[0] == "null":
                stack.append({"type": "null"})
            elif s[0] == "cell":
                stack.append({"type": "cell", "value": Cell.one_from_boc(s[1]["bytes"])})
            elif s[0] == "slice":
                stack.append({"type": "slice", "value": Cell.one_from_boc(s[1]["bytes"])})
            elif s[0] == "builder":
                stack.append({"type": "builder", "value": Cell.one_from_boc(s[1]["bytes"])})

        return stack

    async def getState(address):
        r = await self._request("GET",
                                f"{self.toncenter_url}/getAddressInformation",
                                params={"address": address.to_string(1, 1, 1) if type(address) == Address else address})
        return r["result"]["account_state"]