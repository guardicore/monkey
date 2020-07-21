---
title: "Contribute Documentation"
date: 2020-06-17T17:31:54+03:00
draft: false
weight: 1
tags: ["contribute"]
---

The `/docs` folder contains the Monkey Documentation site.

The site is based on [Hugo](https://gohugo.io/) and the [learn](https://themes.gohugo.io/theme/hugo-theme-learn/en) theme.

- [Directory Structure](#directory-structure)
  - [content](#content)
  - [static](#static)
  - [config](#config)
  - [themes](#themes)
  - [layouts and archtypes](#layouts-and-archtypes)
  - [public and resources](#public-and-resources)
- [How to contribute](#how-to-contribute)
  - [Requirements](#requirements)
  - [Adding and editing content](#adding-and-editing-content)
    - [Add a new page](#add-a-new-page)
    - [Editing an existing page](#editing-an-existing-page)
  - [Building the content](#building-the-content)
    - [Serve the documentation locally](#serve-the-documentation-locally)
    - [Build the content for deployment](#build-the-content-for-deployment)
    - [Troubleshooting](#troubleshooting)
      - [`Error: Unable to locate config file or config directory. Perhaps you need to create a new site.`](#error-unable-to-locate-config-file-or-config-directory-perhaps-you-need-to-create-a-new-site)
      - [`failed to extract shortcode: template for shortcode "children" not found` or theme doesn't seem right?](#failed-to-extract-shortcode-template-for-shortcode-children-not-found-or-theme-doesnt-seem-right)
      - [CSS is missing](#css-is-missing)

## Directory Structure

By order of importance:

### content

The most important directory is `/content`: This is the directory which contains the content files. [Read this to understand how pages are organized in that folder](https://themes.gohugo.io//theme/hugo-theme-learn/en/cont/pages/).

### static

In this directory you should place images, `css` files, `js` files, and other static content the site should serve. To access that static content in a page, use something similar to this:

```markdown
![AWS instance ID](../../images/setup/aws/aws-instance-id.png "AWS instance ID")
```

### config

This folder controls a lot of parameters regarding the site generation.

### themes

This is the theme we're using. It's a submodule (so to get it you need to run `git submodule update`). It's our own fork of the [learn](https://themes.gohugo.io/hugo-theme-learn/) theme. If we want to make changes to the theme itself or pull updates from the upstream you'll do it here. 

### layouts and archtypes

This directory includes custom [HTML partials](https://gohugo.io/templates/partials/), custom [shortcodes](https://gohugo.io/content-management/shortcodes/), and content templates. Best to not mess with the existing stuff here too much, but rather add new things.

### public and resources

These are the build output of `hugo` and should never be `commit`-ed to git.   

## How to contribute

### Requirements

You have to [install `hugo`](https://gohugo.io/getting-started/installing/), a text editor that's good for markdown (`vscode` and `vim` are good options), and `git`.

### Adding and editing content

#### Add a new page

Run `hugo new folder/page.md`. Optionally add `--kind chapter` if this is a new chapter page. For example, `hugo new usage/getting-started.md` created the Getting Started page.

#### Editing an existing page

Edit the markdown file(s). [Here's a markdown cheatsheet](https://themes.gohugo.io//theme/hugo-theme-learn/en/cont/markdown/). If you want to add images, add them to the `static/images` folder and refer to them by name.

### Building the content

#### Serve the documentation locally

Run `hugo server -D`. The server will be available locally at `http://localhost:1313/`. You can change the content/theme and the site will refresh automatically to reflect your changes.

#### Build the content for deployment

Run `hugo --environment staging` or `hugo --environment production`. This will create a static site in the `public` directory. This directory should be ignored by `git` - **make sure you don't add and commit it by mistake!**

#### Troubleshooting

##### `Error: Unable to locate config file or config directory. Perhaps you need to create a new site.`

What is your working directory? It should be `monkey/docs`.
  
##### `failed to extract shortcode: template for shortcode "children" not found` or theme doesn't seem right?

Have you ran `git submodule update`?

##### CSS is missing

- Make sure that you're accessing the correct URL.
- Check the `config.toml` file.
