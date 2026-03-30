# Python Assignments — Data Processing & Web Scraping

> Beginner-to-Intermediate Python exercises covering data manipulation and web scraping.

---

## Repository Structure

```
python-assignments/

 assignment1/
 assignment1.py
 students_data.xlsx
 logs/
 assignment1.log

 assignment2/
 assignment2.py
 scraped_output.json

 README.md
```

---

# Assignment 1 — NumPy, Pandas & Logging

## Objective

Read student data from an Excel file, perform data analysis using **NumPy** and **Pandas**, and log every step using Python's **logging** module.

---

## Libraries Used

| Library | Purpose |
|-----------|--------------------------------------|
| `pandas` | Read Excel, manipulate DataFrames |
| `numpy` | Numerical operations & statistics |
| `logging` | Track execution steps in a log file |
| `openpyxl`| Backend engine to read `.xlsx` files |

Install all dependencies:

```bash
pip install pandas numpy openpyxl
```

---

## Sample Data Preview — `students_data.xlsx`

> The Excel file contains the following sample records:

| StudentID | Name | Age | Math | Science | English | Grade |
|-----------|-----------------|-----|------|---------|---------|-------|
| 101 | Aarav Sharma | 20 | 88 | 76 | 91 | A |
| 102 | Priya Mehta | 21 | 72 | 85 | 68 | B |
| 103 | Rohan Verma | 19 | 55 | 60 | 73 | C |
| 104 | Sneha Iyer | 22 | 95 | 90 | 88 | A |
| 105 | Karan Patel | 20 | 40 | 55 | 62 | D |
| 106 | Divya Nair | 21 | 78 | 82 | 79 | B |
| 107 | Arjun Singh | 23 | 66 | 71 | 58 | C |
| 108 | Meera Joshi | 20 | 91 | 88 | 94 | A |
| 109 | Rahul Gupta | 22 | 33 | 45 | 50 | F |
| 110 | Ananya Reddy | 19 | 82 | 79 | 85 | B |

> **Columns Explained:**
> - `StudentID` — Unique identifier for each student
> - `Name` — Full name of the student
> - `Age` — Student's age
> - `Math`, `Science`, `English` — Marks out of 100
> - `Grade` — Letter grade assigned (A / B / C / D / F)

---

## What the Code Does (Step-by-Step)

1. **Sets up logging** — Logs to both console and a `.log` file
2. **Reads the Excel file** using `pandas.read_excel()`
3. **Explores the data** — shape, dtypes, missing values
4. **Computes statistics** using NumPy:
 - Mean, Median, Standard Deviation of each subject
 - Highest and lowest scorers
5. **Adds a new column** — `Total` (sum of all subject marks)
6. **Filters data** — Students who failed (any mark < 50)
7. **Groups data** — Average marks grouped by `Grade`
8. **Saves the processed output** back to Excel

---

## Full Code — `assignment1.py`

