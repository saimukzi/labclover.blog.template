# LabClover Blog Template AGENT INSTRUCTIONS

This document provides instructions for AI agents working with the "LabClover Blog Template" repository.

## How it Works

The generator's architecture is built around a dynamic, dependency-based step execution system. Here’s a high-level overview of the process:

1.  **Execution starts** with `cmd_gen.py`, the command-line interface.
2.  `cmd_gen.py` invokes `natsumi.py`, which serves as the core step runner.
3.  `natsumi.py` **discovers all modules** with the `_feature_` prefix and identifies functions named with the `_step_` prefix.
4.  It then **sorts these step functions** based on dependencies defined in `_STEP_DEPENDENCY_LIST` within each module, ensuring that steps are executed in the correct order.
5.  Finally, the sorted steps are **executed sequentially**, transforming the input files into a static site.

This modular design allows for easy extension and customization. You can add new features by simply creating a new `_feature_` module with the desired step functions.

## Folder Structure

-   `input/`: Contains all source files for the blog, including articles (`.article.txt`), templates (`.template`), and other resources.
-   `docs/`: The output directory for the generated static site. This folder is self-contained and can be served by any HTTP server.
-   `test/`: Contains tests for the project.
-   `_feature_*.py`: These modules define the processing steps for the static site generation. Each module handles a specific concern, such as processing articles, managing resources, or generating tags.
-   `natsumi.py`: The core script that dynamically loads and executes the feature modules in the correct order.
-   `cmd_gen.py`: The command-line interface for running the static site generator.
-   `config.json`: The main configuration file for the project.

## Environment Setup

Coding agents must use a `.venv` python environment and must not use the system python environment.

1.  **Create and activate the virtual environment:**
    If a `.venv` directory does not exist, create it:
    ```bash
    python -m venv .venv
    ```
    Activate the virtual environment:
    ```bash
    source .venv/bin/activate
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## How to Run

To generate the blog, run the following command from the root of the repository:

```bash
python cmd_gen.py
```

You can also specify a different configuration file using the `--config` argument:

```bash
python cmd_gen.py --config config-local.json
```

## How to run the tests

To run the tests, run the following command from the root of the repository:

```bash
python -m unittest test/test_articles.py
```
