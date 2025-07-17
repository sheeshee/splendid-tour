from bs4 import BeautifulSoup
import re
from datetime import datetime

def parse_lottery_html(html_content):
    """
    Parse National Lottery HTML and extract game information.

    Returns:
        dict: Dictionary containing game information with game names as keys
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    games = {}

    # Extract information from meta tags first
    meta_games = extract_meta_info(soup)
    games.update(meta_games)

    # Extract information from the main content
    content_games = extract_content_info(soup)

    # Merge the information, preferring content info over meta info
    for game_name, game_info in content_games.items():
        if game_name in games:
            games[game_name].update(game_info)
        else:
            games[game_name] = game_info

    return games

def extract_meta_info(soup):
    """Extract game information from meta tags."""
    games = {}

    # Define game name mappings
    game_mappings = {
        'lotto': 'Lotto',
        'euromillions': 'EuroMillions',
        'thunderball': 'Thunderball',
        'setforlife': 'Set For Life',
        'lotto-hotpicks': 'Lotto HotPicks',
        'euromillions-hotpicks': 'EuroMillions HotPicks'
    }

    # Extract meta information
    for game_key, game_name in game_mappings.items():
        game_info = {}

        # Next draw date
        date_meta = soup.find('meta', {'name': f'{game_key}-next-draw-date'})
        if date_meta:
            game_info['next_draw_date'] = date_meta.get('content', '')

        # Price
        price_meta = soup.find('meta', {'name': f'{game_key}-price'})
        if price_meta:
            game_info['price'] = f"£{price_meta.get('content', '')}"

        # Jackpot
        jackpot_meta = soup.find('meta', {'name': f'{game_key}-next-draw-jackpot'})
        if jackpot_meta:
            game_info['jackpot'] = jackpot_meta.get('content', '')

        # Draw day
        day_meta = soup.find('meta', {'name': f'{game_key}-next-draw-day'})
        if day_meta:
            game_info['draw_day'] = day_meta.get('content', '')

        # Roll count (if applicable)
        roll_meta = soup.find('meta', {'name': f'{game_key}-roll-count'})
        if roll_meta:
            roll_count = roll_meta.get('content', '')
            if roll_count and roll_count != '0':
                game_info['roll_count'] = int(roll_count)

        if game_info:
            games[game_name] = game_info

    return games

def extract_content_info(soup):
    """Extract game information from the main content."""
    games = {}

    # Find all game containers
    game_containers = soup.find_all('div', class_='cuk_all_games_container')

    for container in game_containers:
        game_info = {}

        # Extract game name
        game_brand = container.find('h2', class_='game_brand')
        if not game_brand:
            continue

        game_name_elem = game_brand.find('span', class_='game_brand_text')
        if not game_name_elem:
            continue

        game_name = game_name_elem.get_text(strip=True)

        # Extract draw information
        draw_info = container.find('div', class_='draw_information')
        if draw_info:
            # Next draw day
            next_draw_elem = draw_info.find('span', class_='headline')
            if not next_draw_elem:
                next_draw_elem = draw_info.find('span', class_='headline-1')
            if next_draw_elem:
                game_info['draw_day'] = next_draw_elem.get_text(strip=True)

            # Jackpot amount
            amount_elem = draw_info.find('span', class_='amount')
            if amount_elem:
                # Clean up the amount text
                amount_text = amount_elem.get_text(strip=True)
                amount_text = re.sub(r'[*Δ]', '', amount_text)
                game_info['jackpot'] = amount_text

        # Extract game information panel
        game_info_panel = container.find('div', class_='game_information')
        if game_info_panel:
            # Price
            price_elem = game_info_panel.find('span', class_='amount')
            if price_elem:
                game_info['price'] = price_elem.get_text(strip=True)

            # Draw days
            panel_copy = game_info_panel.find('p', class_='panel-copy')
            if panel_copy:
                game_info['draw_days'] = panel_copy.get_text(strip=True)

        if game_info:
            games[game_name] = game_info

    return games

def format_output(games):
    """Format the games dictionary for better readability."""
    formatted_games = {}

    for game_name, info in games.items():
        formatted_game = {
            'name': game_name,
            'jackpot': info.get('jackpot', 'N/A'),
            'price': info.get('price', 'N/A'),
            'next_draw_date': info.get('next_draw_date', 'N/A'),
            'draw_day': info.get('draw_day', 'N/A'),
            'draw_days': info.get('draw_days', 'N/A')
        }

        # Add roll count if present
        if 'roll_count' in info:
            formatted_game['roll_count'] = info['roll_count']

        formatted_games[game_name] = formatted_game

    return formatted_games

# Example usage
def main():
    # Read HTML from file
    with open('lottery.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse the HTML
    games = parse_lottery_html(html_content)

    # Format and display the results
    formatted_games = format_output(games)

    # Print the results
    import json
    print(json.dumps(formatted_games, indent=2))

    # Or print in a more readable format
    print("\n" + "="*50 + "\n")
    for game_name, info in formatted_games.items():
        print(f"Game: {game_name}")
        print(f"  Jackpot: {info['jackpot']}")
        print(f"  Price: {info['price']}")
        print(f"  Next Draw: {info['draw_day']} ({info['next_draw_date']})")
        if 'draw_days' in info and info['draw_days'] != 'N/A':
            print(f"  Draw Days: {info['draw_days']}")
        if 'roll_count' in info:
            print(f"  Roll Count: {info['roll_count']}")
        print()

if __name__ == "__main__":
    # For testing with the provided HTML
    html_sample = """<paste your HTML content here>"""

    # Parse directly from the string
    games = parse_lottery_html(html_sample)
    formatted_games = format_output(games)

    # Print results
    import json
    print(json.dumps(formatted_games, indent=2))
