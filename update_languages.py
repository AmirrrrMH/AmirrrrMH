
import os
import requests
from datetime import datetime
from collections import defaultdict

TOKEN = os.getenv("GH_TOKEN")
USERNAME = "AmirrrrMH"

headers = {"Authorization": f"Bearer {TOKEN}"}
api_url = f"https://api.github.com/users/{USERNAME}/repos?per_page=200&type=owner"

def fetch_languages():
    repos = requests.get(api_url, headers=headers).json()
    language_stats = defaultdict(int)

    for repo in repos:
        lang_url = repo["languages_url"]
        langs = requests.get(lang_url, headers=headers).json()
        for lang, bytes_count in langs.items():
            language_stats[lang] += bytes_count

    total = sum(language_stats.values())
    lang_percent = {k: round((v / total) * 100, 2) for k, v in language_stats.items()}
    return dict(sorted(lang_percent.items(), key=lambda x: x[1], reverse=True))

def generate_table(lang_data):
    table = "| Language | Percentage |
|----------|-------------|
"
    for lang, percent in lang_data.items():
        table += f"| {lang} | {percent}% |
"
    return table

def update_readme(content):
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

def main():
    langs = fetch_languages()
    table = generate_table(langs)

    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()

    start = "<!-- LANGUAGES-OVERVIEW:START -->"
    end = "<!-- LANGUAGES-OVERVIEW:END -->"

    updated = readme.split(start)[0] + start + "\n" + table + "\n" + end + readme.split(end)[1]
    update_readme(updated)

if __name__ == "__main__":
    main()
