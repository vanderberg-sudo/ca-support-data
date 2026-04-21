# CA Support Data

This repo powers the Comparative Agility support chat agent.

## How it works

1. Help articles live as `.md` files in the `articles/` folder
2. Whenever anyone edits or adds an article, GitHub automatically rebuilds `articles_all.jsonl`
3. The support widget reads `articles_all.jsonl` to answer user questions

## How to add or edit an article

1. Go to the `articles/` folder in GitHub
2. Click an existing file to edit it, or click **Add file → Create new file** for a new one
3. Use this format at the top of every file:

```
---
title: Your Article Title
url: https://help.comparativeagility.com/your-article-url/
category: Get Started
---

Your content here in plain text or markdown...

## Videos
- [Video title](https://www.youtube.com/watch?v=...)
```

4. Click **Commit changes** — the `articles_all.jsonl` file updates automatically within ~30 seconds

## Categories

Use one of these category names for consistency:
- Get Started
- Advanced Topics
- General
- Account
- Billing
- Reports
- Personal Improvement
- Feedback 360
- Instant Insights
- Privacy & Legal

## Folder structure

```
articles/          ← edit files here
  reset-password.md
  impact-matrix.md
  ...
articles_all.jsonl ← auto-generated, never edit manually
build.py           ← build script, never edit manually
.github/
  workflows/
    build.yml      ← automation config, never edit manually
```
