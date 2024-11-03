# AdScrapeX

### Overview

**AdScrapeX** is a Python-based web scraping project using **Scrapy** and **Scrapy Playwright** to crawl and extract data from various classified advertisement websites. It’s designed to efficiently scrape information such as vehicle listings, property ads, and general classifieds, providing structured data that can be further processed or analyzed.

### Features

- Scrapes multiple classified ads websites efficiently.
- Handles dynamic websites using Scrapy Playwright for better interaction with JavaScript-heavy pages.
- Can be easily customized to add more classified ad websites.
- Built-in support for pagination and dynamic content handling.
- Error handling and logging mechanisms to ensure robust data scraping.
  
### Supported Websites

This project currently supports scraping the following classified ad websites:

- [Ikman.lk](https://ikman.lk) - Sri Lanka's largest marketplace for vehicles, properties, jobs, and more.
- [PatPat.lk](https://patpat.lk) - Online marketplace in Sri Lanka, specializing in vehicles and properties.
- [Adz.lk](https://adz.lk) - A classified ads platform in Sri Lanka for vehicles, properties, and services.
- [HitAd.lk](https://hitad.lk) - A leading classified ads site in Sri Lanka, listing jobs, vehicles, real estate, and services.
- [Sunday Observer](https://www.sundayobserver.lk/classifieds) - The classified section of the Sunday Observer, a major Sri Lankan newspaper.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/DamikaAlwis-Gif/AdScrapeX.git
```
### 2.Create a Virtual Environment
Create a virtual environment to manage project dependencies.

```bash
python -m venv venv
venv\Scripts\activate # On Windows
# On macOS/Linux: source venv/bin/activate  
```
### 3.Install Required Packages
Install the project dependencies listed in requirements.txt.

```bash
pip install -r requirements.txt
```
### 4.Install Browser binaries
Once Playwright is installed, you need to install the browser binaries (Chromium, Firefox, and WebKit) that Playwright will automate.

```bash
playwright install
```

 ### 5.Set Up Environment Variables
Navigate to the ad_scraper folder and create a .env file based on the .env.example file. 

```bash
cd ad_scraper
```

```bash
SCRAPEOPS_API_KEY=your_scrapeops_api_key
```

## Usage

### 1.You can find the created spiders in the spiders folder
### 2.Replace the start_urls with your desired urls
Before running the spider, make sure to replace the start_urls in your spider file with the URLs you want to scrape.

### 3.Run the Spider
To start a spider, run the following command in the terminal:

```bash
scrapy crawl spider_name -L INFO
```





