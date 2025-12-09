import _common
import json
import os
import shutil

_STEP_DEPENDENCY_LIST = []

def _step_main_init_blog_meta_dict(runtime):
    """Initializes the blog metadata dictionary in the runtime environment.

    Args:
        runtime: The runtime environment object.
    """
    runtime.blog_meta_dict = {}

# func before it should just init var existence
# func before it should have no dependency to other
def _step_main_init_done(runtime):
    """A placeholder step indicating that the basic initialization is complete.

    Args:
        runtime: The runtime environment object.
    """
    pass

_STEP_DEPENDENCY_LIST.append((_step_main_init_blog_meta_dict, _step_main_init_done))

def _step_main_load_config(runtime):
    """Loads the configuration data from the specified config file.

    Args:
        runtime: The runtime environment object.
    """
    config_path = runtime.args.config
    with open(config_path, 'r') as f:
        runtime.config_data = json.load(f)
    for k,v in runtime.config_data.items():
        if k.endswith('_path'):
            runtime.config_data[k] = _common.to_native_path(v)

_STEP_DEPENDENCY_LIST.append((_step_main_init_done, _step_main_load_config))

def _step_main_reset_output_folder(runtime):
    """Resets the output folder by deleting and recreating it.

    Args:
        runtime: The runtime environment object.
    """
    shutil.rmtree(runtime.config_data['output_path'], ignore_errors=True)
    os.makedirs(runtime.config_data['output_path'])

_STEP_DEPENDENCY_LIST.append((_step_main_load_config, _step_main_reset_output_folder))

def _step_main_output_ready(runtime):
    """A placeholder step indicating that the output folder is ready.

    Args:
        runtime: The runtime environment object.
    """
    pass

_STEP_DEPENDENCY_LIST.append((_step_main_reset_output_folder, _step_main_output_ready))

def _step_main_output_blog_meta(runtime):
    """Outputs the blog metadata to a JSON file.

    Args:
        runtime: The runtime environment object.
    """
    blog_meta_path = os.path.join(runtime.config_data['output_path'], 'blog_meta.json')
    with open(blog_meta_path, 'w') as f:
        json.dump(runtime.blog_meta_dict, f, indent=2, sort_keys=True)

_STEP_DEPENDENCY_LIST.append((_step_main_output_ready, _step_main_output_blog_meta))
