from fetch import Game
from storage import GamesRepository
import datetime
import pathlib


def test_store(tmp_path: pathlib.Path):
    repo = GamesRepository(tmp_path / "games.yml")
    game = Game(
        next_draw_date=datetime.date(2023, 10, 1), jackpot=5000000, roll_count=2
    )
    repo.add("lotto", game)

    retrieved_games = repo.get_all()
    assert len(retrieved_games) == 1
    assert retrieved_games["lotto"].as_dict() == game.as_dict()
