
# IPL Data Scraper

This project scrapes cricket match data (from ESPN Cricinfo) for the Indian Premier League (IPL), including overs, match summaries, player statistics, and more, storing the results in CSV files.

## Project Structure

```
├── main.py               # Main script to initiate scraping of matches and overs.
├── scrape_match.py        # Script to handle scraping match data, including batting and bowling stats.
├── scrape_overs.py        # Script to scrape detailed overs data for a match.
├── requirements.txt       # Python dependencies for the project.
├── ipl/
│   ├── dim_players.csv    # CSV to store player information.
│   ├── batting_stats.csv  # CSV to store batting statistics of matches.
│   ├── bowling_stats.csv  # CSV to store bowling statistics of matches.
│   ├── match_summary.csv  # CSV to store match summaries.
│   ├── overs.csv          # CSV to store ball-by-ball data from overs.
```

## Prerequisites

Ensure that you have Python 3.6+ installed on your machine.

## Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

### 2. Set up a virtual environment

It is recommended to use a Python virtual environment to manage dependencies. Run the following commands:

```bash
python3 -m venv venv
source venv/bin/activate  # For Linux/MacOS
# or
venv\Scripts\activate  # For Windows
```

### 3. Install required dependencies

Once the virtual environment is activated, install the dependencies using `pip`:

```bash
pip install -r requirements.txt
```

### 4. Directory Setup

Ensure that the `ipl` folder exists in the project directory, as the scraped data will be saved to CSV files in this folder. If it doesn’t exist, create the directory:

```bash
mkdir ipl
```

## Running the Project

To start scraping IPL data, simply run the `main.py` script:

```bash
python main.py
```

The script will:

1. Scrape match schedules and retrieve match IDs.
2. Use match IDs to gather detailed match data, including overs and player statistics.
3. Store the scraped data in the corresponding CSV files located in the `ipl` folder.

## File Descriptions

- **`main.py`**: Scrapes the IPL match schedule and triggers the scraping of match details (overs, player stats, and summary) by calling functions from `scrape_overs.py` and `scrape_match.py`.
  
- **`scrape_match.py`**:
  - Fetches and stores match details such as team information, batting, and bowling statistics.
  - Stores the match summary in `match_summary.csv`, batting data in `batting_stats.csv`, and bowling data in `bowling_stats.csv`.
  
- **`scrape_overs.py`**:
  - Scrapes detailed ball-by-ball data from each over of a match and stores it in `overs.csv`.

## Example Output

- `dim_players.csv`: Stores information about players like name, role, and country.
- `batting_stats.csv`: Stores batting statistics of each player for each match.
- `bowling_stats.csv`: Stores bowling statistics of each player for each match.
- `match_summary.csv`: Stores overall match summaries including teams and results.
- `overs.csv`: Stores ball-by-ball data including bowler, batsman, and the runs scored.

## Notes

- The project fetches data using ESPN Cricinfo's API, and the URLs in the code are constructed based on the series ID for IPL (`2024-1410320`).
- Modify the `SERIES_ID` in `main.py` if you want to scrape data for another IPL season or cricket series.

---

