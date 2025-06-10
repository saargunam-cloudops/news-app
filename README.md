# Hot News Dashboard

A Flask-based web application that aggregates and displays the latest news articles from multiple RSS feeds, categorized into India News, World News, Indian Finance, and Global Tech. The dashboard shows news from the last 24 hours and can be refreshed manually.

---

## Features

- **Aggregates news** from multiple RSS feeds across four categories:
  - 🇮🇳 India News
  - 🌍 World News
  - 📈 Indian Stock Market & Finance
  - 💻 Global Tech News
- **Filters articles** published within the last 24 hours
- **Removes duplicate articles** by title and link
- **Displays the top 5 latest articles** per category
- **Responsive, dark-themed UI** for desktop and mobile
- **Manual refresh button** to reload the latest news
- **Displays source and published date** for each article
- **Handles malformed feeds and date parsing errors gracefully**

---

## Demo

![Screenshot of Hot News Dashboard](screenshot.png) <!-- Add a screenshot if available -->

---

## Tech Stack

- Python 3.8+
- [Flask](https://flask.palletsprojects.com/)
- [feedparser](https://pythonhosted.org/feedparser/)
- [requests](https://docs.python-requests.org/)
- [python-dateutil](https://dateutil.readthedocs.io/)

---

## Setup & Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/news-app.git
    cd news-app
    ```

2. **Create a virtual environment (recommended):**
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```
    If `requirements.txt` is missing, install manually:
    ```sh
    pip install flask feedparser requests python-dateutil
    ```

4. **Run the application:**
    ```sh
    python news_dashboard.py
    ```

5. **Open your browser and visit:**
    ```
    http://127.0.0.1:5000/
    ```

---

## Usage

- The dashboard loads the latest news from all sources on page load.
- Click the **🔄 Refresh News** button to manually reload the latest articles.
- Each section displays up to 5 of the most recent articles from the last 24 hours.
- Article titles link directly to the original news source.

---

## Configuration

- **Adding/Removing Feeds:**  
  Edit the `INDIA_FEEDS`, `WORLD_FEEDS`, `INDIAN_FINANCE_FEEDS`, or `TECH_FEEDS` dictionaries in `news_dashboard.py` to customize sources.

---

## Troubleshooting

- If you see errors about missing modules, ensure all dependencies are installed.
- Some feeds may occasionally fail to load due to network issues or malformed RSS; these are handled gracefully and logged to the console.

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

## Credits

- Built with [Flask](https://flask.palletsprojects.com/) and [feedparser](https://pythonhosted.org/feedparser/).
- RSS feeds provided by their respective news organizations.

---
