import os
from dotenv import load_dotenv
import requests


load_dotenv()


if __name__ == "__main__":
    from fetch import NationalLotterySource, Fetcher

    source = NationalLotterySource()
    fetcher = Fetcher(source=source)
    games = fetcher.fetch()
    message = ""

    # National Lottery
    if games["lotto"].roll_count >= 5:
        message += f"Lotto must be won! Next draw: {games['lotto'].next_draw_date}, Jackpot: {games['lotto'].jackpot}"

    if games["euromillions"].jackpot >= 100_000_000:
        message += f"Euromillions jackpot is over £100 million! Next draw: {games['euromillions'].next_draw_date}, Jackpot: {games['euromillions'].jackpot}"

    requests.post(os.environ["WEBHOOK"], data=message.encode(encoding="utf-8"))
