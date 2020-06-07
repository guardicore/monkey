# Monkey documentation

This folder contains the Monkey Documentation site. The site is based on [Hugo](https://gohugo.io/) and the [learn](https://themes.gohugo.io/theme/hugo-theme-learn/en) theme.

## Directory Structure

The most important directory is `content`: This is the directory which contains the content files. [Read this to understand how pages are organized in that folder](https://themes.gohugo.io//theme/hugo-theme-learn/en/cont/pages/).

## How to contribute

### Requirements

You have to install `hugo` and a text editor that's good for markdown (`vscode` and `vim` are good options).

### Add content

Run `hugo new folder/page.md`. Optionally add `--kind chapter` if this is a new chapter page. For example, `hugo new usage/getting-started.md` created the Getting Started page.

### Editing content

Edit the markdown file(s). [Here's a markdown cheatsheet](https://themes.gohugo.io//theme/hugo-theme-learn/en/cont/markdown/). If you want to add images, add them to the `static/images` folder and refer to them by name.

### Test the content locally

Run `hugo server -D`. The server will be available locally at `http://localhost:1313/infectionmonkey/docs/`. You can change the content and the site will refresh automatically

### Build the content

Run `hugo`. This will create a static site in the `public` directory. This directory should be ignored by `git` - **make sure you don't add and commit it by mistake!**
