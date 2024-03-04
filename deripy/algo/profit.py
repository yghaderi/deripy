from pydantic import BaseModel, validate_call


class Commission(BaseModel):
    long: float
    short: float


class OptionPositionProfit:
    """
    سودِ موقعیتِ اختیارِ-معامله رو محسابه می‌کنه.

    Parameters
    ----------
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

    @validate_call
    def __init__(
        self,
        st: int,
        k: int,
        premium: int,
        qty: int = 1,
        commission: Commission = Commission(long=0.0, short=0.0),
    ) -> None:
        self.st = st
        self.k = k
        self.premium = premium
        self.qty = qty
        self.commission = commission

    @property
    def long_call(self) -> float:
        """
        Calculate long call position profit.

        Returns
        -------
        int
        """
        return round((
            max(self.st - self.k, 0) - self.premium * (1 + self.commission.long)
        ) * self.qty, 2)

    @property
    def short_call(self) -> float:
        """Calculate short call position profit.

        Returns
        -------
        int
        """
        return round((
            -max(self.st - self.k, 0) + self.premium * (1 - self.commission.short)
        ) * self.qty,2)

    @property
    def long_put(self) -> float:
        """Calculate long put position profit.

        Returns
        -------
        int
        """
        return round((
            max(self.k - self.st, 0) - self.premium * (1 + self.commission.long)
        ) * self.qty,2)

    @property
    def short_put(self) -> float:
        """Calculate short call position profit.

        Returns
        -------
        int
        """
        return round((
            -max(self.k - self.st, 0) + self.premium * (1 - self.commission.short)
        ) * self.qty,2)


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

    def __init__(
        self,
        price: int,
        st: int,
        qty: int = 1,
        commission: Commission = Commission(long=0.0, short=0.0),
    ) -> None:
        self.price = price
        self.st = st
        self.qty = qty
        self.commission = commission

    @property
    def long(self) -> float:
        """
        Calculate long UA position profit.

        Returns
        -------
        int
        """
        return round((self.st - self.price * (1 + self.commission.long)) * self.qty,2)

    @property
    def short(self) -> float:
        """
        Calculate short UA position profit.

        Returns
        -------
        int
        """
        return round((self.price * (1 - self.commission.short) - self.st) * self.qty,2)
