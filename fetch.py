from abc import ABC, abstractmethod
from dataclasses import dataclass
import datetime
from decimal import Decimal


from parse import parse_lottery_html


class AbstractSource(ABC):
    @abstractmethod
    def get(self) -> str: ...


@dataclass
class Game:
    next_draw_date: datetime.date
    jackpot: int


@dataclass
class Fetcher:
    source: AbstractSource

    def fetch(self) -> dict[str, Game]:
        # Simulated fetch logic
        html_content = self.source.get()
        games_data = parse_lottery_html(html_content)
        result = {}
        for name, data in games_data.items():
            data["next_draw_date"] = datetime.datetime.strptime(
                data["next_draw_date"], "%d-%m-%Y"
            ).date()
            data["jackpot"] = Decimal(
                data["jackpot"].replace("£", "").replace(",", "").replace("M", "E6")
            )
            result[name] = Game(data["next_draw_date"], int(data["jackpot"]))
        return result
