# LabClover Blog Template

"LabClover Blog Template" is a template of web site generation projects.

This project is a lightweight, extensible static site generator designed to build blogs from simple text files. It reads articles from an `input` folder, processes them through a series of customizable steps, and generates a complete blog in the `docs` folder, ready to be served by any static file server.

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

## Configuration

The site's behavior is controlled by `config.json`. Here are the available options:

-   `title`: The title of the blog.
-   `input_path`: The directory where the source files are located.
-   `templates_path`: The directory containing the Jinja2 templates.
-   `output_path`: The directory where the generated site will be saved.
-   `base_url`: The base URL of the site, used to generate absolute URLs for resources.
-   `copy_re_list`: A list of regular expressions that match files to be copied directly to the output directory without processing.

## Adding a New Processing Step

To add a new feature or processing step, follow these steps:

1.  **Create a new `_feature_mynewfeature.py` file.**
2.  **Define a new step function** in the file with the `_step_` prefix (e.g., `_step_main_my_new_step(runtime)`). The function should accept the `runtime` object as an argument, which provides access to the configuration and other shared data.
3.  **Add dependencies** to the `_STEP_DEPENDENCY_LIST` at the bottom of the file. This ensures your step runs at the correct point in the process. For example, to run your step after the configuration is loaded but before the output is generated, you would add:
    ```python
    _STEP_DEPENDENCY_LIST.append((_feature_base._step_main_load_config, _step_main_my_new_step, _feature_base._step_main_output_ready))
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
