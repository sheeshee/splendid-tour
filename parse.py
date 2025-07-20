import decimal
from datetime import datetime, date
from decimal import Decimal

import bs4
from bs4 import BeautifulSoup

game_mappings = {
    "lotto": "Lotto",
    "euromillions": "EuroMillions",
    "thunderball": "Thunderball",
    "setforlife": "Set For Life",
    "lotto-hotpicks": "Lotto HotPicks",
    "euromillions-hotpicks": "EuroMillions HotPicks",
}

properties = [
    "next-draw-date",
    "price",
    "roll-count",
    "next-draw-jackpot",
    "next-draw-jackpot-short",
]


def parse_lottery_html(html_content):
    """
    Parse National Lottery HTML and extract game information.

    Returns:
        dict: Dictionary containing game information with game names as keys
    """
    soup = BeautifulSoup(html_content, "html.parser")
    games = {}

    for game_key, game_name in game_mappings.items():
        info = {}
        for property in properties:
            tag = soup.find("meta", {"name": f"{game_key}-{property}"})
            if tag:
                if isinstance(tag, bs4.element.Tag):
                    content = tag.get("content")
                    assert content is not None
                    content = str(content).strip()
                    if property == "next-draw-date":
                        info[property] = datetime.strptime(content, "%d-%m-%Y").date()
                    elif property == "next-draw-jackpot":
                        info[property] = clean_jackpot(content)
                    elif property == "next-draw-jackpot-short":
                        info[property] = content.replace("£", "")
                    elif property == "roll-count":
                        info[property] = int(content)
                    else:
                        info[property] = tag.get("content")
                else:
                    raise ValueError("tried parsing non-tag element", tag, type(tag))
        games[game_key] = info
    return games


def clean_jackpot(original_jackpot: str) -> int | str:
    jackpot = original_jackpot.strip().lower()
    pound_sign = "\u00a3"
    multiplier_groups = {
        ("million", "m"): 1_000_000,
        (
            "thousand",
            "k",
        ): 1_000,
    }
    jackpot_mag = 1
    for multipliers, value in multiplier_groups.items():
        for multiplier in multipliers:
            if multiplier in jackpot:
                jackpot_mag = value
                continue

    output = jackpot.replace(pound_sign, "").replace(",", "")
    for multipliers in multiplier_groups:
        for multiplier in multipliers:
            output = output.replace(multiplier, "")

    try:
        as_number = Decimal(output)
    except decimal.InvalidOperation:
        return original_jackpot
    return int(as_number * jackpot_mag)


if __name__ == "__main__":
    # For testing with the provided HTML
    import json
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "-f":
        # Read HTML from a file specified in command line arguments
        filename = sys.argv[2]

        with open(filename, "r", encoding="utf-8") as file:
            html_source = file.read()

    elif len(sys.argv) == 1:
        # read from stdin
        html_source = sys.stdin.read()
    else:
        raise ValueError(
            "Invalid arguments. Use -f <filename> to read from a file or pipe HTML content directly."
        )

    # Parse directly from the string
    games = parse_lottery_html(html_source)

    def serialize(obj):
        """Custom serializer for JSON to handle Decimal and datetime objects."""
        if isinstance(obj, Decimal):
            return str(obj)
        elif isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, date):
            return obj.isoformat()
        elif isinstance(obj, dict):
            return {k: serialize(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [serialize(item) for item in obj]
        else:
            return obj

    # Print results
    games = serialize(games)
    print(json.dumps(games, indent=2))
