import os
import requests
import math
import re

USERNAME = "AmirrrrMH"
TOKEN = os.getenv("GH_TOKEN")

API_URL = "https://api.github.com/user/repos?per_page=100&type=owner"

LANG_COLORS = {
    "Python": "#3572A5",
    "JavaScript": "#F1E05A",
    "HTML": "#E34C26",
    "CSS": "#563D7C",
    "C": "#555555",
    "C++": "#00599C",
    "C#": "#178600",
    "Django": "#092E20",
}

def fetch_repos():
    headers = {"Authorization": f"token {TOKEN}"}
    repos = []
    page = 1
    while True:
        res = requests.get(f"{API_URL}&page={page}", headers=headers).json()
        if not res or "message" in res:
            break
        repos.extend(res)
        page += 1
    return repos

def fetch_languages(repo_full_name):
    headers = {"Authorization": f"token {TOKEN}"}
    url = f"https://api.github.com/repos/{repo_full_name}/languages"
    return requests.get(url, headers=headers).json()

def generate_bar_chart(lang, percent, color):
    bar_length = math.floor(percent / 4)
    bar = "█" * bar_length
    return f"<span style='color:{color}; font-weight:bold'>{lang.ljust(12)}</span> {bar} {percent:.1f}%"

def update_readme(content_block):
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()
    
    pattern = r"(<!-- LANGUAGES-OVERVIEW:START -->)(.*?)(<!-- LANGUAGES-OVERVIEW:END -->)"
    replacement = r"\1\n" + content_block + r"\n\3"
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

def main():
    repos = fetch_repos()
    language_totals = {}

    for repo in repos:
        langs = fetch_languages(repo["full_name"])
        for lang, value in langs.items():
            language_totals[lang] = language_totals.get(lang, 0) + value

    total = sum(language_totals.values())
    if total == 0:
        return

    sorted_langs = sorted(language_totals.items(), key=lambda x: x[1], reverse=True)[:6]

    md = "## 📊 Languages Overview (Auto Updated)\n\n"
    for lang, val in sorted_langs:
        percent = (val / total) * 100
        color = LANG_COLORS.get(lang, "#AAAAAA")
        md += generate_bar_chart(lang, percent, color) + "<br>\n"

    update_readme(md)

if __name__ == "__main__":
    main()

