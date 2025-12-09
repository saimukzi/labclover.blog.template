# Natsumi Static Site Generator

This project is a static site generator that reads article files from the `input` folder and generates a blog in the `docs` folder. The `docs` folder is intended to be served by a static file server.

## How it works

The main script is `cmd_gen.py`. It uses `natsumi.py` to dynamically load and execute functions from modules with the `_feature_` prefix. These modules define the steps for processing the input files, such as reading articles, parsing metadata, and generating HTML.

The core logic is in the `_feature_` modules, which handle specific tasks like processing articles, managing resources, and creating tags. The `input` folder contains the source files, including templates and articles, while the `docs` folder is the output directory for the generated site.

## Folder Structure

- `input/`: Contains the source files for the blog, such as articles and templates.
- `docs/`: The output directory for the generated static site. This folder can be served by an HTTP server.
- `test/`: Contains tests for the project.
- `_feature_*.py`: Modules that define the steps for the static site generation.
- `natsumi.py`: The core script that dynamically loads and executes the feature modules.
- `cmd_gen.py`: The command-line interface for running the static site generator.

## How to run

To generate the blog, run the following command:

```
python cmd_gen.py
```
