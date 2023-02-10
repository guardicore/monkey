# Infection Monkey Code Documentation

# Configuration

To change the sphinx configuration change the attributes at `monkey_island/docs/source/conf.py`.
The documentation uses `source/_static` as a folder where we keep the custom media, stylesheets, js scripts etc.
`source/_templates` is the place where we store the custom templates which are used in the documentation, examples:

- `custom-module-template.rst`: used from autosummary to define the modules from the code
- `custom-class-template.rst`: used from autosummary to define the classes from the code
- `custom-function-template.rst`: used from autosummary to define the function from the code
- `layout.html`: define custom layout

`source/index.rst` is the main rst file in which we define the look of the index HTML page.
`source/docs.rst` is generating the automatic rst files using `autosummary`.

# Building Documentation

The make script generates the documentation using autosummary and deletes previously created build and autosummary source files.

## Linux

1. From `monkey/monkey_island`, install python dependencies:
    - `pipenv sync --dev`

1. Activate the python venv

    - `pipenv shell`

1. Generate the documentation:
    - `cd monkey/monkey_island/docs`
    - `make html`


## Windows

1. From `monkey\monkey_island`, install python dependencies:
    - `pipenv sync --dev`

1. Activate the python virtual enviroment using `activate` script from the venv.

1. Generate the documentation:
   - `cd monkey\monkey_island\docs`
   - `make.bat html`


# Deployment

To deploy the documentation locally run `python3.7 -m http.server <port-number>` and open
http://localhost:<port-number>/build/html in a browser.
