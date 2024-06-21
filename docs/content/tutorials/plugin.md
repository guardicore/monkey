---
title: "Plugin"
date: 2024-06-21T15:49:56Z
draft: true
tags: ["tutorials", "plugins"]
---

In this tutorial, we'll create a simple INSERT_TYPE_HERE plugin.

You will learn INSERT_LEARNING_OBJECTIVES.

### Prerequisites

- cookiecutter

### Create your project

We will use the cookiecutter template to create our plugin.

Download [plugin-cookiecutter.yaml](plugin/plugin-cookiecutter.yaml)

Then, run the following command to create a plugin project:
```
cookiecutter https://github.com/guardicode/infection-monkey-cookiecutter \
    --no-input \
    --config-file plugin-cookiecutter.yaml
```

When prompted about what type of project to create, choose option 2 (Agent plugin).

You should now have a folder named _Blah-Exploiter_.

### Modify the plugin

...
