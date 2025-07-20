from abc import ABC, abstractmethod
from dataclasses import dataclass
import datetime


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
    WACTHED_GAMES = {
        "lotto",
        "euromillions",
    }

    source: AbstractSource

    def fetch(self) -> dict[str, Game]:
        # Simulated fetch logic
        html_content = self.source.get()
        games_data = parse_lottery_html(html_content)
        games = {}
        for game in self.WACTHED_GAMES:
            if game in games_data:
                game_info = games_data[game]
                next_draw_date = game_info.get("next-draw-date")
                jackpot = game_info.get("next-draw-jackpot")
                if next_draw_date and jackpot:
                    games[game] = Game(
                        next_draw_date=next_draw_date,
                        jackpot=jackpot,
                    )
                else:
                    games[game] = None
            else:
                games[game] = None

        return games
