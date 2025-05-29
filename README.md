# FOIA Web Crawler

A recursive web crawler built with Scrapy to extract and download PDF documents from U.S. government FOIA reading room pages.

## 🔍 Features

- Starts from a list of FOIA agency URLs (e.g., TSA, ICE)
- Recursively follows internal links (up to 3 levels deep)
- Detects and downloads PDF files
- Automatically saves files into agency-specific folders
- Easy to expand for additional agencies

## 📂 Project Structure

foia_web_crawler/
├── scrapy.cfg
├── foia_web_crawler/
│ ├── items.py
│ ├── middlewares.py
│ ├── pipelines.py
│ ├── settings.py
│ └── spiders/
│ └── foia_spider.py

1. Clone the repo:
   ```bash
   git clone https://github.com/Matt-Collman/foia_web_crawler.git
   cd foia_web_crawler