```python
import pandas as pd
import numpy as np
import logging
import os

# 
# 1. LOGGING SETUP
# 
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
 level=logging.INFO,
 format="%(asctime)s | %(levelname)s | %(message)s",
 handlers=[
 logging.FileHandler("logs/assignment1.log"),
 logging.StreamHandler()
 ]
)

logger = logging.getLogger(__name__)
logger.info("====== Assignment 1 Started ======")


# 
# 2. LOAD EXCEL FILE
# 
FILE_PATH = "students_data.xlsx"

try:
 df = pd.read_excel(FILE_PATH, engine="openpyxl")
 logger.info(f"File loaded successfully: {FILE_PATH}")
except FileNotFoundError:
 logger.error(f"File not found: {FILE_PATH}")
 raise


# 
# 3. BASIC EXPLORATION
# 
logger.info(f"Shape of dataset: {df.shape}")
logger.info(f"Column names: {list(df.columns)}")

print("\n First 5 rows:")
print(df.head())

print("\n Data Types:")
print(df.dtypes)

missing = df.isnull().sum()
logger.info(f"Missing values per column:\n{missing}")
print("\n Missing Values:")
print(missing)


# 
# 4. NUMPY STATISTICS
# 
subjects = ["Math", "Science", "English"]

logger.info("Computing NumPy statistics for all subjects...")

for subject in subjects:
 scores = df[subject].to_numpy()
 mean = np.mean(scores)
 median = np.median(scores)
 std = np.std(scores)
 high = np.max(scores)
 low = np.min(scores)

 logger.info(
 f"{subject} → Mean: {mean:.2f} | Median: {median} | "
 f"Std: {std:.2f} | Max: {high} | Min: {low}"
 )
 print(f"\n {subject} Stats:")
 print(f" Mean: {mean:.2f} | Median: {median} | Std Dev: {std:.2f}")
 print(f" Highest: {high} | Lowest: {low}")


# 
# 5. ADD TOTAL COLUMN
# 
df["Total"] = df["Math"] + df["Science"] + df["English"]
logger.info("Added 'Total' column (sum of all subjects).")

print("\n DataFrame with Total:")
print(df[["Name", "Math", "Science", "English", "Total"]].to_string(index=False))


# 
# 6. FILTER — STUDENTS WHO FAILED
# 
failed = df[(df["Math"] < 50) | (df["Science"] < 50) | (df["English"] < 50)]
logger.warning(f"{len(failed)} student(s) have at least one failing mark (<50).")

print("\n Students with Failing Marks:")
print(failed[["StudentID", "Name", "Math", "Science", "English"]].to_string(index=False))


# 
# 7. GROUP BY GRADE — AVERAGE MARKS
# 
grade_avg = df.groupby("Grade")[subjects].mean().round(2)
logger.info("Grouped data by Grade and computed average marks.")

print("\n Average Marks by Grade:")
print(grade_avg)


# 
# 8. SAVE PROCESSED FILE
# 
OUTPUT_PATH = "students_processed.xlsx"
df.to_excel(OUTPUT_PATH, index=False, engine="openpyxl")
logger.info(f"Processed data saved to: {OUTPUT_PATH}")
logger.info("====== Assignment 1 Completed ======")
```

---

## Sample Log Output (`logs/assignment1.log`)

```
2025-08-10 10:22:01 | INFO | ====== Assignment 1 Started ======
2025-08-10 10:22:01 | INFO | File loaded successfully: students_data.xlsx
2025-08-10 10:22:01 | INFO | Shape of dataset: (10, 7)
2025-08-10 10:22:01 | INFO | Column names: ['StudentID', 'Name', 'Age', 'Math', 'Science', 'English', 'Grade']
2025-08-10 10:22:01 | INFO | Missing values per column: (all zeros)
2025-08-10 10:22:01 | INFO | Math → Mean: 70.00 | Median: 75.0 | Std: 20.45 | Max: 95 | Min: 33
2025-08-10 10:22:01 | INFO | Science → Mean: 73.10 | Median: 77.0 | Std: 15.23 | Max: 90 | Min: 45
2025-08-10 10:22:01 | INFO | English → Mean: 74.80 | Median: 76.0 | Std: 14.87 | Max: 94 | Min: 50
2025-08-10 10:22:01 | INFO | Added 'Total' column (sum of all subjects).
2025-08-10 10:22:01 | WARNING | 2 student(s) have at least one failing mark (<50).
2025-08-10 10:22:01 | INFO | Grouped data by Grade and computed average marks.
2025-08-10 10:22:01 | INFO | Processed data saved to: students_processed.xlsx
2025-08-10 10:22:01 | INFO | ====== Assignment 1 Completed ======
```

---

## Expected Output Summary

- `students_processed.xlsx` — Updated file with the `Total` column added
- `logs/assignment1.log` — Full execution log with timestamps
- Console output showing stats, failing students, and grade-wise averages

---
---

# Assignment 2 — Web Scraping with BeautifulSoup & Requests

## Objective

Scrape article/product data from a public website using **`requests`** and **`BeautifulSoup (bs4)`**, parse the HTML content, and save the structured data.

