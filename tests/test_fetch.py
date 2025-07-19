import datetime

from fetch import AbstractSource, Fetcher


class FakeSource(AbstractSource):
    def __init__(self):
        with open("tests/national_lottery_games.html", "r") as file:
            self.content = file.read()

    def get(self):
        return self.content


def test_fetch():
    source = FakeSource()
    fetcher = Fetcher(source=source)

    result = fetcher.fetch()

    game = result.get("euromillions")
    assert game is not None
    assert game.next_draw_date == datetime.date(2023, 10, 27)
    assert game.jackpot == 14_000_000
