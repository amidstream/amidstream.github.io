# Amidstream

A lean Jekyll blog for GitHub Pages. No theme, no JavaScript, one stylesheet.

## Publish on GitHub Pages

1. Create a repo and push these files to the `main` branch.
2. Repo Settings > Pages > Build and deployment > Source: "Deploy from a branch", branch `main`, folder `/ (root)`.
3. Naming the repo `USERNAME.github.io` serves it at `https://USERNAME.github.io`. Any other repo name serves it at `https://USERNAME.github.io/REPO`; in that case set `baseurl: "/REPO"` in `_config.yml`.
4. Set `url` in `_config.yml` to the final address so the RSS feed has correct links.

## Add a Record

Create `_posts/YYYY-MM-DD-title.md`:

```
---
layout: post
title: "Record 001"
---
Your text, in Markdown.
```

Push it. The site and `feed.xml` update on their own.

## Preview locally (optional)

```
bundle install
bundle exec jekyll serve
```

## Moving later

Everything is plain Markdown plus a few templates, so the site moves unchanged to Cloudflare Pages, Netlify or a custom domain. Update `url` and `baseurl` when you do.

## Reading Log

The Reading Log page (`reading-log.html`) is built from `_data/reading_log.csv`. To refresh it from a new Goodreads export:

```
python3 scripts/build_reading_log.py path/to/goodreads_reading_log.csv
```

The script shortens titles (drops series and subtitles), sorts newest to oldest, and puts books without a read date in a "Pre-2016" group at the end.
