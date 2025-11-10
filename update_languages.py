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
    table = "| Language | Percentage |\n"
    table += "|----------|-------------|\n"
    for lang, percent in lang_data.items():
        table += f"| {lang} | {percent}% |\n"
    return table

def main():
    langs = fetch_languages()
    table = generate_table(langs)

    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()

    start = "<!-- LANGUAGES-OVERVIEW:START -->"
    end = "<!-- LANGUAGES-OVERVIEW:END -->"

    # فقط بخش بین کامنت‌ها رو عوض کن
    if start in readme and end in readme:
        before = readme.split(start)[0]
        after = readme.split(end)[1]
        updated = before + start + "\n" + table + end + after
    else:
        # اگر کامنت‌ها وجود ندارن، تغییر نده
        print("Comment markers not found. No changes made.")
        return

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(updated)

if __name__ == "__main__":
    main()
