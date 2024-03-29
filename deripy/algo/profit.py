from typing import Literal
from pydantic import BaseModel, validate_call


class Commission(BaseModel):
    long: float
    short: float


class OptionParam(BaseModel):
    """
    st : int
        قیمتِ داراییِ پایه در زمانِ t
    k : int
        قیمتِ اعمال
    premium : int
        قیمتِ اختیار
    qty : int, default 1
        مقدار
    commission : Commission
        نرخِ کارمزدِ معامله که بسته به شرایط می‌تونه شاملِ کارمزدِ اعمال هم باشه
    """

    position: Literal["short", "long"]
    type_: Literal["call", "put"]
    st: int
    k: int
    premium: int
    qty: int = 1
    commission: Commission = Commission(long=0.0, short=0.0)


class AssetParam(BaseModel):
    """
    price : int
        قیمتِ
    st : int
        قیمتِ داراییِ پایه در زمانِ t

    qty : int, default 1
        مقدار
    commission : Commission
        نرخِ کارمزدِ معامله که بسته به شرایط می‌تونه شاملِ کارمزدِ اعمال هم باشه
    """

    position: Literal["short", "long"]
    price: int
    st: int
    qty: int = 1
    commission: Commission = Commission(long=0.0, short=0.0)


class OptionPositionProfit:
    """
    سودِ موقعیتِ اختیارِ-معامله رو محسابه می‌کنه.

    Parameters
    ----------
    param : OptionParam
    """

    @validate_call
    def __init__(self, param: OptionParam) -> None:
        self.param = param

    @property
    def _net_premium(self):
        f = 1 if self.param.position == "long" else -1
        return round(self.param.premium * (1 + self.param.commission.long * f), 2)

    @property
    def profit(self):
        ua_change = self.param.st - self.param.k
        p = 0
        match self.param.position:
            case "long":
                match self.param.type_:
                    case "call":
                        p = max(ua_change, 0) - self._net_premium
                    case "put":
                        p = max(-ua_change, 0) - self._net_premium
            case "short":
                match self.param.type_:
                    case "call":
                        p = -max(ua_change, 0) + self._net_premium
                    case "put":
                        p = -max(-ua_change, 0) + self._net_premium
        return p * self.param.qty

    def break_even(self):
        return self.param.st - self.profit


class AssetPositionProfit:
    """
    Calculate asset position profit.

    Parameters
    ----------
    price
        int, asset price at time of 0
    st
        int, asset price at time of t
    qty
        int, quantity
    """

    def __init__(self, param: AssetParam) -> None:
        self.param = param

    @property
    def profit(self):
        match self.param.position:
            case "long":
                return round(
                    (
                        self.param.st * (1 - self.param.commission.short)
                        - self.param.price * (1 + self.param.commission.long)
                    )
                    * self.param.qty,
                    2,
                )
            case "short":
                return round(
                    (
                        self.param.price * (1 - self.param.commission.short)
                        - self.param.st * (1 + self.param.commission.long)
                    )
                    * self.param.qty,
                    2,
                )
