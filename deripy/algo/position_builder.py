from pydantic import BaseModel
from deripy.algo.profit import OptionPositionProfit, AssetPositionProfit, OptionParam, AssetParam


class SimulateRange(BaseModel):
    min: int
    max: int
    step: int


class PositionBuilder:
    """Build any position and get simulate profit.
    """

    def __init__(
            self,
            o_positions: list[OptionParam],
            ua_positions: list[AssetParam],
            st_range: SimulateRange,
    ) -> None:
        self.op = o_positions
        self.uap = ua_positions
        self.st_range = st_range
        self._st_range = range(
            st_range.min, st_range.max, st_range.get("step")
        )

    def simulate_profit(self) -> list[int]:
        """
        The simulation of profit for all given position within the specified range.

        Returns
        -------
        List[int]

        Examples
        --------
        """
        sim_profit = []
        for i in self.st_range:
            profit = 0
            profit += sum(
                [OptionPositionProfit(param.model_copy(update={"st": i})).profit for param in self.op]
            )
            profit += sum(
                [AssetPositionProfit(param.model_copy(update={"st": i})).profit for param in self.uap]
            )
            sim_profit.append(profit)
        return sim_profit
