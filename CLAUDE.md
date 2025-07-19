# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Status

This is a Python project for parsing National Lottery HTML data. The project uses Beautiful Soup for HTML parsing and includes a command-line interface for processing lottery game information.

## Project Structure

- `parse.py` - Main Python module containing HTML parsing logic for National Lottery games
- `pyproject.toml` - Python project configuration file
- `sample_html/` - Directory containing sample HTML files for testing
- `README.md` - Project documentation

## Dependencies

The project uses Python 3.11+ and requires:
- Beautiful Soup 4 (for HTML parsing)
- Standard library modules: re, datetime, json

## Development Commands

To run the lottery HTML parser:
```bash
python parse.py
```

The parser can process HTML content from files or strings and extracts game information including jackpots, prices, draw dates, and roll counts.

## Architecture

The project follows a modular architecture:
- `parse_lottery_html()` - Main parsing function
- `extract_meta_info()` - Extracts game data from HTML meta tags
- `extract_content_info()` - Extracts game data from main content
- `format_output()` - Formats parsed data for display

The parser handles multiple lottery games including Lotto, EuroMillions, Thunderball, Set For Life, and their HotPicks variants.
