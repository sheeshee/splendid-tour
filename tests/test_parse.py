import pytest


from datetime import date

from parse import clean_jackpot, parse_lottery_html


@pytest.mark.parametrize(
    "jackpot, expected",
    [
        ("£1,000,000", 1000000),
        ("£96,000,000", 96000000),
    ],
)
def test_clean_jackpot(jackpot, expected):
    assert clean_jackpot(jackpot) == expected


def test_parse_html_output():
    with open("tests/national_lottery_games.html", "r") as file:
        html_content = file.read()

    games = parse_lottery_html(html_content)
    assert "euromillions" in games
    assert games["euromillions"]["next-draw-date"] == date(2025, 7, 18)
    assert games["euromillions"]["next-draw-jackpot"] == 96_000_000