> **Target Site Used:** [https://books.toscrape.com](https://books.toscrape.com) *(a free, legal scraping practice site)*

---

## Libraries Used

| Library | Purpose |
|------------------|------------------------------------------|
| `requests` | Send HTTP GET requests to websites |
| `bs4` (BeautifulSoup) | Parse and extract data from HTML |
| `json` | Save scraped data as a JSON file |
| `logging` | Log progress and errors |
| `time` | Add delays between requests (polite scraping) |

Install dependencies:

```bash
pip install requests beautifulsoup4
```

---

## What the Code Does (Step-by-Step)

1. **Sends HTTP GET request** to the target URL using `requests`
2. **Checks response status** (200 = OK, anything else = error)
3. **Parses HTML** using `BeautifulSoup` with the `html.parser`
4. **Extracts data** — book title, price, star rating, availability
5. **Scrapes multiple pages** by following pagination links
6. **Stores results** in a list of dictionaries
7. **Saves the data** to a `scraped_output.json` file
8. **Logs all steps** including errors and warnings

---

## Full Code — `assignment2.py`

```python
import requests
from bs4 import BeautifulSoup
import json
import logging
import time

# 
# 1. LOGGING SETUP
# 
logging.basicConfig(
 level=logging.INFO,
 format="%(asctime)s | %(levelname)s | %(message)s",
 handlers=[
 logging.FileHandler("scraper.log"),
 logging.StreamHandler()
 ]
)
logger = logging.getLogger(__name__)
logger.info("====== Assignment 2 Web Scraper Started ======")


# 
# 2. CONFIGURATION
# 
BASE_URL = "https://books.toscrape.com/catalogue/"
START_URL = "https://books.toscrape.com/catalogue/page-1.html"
MAX_PAGES = 5 # Scrape first 5 pages only
DELAY = 1 # Seconds between requests (be polite!)

HEADERS = {
 "User-Agent": (
 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
 "AppleWebKit/537.36 (KHTML, like Gecko) "
 "Chrome/122.0 Safari/537.36"
 )
}

# Star rating words on the site map to numbers
RATING_MAP = {
 "One": 1, "Two": 2, "Three": 3,
 "Four": 4, "Five": 5
}


# 
# 3. HELPER — FETCH A PAGE
# 
def fetch_page(url):
 """Send GET request and return BeautifulSoup object, or None on failure."""
 try:
 response = requests.get(url, headers=HEADERS, timeout=10)
 response.raise_for_status() # Raises HTTPError for 4xx/5xx
 logger.info(f"Fetched URL: {url} | Status: {response.status_code}")
 return BeautifulSoup(response.text, "html.parser")
 except requests.exceptions.HTTPError as e:
 logger.error(f"HTTP Error for {url}: {e}")
 except requests.exceptions.ConnectionError:
 logger.error(f"Connection failed for {url}")
 except requests.exceptions.Timeout:
 logger.error(f"Request timed out: {url}")
 return None


# 
# 4. HELPER — PARSE BOOKS FROM A PAGE
# 
def parse_books(soup):
 """Extract book info from a parsed BeautifulSoup page."""
 books = []
 articles = soup.find_all("article", class_="product_pod")

 for article in articles:
 # Title
 title = article.h3.a["title"]

 # Price
 price = article.find("p", class_="price_color").text.strip()

 # Star Rating (stored as word class like "Three")
 rating_class = article.find("p", class_="star-rating")["class"][1]
 rating = RATING_MAP.get(rating_class, 0)

 # Availability
 availability = article.find("p", class_="instock availability").text.strip()

 books.append({
 "title": title,
 "price": price,
 "rating": rating,
 "availability": availability
 })

 logger.info(f"Parsed {len(books)} books from current page.")
 return books


# 
# 5. HELPER — GET NEXT PAGE URL
# 
def get_next_page(soup):
 """Return the next page URL, or None if on the last page."""
 next_btn = soup.find("li", class_="next")
 if next_btn:
 next_href = next_btn.a["href"]
 return BASE_URL + next_href
 return None


# 
# 6. MAIN SCRAPER LOOP
# 
all_books = []
current_url = START_URL
page_count = 0

while current_url and page_count < MAX_PAGES:
 page_count += 1
 logger.info(f"--- Scraping page {page_count} ---")

 soup = fetch_page(current_url)

 if soup is None:
 logger.warning("Skipping page due to fetch error.")
 break

 books = parse_books(soup)
 all_books.extend(books)

 current_url = get_next_page(soup)
 time.sleep(DELAY) # Polite delay between requests

logger.info(f"Total books scraped: {len(all_books)}")


# 
# 7. SAVE TO JSON
# 
OUTPUT_FILE = "scraped_output.json"

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
 json.dump(all_books, f, indent=4, ensure_ascii=False)

logger.info(f"Data saved to: {OUTPUT_FILE}")
logger.info("====== Assignment 2 Completed ======")


# 
# 8. QUICK PREVIEW
# 
print(f"\n Scraped {len(all_books)} books across {page_count} pages.\n")
print(" First 3 results preview:")
for book in all_books[:3]:
 print(f" {book['title']}")
 print(f" Price: {book['price']} | Rating: {book['rating']}/5 | {book['availability']}")
 print()
```

---

## Sample Console Output

```
2025-08-10 11:05:01 | INFO | ====== Assignment 2 Web Scraper Started ======
2025-08-10 11:05:01 | INFO | --- Scraping page 1 ---
2025-08-10 11:05:02 | INFO | Fetched URL: https://books.toscrape.com/catalogue/page-1.html | Status: 200
2025-08-10 11:05:02 | INFO | Parsed 20 books from current page.
2025-08-10 11:05:03 | INFO | --- Scraping page 2 ---
...
2025-08-10 11:05:07 | INFO | Total books scraped: 100
2025-08-10 11:05:07 | INFO | Data saved to: scraped_output.json

 Scraped 100 books across 5 pages.

 First 3 results preview:
 A Light in the Attic
 Price: £51.77 | Rating: 3/5 | In stock

 Tipping the Velvet
 Price: £53.74 | Rating: 1/5 | In stock

 Soumission
 Price: £50.10 | Rating: 1/5 | In stock
```

---

## Sample `scraped_output.json`

```json
[
 {
 "title": "A Light in the Attic",
 "price": "£51.77",
 "rating": 3,
 "availability": "In stock"
 },
 {
 "title": "Tipping the Velvet",
 "price": "£53.74",
 "rating": 1,
 "availability": "In stock"
 },
 {
 "title": "Soumission",
 "price": "£50.10",
 "rating": 1,
 "availability": "In stock"
 }
]
```

---

## Important Notes on Web Scraping

| Tip | Details |
|-----|---------|
| Be polite | Always add `time.sleep()` between requests |
| Check robots.txt | Visit `https://site.com/robots.txt` before scraping |
| Use headers | Mimic a real browser with a `User-Agent` header |
| Don't scrape private data | Only scrape publicly available, permitted content |
| Cache responses | Don't hit the same URL twice unnecessarily |

---

## Expected Output Summary

- `scraped_output.json` — JSON file with all scraped book records
- `scraper.log` — Full log of the scraping session
- Console preview showing first 3 scraped books

---

## Key Concepts Quick Reference

| Concept | Assignment 1 | Assignment 2 |
|---------|-------------|-------------|
| Read data | `pd.read_excel()` | `requests.get()` |
| Process/parse | `df`, `numpy` ops | `BeautifulSoup.find_all()` |
| Filter | `df[condition]` | `if` checks on tags |
| Group/aggregate | `df.groupby()` | Manual list building |
| Save output | `df.to_excel()` | `json.dump()` |
| Log steps | `logging.info()` | `logging.info()` |

---

*Assignments designed for beginner-to-intermediate Python learners. Feel free to extend these with more pages, more data columns, or database storage!*
