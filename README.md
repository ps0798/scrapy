# 🕸️ Scrapy News Scraper 📰

This project is a Scrapy-based web scraping application designed to scrape news articles from different websites. With minimal setup, you can extract headlines, summaries, and URLs of articles into structured data formats such as JSON or CSV.

## 🚀 Getting Started

### Prerequisites

Make sure you have Python (>=3.7) installed. You can download Python from [here](https://www.python.org/downloads/).

### 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ps0798/scrapy
   cd scrapy

2. **Install required dependencies**:
  
   `pip install -r requirements.txt`

3. **🔐 Setting Up Environment Variables**

    - Create a .env file at the root of the project (sample file is already present):
      
      `touch .env`
    - Add your environment variables to the .env file
      
      ```bash
      STATIC_DATA_PATH=static/data.json
      AUTH_TOKEN=74da97c4-3ac7-487a-bb3d-3749eca7ca0a`

4. **How to run?**
  
    `uvicorn main:app  --reload`  


