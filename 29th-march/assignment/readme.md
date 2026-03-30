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
